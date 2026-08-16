from __future__ import annotations

from fraud_graph_arena.catalogue.domain import CaseSummary
from fraud_graph_arena.narrative.domain import ComicKind, ComicSequence
from fraud_graph_arena.narrative.ports import NarrativeRepository
from fraud_graph_arena.shared.errors import NotFoundError


class NarrativeService:
    def __init__(self, repository: NarrativeRepository) -> None:
        self._repository = repository

    def require_sequence(
        self,
        *,
        case_id: str,
        case_version: str,
        kind: ComicKind,
    ) -> ComicSequence:
        sequence = self._repository.get_sequence(
            case_id=case_id,
            case_version=case_version,
            kind=kind,
        )
        if sequence is None:
            raise NotFoundError(
                code="COMIC_SEQUENCE_NOT_FOUND",
                title="Comic sequence not found",
                detail=(
                    f"Case '{case_id}' version '{case_version}' has no registered "
                    f"{kind.value.lower()} sequence."
                ),
            )
        return sequence

    def validate_case(self, case: CaseSummary) -> None:
        for kind in (ComicKind.OPENING, ComicKind.CLOSING):
            sequence = self.require_sequence(
                case_id=case.id,
                case_version=case.version,
                kind=kind,
            )
            if not sequence.pages:
                raise ValueError(f"{sequence.id} must contain at least one comic page")
            if not sequence.id or sequence.case_id != case.id or sequence.case_version != case.version or sequence.kind != kind:
                raise ValueError(f"{sequence.id or '<unnamed>'} has inconsistent sequence metadata")
            positions = tuple(page.position for page in sequence.pages)
            if positions != tuple(range(1, len(sequence.pages) + 1)):
                raise ValueError(f"{sequence.id} page positions must be contiguous and one-based")
            ids = tuple(page.id for page in sequence.pages)
            if any(not page.id.strip() or not page.title.strip() for page in sequence.pages) or len(set(ids)) != len(ids):
                raise ValueError(f"{sequence.id} pages require unique ids and non-empty titles")
            if any(not page.alt_text.strip() or not page.narration.strip() or not page.image_url.strip() for page in sequence.pages):
                raise ValueError(f"{sequence.id} pages require narration, image reference and alt text")
