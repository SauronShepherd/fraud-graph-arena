"""Durable, player-authored investigation commands."""

from .service import InvestigationCommand, InvestigationCommandService, command_to_dict

__all__ = ["InvestigationCommand", "InvestigationCommandService", "command_to_dict"]
