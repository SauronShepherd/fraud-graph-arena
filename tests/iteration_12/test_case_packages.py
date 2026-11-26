from __future__ import annotations

import json
from pathlib import Path

from fraud_graph_arena.case_packages import CasePackageRegistry, validate_all_case_packages, validate_case_package

from .conftest import active_t03


CLAIMS_T03 = [
    "CONTROL_AND_BENEFIT",
    "IMPOSSIBLE_CHRONOLOGY",
    "LIMITS_OF_SERVICE_EVIDENCE",
    "PROTECT_TARA",
    "RESIDUAL_UNCERTAINTY",
    "VALID_TIMEZONE_CONTROL",
]


def test_published_packages_are_discovered_and_validated() -> None:
    results = validate_all_case_packages()
    assert results == {"academy-001": [], "academy-t02": [], "academy-t03": []}
    registry = CasePackageRegistry()
    t03 = registry.require("ACADEMY_T03", "1.0.0-fga12")
    assert t03.is_published is True
    assert t03.initial_credits == 15
    assert t03.supports("RUN_GRAPH_ANALYSIS") is True
    assert t03.supports("SUBMIT") is True
    assert t03.supports("COMPARE_IDENTITIES") is False
    assert t03.supports("CREATE_HYPOTHESIS") is False
    assert len(t03.rows("published/records.csv")) == 23
    assert len(t03.rows("published/relationships.csv")) == 27


def test_schema_rejects_arbitrary_executable_configuration(tmp_path: Path) -> None:
    source = Path("case-packages/academy-t03")
    target = tmp_path / "academy-t03"
    target.mkdir()
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    manifest["runtime_command"] = "python -c 'rewrite_the_case'"
    (target / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_case_package(target)
    assert any(error["check_id"] == "PACKAGE.SCHEMA" for error in errors)


def test_validator_rejects_cost_for_undeclared_action(tmp_path: Path) -> None:
    source = Path("case-packages/academy-t03")
    target = tmp_path / "academy-t03"
    target.mkdir()
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    manifest["economy"]["costs"]["COMPARE_IDENTITIES"] = 3
    (target / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_case_package(target)
    assert any(error["check_id"] == "PACKAGE.ECONOMY.UNSUPPORTED_ACTION" for error in errors)


def test_new_case_uses_the_shared_workspace_without_case_specific_application_branch(client) -> None:
    round_id = active_t03(client)
    workspace = client.get(f"/api/v1/rounds/{round_id}/workspace")
    assert workspace.status_code == 200, workspace.text
    payload = workspace.json()
    assert payload["evidence_count"] == 23
    assert payload["graph"]["node_count"] == 23
    assert payload["graph"]["edge_count"] == 27
    assert [item["id"] for item in payload["actions"]] == ["RUN_GRAPH_ANALYSIS"]
    assert payload["round"]["credits_remaining"] == 15
    public_text = json.dumps(payload).lower()
    assert "culpability" not in public_text
    assert "expected_truth" not in public_text


def test_new_case_can_analyse_and_submit_six_required_claims(client) -> None:
    round_id = active_t03(client)
    analysis = client.post(
        f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
        json={"idempotency_key": "t03-graph-1", "algorithm": "CENTRALITY", "centrality_metric": "degree", "result_limit": 5},
    )
    assert analysis.status_code == 200, analysis.text
    analysis_payload = analysis.json()
    assert analysis_payload["status"] == "COMPLETED"
    assert analysis_payload["snapshot_version"] == "2026.07.19.1"
    assert analysis_payload["actual_engine_run"] is False
    assert "culpability" not in json.dumps(analysis_payload["nodes"] + analysis_payload["edges"]).lower()
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 12

    submission = client.post(
        f"/api/v1/rounds/{round_id}/submission",
        json={
            "idempotency_key": "t03-submit-1",
            "suspect_record_ids": ["T3-P-VERA"],
            "evidence_claim_ids": CLAIMS_T03,
        },
    )
    assert submission.status_code == 200, submission.text
    result = submission.json()
    assert result["score"] == 1000
    assert result["ending_code"] == "CLEAN_COLLAR"
    assert result["required_claims_complete"] is True
    assert result["credits_remaining"] == 12
    assert result["scoring_version"] == "fga12-scoring-v1"
    assert result["economy_version"] == "fga12-economy-v1"
    assert "expected_truth" not in json.dumps(result).lower()
    assert client.get(f"/api/v1/rounds/{round_id}/closing").status_code == 200


def test_declared_action_contract_blocks_undeclared_identity_resolution(client) -> None:
    round_id = active_t03(client)
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "t03-identity"})
    assert response.status_code == 409
    assert response.json()["code"] == "ACTION_NOT_AVAILABLE"

