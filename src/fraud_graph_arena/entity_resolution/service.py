from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import json
import re
from threading import RLock
from typing import Any, Callable
from uuid import uuid4

from fraud_graph_arena.rounds.domain import RoundStatus
from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.shared.errors import ConflictError, InvalidRequestError, NotFoundError
from fraud_graph_arena.economy import EconomyReservation, EconomyService

from .engine import EntityResolutionEngine, load_t02_identity_records
from .models import IdentityReview, ResolutionRun
from .repository import EntityResolutionRepository

IDEMPOTENCY_KEY_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
ANALYSIS_COST = 3


class EntityResolutionService:
    def __init__(
        self,
        rounds: RoundService,
        repository: EntityResolutionRepository,
        *,
        engine: EntityResolutionEngine | None = None,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
        new_id: Callable[[], str] = lambda: str(uuid4()),
        economy: EconomyService | None = None,
        package_provider: Callable[[Any], Any] | None = None,
    ) -> None:
        self._rounds = rounds
        self._repository = repository
        self._engine = engine or EntityResolutionEngine()
        self._now = now
        self._new_id = new_id
        self._economy = economy
        self._package_provider = package_provider
        self._lock = RLock()

    def analyze(self, round_id: str, idempotency_key: str, focus_record_id: str | None = None) -> tuple[ResolutionRun, bool]:
        self._validate_key(idempotency_key)
        round_ = self._require_active_case(round_id)
        package = self._package_provider(round_) if self._package_provider is not None else None
        analysis_cost = int(package.economy.get("costs", {}).get("COMPARE_IDENTITIES", ANALYSIS_COST)) if package is not None else ANALYSIS_COST
        records = package.rows("published/records.csv") if package is not None else load_t02_identity_records()
        allowed_ids = {
            str(row["record_id"])
            for row in records
            if str(row.get("record_type", "")).upper() == "PERSON_RECORD"
        }
        if focus_record_id is not None and focus_record_id not in allowed_ids:
            raise NotFoundError(code="SUBJECT_NOT_AVAILABLE", title="Record is unavailable", detail="The selected record is not part of the published identity-resolution scope.")
        request_hash = self._hash({"action": "ENTITY_RESOLUTION", "focus_record_id": focus_record_id})
        with self._lock:
            existing = self._repository.get_run_by_key(round_id, idempotency_key)
            if existing is not None:
                if existing.request_hash != request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Analysis request identity was reused", detail="The idempotency key already belongs to a different entity-resolution request.", recovery="Use the original analysis request or choose a new idempotency key.")
                return existing, False
            reservation: EconomyReservation | None = None
            if self._economy is not None:
                reservation = self._economy.reserve(round_id, "COMPARE_IDENTITIES", idempotency_key, request_hash)
            else:
                self._rounds.charge(round_id, analysis_cost)
            try:
                created_at = self._now().astimezone(UTC).isoformat()
                run = self._engine.analyze(
                    records,
                    analysis_id=self._new_id(),
                    round_id=round_id,
                    idempotency_key=idempotency_key,
                    request_hash=request_hash,
                    focus_record_id=focus_record_id,
                    charged_credits=analysis_cost,
                    created_at=created_at,
                )
                stored, created = self._repository.accept_run(run)
            except Exception:
                if reservation is not None:
                    self._economy.settle(reservation, None, refund=True)
                else:
                    self._rounds.refund(round_id, analysis_cost)
                raise
            if not created:
                if reservation is not None:
                    self._economy.settle(reservation, stored, refund=True)
                else:
                    self._rounds.refund(round_id, analysis_cost)
            elif reservation is not None:
                self._economy.settle(reservation, stored)
            return stored, created

    def review(self, round_id: str, candidate_id: str, idempotency_key: str, outcome: str) -> tuple[IdentityReview, bool]:
        self._validate_key(idempotency_key)
        if outcome not in {"ACCEPTED", "REJECTED", "UNRESOLVED"}:
            raise InvalidRequestError(code="INVALID_REVIEW_OUTCOME", title="Invalid candidate outcome", detail="Choose accepted, rejected or unresolved for this player review.", recovery="Submit one of the supported candidate outcomes.")
        self._require_active_case(round_id)
        candidate = self._repository.find_candidate(round_id, candidate_id)
        if candidate is None:
            raise NotFoundError(code="CANDIDATE_NOT_FOUND", title="Identity candidate was not found", detail="Run the identity comparison before reviewing a candidate.")
        request_hash = self._hash({"action": "ENTITY_RESOLUTION_REVIEW", "candidate_id": candidate_id, "outcome": outcome})
        with self._lock:
            existing = self._repository.get_review_by_key(round_id, idempotency_key)
            if existing is not None:
                if existing.request_hash != request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Review request identity was reused", detail="The idempotency key already belongs to a different candidate review.", recovery="Use the original review request or choose a new idempotency key.")
                return existing, False
            review = IdentityReview(
                review_id=self._new_id(),
                round_id=round_id,
                candidate_id=candidate_id,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                outcome=outcome,
                status="RECORDED",
                created_at=self._now().astimezone(UTC).isoformat(),
            )
            return self._repository.accept_review(review)

    def history(self, round_id: str) -> tuple[tuple[ResolutionRun, ...], tuple[IdentityReview, ...]]:
        self._rounds.require(round_id)
        return self._repository.list_runs(round_id), self._repository.list_reviews(round_id)

    def graph_with_reviews(self, round_id: str, graph: dict) -> dict:
        latest_reviews: dict[str, IdentityReview] = {}
        for review in self._repository.list_reviews(round_id):
            previous = latest_reviews.get(review.candidate_id)
            if previous is None or (review.created_at, review.review_id) >= (previous.created_at, previous.review_id):
                latest_reviews[review.candidate_id] = review
        reviews = {candidate_id: review for candidate_id, review in latest_reviews.items() if review.outcome == "ACCEPTED"}
        if not reviews:
            return graph
        edges = list(graph["edges"])
        from fraud_graph_arena.case_data.graph_data import GraphEdge

        for candidate_id, review in reviews.items():
            candidate = self._repository.find_candidate(round_id, candidate_id)
            if candidate is None:
                continue
            edges.append(GraphEdge(
                relationship_id=f"ER-REVIEW-{review.review_id}",
                source_record_id=candidate.left_record_id,
                target_record_id=candidate.right_record_id,
                relationship_family="IDENTITY_REVIEW",
                directed=False,
                provenance=f"FGA09:ENTITY_RESOLUTION_REVIEW:{review.review_id}",
                relationship_type="PLAYER_REVIEWED_IDENTITY",
                player_safe_summary="Player-reviewed identity candidate; not a canonical merge or fraud verdict.",
                event_time=review.created_at,
            ))
        return {**graph, "edges": tuple(sorted(edges, key=lambda edge: edge.relationship_id)), "edge_count": len(edges)}

    @staticmethod
    def _validate_key(key: str) -> None:
        if not IDEMPOTENCY_KEY_PATTERN.fullmatch(key):
            raise InvalidRequestError(code="INVALID_IDEMPOTENCY_KEY", title="Invalid request identity", detail="Use 1 to 128 letters, digits, dots, underscores, colons or hyphens; the first character must be alphanumeric.", recovery="Generate a fresh key and retry the unchanged request.")

    def _require_active_case(self, round_id: str):
        round_ = self._rounds.require(round_id)
        if round_.status != RoundStatus.ACTIVE:
            raise ConflictError(code="ROUND_NOT_ACTIVE", title="Investigation is not active", detail="Entity resolution can only run in an active round.", recovery="Open an active round and retry.")
        package = self._package_provider(round_) if self._package_provider is not None else None
        if package is not None and not package.supports("COMPARE_IDENTITIES"):
            raise ConflictError(code="ACTION_NOT_AVAILABLE", title="Action is unavailable", detail="This case package does not declare identity comparison.", recovery="Choose one of the actions declared by the active case package.")
        return round_

    @staticmethod
    def _hash(payload: dict) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
