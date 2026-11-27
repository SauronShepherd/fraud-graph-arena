from __future__ import annotations

import json

from fraud_graph_arena.academy import AcademyValidationRunner
from fraud_graph_arena.case_packages import CasePackageRegistry


def test_regression_smoke_covers_every_published_case_without_protected_truth() -> None:
    report = AcademyValidationRunner()._run_regression()
    assert report["status"] == "PASS", report
    assert len(report["smoke"]) == len(CasePackageRegistry().published())
    assert all(item["status"] == "PASS" for item in report["smoke"])
    assert "expected_truth" not in json.dumps(report).lower()
