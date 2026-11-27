from __future__ import annotations

from pathlib import Path
from typing import Iterator

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
