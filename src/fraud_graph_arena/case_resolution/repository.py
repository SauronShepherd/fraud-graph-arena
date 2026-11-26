from __future__ import annotations

from dataclasses import asdict, replace
from pathlib import Path
import json
import sqlite3
from threading import RLock
from typing import Protocol

from fraud_graph_arena.shared.errors import ConflictError

from .models import ScoreDimensions, SubmissionResult


class SubmissionRepository(Protocol):
    def get_by_key(self, round_id: str, idempotency_key: str) -> SubmissionResult | None: ...
    def add(self, result: SubmissionResult) -> None: ...
    def list_for_round(self, round_id: str) -> tuple[SubmissionResult, ...]: ...


def _payload(result: SubmissionResult) -> str:
    value = asdict(result)
    value["dimensions"] = result.dimensions.as_dict()
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _from_payload(value: str) -> SubmissionResult:
    raw = json.loads(value)
    raw["dimensions"] = ScoreDimensions(**raw["dimensions"])
    return SubmissionResult(**raw)


class InMemorySubmissionRepository:
    def __init__(self) -> None:
        self._results: dict[tuple[str, str], SubmissionResult] = {}
        self._lock = RLock()

    def get_by_key(self, round_id: str, idempotency_key: str) -> SubmissionResult | None:
        with self._lock:
            return self._results.get((round_id, idempotency_key))

    def add(self, result: SubmissionResult) -> None:
        with self._lock:
            key = (result.round_id, result.idempotency_key)
            existing = self._results.get(key)
            if existing is not None:
                if existing.request_hash != result.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Submission request identity was reused", detail="The submission key already belongs to different evidence.")
                return
            if any(item.round_id == result.round_id for item in self._results.values()):
                raise ConflictError(code="ROUND_ALREADY_SUBMITTED", title="Case is already closed", detail="A submitted case cannot be replaced by another submission.")
            self._results[key] = result

    def list_for_round(self, round_id: str) -> tuple[SubmissionResult, ...]:
        with self._lock:
            return tuple(sorted((item for item in self._results.values() if item.round_id == round_id), key=lambda item: (item.created_at, item.submission_id)))


class SqliteSubmissionRepository:
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
            connection.execute("CREATE TABLE IF NOT EXISTS case_submissions (submission_id TEXT PRIMARY KEY, round_id TEXT NOT NULL, idempotency_key TEXT NOT NULL, request_hash TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL, UNIQUE(round_id, idempotency_key), UNIQUE(round_id))")

    def get_by_key(self, round_id: str, idempotency_key: str) -> SubmissionResult | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload_json FROM case_submissions WHERE round_id=? AND idempotency_key=?", (round_id, idempotency_key)).fetchone()
        return None if row is None else _from_payload(row["payload_json"])

    def add(self, result: SubmissionResult) -> None:
        try:
            with self._connect() as connection:
                connection.execute("INSERT INTO case_submissions (submission_id,round_id,idempotency_key,request_hash,payload_json,created_at) VALUES (?,?,?,?,?,?)", (result.submission_id, result.round_id, result.idempotency_key, result.request_hash, _payload(result), result.created_at))
        except sqlite3.IntegrityError as error:
            with self._connect() as connection:
                existing = connection.execute("SELECT payload_json FROM case_submissions WHERE round_id=? AND idempotency_key=?", (result.round_id, result.idempotency_key)).fetchone()
            if existing is not None and _from_payload(existing["payload_json"]).request_hash == result.request_hash:
                return
            raise ConflictError(code="ROUND_ALREADY_SUBMITTED", title="Case is already closed", detail="A submitted case cannot be replaced by another submission.") from error

    def list_for_round(self, round_id: str) -> tuple[SubmissionResult, ...]:
        with self._connect() as connection:
            rows = connection.execute("SELECT payload_json FROM case_submissions WHERE round_id=? ORDER BY created_at, submission_id", (round_id,)).fetchall()
        return tuple(_from_payload(row["payload_json"]) for row in rows)
