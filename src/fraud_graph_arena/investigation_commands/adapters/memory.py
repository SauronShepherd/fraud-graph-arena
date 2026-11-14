from __future__ import annotations

from threading import RLock

from fraud_graph_arena.shared.errors import ConflictError

from ..service import InvestigationCommand


class InMemoryInvestigationCommandRepository:
    """Thread-safe reference adapter used by tests and ephemeral development."""

    def __init__(self) -> None:
        self._commands: dict[tuple[str, str], InvestigationCommand] = {}
        self._lock = RLock()

    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]:
        key = (command.round_id, command.idempotency_key)
        with self._lock:
            existing = self._commands.get(key)
            if existing is not None:
                if existing.request_hash != command.request_hash:
                    raise ConflictError(
                        code="IDEMPOTENCY_KEY_REUSED",
                        title="Investigation request identity was reused",
                        detail="The idempotency key already belongs to a different hypothesis.",
                        recovery="Use the original request or choose a new idempotency key.",
                    )
                return existing, False
            self._commands[key] = command
            return command, True

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        with self._lock:
            values = [item for item in self._commands.values() if item.round_id == round_id]
        return tuple(sorted(values, key=lambda item: (item.created_at, item.command_id)))
