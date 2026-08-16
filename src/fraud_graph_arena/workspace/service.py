from __future__ import annotations

from dataclasses import dataclass

from fraud_graph_arena.catalogue import CaseSummary, CatalogueService
from fraud_graph_arena.rounds.domain import Round, RoundStatus
from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.shared.errors import ConflictError

@dataclass(frozen=True, slots=True)
class WorkspaceProjection:
    round: Round
    case: CaseSummary
    path_name: str
    empty_state_code: str
    evidence_count: int
    suspect_count: int
    actions: tuple[dict[str, str], ...]

class WorkspaceService:
    def __init__(self, rounds: RoundService, catalogue: CatalogueService) -> None:
        self._rounds = rounds
        self._catalogue = catalogue

    def get(self, round_id: str) -> WorkspaceProjection:
        round_ = self._rounds.require(round_id)
        if round_.status == RoundStatus.CREATED:
            raise ConflictError(code="ROUND_NOT_STARTED", title="Investigation has not started", detail=f"Round '{round_id}' has not started.", recovery="Start the investigation before opening the board.")
        if round_.status == RoundStatus.INTRO_PENDING:
            raise ConflictError(code="INTRO_REQUIRED", title="Academy introduction required", detail="Complete or skip the registered opening comic before entering the board.", recovery=f"Open /rounds/{round_id}/intro and finish the Academy briefing.")
        case = self._catalogue.require_case_for_path(raw_path_id=round_.path_id.value, case_id=round_.case_id, case_version=round_.case_version)
        actions = tuple({"id": action, "state": "NOT_IMPLEMENTED", "reason_code": "CAPABILITY_NOT_IMPLEMENTED", "reason": reason} for action, reason in (
            ("COMPARE_IDENTITIES", "Identity comparison is not available in Academy yet."),
            ("FIND_SHARED_FIELDS", "Exact shared-field analysis is not available in Academy yet."),
            ("SEARCH_EVIDENCE", "Evidence search will unlock when the case publishes evidence."),
            ("OPEN_CASE_FILE", "Case-file construction is not available in the empty Academy round."),
        ))
        path = next(path for path in self._catalogue.list_paths() if path.id == round_.path_id)
        return WorkspaceProjection(round_, case, path.name, "NO_EVIDENCE_REVEALED", 0, 0, actions)
