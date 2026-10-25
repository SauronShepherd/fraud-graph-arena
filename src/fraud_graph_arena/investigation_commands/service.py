from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
from typing import Callable
from uuid import uuid4

from fraud_graph_arena.case_data.academy_graph import t02_expandable_graph
from fraud_graph_arena.rounds.domain import RoundStatus
from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.shared.errors import ConflictError, InvalidRequestError, NotFoundError

from .ports import InvestigationCommandRepository

ALLOWED_RELATIONSHIPS = frozenset({"POSSIBLE_IDENTITY", "POSSIBLE_CONTROL", "POSSIBLE_FLOW"})


@dataclass(frozen=True, slots=True)
class InvestigationCommand:
    command_id: str
    round_id: str
    idempotency_key: str
    request_hash: str
    action: str
    source_record_id: str
    target_record_id: str
    relationship_type: str
    status: str
    charged_credits: int
    revealed_record_ids: tuple[str, ...]
    created_at: str


class InvestigationCommandService:
    """Accept a bounded, free manual hypothesis without changing evidence state."""

    def __init__(
        self,
        rounds: RoundService,
        repository: InvestigationCommandRepository,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        new_id: Callable[[], str] = lambda: str(uuid4()),
    ) -> None:
        self._rounds = rounds
        self._repository = repository
        self._now = now
        self._new_id = new_id

    def submit_hypothesis(
        self, round_id: str, idempotency_key: str, source_record_id: str,
        target_record_id: str, relationship_type: str,
    ) -> tuple[InvestigationCommand, bool]:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", idempotency_key):
            raise InvalidRequestError(code="INVALID_IDEMPOTENCY_KEY", title="Invalid request identity", detail="Use 1 to 128 letters, digits, dots, underscores, colons or hyphens; the first character must be alphanumeric.")
        if source_record_id == target_record_id:
            raise InvalidRequestError(code="INVALID_HYPOTHESIS_SUBJECTS", title="Invalid hypothesis subjects", detail="A hypothesis needs two different records.")
        if relationship_type not in ALLOWED_RELATIONSHIPS:
            raise InvalidRequestError(code="INVALID_HYPOTHESIS_TYPE", title="Invalid hypothesis type", detail="Choose a supported hypothesis relationship type.")

        round_ = self._rounds.require(round_id)
        if round_.status != RoundStatus.ACTIVE:
            raise ConflictError(code="ROUND_NOT_ACTIVE", title="Investigation is not active", detail="A hypothesis can only be recorded in an active round.", recovery="Open an active round and retry.")
        if round_.case_id != "ACADEMY_T02":
            raise ConflictError(code="ACTION_NOT_AVAILABLE", title="Action is unavailable", detail="Manual hypotheses are not enabled for this case.", recovery="Use a case with the manual-hypothesis capability.")
        allowed_ids = {node.record_id for node in t02_expandable_graph()["nodes"]}
        if source_record_id not in allowed_ids or target_record_id not in allowed_ids:
            raise NotFoundError(code="SUBJECT_NOT_AVAILABLE", title="Record is unavailable", detail="One or more hypothesis subjects are not available in this case.")

        payload = {
            "action": "MANUAL_HYPOTHESIS",
            "source_record_id": source_record_id,
            "target_record_id": target_record_id,
            "relationship_type": relationship_type,
        }
        request_hash = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        command = InvestigationCommand(
            command_id=self._new_id(), round_id=round_id, idempotency_key=idempotency_key,
            request_hash=request_hash, action="MANUAL_HYPOTHESIS", source_record_id=source_record_id,
            target_record_id=target_record_id, relationship_type=relationship_type, status="RECORDED",
            charged_credits=0, revealed_record_ids=(), created_at=self._now().astimezone(timezone.utc).isoformat(),
        )
        return self._repository.accept(command)

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        self._rounds.require(round_id)
        return self._repository.list_for_round(round_id)


def command_to_dict(command: InvestigationCommand) -> dict:
    return asdict(command)
