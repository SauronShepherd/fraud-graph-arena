from __future__ import annotations

from typing import Protocol

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .service import InvestigationCommand


class InvestigationCommandRepository(Protocol):
    def accept(self, command: InvestigationCommand) -> tuple[InvestigationCommand, bool]: ...
    def list_for_round(self, round_id: str) -> tuple[InvestigationCommand, ...]: ...
