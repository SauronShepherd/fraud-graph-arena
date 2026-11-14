from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from fraud_graph_arena.shared.errors import ConflictError

from ..service import InvestigationCommand


class SqliteInvestigationCommandRepository:
    """Durable adapter sharing the application's SQLite file with round state."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=5, isolation_level=None)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS investigation_commands (
                    command_id TEXT PRIMARY KEY,
                    round_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    action TEXT NOT NULL,
                    source_record_id TEXT NOT NULL,
                    target_record_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    charged_credits INTEGER NOT NULL,
                    revealed_record_ids_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE (round_id, idempotency_key)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_investigation_commands_round
                    ON investigation_commands(round_id, created_at, command_id)
                """
            )

    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                """
                SELECT * FROM investigation_commands
                 WHERE round_id = ? AND idempotency_key = ?
                """,
                (command.round_id, command.idempotency_key),
            ).fetchone()
            if existing is not None:
                stored = self._from_row(existing)
                if stored.request_hash != command.request_hash:
                    raise ConflictError(
                        code="IDEMPOTENCY_KEY_REUSED",
                        title="Investigation request identity was reused",
                        detail="The idempotency key already belongs to a different hypothesis.",
                        recovery="Use the original request or choose a new idempotency key.",
                    )
                connection.commit()
                return stored, False
            try:
                connection.execute(
                    """
                    INSERT INTO investigation_commands (
                        command_id, round_id, idempotency_key, request_hash, action,
                        source_record_id, target_record_id, relationship_type, status,
                        charged_credits, revealed_record_ids_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        command.command_id,
                        command.round_id,
                        command.idempotency_key,
                        command.request_hash,
                        command.action,
                        command.source_record_id,
                        command.target_record_id,
                        command.relationship_type,
                        command.status,
                        command.charged_credits,
                        json.dumps(list(command.revealed_record_ids), separators=(",", ":")),
                        command.created_at,
                    ),
                )
            except sqlite3.IntegrityError:
                raced = connection.execute(
                    """
                    SELECT * FROM investigation_commands
                     WHERE round_id = ? AND idempotency_key = ?
                    """,
                    (command.round_id, command.idempotency_key),
                ).fetchone()
                if raced is None:
                    raise
                stored = self._from_row(raced)
                if stored.request_hash != command.request_hash:
                    raise ConflictError(
                        code="IDEMPOTENCY_KEY_REUSED",
                        title="Investigation request identity was reused",
                        detail="The idempotency key already belongs to a different hypothesis.",
                        recovery="Use the original request or choose a new idempotency key.",
                    )
                connection.commit()
                return stored, False
            connection.commit()
            return command, True
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM investigation_commands
                 WHERE round_id = ?
                 ORDER BY created_at, command_id
                """,
                (round_id,),
            ).fetchall()
        return tuple(self._from_row(row) for row in rows)

    @staticmethod
    def _from_row(row: sqlite3.Row) -> InvestigationCommand:
        return InvestigationCommand(
            command_id=row["command_id"],
            round_id=row["round_id"],
            idempotency_key=row["idempotency_key"],
            request_hash=row["request_hash"],
            action=row["action"],
            source_record_id=row["source_record_id"],
            target_record_id=row["target_record_id"],
            relationship_type=row["relationship_type"],
            status=row["status"],
            charged_credits=int(row["charged_credits"]),
            revealed_record_ids=tuple(json.loads(row["revealed_record_ids_json"])),
            created_at=row["created_at"],
        )
