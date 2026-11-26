from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


@pytest.fixture
def client(tmp_path: Path):
    settings = Settings(environment="test", round_repository="memory", sqlite_path=tmp_path / "rounds.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as value:
        yield value


def active_t02(client: TestClient) -> str:
    response = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"})
    assert response.status_code == 201, response.text
    round_id = response.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete").status_code == 200
    return round_id
