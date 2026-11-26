from __future__ import annotations

import json

import pytest


@pytest.mark.parametrize(
    ("path_id", "case_id", "credits"),
    (
        ("DETECTIVE_ACADEMY", "ACADEMY_T02", 9),
        ("PUPPY", "MADDOG", 100),
        ("ADULT_DOG", "BONE_LEDGER", 80),
        ("SENIOR_DOG", "LOVE_LEASHES_OFFSHORE", 55),
    ),
)
def test_one_shared_round_engine_serves_each_path(client, path_id: str, case_id: str, credits: int) -> None:
    created = client.post("/api/v1/rounds", json={"player_id": "hercule", "path_id": path_id, "case_id": case_id})
    assert created.status_code == 201, created.text
    round_id = created.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    opening = client.get(f"/api/v1/rounds/{round_id}/opening")
    assert opening.status_code == 200, opening.text
    assert opening.json()["case"]["id"] == case_id
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete").status_code == 200
    workspace = client.get(f"/api/v1/rounds/{round_id}/workspace")
    assert workspace.status_code == 200, workspace.text
    payload = workspace.json()
    assert payload["round"]["path_id"] == path_id
    assert payload["round"]["credits_remaining"] == credits
    assert payload["evidence_count"] > 0
    assert payload["graph"]["node_count"] == payload["evidence_count"]
    assert "expected_truth" not in json.dumps(payload).lower()

