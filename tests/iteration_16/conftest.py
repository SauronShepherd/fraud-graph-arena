from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(environment="test", round_repository="memory", sqlite_path=tmp_path / "rounds.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as value:
        yield value
