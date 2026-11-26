from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import json
import re
from typing import Any, Callable
from uuid import uuid4

from fraud_graph_arena.economy import ECONOMY_VERSION, EconomyService
from fraud_graph_arena.rounds.domain import RoundStatus
from fraud_graph_arena.rounds.service import Closing, RoundService
from fraud_graph_arena.shared.errors import ConflictError, InvalidRequestError, NotFoundError

from .evaluator import evaluate, published_record_ids
from .models import SCORING_VERSION, SubmissionResult
from .repository import SubmissionRepository


KEY_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")


class CaseResolutionService:
    def __init__(self, rounds: RoundService, economy: EconomyService, repository: SubmissionRepository, *, package_provider: Callable[[Any], Any] | None = None, now: Callable[[], datetime] = lambda: datetime.now(UTC), new_id: Callable[[], str] = lambda: str(uuid4())) -> None:
        self._rounds = rounds
        self._economy = economy
        self._repository = repository
        self._package_provider = package_provider
        self._now = now
        self._new_id = new_id

    def submit(self, round_id: str, idempotency_key: str, suspect_record_ids: list[str], evidence_claim_ids: list[str], expected_round_version: int | None = None) -> tuple[SubmissionResult, bool]:
        if not KEY_PATTERN.fullmatch(idempotency_key):
            raise InvalidRequestError(code="INVALID_IDEMPOTENCY_KEY", title="Invalid submission identity", detail="Use 1 to 128 letters, digits, dots, underscores, colons or hyphens; the first character must be alphanumeric.")
        round_ = self._rounds.require(round_id)
        package = self._package_provider(round_) if self._package_provider is not None else None
        if package is None or not package.supports("SUBMIT"):
            raise ConflictError(code="ACTION_NOT_AVAILABLE", title="Case resolution is unavailable", detail="This case package has no submission contract.", recovery="Choose a published package with a resolution workflow.")
        request = {"suspect_record_ids": sorted(set(suspect_record_ids)), "evidence_claim_ids": sorted(set(evidence_claim_ids)), "expected_round_version": expected_round_version}
        request_hash = hashlib.sha256(json.dumps(request, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        existing = self._repository.get_by_key(round_id, idempotency_key)
        if existing is not None:
            if existing.request_hash != request_hash:
                raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Submission request identity was reused", detail="The submission key already belongs to different evidence.", recovery="Retry the unchanged submission or choose a new key.")
            return existing, False
        if round_.status != RoundStatus.ACTIVE:
            raise ConflictError(code="ROUND_NOT_ACTIVE", title="Investigation is not active", detail="A case can only be submitted from an active round.", recovery="Use the active case board before submitting.")
        if expected_round_version is not None and expected_round_version != round_.version:
            raise ConflictError(code="STALE_ROUND_VERSION", title="The case changed while you were investigating", detail="The submission was based on an older round version and was not recorded.", recovery="Reload the board and review the current ledger before submitting again.")
        if len(suspect_record_ids) > 20 or len(evidence_claim_ids) > 32:
            raise InvalidRequestError(code="SUBMISSION_TOO_LARGE", title="Submission is too large", detail="A submission is limited to twenty suspect records and thirty-two evidence claims.")
        unknown = sorted(set(suspect_record_ids) - published_record_ids(package))
        if unknown:
            raise NotFoundError(code="SUBJECT_NOT_AVAILABLE", title="A submitted record is unavailable", detail=f"The published case does not contain: {', '.join(unknown[:5])}.")
        score, ending, dimensions, false_accusations, complete, title, narrative = evaluate(round_, package, self._economy.ledger(round_id), suspect_record_ids, evidence_claim_ids)
        result = SubmissionResult(
            submission_id=self._new_id(), round_id=round_id, idempotency_key=idempotency_key, status="RECORDED", score=score, ending_code=ending, ending_title=title, ending_narrative=narrative, dimensions=dimensions, false_accusations=false_accusations, required_claims_complete=complete, submitted_suspect_count=len(set(suspect_record_ids)), credits_remaining=round_.credits_remaining, scoring_version=package.scoring_version, economy_version=package.economy_version, created_at=self._now().astimezone(UTC).isoformat(), request_hash=request_hash,
        )
        self._repository.add(result)
        self._rounds.submit(round_id, result.submission_id)
        return result, True

    def get(self, round_id: str) -> SubmissionResult | None:
        self._rounds.require(round_id)
        results = self._repository.list_for_round(round_id)
        return results[0] if results else None

    def closing(self, round_id: str) -> Closing:
        return self._rounds.closing(round_id)
