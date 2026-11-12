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
