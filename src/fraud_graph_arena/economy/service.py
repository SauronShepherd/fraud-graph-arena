from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
import hashlib
import json
from threading import RLock
from typing import Any, Callable, TypeVar
from uuid import uuid4

from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.shared.errors import ConflictError
from fraud_graph_arena.observability import instrumented

from .models import ACTION_COSTS, ECONOMY_VERSION, LedgerEntry, LedgerEntryType
from .repository import LedgerRepository

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class EconomyReservation:
    entry: LedgerEntry
    created: bool
    replay_json: str | None = None


class EconomyService:
    """Own the debit/refund contract while Round keeps the fast balance snapshot."""

    def __init__(
        self,
        rounds: RoundService,
        repository: LedgerRepository,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
        new_id: Callable[[], str] = lambda: str(uuid4()),
        cost_provider: Callable[[str, str], int | None] | None = None,
    ) -> None:
        self._rounds = rounds
        self._repository = repository
        self._now = now
        self._new_id = new_id
        self._cost_provider = cost_provider
        self._lock = RLock()

    @instrumented("repository.economy.reserve")
    def reserve(self, round_id: str, action: str, idempotency_key: str, request_hash: str, cost: int | None = None) -> EconomyReservation:
        amount = (self._cost_provider(round_id, action) if self._cost_provider is not None else ACTION_COSTS.get(action)) if cost is None else cost
        if amount is None or amount <= 0:
            raise ValueError(f"unknown economy action: {action}")
        with self._lock:
            existing = self._repository.get_charge(round_id, idempotency_key)
            if existing is not None:
                if existing.request_hash != request_hash or existing.action != action:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Economy request identity was reused", detail="The idempotency key already belongs to a different paid action.", recovery="Retry the unchanged request or choose a new idempotency key.")
                if existing.status == "REFUNDED" and existing.result_json is None:
                    raise ConflictError(code="PAID_ACTION_RETRY_REQUIRES_NEW_KEY", title="The failed paid action was refunded", detail="This failed attempt is already recorded and refunded; a new attempt needs a new idempotency key.", recovery="Keep the request unchanged and generate a fresh key for a new attempt.")
                return EconomyReservation(existing, False, existing.result_json)
            updated_round = self._rounds.charge(round_id, amount)
            entry = LedgerEntry(
                entry_id=self._new_id(), round_id=round_id, idempotency_key=idempotency_key,
                request_hash=request_hash, action=action, entry_type=LedgerEntryType.CHARGE,
                amount=amount, balance_after=updated_round.credits_remaining, status="RESERVED",
                rules_version=ECONOMY_VERSION, created_at=self._now().astimezone(UTC).isoformat(),
            )
            try:
                self._repository.add(entry)
            except Exception:
                self._rounds.refund(round_id, amount)
                raise
            return EconomyReservation(entry, True)

    def settle(self, reservation: EconomyReservation, result: T, *, serialize: Callable[[T], str] | None = None, refund: bool = False) -> LedgerEntry:
        with self._lock:
            current_round = self._rounds.require(reservation.entry.round_id)
            entry = replace(
                reservation.entry,
                status="REFUNDED" if refund else "SETTLED",
                balance_after=current_round.credits_remaining,
                result_json=None if serialize is None else serialize(result),
            )
            if refund:
                current_round = self._rounds.refund(reservation.entry.round_id, reservation.entry.amount)
                entry = replace(entry, balance_after=current_round.credits_remaining)
                refund_entry = replace(entry, entry_id=self._new_id(), idempotency_key=f"{reservation.entry.idempotency_key}:refund", entry_type=LedgerEntryType.REFUND, status="SETTLED", amount=reservation.entry.amount, created_at=self._now().astimezone(UTC).isoformat())
                self._repository.add(refund_entry)
            self._repository.update(entry)
            return entry

    def execute(
        self,
        round_id: str,
        action: str,
        idempotency_key: str,
        request_hash: str,
        operation: Callable[[], T],
        *,
        serialize: Callable[[T], str] | None = None,
        deserialize: Callable[[str], T] | None = None,
        refund_if: Callable[[T], bool] = lambda result: False,
    ) -> tuple[T, bool]:
        with self._lock:
            reservation = self.reserve(round_id, action, idempotency_key, request_hash)
            if not reservation.created and reservation.replay_json is not None:
                if deserialize is None:
                    raise RuntimeError("a replayable economy result needs a deserializer")
                return deserialize(reservation.replay_json), False
            try:
                result = operation()
            except Exception:
                if reservation.created:
                    self.settle(reservation, None, refund=True)  # type: ignore[arg-type]
                raise
            self.settle(reservation, result, serialize=serialize, refund=refund_if(result))
            return result, reservation.created

    def ledger(self, round_id: str) -> tuple[LedgerEntry, ...]:
        self._rounds.require(round_id)
        return self._repository.list_for_round(round_id)

    @staticmethod
    def request_hash(payload: dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
