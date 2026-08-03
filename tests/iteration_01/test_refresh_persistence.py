from pathlib import Path

from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def test_academy_context_and_intro_completion_survive_application_recomposition(
    tmp_path: Path,
) -> None:
    database = tmp_path / "durable-rounds.sqlite3"
    settings = Settings(
        environment="test",
        round_repository="sqlite",
        sqlite_path=database,
        frontend_dist=tmp_path / "missing",
        allowed_origins=["http://testserver"],
    )

    with TestClient(create_app(settings)) as first_client:
        created = first_client.post(
            "/api/v1/rounds",
            json={
                "player_id": "hercule",
                "path_id": "DETECTIVE_ACADEMY",
                "case_id": "ACADEMY_001",
            },
        ).json()
        first_client.post(f"/api/v1/rounds/{created['id']}/start")
        first_client.post(f"/api/v1/rounds/{created['id']}/opening/complete")

    # Rebuilding the app proves the selected training file and progression are not
    # merely process-local React/Python variables.
    with TestClient(create_app(settings)) as second_client:
        response = second_client.get(f"/api/v1/rounds/{created['id']}/workspace")

    assert response.status_code == 200
    assert response.json()["round"]["case_id"] == "ACADEMY_001"
    assert response.json()["round"]["status"] == "ACTIVE"
    assert response.json()["round"]["intro_completed_at"] is not None
