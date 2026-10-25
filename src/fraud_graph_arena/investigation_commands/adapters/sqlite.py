from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from fraud_graph_arena.shared.errors import ConflictError
from ..service import InvestigationCommand


class SqliteInvestigationCommandRepository:
    """Durable command ledger; inserts are atomic and keyed per round."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS investigation_commands (
                command_id TEXT PRIMARY KEY, round_id TEXT NOT NULL, idempotency_key TEXT NOT NULL,
                request_hash TEXT NOT NULL, action TEXT NOT NULL, source_record_id TEXT NOT NULL,
                target_record_id TEXT NOT NULL, relationship_type TEXT NOT NULL, status TEXT NOT NULL,
                charged_credits INTEGER NOT NULL CHECK(charged_credits = 0), revealed_record_ids TEXT NOT NULL,
                created_at TEXT NOT NULL, UNIQUE(round_id, idempotency_key)
            )""")

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self._path, timeout=5, isolation_level="IMMEDIATE")
        db.row_factory = sqlite3.Row
        return db

    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]:
        try:
            with self._connect() as db:
                db.execute("""INSERT INTO investigation_commands VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                    command.command_id, command.round_id, command.idempotency_key, command.request_hash,
                    command.action, command.source_record_id, command.target_record_id, command.relationship_type,
                    command.status, command.charged_credits, json.dumps(command.revealed_record_ids), command.created_at,
                ))
                return command, True
        except sqlite3.IntegrityError:
            with self._connect() as db:
                row = db.execute("SELECT * FROM investigation_commands WHERE round_id=? AND idempotency_key=?", (command.round_id, command.idempotency_key)).fetchone()
            if row is None:
                raise
            previous = self._from_row(row)
            if previous.request_hash != command.request_hash:
                raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Request identity conflict", detail="This idempotency key was already used for a different request.")
            return previous, False

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        with self._connect() as db:
            rows = db.execute("SELECT * FROM investigation_commands WHERE round_id=? ORDER BY created_at, command_id", (round_id,)).fetchall()
        return tuple(self._from_row(row) for row in rows)

    @staticmethod
    def _from_row(row: sqlite3.Row) -> InvestigationCommand:
        return InvestigationCommand(
            command_id=row["command_id"], round_id=row["round_id"], idempotency_key=row["idempotency_key"],
            request_hash=row["request_hash"], action=row["action"], source_record_id=row["source_record_id"],
            target_record_id=row["target_record_id"], relationship_type=row["relationship_type"], status=row["status"],
            charged_credits=row["charged_credits"], revealed_record_ids=tuple(json.loads(row["revealed_record_ids"])),
            created_at=row["created_at"],
        )
