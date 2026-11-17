from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from fraud_graph_arena.catalogue.domain import PathId
from fraud_graph_arena.rounds.domain import Round, RoundStatus


class SqliteRoundRepository:
    """Small durable adapter for Iteration 01.

    The domain depends only on the RoundRepository port. This adapter can be replaced
    without changing round rules or API contracts.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS rounds (
                    id TEXT PRIMARY KEY,
                    player_id TEXT NOT NULL,
                    path_id TEXT NOT NULL,
                    case_id TEXT NOT NULL,
                    case_version TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT NULL,
                    intro_completed_at TEXT NULL,
                    credits_remaining INTEGER NOT NULL DEFAULT 0,
                    version INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(rounds)").fetchall()
            }
            if "intro_completed_at" not in columns:
                connection.execute("ALTER TABLE rounds ADD COLUMN intro_completed_at TEXT NULL")
            if "credits_remaining" not in columns:
                connection.execute("ALTER TABLE rounds ADD COLUMN credits_remaining INTEGER NOT NULL DEFAULT 0")
            if "version" not in columns:
                connection.execute("ALTER TABLE rounds ADD COLUMN version INTEGER NOT NULL DEFAULT 1")

    def add(self, round_: Round) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO rounds (
                    id, player_id, path_id, case_id, case_version, status, created_at,
                    started_at, intro_completed_at, credits_remaining, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._to_row(round_),
            )

    def get(self, round_id: str) -> Round | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM rounds WHERE id = ?",
                (round_id,),
            ).fetchone()
        return None if row is None else self._from_row(row)

    def save(self, round_: Round) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE rounds
                   SET player_id = ?, path_id = ?, case_id = ?, case_version = ?, status = ?,
                       created_at = ?, started_at = ?, intro_completed_at = ?,
                       credits_remaining = ?, version = ?
                 WHERE id = ?
                """,
                (
                    round_.player_id,
                    round_.path_id.value,
                    round_.case_id,
                    round_.case_version,
                    round_.status.value,
                    round_.created_at.isoformat(),
                    None if round_.started_at is None else round_.started_at.isoformat(),
                    (
                        None
                        if round_.intro_completed_at is None
                        else round_.intro_completed_at.isoformat()
                    ),
                    round_.credits_remaining,
                    round_.version,
                    round_.id,
                ),
            )
            if cursor.rowcount != 1:
                raise KeyError(round_.id)

    def is_ready(self) -> bool:
        try:
            with self._connect() as connection:
                value = connection.execute("SELECT 1").fetchone()[0]
            return value == 1
        except sqlite3.Error:
            return False

    def charge(self, round_id: str, amount: int) -> Round:
        if amount <= 0:
            raise ValueError("charge amount must be positive")
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE rounds
                   SET credits_remaining = credits_remaining - ?, version = version + 1
                 WHERE id = ? AND credits_remaining >= ?
                """,
                (amount, round_id, amount),
            )
            if cursor.rowcount != 1:
                row = connection.execute("SELECT id, credits_remaining FROM rounds WHERE id = ?", (round_id,)).fetchone()
                if row is None:
                    raise KeyError(round_id)
                raise ValueError("INSUFFICIENT_CREDITS")
            row = connection.execute("SELECT * FROM rounds WHERE id = ?", (round_id,)).fetchone()
        return self._from_row(row)

    def refund(self, round_id: str, amount: int) -> Round:
        if amount <= 0:
            raise ValueError("refund amount must be positive")
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE rounds
                   SET credits_remaining = credits_remaining + ?, version = version + 1
                 WHERE id = ?
                """,
                (amount, round_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(round_id)
            row = connection.execute("SELECT * FROM rounds WHERE id = ?", (round_id,)).fetchone()
        return self._from_row(row)

    @staticmethod
    def _to_row(round_: Round) -> tuple[str, str, str, str, str, str, str, str | None, str | None, int, int]:
        return (
            round_.id,
            round_.player_id,
            round_.path_id.value,
            round_.case_id,
            round_.case_version,
            round_.status.value,
            round_.created_at.isoformat(),
            None if round_.started_at is None else round_.started_at.isoformat(),
            (
                None
                if round_.intro_completed_at is None
                else round_.intro_completed_at.isoformat()
            ),
            round_.credits_remaining,
            round_.version,
        )

    @staticmethod
    def _from_row(row: sqlite3.Row) -> Round:
        return Round(
            id=row["id"],
            player_id=row["player_id"],
            path_id=PathId(row["path_id"]),
            case_id=row["case_id"],
            case_version=row["case_version"],
            status=RoundStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            started_at=(
                None if row["started_at"] is None else datetime.fromisoformat(row["started_at"])
            ),
            intro_completed_at=(
                None
                if row["intro_completed_at"] is None
                else datetime.fromisoformat(row["intro_completed_at"])
            ),
            credits_remaining=int(row["credits_remaining"] or 0),
            version=int(row["version"] or 1),
        )
