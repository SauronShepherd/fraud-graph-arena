from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum

from fraud_graph_arena.catalogue.domain import PathId
from fraud_graph_arena.release_engineering.migration import LEGACY_RELEASE_ID


class RoundStatus(StrEnum):
    CREATED = "CREATED"
    INTRO_PENDING = "INTRO_PENDING"
    ACTIVE = "ACTIVE"
    SUBMITTED = "SUBMITTED"

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
    credits_remaining: int = 0
    version: int = 1
    submitted_at: datetime | None = None
    submission_id: str | None = None
    # The authoritative investigation contract is bound when the round is
    # created. A later release may improve the board, but it must not silently
    # replace the rules that produced this round's evidence or score.
    release_id: str = LEGACY_RELEASE_ID
    package_version: str = "legacy-package"
    rules_version: str = "legacy-rules"
    economy_version: str = "legacy-economy"
    scoring_version: str = "legacy-scoring"
    screen_set_version: str = "legacy-screen-set"
    api_contract_version: str = "v1"
    analytics_version: str = "legacy-analytics"
    package_digest: str = "legacy-package-digest"

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

    def submit(self, submission_id: str, now: datetime | None = None) -> "Round":
        if self.status != RoundStatus.ACTIVE:
            return self
        return replace(
            self,
            status=RoundStatus.SUBMITTED,
            submitted_at=now or datetime.now(UTC),
            submission_id=submission_id,
            version=self.version + 1,
        )
