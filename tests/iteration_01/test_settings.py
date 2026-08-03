from pathlib import Path

import pytest
from pydantic import ValidationError

from fraud_graph_arena.config import Settings


def test_production_rejects_process_local_round_state(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="durable round repository"):
        Settings(
            environment="production",
            round_repository="memory",
            sqlite_path=tmp_path / "unused.sqlite3",
            allowed_origins=["https://fga.example"],
        )


def test_production_rejects_wildcard_cors(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="origins must be explicit"):
        Settings(
            environment="production",
            round_repository="sqlite",
            sqlite_path=tmp_path / "rounds.sqlite3",
            allowed_origins=["*"],
        )
