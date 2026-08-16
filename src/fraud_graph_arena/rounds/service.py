from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from fraud_graph_arena.catalogue import CaseStatus, CaseSummary, CatalogueService
from fraud_graph_arena.narrative import ComicKind, ComicSequence, NarrativeService
from fraud_graph_arena.rounds.domain import IntroCompletion, Round, RoundStatus
from fraud_graph_arena.rounds.ports import RoundRepository
from fraud_graph_arena.shared.errors import ConflictError, NotFoundError


@dataclass(frozen=True, slots=True)
class Opening:
    round: Round
    case: CaseSummary
    sequence: ComicSequence


class RoundService:
    def __init__(
        self,
        *,
        repository: RoundRepository,
        catalogue: CatalogueService,
        narrative: NarrativeService,
    ) -> None:
        self._repository = repository
        self._catalogue = catalogue
        self._narrative = narrative

    def create(self, *, player_id: str, path_id: str, case_id: str) -> Round:
        case = self._catalogue.require_case_for_path(raw_path_id=path_id, case_id=case_id)
        if case.status != CaseStatus.OPEN:
            raise ConflictError(
                code="CASE_NOT_OPEN",
                title="Case is not open",
                detail=f"Case '{case.id}' cannot start from its current catalogue state.",
                recovery="Refresh the catalogue and choose an open case.",
            )
        self._narrative.validate_case(case)
        round_ = Round(
            id=str(uuid4()),
            player_id=player_id.strip() or "demo-hercule",
            path_id=case.path_id,
            case_id=case.id,
            case_version=case.version,
            status=RoundStatus.CREATED,
            created_at=datetime.now(UTC),
        )
        self._repository.add(round_)
        return round_

    def start(self, round_id: str) -> Round:
        round_ = self.require(round_id)
        case = self._case_for(round_)
        self._narrative.require_sequence(
            case_id=case.id,
            case_version=case.version,
            kind=ComicKind.OPENING,
        )
        started = round_.start()
        if started != round_:
            self._repository.save(started)
        return started

    def opening(self, round_id: str) -> Opening:
        round_ = self.require(round_id)
        if round_.status == RoundStatus.CREATED:
            raise ConflictError(
                code="ROUND_NOT_STARTED",
                title="Investigation has not started",
                detail=f"Round '{round_id}' must be started before its introduction is opened.",
                recovery="Start the round, then request its opening sequence.",
            )
        case = self._case_for(round_)
        sequence = self._narrative.require_sequence(
            case_id=case.id,
            case_version=case.version,
            kind=ComicKind.OPENING,
        )
        return Opening(round=round_, case=case, sequence=sequence)

    def complete_opening(self, round_id: str, *, completion: IntroCompletion = IntroCompletion.FINISHED) -> Round:
        round_ = self.require(round_id)
        if round_.status == RoundStatus.CREATED:
            raise ConflictError(
                code="ROUND_NOT_STARTED",
                title="Investigation has not started",
                detail=f"Round '{round_id}' cannot complete an introduction before it starts.",
                recovery="Start the round before completing its opening sequence.",
            )
        if completion == IntroCompletion.SKIPPED:
            case = self._case_for(round_)
            sequence = self._narrative.require_sequence(case_id=case.id, case_version=case.version, kind=ComicKind.OPENING)
            if not sequence.skippable:
                raise ConflictError(code="INTRO_NOT_SKIPPABLE", title="Introduction cannot be skipped", detail="This case requires the complete opening sequence.")
        completed = round_.complete_intro()
        if completed != round_:
            self._repository.save(completed)
        return completed

    def require(self, round_id: str) -> Round:
        round_ = self._repository.get(round_id)
        if round_ is None:
            raise NotFoundError(
                code="ROUND_NOT_FOUND",
                title="Investigation not found",
                detail=f"Round '{round_id}' does not exist or is no longer available.",
            )
        return round_

    def _case_for(self, round_: Round) -> CaseSummary:
        return self._catalogue.require_case_for_path(
            raw_path_id=round_.path_id.value,
            case_id=round_.case_id,
            case_version=round_.case_version,
        )
