from __future__ import annotations

from dataclasses import asdict
from contextlib import contextmanager
import json
import sqlite3
from pathlib import Path
from threading import RLock
from typing import Protocol

from fraud_graph_arena.shared.errors import ConflictError

from .models import ExactIdentityMatch, IdentityCandidate, IdentityReview, ResolutionRun


class EntityResolutionRepository(Protocol):
    def get_run_by_key(self, round_id: str, idempotency_key: str) -> ResolutionRun | None: ...
    def accept_run(self, run: ResolutionRun) -> tuple[ResolutionRun, bool]: ...
    def list_runs(self, round_id: str) -> tuple[ResolutionRun, ...]: ...
    def find_candidate(self, round_id: str, candidate_id: str) -> IdentityCandidate | None: ...
    def get_review_by_key(self, round_id: str, idempotency_key: str) -> IdentityReview | None: ...
    def accept_review(self, review: IdentityReview) -> tuple[IdentityReview, bool]: ...
    def list_reviews(self, round_id: str) -> tuple[IdentityReview, ...]: ...


def _candidate_to_dict(item: IdentityCandidate) -> dict:
    return asdict(item)


def _match_to_dict(item: ExactIdentityMatch) -> dict:
    return asdict(item)


def _run_to_payload(run: ResolutionRun) -> str:
    payload = asdict(run)
    payload["exact_matches"] = [_match_to_dict(item) for item in run.exact_matches]
    payload["candidates"] = [_candidate_to_dict(item) for item in run.candidates]
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def _run_from_payload(payload: str) -> ResolutionRun:
    raw = json.loads(payload)
    for item in raw["exact_matches"]:
        item.setdefault("provenance_refs", [])
    raw["exact_matches"] = tuple(ExactIdentityMatch(**item) for item in raw["exact_matches"])
    raw["candidates"] = tuple(IdentityCandidate(**item) for item in raw["candidates"])
    return ResolutionRun(**raw)


class InMemoryEntityResolutionRepository:
    def __init__(self) -> None:
        self._runs: dict[tuple[str, str], ResolutionRun] = {}
        self._reviews: dict[tuple[str, str], IdentityReview] = {}
        self._lock = RLock()

    def get_run_by_key(self, round_id: str, idempotency_key: str) -> ResolutionRun | None:
        with self._lock:
            return self._runs.get((round_id, idempotency_key))

    def accept_run(self, run: ResolutionRun) -> tuple[ResolutionRun, bool]:
        with self._lock:
            key = (run.round_id, run.idempotency_key)
            existing = self._runs.get(key)
            if existing is not None:
                if existing.request_hash != run.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Analysis request identity was reused", detail="The idempotency key already belongs to a different entity-resolution request.", recovery="Use the original request or choose a new idempotency key.")
                return existing, False
            self._runs[key] = run
            return run, True

    def list_runs(self, round_id: str) -> tuple[ResolutionRun, ...]:
        with self._lock:
            return tuple(sorted((run for run in self._runs.values() if run.round_id == round_id), key=lambda item: (item.created_at, item.analysis_id)))

    def find_candidate(self, round_id: str, candidate_id: str) -> IdentityCandidate | None:
        with self._lock:
            for run in self.list_runs(round_id):
                for candidate in run.candidates:
                    if candidate.candidate_id == candidate_id:
                        return candidate
        return None

    def get_review_by_key(self, round_id: str, idempotency_key: str) -> IdentityReview | None:
        with self._lock:
            return self._reviews.get((round_id, idempotency_key))

    def accept_review(self, review: IdentityReview) -> tuple[IdentityReview, bool]:
        with self._lock:
            key = (review.round_id, review.idempotency_key)
            existing = self._reviews.get(key)
            if existing is not None:
                if existing.request_hash != review.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Review request identity was reused", detail="The idempotency key already belongs to a different candidate review.", recovery="Use the original review request or choose a new idempotency key.")
                return existing, False
            self._reviews[key] = review
            return review, True

    def list_reviews(self, round_id: str) -> tuple[IdentityReview, ...]:
        with self._lock:
            return tuple(sorted((review for review in self._reviews.values() if review.round_id == round_id), key=lambda item: (item.created_at, item.review_id)))


class SqliteEntityResolutionRepository:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS identity_resolution_runs (
                    analysis_id TEXT PRIMARY KEY,
                    round_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(round_id, idempotency_key)
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS identity_resolution_reviews (
                    review_id TEXT PRIMARY KEY,
                    round_id TEXT NOT NULL,
                    candidate_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(round_id, idempotency_key)
                )
            """)

    def get_run_by_key(self, round_id: str, idempotency_key: str) -> ResolutionRun | None:
        with self._connection() as connection:
            row = connection.execute("SELECT payload_json FROM identity_resolution_runs WHERE round_id=? AND idempotency_key=?", (round_id, idempotency_key)).fetchone()
        return None if row is None else _run_from_payload(row["payload_json"])

    def accept_run(self, run: ResolutionRun) -> tuple[ResolutionRun, bool]:
        with self._connection() as connection:
            existing = connection.execute("SELECT payload_json FROM identity_resolution_runs WHERE round_id=? AND idempotency_key=?", (run.round_id, run.idempotency_key)).fetchone()
            if existing is not None:
                stored = _run_from_payload(existing["payload_json"])
                if stored.request_hash != run.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Analysis request identity was reused", detail="The idempotency key already belongs to a different entity-resolution request.", recovery="Use the original request or choose a new idempotency key.")
                return stored, False
            connection.execute("INSERT INTO identity_resolution_runs (analysis_id,round_id,idempotency_key,request_hash,payload_json,created_at) VALUES (?,?,?,?,?,?)", (run.analysis_id, run.round_id, run.idempotency_key, run.request_hash, _run_to_payload(run), run.created_at))
            return run, True

    def list_runs(self, round_id: str) -> tuple[ResolutionRun, ...]:
        with self._connection() as connection:
            rows = connection.execute("SELECT payload_json FROM identity_resolution_runs WHERE round_id=? ORDER BY created_at, analysis_id", (round_id,)).fetchall()
        return tuple(_run_from_payload(row["payload_json"]) for row in rows)

    def find_candidate(self, round_id: str, candidate_id: str) -> IdentityCandidate | None:
        for run in self.list_runs(round_id):
            for candidate in run.candidates:
                if candidate.candidate_id == candidate_id:
                    return candidate
        return None

    def get_review_by_key(self, round_id: str, idempotency_key: str) -> IdentityReview | None:
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM identity_resolution_reviews WHERE round_id=? AND idempotency_key=?", (round_id, idempotency_key)).fetchone()
        return None if row is None else self._review_from_row(row)

    def accept_review(self, review: IdentityReview) -> tuple[IdentityReview, bool]:
        with self._connection() as connection:
            existing = connection.execute("SELECT * FROM identity_resolution_reviews WHERE round_id=? AND idempotency_key=?", (review.round_id, review.idempotency_key)).fetchone()
            if existing is not None:
                stored = self._review_from_row(existing)
                if stored.request_hash != review.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Review request identity was reused", detail="The idempotency key already belongs to a different candidate review.", recovery="Use the original review request or choose a new idempotency key.")
                return stored, False
            connection.execute("INSERT INTO identity_resolution_reviews (review_id,round_id,candidate_id,idempotency_key,request_hash,outcome,status,created_at) VALUES (?,?,?,?,?,?,?,?)", (review.review_id, review.round_id, review.candidate_id, review.idempotency_key, review.request_hash, review.outcome, review.status, review.created_at))
            return review, True

    def list_reviews(self, round_id: str) -> tuple[IdentityReview, ...]:
        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM identity_resolution_reviews WHERE round_id=? ORDER BY created_at, review_id", (round_id,)).fetchall()
        return tuple(self._review_from_row(row) for row in rows)

    @staticmethod
    def _review_from_row(row: sqlite3.Row) -> IdentityReview:
        return IdentityReview(review_id=row["review_id"], round_id=row["round_id"], candidate_id=row["candidate_id"], idempotency_key=row["idempotency_key"], request_hash=row["request_hash"], outcome=row["outcome"], status=row["status"], created_at=row["created_at"])
