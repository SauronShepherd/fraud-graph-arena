from __future__ import annotations

from typing import Protocol

from fraud_graph_arena.rounds.domain import Round


class RoundRepository(Protocol):
    def add(self, round_: Round) -> None: ...

    def get(self, round_id: str) -> Round | None: ...

    def save(self, round_: Round) -> None: ...

    def is_ready(self) -> bool: ...
