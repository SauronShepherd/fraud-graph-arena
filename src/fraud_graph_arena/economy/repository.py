from __future__ import annotations

from dataclasses import asdict, replace
from pathlib import Path
import json
import sqlite3
from threading import RLock
from typing import Protocol

from fraud_graph_arena.shared.errors import ConflictError

from .models import ECONOMY_VERSION, LedgerEntry, LedgerEntryType


class LedgerRepository(Protocol):
    def get_charge(self, round_id: str, idempotency_key: str) -> LedgerEntry | None: ...
    def add(self, entry: LedgerEntry) -> None: ...
    def update(self, entry: LedgerEntry) -> None: ...
    def list_for_round(self, round_id: str) -> tuple[LedgerEntry, ...]: ...


class InMemoryLedgerRepository:
    def __init__(self) -> None:
        self._entries: dict[tuple[str, str, LedgerEntryType], LedgerEntry] = {}
        self._lock = RLock()

    def get_charge(self, round_id: str, idempotency_key: str) -> LedgerEntry | None:
        with self._lock:
            return self._entries.get((round_id, idempotency_key, LedgerEntryType.CHARGE))

    def add(self, entry: LedgerEntry) -> None:
        with self._lock:
            key = (entry.round_id, entry.idempotency_key, entry.entry_type)
            if key in self._entries:
                raise ConflictError(code="LEDGER_ENTRY_EXISTS", title="Ledger entry already exists", detail="The same economy event has already been recorded.")
            self._entries[key] = entry

    def update(self, entry: LedgerEntry) -> None:
        with self._lock:
            key = (entry.round_id, entry.idempotency_key, entry.entry_type)
            if key not in self._entries:
                raise KeyError(key)
            self._entries[key] = entry

    def list_for_round(self, round_id: str) -> tuple[LedgerEntry, ...]:
        with self._lock:
            return tuple(sorted((entry for entry in self._entries.values() if entry.round_id == round_id), key=lambda item: (item.created_at, item.entry_id)))


class SqliteLedgerRepository:
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
                CREATE TABLE IF NOT EXISTS credit_ledger (
                    entry_id TEXT PRIMARY KEY,
                    round_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    action TEXT NOT NULL,
                    entry_type TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    balance_after INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    rules_version TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    result_json TEXT NULL,
                    UNIQUE(round_id, idempotency_key, entry_type)
                )
                """
            )

    def get_charge(self, round_id: str, idempotency_key: str) -> LedgerEntry | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM credit_ledger WHERE round_id=? AND idempotency_key=? AND entry_type=?", (round_id, idempotency_key, LedgerEntryType.CHARGE.value)).fetchone()
        return None if row is None else self._from_row(row)

    def add(self, entry: LedgerEntry) -> None:
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO credit_ledger (entry_id,round_id,idempotency_key,request_hash,action,entry_type,amount,balance_after,status,rules_version,created_at,result_json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    self._to_row(entry),
                )
        except sqlite3.IntegrityError as error:
            raise ConflictError(code="LEDGER_ENTRY_EXISTS", title="Ledger entry already exists", detail="The same economy event has already been recorded.") from error

    def update(self, entry: LedgerEntry) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE credit_ledger SET request_hash=?, action=?, amount=?, balance_after=?, status=?, rules_version=?, created_at=?, result_json=? WHERE entry_id=?",
                (entry.request_hash, entry.action, entry.amount, entry.balance_after, entry.status, entry.rules_version, entry.created_at, entry.result_json, entry.entry_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(entry.entry_id)

    def list_for_round(self, round_id: str) -> tuple[LedgerEntry, ...]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM credit_ledger WHERE round_id=? ORDER BY created_at, entry_id", (round_id,)).fetchall()
        return tuple(self._from_row(row) for row in rows)

    @staticmethod
    def _to_row(entry: LedgerEntry) -> tuple[object, ...]:
        return (entry.entry_id, entry.round_id, entry.idempotency_key, entry.request_hash, entry.action, entry.entry_type.value, entry.amount, entry.balance_after, entry.status, entry.rules_version, entry.created_at, entry.result_json)

    @staticmethod
    def _from_row(row: sqlite3.Row) -> LedgerEntry:
        return LedgerEntry(
            entry_id=row["entry_id"], round_id=row["round_id"], idempotency_key=row["idempotency_key"], request_hash=row["request_hash"], action=row["action"], entry_type=LedgerEntryType(row["entry_type"]), amount=int(row["amount"]), balance_after=int(row["balance_after"]), status=row["status"], rules_version=row["rules_version"] or ECONOMY_VERSION, created_at=row["created_at"], result_json=row["result_json"],
        )
