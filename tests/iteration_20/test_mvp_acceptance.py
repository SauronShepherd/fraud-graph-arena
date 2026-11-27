from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports/iteration-20/fga20-mvp-acceptance-current.json"
SCHEMA = ROOT / "contracts/retrospective/fga20-mvp-acceptance.schema.json"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_acceptance_report_matches_schema_and_passes() -> None:
    report = _report()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(report))
    assert not errors
    assert report["status"] == "pass"


def test_player_journey_and_remote_boundary_are_separate_and_explicit() -> None:
    report = _report()
    assert report["player_journey"]["status"] == "PASS"
    assert report["outcomes"]["local_academy"]["complete_loop"]["status"] == "PASS"
    assert report["outcomes"]["deployment_evidence"]["databricks_profile"] == "fga"
    assert report["outcomes"]["deployment_evidence"]["databricks_read_only"] is True
    assert report["outcomes"]["qualified_case_packages"] == 13


def test_retrospective_keeps_unproven_questions_and_next_season_hypotheses() -> None:
    report = _report()
    assert report["outcomes"]["not_measured"]
    assert report["verdict"]["unproven"]
    assert len(report["next_season"]) >= 5
    statuses = {item["status"] for item in report["plan_vs_reality"]}
    assert {"delivered", "limited", "deferred"}.issubset(statuses)
