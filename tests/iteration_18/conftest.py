from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(
        environment="test",
        round_repository="sqlite",
        sqlite_path=tmp_path / "rounds.sqlite3",
        frontend_dist=tmp_path / "missing",
        allowed_origins=[],
    )
    with TestClient(create_app(settings)) as value:
        yield value


def active_t02(client: TestClient, *, headers: dict[str, str] | None = None) -> str:
    request_headers = headers or {}
    created = client.post(
        "/api/v1/rounds",
        headers=request_headers,
        json={"player_id": "observability-test-player", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"},
    )
    assert created.status_code == 201, created.text
    round_id = created.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start", headers=request_headers).status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete", headers=request_headers).status_code == 200
    return round_id
