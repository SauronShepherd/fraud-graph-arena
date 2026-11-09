import json
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/qualify_databricks_security.py"


def _run_script(monkeypatch, tmp_path, identity, sql_responses=()):
    output = tmp_path / "security.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["qualify_databricks_security.py", "--profile", "synthetic", "--output", str(output)],
    )
    monkeypatch.setattr(
        subprocess,
        "check_output",
        lambda *args, **kwargs: json.dumps(identity),
    )
    calls = []
    responses = iter(sql_responses)

    def fake_run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(next(responses)))

    monkeypatch.setattr(subprocess, "run", fake_run)
    namespace = runpy.run_path(str(SCRIPT))
    assert namespace["main"]() == 0
    return json.loads(output.read_text(encoding="utf-8")), calls


def test_admin_profile_is_not_misreported_as_permission_pass(monkeypatch, tmp_path):
    report, calls = _run_script(
        monkeypatch,
        tmp_path,
        {"userName": "synthetic-admin@example.invalid", "groups": [{"display": "admins"}]},
    )

    assert report["is_admin"] is True
    assert report["status"] == "not_qualified"
    assert calls == []


def test_non_admin_security_qualification_uses_only_synthetic_cli_responses(monkeypatch, tmp_path):
    responses = [
        {"status": {"state": "SUCCEEDED"}},
        {"status": {"state": "FAILED"}},
        {"status": {"state": "FAILED"}},
    ]
    report, calls = _run_script(
        monkeypatch,
        tmp_path,
        {"userName": "synthetic-player@example.invalid", "groups": []},
        responses,
    )

    assert report["status"] == "pass"
    assert report["active_view_select"] == "pass"
    assert report["raw_safe_select"] == "pass"
    assert report["truth_select"] == "pass"
    assert len(calls) == 3
    assert all(args[0] == "databricks" for args in calls)
