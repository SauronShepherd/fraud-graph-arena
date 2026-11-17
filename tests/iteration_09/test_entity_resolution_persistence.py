from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def test_sqlite_analysis_and_review_survive_application_restart(tmp_path: Path) -> None:
    path = tmp_path / "durable.sqlite3"
    settings = Settings(environment="test", round_repository="sqlite", sqlite_path=path, frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as first:
        created = first.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"}).json()
        round_id = created["id"]
        first.post(f"/api/v1/rounds/{round_id}/start")
        first.post(f"/api/v1/rounds/{round_id}/opening/complete")
        run = first.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "durable-analysis"}).json()
        candidate = next(item for item in run["candidates"] if item["right_record_id"] == "T2-P-CYPHER" and item["left_record_id"] == "T2-P-CIPHER-A")
        first.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution/{candidate['candidate_id']}/review", json={"idempotency_key": "durable-review", "outcome": "UNRESOLVED"})
    with TestClient(create_app(settings)) as restarted:
        replay = restarted.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", json={"idempotency_key": "durable-analysis"}).json()
        history = restarted.get(f"/api/v1/rounds/{round_id}/investigations/entity-resolution/history").json()
    assert replay["replayed"] is True
    assert len(history["analyses"]) == 1
    assert history["reviews"][0]["outcome"] == "UNRESOLVED"


def test_sqlite_failed_analysis_refunds_credits(tmp_path: Path) -> None:
    path = tmp_path / "failed.sqlite3"
    settings = Settings(environment="test", round_repository="sqlite", sqlite_path=path, frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings), raise_server_exceptions=False) as client:
        round_id = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"}).json()["id"]
        client.post(f"/api/v1/rounds/{round_id}/start")
        client.post(f"/api/v1/rounds/{round_id}/opening/complete")

        class FailingEngine:
            def analyze(self, *args, **kwargs):
                raise RuntimeError("synthetic sqlite engine failure")

        client.app.state.container.entity_resolution._engine = FailingEngine()
        response = client.post(
            f"/api/v1/rounds/{round_id}/investigations/entity-resolution",
            json={"idempotency_key": "sqlite-analysis-failure"},
        )
        assert response.status_code == 500
        assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 9

    with TestClient(create_app(settings)) as restarted:
        assert restarted.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 9
