from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum

from fraud_graph_arena.catalogue.domain import PathId


class RoundStatus(StrEnum):
    CREATED = "CREATED"
    INTRO_PENDING = "INTRO_PENDING"
    ACTIVE = "ACTIVE"

class IntroCompletion(StrEnum):
    FINISHED = "FINISHED"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True, slots=True)
class Round:
    id: str
    player_id: str
    path_id: PathId
    case_id: str
    case_version: str
    status: RoundStatus
    created_at: datetime
    started_at: datetime | None = None
    intro_completed_at: datetime | None = None

    def start(self, now: datetime | None = None) -> "Round":
        if self.status != RoundStatus.CREATED:
            return self
        return replace(
            self,
            status=RoundStatus.INTRO_PENDING,
            started_at=now or datetime.now(UTC),
        )

    def complete_intro(self, now: datetime | None = None) -> "Round":
        if self.status == RoundStatus.ACTIVE:
            return self
        if self.status != RoundStatus.INTRO_PENDING:
            return self
        return replace(
            self,
            status=RoundStatus.ACTIVE,
            intro_completed_at=now or datetime.now(UTC),
        )
