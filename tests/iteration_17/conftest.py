from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    frontend = tmp_path / "dist"
    frontend.mkdir()
    (frontend / "index.html").write_text("<html><body>FGA</body></html>", encoding="utf-8")
    settings = Settings(
        environment="production",
        round_repository="sqlite",
        sqlite_path=tmp_path / "rounds.sqlite3",
        frontend_dist=frontend,
        allowed_origins=[],
    )
    with TestClient(create_app(settings)) as value:
        yield value
