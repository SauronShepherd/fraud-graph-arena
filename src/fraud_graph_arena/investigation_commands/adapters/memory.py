from __future__ import annotations

from threading import RLock

from fraud_graph_arena.shared.errors import ConflictError
from ..service import InvestigationCommand


class InMemoryInvestigationCommandRepository:
    def __init__(self) -> None:
        self._lock = RLock()
        self._by_key: dict[tuple[str, str], InvestigationCommand] = {}

    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]:
        key = (command.round_id, command.idempotency_key)
        with self._lock:
            previous = self._by_key.get(key)
            if previous:
                if previous.request_hash != command.request_hash:
                    raise ConflictError(code="IDEMPOTENCY_KEY_REUSED", title="Request identity conflict", detail="This idempotency key was already used for a different request.")
                return previous, False
            self._by_key[key] = command
            return command, True

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        with self._lock:
            return tuple(sorted((item for item in self._by_key.values() if item.round_id == round_id), key=lambda item: (item.created_at, item.command_id)))
