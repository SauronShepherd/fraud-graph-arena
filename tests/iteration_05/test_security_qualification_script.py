from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[2]
def test_admin_profile_is_not_misreported_as_permission_pass(tmp_path):
    output=tmp_path/"security.json"
    subprocess.run([sys.executable,"scripts/qualify_databricks_security.py","--profile","sda","--output",str(output)],cwd=ROOT,check=True)
    report=json.loads(output.read_text())
    assert report["status"]=="not_qualified"
    if report["reason"] == "identity is a member of admins; admin sessions cannot prove denial":
        assert report["is_admin"] is True
    else:
        assert report["is_admin"] is None
