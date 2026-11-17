from __future__ import annotations

from threading import RLock

from fraud_graph_arena.rounds.domain import Round


class InMemoryRoundRepository:
    def __init__(self) -> None:
        self._rounds: dict[str, Round] = {}
        self._lock = RLock()

    def add(self, round_: Round) -> None:
        with self._lock:
            if round_.id in self._rounds:
                raise ValueError(f"round already exists: {round_.id}")
            self._rounds[round_.id] = round_

    def get(self, round_id: str) -> Round | None:
        with self._lock:
            return self._rounds.get(round_id)

    def save(self, round_: Round) -> None:
        with self._lock:
            if round_.id not in self._rounds:
                raise KeyError(round_.id)
            self._rounds[round_.id] = round_

    def is_ready(self) -> bool:
        return True

    def charge(self, round_id: str, amount: int) -> Round:
        if amount <= 0:
            raise ValueError("charge amount must be positive")
        with self._lock:
            round_ = self._rounds.get(round_id)
            if round_ is None:
                raise KeyError(round_id)
            if round_.credits_remaining < amount:
                raise ValueError("INSUFFICIENT_CREDITS")
            charged = Round(
                id=round_.id,
                player_id=round_.player_id,
                path_id=round_.path_id,
                case_id=round_.case_id,
                case_version=round_.case_version,
                status=round_.status,
                created_at=round_.created_at,
                started_at=round_.started_at,
                intro_completed_at=round_.intro_completed_at,
                credits_remaining=round_.credits_remaining - amount,
                version=round_.version + 1,
            )
            self._rounds[round_id] = charged
            return charged

    def refund(self, round_id: str, amount: int) -> Round:
        if amount <= 0:
            raise ValueError("refund amount must be positive")
        with self._lock:
            round_ = self._rounds.get(round_id)
            if round_ is None:
                raise KeyError(round_id)
            refunded = Round(
                id=round_.id,
                player_id=round_.player_id,
                path_id=round_.path_id,
                case_id=round_.case_id,
                case_version=round_.case_version,
                status=round_.status,
                created_at=round_.created_at,
                started_at=round_.started_at,
                intro_completed_at=round_.intro_completed_at,
                credits_remaining=round_.credits_remaining + amount,
                version=round_.version + 1,
            )
            self._rounds[round_id] = refunded
            return refunded
