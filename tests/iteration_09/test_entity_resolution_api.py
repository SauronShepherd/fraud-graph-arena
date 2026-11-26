from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def _active_round(client: TestClient) -> str:
    created = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"})
    assert created.status_code == 201
    round_id = created.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete").status_code == 200
    return round_id


@pytest.fixture
def client(tmp_path: Path):
    settings = Settings(environment="test", round_repository="memory", sqlite_path=tmp_path / "rounds.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as value:
        yield value


def test_analysis_is_paid_once_and_replayed_without_hidden_truth(client: TestClient) -> None:
    round_id = _active_round(client)
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-1", "focus_record_id": "T2-P-CIPHER-A"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["charged_credits"] == 3
    assert body["actual_engine_run"] is False
    assert body["generation_mode"] == "RUNTIME_DETERMINISTIC_FALLBACK"
    assert len(body["exact_matches"]) == 1
    assert body["exact_matches"][0]["provenance_refs"]
    assert any(item["right_record_id"] == "T2-P-CYPHER" for item in body["candidates"])
    serialized = response.text.lower()
    assert "expected_truth" not in serialized
    assert "culpability" not in serialized
    replay = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-1", "focus_record_id": "T2-P-CIPHER-A"})
    assert replay.status_code == 200
    assert replay.json()["replayed"] is True
    assert replay.json()["analysis_id"] == body["analysis_id"]
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 6


def test_analysis_reuses_key_only_for_the_same_request(client: TestClient) -> None:
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/entity-resolution"
    first = client.post(path, json={"idempotency_key": "analysis-conflict", "focus_record_id": "T2-P-CIPHER-A"})
    changed = client.post(path, json={"idempotency_key": "analysis-conflict", "focus_record_id": "T2-P-CYPHER"})
    assert first.status_code == 200
    assert changed.status_code == 409
    assert changed.json()["code"] == "IDEMPOTENCY_KEY_REUSED"
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 6


def test_concurrent_same_analysis_key_has_one_charge(client: TestClient) -> None:
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/entity-resolution"
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(lambda _: client.post(path, json={"idempotency_key": "analysis-race"}), range(8)))
    assert all(response.status_code == 200 for response in responses)
    bodies = [response.json() for response in responses]
    assert len({body["analysis_id"] for body in bodies}) == 1
    assert sum(not body["replayed"] for body in bodies) == 1
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 6


def test_player_can_review_candidate_without_canonical_merge(client: TestClient) -> None:
    round_id = _active_round(client)
    body = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-review"}).json()
    candidate = next(item for item in body["candidates"] if item["right_record_id"] == "T2-P-CYPHER" and item["left_record_id"] == "T2-P-CIPHER-A")
    review_path = f"/api/v1/rounds/{round_id}/investigations/entity-resolution/{candidate['candidate_id']}/review"
    review = client.post(review_path, json={"idempotency_key": "review-1", "outcome": "REJECTED"})
    assert review.status_code == 200, review.text
    assert review.json()["outcome"] == "REJECTED"
    replay = client.post(review_path, json={"idempotency_key": "review-1", "outcome": "REJECTED"})
    assert replay.json()["replayed"] is True
    assert client.get(f"/api/v1/rounds/{round_id}/investigations/entity-resolution/history").json()["reviews"][0]["candidate_id"] == candidate["candidate_id"]


def test_review_reuses_key_only_for_the_same_outcome(client: TestClient) -> None:
    round_id = _active_round(client)
    body = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-review-conflict"}).json()
    candidate = next(item for item in body["candidates"] if item["right_record_id"] == "T2-P-CYPHER" and item["left_record_id"] == "T2-P-CIPHER-A")
    review_path = f"/api/v1/rounds/{round_id}/investigations/entity-resolution/{candidate['candidate_id']}/review"
    assert client.post(review_path, json={"idempotency_key": "review-conflict", "outcome": "ACCEPTED"}).status_code == 200
    changed = client.post(review_path, json={"idempotency_key": "review-conflict", "outcome": "REJECTED"})
    assert changed.status_code == 409
    assert changed.json()["code"] == "IDEMPOTENCY_KEY_REUSED"


def test_accept_review_is_a_player_safe_review_edge_not_a_canonical_merge(client: TestClient) -> None:
    round_id = _active_round(client)
    body = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-edge"}).json()
    candidate = next(item for item in body["candidates"] if item["right_record_id"] == "T2-P-CYPHER" and item["left_record_id"] == "T2-P-CIPHER-A")
    client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution/{candidate['candidate_id']}/review", json={"idempotency_key": "review-edge", "outcome": "ACCEPTED"})
    graph = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"]
    edge = next(item for item in graph["edges"] if item["relationship_type"] == "PLAYER_REVIEWED_IDENTITY")
    assert edge["relationship_family"] == "IDENTITY_REVIEW"
    assert "canonical merge" in edge["player_safe_summary"]


def test_latest_review_outcome_controls_the_player_review_edge(client: TestClient) -> None:
    round_id = _active_round(client)
    body = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "analysis-review-revision"}).json()
    candidate = next(item for item in body["candidates"] if item["right_record_id"] == "T2-P-CYPHER" and item["left_record_id"] == "T2-P-CIPHER-A")
    review_path = f"/api/v1/rounds/{round_id}/investigations/entity-resolution/{candidate['candidate_id']}/review"
    assert client.post(review_path, json={"idempotency_key": "review-accepted-first", "outcome": "ACCEPTED"}).status_code == 200
    assert client.post(review_path, json={"idempotency_key": "review-rejected-later", "outcome": "REJECTED"}).status_code == 200
    graph = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"]
    assert not any(item["relationship_type"] == "PLAYER_REVIEWED_IDENTITY" for item in graph["edges"])
    history = client.get(f"/api/v1/rounds/{round_id}/investigations/entity-resolution/history").json()
    assert [item["outcome"] for item in history["reviews"]] == ["ACCEPTED", "REJECTED"]


def test_analysis_is_rejected_when_credits_are_exhausted(client: TestClient) -> None:
    round_id = _active_round(client)
    for key in ("a1", "a2", "a3"):
        assert client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": key}).status_code == 200
    denied = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "a4"})
    assert denied.status_code == 409
    assert denied.json()["code"] == "INSUFFICIENT_CREDITS"


def test_analysis_focus_must_be_a_published_person(client: TestClient) -> None:
    round_id = _active_round(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/investigations/entity-resolution",
        json={"idempotency_key": "organization-focus", "focus_record_id": "T2-O-ALPHA"},
    )
    assert response.status_code == 404
    assert response.json()["code"] == "SUBJECT_NOT_AVAILABLE"


def test_failed_analysis_refunds_credits(tmp_path: Path) -> None:
    settings = Settings(environment="test", round_repository="memory", sqlite_path=tmp_path / "rounds.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings), raise_server_exceptions=False) as client:
        round_id = _active_round(client)

        class FailingEngine:
            def analyze(self, *args, **kwargs):
                raise RuntimeError("synthetic engine failure")

        client.app.state.container.entity_resolution._engine = FailingEngine()
        response = client.post(
            f"/api/v1/rounds/{round_id}/investigations/entity-resolution",
            json={"idempotency_key": "analysis-failure"},
        )
        assert response.status_code == 500
        assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 9
