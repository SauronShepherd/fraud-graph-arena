from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings
from fraud_graph_arena.ethics.review import review_all_packages, validate_adversarial_cases, validate_ethical_contract

from .conftest import active_t02


CLAIMS = [
    "IDENTITY_MERGE",
    "FALSE_MERGE_REJECTION",
    "DIRECTED_PAYMENT_CYCLE",
    "COORDINATED_ADMINISTRATION",
    "BENIGN_SHARED_INFRASTRUCTURE",
]

ANCHORS = [
    "T2-P-CIPHER-A",
    "T2-P-CIPHER-B",
    "T2-DOC-CIPHER-ID",
    "T2-P-CYPHER",
    "T2-DOC-CYPHER-ID",
    "T2-TX-AB",
    "T2-TX-BC",
    "T2-TX-CA",
    "T2-DEV-ADMIN",
    "T2-LOGIN-A",
    "T2-LOGIN-B",
    "T2-LOGIN-C",
    "T2-ADDR-HUB",
    "T2-DEV-KIOSK",
    "T2-FILE-GAMMA",
    "T2-FILE-BAKERY",
]


def test_public_submission_reports_support_without_protected_truth(client) -> None:
    round_id = active_t02(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/submission",
        json={
            "idempotency_key": "ethics-clean",
            "suspect_record_ids": ["T2-P-CIPHER-A", "T2-P-CIPHER-B"],
            "evidence_claim_ids": CLAIMS,
            "evidence_record_ids": ANCHORS,
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    ethics = body["ethics"]
    assert ethics["status"] == "SUPPORTED"
    assert ethics["evidence_mode"] == "EXPLICIT_ANCHORS"
    assert ethics["submitted_record_count"] == len(ANCHORS)
    assert ethics["unsupported_accusation_count"] == 0
    assert ethics["role_dimensions"] == ["OWNERSHIP", "CONTROL", "AUTHORISATION", "CUSTODY", "PROFESSIONAL_RESPONSIBILITY"]
    assert ethics["impact_dimensions"] == ["BENEFIT", "HARM"]
    assert {item["support"] for item in ethics["statements"]} == {"ANCHORED"}
    serialized = json.dumps(body).lower()
    for marker in ("culpability", "expected_truth", "expected_classification", "protected_notes", "scoring_rule", "ending_rule"):
        assert marker not in serialized


def test_protected_actor_accusation_has_a_meaningful_ethical_consequence(client) -> None:
    round_id = active_t02(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/submission",
        json={"idempotency_key": "ethics-wrong", "suspect_record_ids": ["T2-P-CYPHER"]},
    )
    assert response.status_code == 200, response.text
    ethics = response.json()["ethics"]
    assert ethics["status"] == "UNSUPPORTED"
    assert ethics["unsupported_accusation_count"] == 1
    assert ethics["harm_penalty"] == 150
    assert "proximity" in ethics["explanation"]


def test_unknown_evidence_anchor_is_rejected_without_closing_the_round(client) -> None:
    round_id = active_t02(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/submission",
        json={"idempotency_key": "ethics-unknown", "evidence_record_ids": ["NOT-PUBLISHED"]},
    )
    assert response.status_code == 404
    assert response.json()["code"] == "EVIDENCE_NOT_AVAILABLE"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["status"] == "ACTIVE"


def test_insufficient_explicit_anchors_remain_incomplete(client) -> None:
    round_id = active_t02(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/submission",
        json={"idempotency_key": "ethics-incomplete", "suspect_record_ids": ["T2-P-CIPHER-A", "T2-P-CIPHER-B"], "evidence_claim_ids": CLAIMS, "evidence_record_ids": ["T2-DOC-CIPHER-ID"]},
    )
    assert response.status_code == 200, response.text
    ethics = response.json()["ethics"]
    assert ethics["status"] == "INCOMPLETE"
    assert ethics["evidence_mode"] == "EXPLICIT_ANCHORS"
    assert ethics["unsupported_claim_count"] >= 1


def test_changed_evidence_anchors_cannot_reuse_an_idempotency_key(client) -> None:
    round_id = active_t02(client)
    payload = {"idempotency_key": "ethics-idempotency", "suspect_record_ids": ["T2-P-CYPHER"], "evidence_claim_ids": ["IDENTITY_MERGE"], "evidence_record_ids": ["T2-DOC-CIPHER-ID"]}
    assert client.post(f"/api/v1/rounds/{round_id}/submission", json=payload).status_code == 200
    changed = {**payload, "evidence_record_ids": ["T2-DOC-CYPHER-ID"]}
    response = client.post(f"/api/v1/rounds/{round_id}/submission", json=changed)
    assert response.status_code == 409
    assert response.json()["code"] == "IDEMPOTENCY_KEY_REUSED"


def test_submission_anchor_limit_is_enforced(client) -> None:
    round_id = active_t02(client)
    response = client.post(f"/api/v1/rounds/{round_id}/submission", json={"idempotency_key": "ethics-limit", "evidence_record_ids": [f"T2-P-CIPHER-A-{index}" for index in range(65)]})
    assert response.status_code == 422


def test_sqlite_restart_restores_the_nested_ethical_assessment(tmp_path: Path) -> None:
    settings = Settings(environment="test", round_repository="sqlite", sqlite_path=tmp_path / "restart.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as first_client:
        round_id = active_t02(first_client)
        first = first_client.post(
            f"/api/v1/rounds/{round_id}/submission",
            json={"idempotency_key": "ethics-restart", "suspect_record_ids": ["T2-P-CYPHER"], "evidence_claim_ids": ["IDENTITY_MERGE"]},
        )
        assert first.status_code == 200, first.text
        expected = first.json()["ethics"]
    with TestClient(create_app(settings)) as second_client:
        replay = second_client.get(f"/api/v1/rounds/{round_id}/submission")
        assert replay.status_code == 200, replay.text
        assert replay.json()["ethics"] == expected


def test_ethics_publication_review_and_adversarial_fixtures_pass() -> None:
    assert validate_ethical_contract() == []
    assert validate_adversarial_cases() == []
    reports = review_all_packages()
    assert len(reports) == 14
    assert all(report.status == "PASS" for report in reports)
    assert all(report.adversarial_case_count == 6 for report in reports)
