from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    return Settings(
        environment="test",
        round_repository="memory",
        sqlite_path=tmp_path / "rounds.sqlite3",
        frontend_dist=tmp_path / "missing-dist",
        allowed_origins=["http://testserver"],
    )


@pytest.fixture
def client(test_settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(test_settings)) as value:
        yield value
