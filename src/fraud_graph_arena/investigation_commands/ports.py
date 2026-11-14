from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .service import InvestigationCommand


class InvestigationCommandRepository(Protocol):
    """Storage contract for accepted investigation commands."""

    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]:
        """Return the stored command and whether this call created it."""

    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]:
        """Return the semantic command history for one round."""
