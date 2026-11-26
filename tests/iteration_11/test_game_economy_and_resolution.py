from __future__ import annotations

import json

from fastapi.testclient import TestClient

from .conftest import active_t02


CLAIMS = ["IDENTITY_MERGE", "FALSE_MERGE_REJECTION", "DIRECTED_PAYMENT_CYCLE", "COORDINATED_ADMINISTRATION", "BENIGN_SHARED_INFRASTRUCTURE"]
PRIMARY = ["T2-P-CIPHER-A", "T2-P-CIPHER-B"]


def paid_identity(client: TestClient, round_id: str, key: str = "identity-1"):
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": key})
    assert response.status_code == 200, response.text
    return response


def paid_graph(client: TestClient, round_id: str, key: str = "graph-1"):
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", json={"idempotency_key": key, "algorithm": "CENTRALITY", "result_limit": 5})
    assert response.status_code == 200, response.text
    return response


def submit(client: TestClient, round_id: str, suspects: list[str], claims: list[str] = CLAIMS, key: str = "submission-1"):
    response = client.post(f"/api/v1/rounds/{round_id}/submission", json={"idempotency_key": key, "suspect_record_ids": suspects, "evidence_claim_ids": claims})
    assert response.status_code == 200, response.text
    return response


def test_six_case_doors_have_explicit_scores_and_endings(client: TestClient) -> None:
    cases = [
        ("clean", PRIMARY, CLAIMS, 2, 1000, "CLEAN_COLLAR", 3, 0),
        ("wrecked", PRIMARY + ["T2-O-BAKERY"], [], 2, 760, "CASE_CLOSED_KENNEL_WRECKED", 3, 1),
        ("cold", [], CLAIMS, 2, 520, "THE_SCENT_WENT_COLD", 3, 0),
        ("budget", [], [], 3, 280, "BISCUIT_BUDGET_BLOWN", 0, 0),
        ("squirrel", ["T2-P-CIPHER-A", "T2-P-CIPHER-B", "T2-P-CYPHER", "T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA", "T2-O-BAKERY"], [], 2, 120, "CHASED_EVERY_SQUIRREL", 3, 2),
        ("wrong-tree", ["T2-P-CYPHER"], [], 1, 40, "BARKING_UP_THE_WRONG_TREE", 6, 1),
    ]
    for label, suspects, claims, paid, expected_score, expected_ending, expected_credits, false_count in cases:
        round_id = active_t02(client)
        if paid >= 1:
            paid_identity(client, round_id, f"{label}-identity")
        for index in range(paid - 1):
            paid_graph(client, round_id, f"{label}-graph-{index}")
        result = submit(client, round_id, suspects, claims, f"{label}-submission")
        body = result.json()
        assert body["score"] == expected_score
        assert body["ending_code"] == expected_ending
        assert body["credits_remaining"] == expected_credits
        assert body["false_accusations"] == false_count
        assert "expected_truth" not in json.dumps(body).lower()
        assert "culpability" not in json.dumps(body).lower()
        assert client.get(f"/api/v1/rounds/{round_id}/closing").status_code == 200


def test_paid_action_replay_is_idempotent_and_does_not_debit_twice(client: TestClient) -> None:
    round_id = active_t02(client)
    first = paid_graph(client, round_id, "same-graph")
    replay = paid_graph(client, round_id, "same-graph")
    assert replay.json()["analysis_id"] == first.json()["analysis_id"]
    assert replay.json()["cached"] is True
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 6
    ledger = client.get(f"/api/v1/rounds/{round_id}/economy/ledger").json()["entries"]
    assert [item["entry_type"] for item in ledger] == ["CHARGE"]


def test_idempotency_key_cannot_change_the_graph_scope(client: TestClient) -> None:
    round_id = active_t02(client)
    first = paid_graph(client, round_id, "same-request")
    changed = client.post(
        f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
        json={"idempotency_key": "same-request", "algorithm": "CENTRALITY", "result_limit": 5, "visible_record_ids": ["T2-P-CIPHER-A"]},
    )
    assert first.status_code == 200
    assert changed.status_code == 409
    assert changed.json()["code"] == "IDEMPOTENCY_KEY_REUSED"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 6


def test_insufficient_credits_are_a_hard_stop_without_a_ledger_entry(client: TestClient) -> None:
    round_id = active_t02(client)
    paid_identity(client, round_id, "spent-identity-1")
    paid_graph(client, round_id, "spent-graph")
    paid_identity(client, round_id, "spent-identity-2")
    exhausted = client.post(
        f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
        json={"idempotency_key": "unaffordable-graph", "algorithm": "CENTRALITY", "result_limit": 5},
    )
    assert exhausted.status_code == 409
    assert exhausted.json()["code"] == "INSUFFICIENT_CREDITS"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 0
    ledger = client.get(f"/api/v1/rounds/{round_id}/economy/ledger").json()["entries"]
    assert len(ledger) == 3
    assert all(item["entry_type"] == "CHARGE" for item in ledger)


def test_provider_failure_refunds_and_is_visible_in_the_ledger(client: TestClient) -> None:
    round_id = active_t02(client)
    service = client.app.state.container.graph_analytics

    class FailingEngine:
        def analyze(self, graph, request):
            raise RuntimeError("synthetic provider failure")

    service._engine = FailingEngine()
    response = paid_graph(client, round_id, "failed-graph")
    assert response.json()["status"] == "FAILED"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 9
    ledger = client.get(f"/api/v1/rounds/{round_id}/economy/ledger").json()["entries"]
    assert [item["entry_type"] for item in ledger] == ["CHARGE", "REFUND"]
    assert ledger[0]["status"] == "REFUNDED"


def test_submission_is_immutable_and_replayable(client: TestClient) -> None:
    round_id = active_t02(client)
    first = submit(client, round_id, PRIMARY, CLAIMS, "submit-once")
    replay = submit(client, round_id, PRIMARY, CLAIMS, "submit-once")
    assert replay.json()["submission_id"] == first.json()["submission_id"]
    assert replay.json()["replayed"] is True
    changed = client.post(f"/api/v1/rounds/{round_id}/submission", json={"idempotency_key": "submit-two", "suspect_record_ids": ["T2-P-CYPHER"], "evidence_claim_ids": CLAIMS})
    assert changed.status_code == 409
    assert changed.json()["code"] == "ROUND_NOT_ACTIVE"


def test_stale_submission_version_is_rejected_without_closing_the_round(client: TestClient) -> None:
    round_id = active_t02(client)
    current_version = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["version"]
    stale = client.post(f"/api/v1/rounds/{round_id}/submission", json={"idempotency_key": "stale-submit", "suspect_record_ids": PRIMARY, "evidence_claim_ids": CLAIMS, "expected_round_version": current_version - 1})
    assert stale.status_code == 409
    assert stale.json()["code"] == "STALE_ROUND_VERSION"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["status"] == "ACTIVE"


def test_sqlite_round_and_ledger_survive_a_restart(tmp_path) -> None:
    settings = __import__("fraud_graph_arena.config", fromlist=["Settings"]).Settings(environment="test", round_repository="sqlite", sqlite_path=tmp_path / "restart.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(__import__("fraud_graph_arena.application", fromlist=["create_app"]).create_app(settings)) as first_client:
        round_id = active_t02(first_client)
        paid_identity(first_client, round_id, "restart-identity")
        assert first_client.get(f"/api/v1/rounds/{round_id}/economy/ledger").json()["entries"][0]["balance_after"] == 6
    with TestClient(__import__("fraud_graph_arena.application", fromlist=["create_app"]).create_app(settings)) as second_client:
        workspace = second_client.get(f"/api/v1/rounds/{round_id}/workspace")
        assert workspace.status_code == 200
        assert workspace.json()["round"]["credits_remaining"] == 6
        replay = paid_identity(second_client, round_id, "restart-identity")
        assert replay.json()["replayed"] is True
        assert len(second_client.get(f"/api/v1/rounds/{round_id}/economy/ledger").json()["entries"]) == 1
