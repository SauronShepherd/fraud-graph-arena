from fraud_graph_arena.application import build_container
from fraud_graph_arena.config import Settings
import pytest
from dataclasses import replace
from fraud_graph_arena.catalogue.domain import CaseStatus, CaseSummary, PathId
from fraud_graph_arena.narrative import ComicKind, ComicPage, ComicSequence, NarrativeService


def test_every_published_case_registers_opening_and_closing_sequences(test_settings: Settings) -> None:
    container = build_container(test_settings)

    for case in container.catalogue.list_cases():
        for kind in (ComicKind.OPENING, ComicKind.CLOSING):
            sequence = container.narrative.require_sequence(
                case_id=case.id,
                case_version=case.version,
                kind=kind,
            )
            assert sequence.pages
            assert all(page.narration and page.alt_text for page in sequence.pages)


def test_closing_sequence_is_registered_but_not_exposed_as_iteration_01_route(
    test_settings: Settings,
) -> None:
    container = build_container(test_settings)
    closing = container.narrative.require_sequence(
        case_id="ACADEMY_001",
        case_version="1.0.0-i01",
        kind=ComicKind.CLOSING,
    )

    assert closing.id == "ACADEMY_001_CLOSING"
    assert "conclusion" in closing.pages[0].narration.lower()


class SingleSequenceRepository:
    def __init__(self, sequence: ComicSequence):
        self.sequence = sequence

    def get_sequence(self, *, case_id: str, case_version: str, kind: ComicKind) -> ComicSequence | None:
        return self.sequence if kind == self.sequence.kind else None


def valid_case() -> CaseSummary:
    return CaseSummary("ACADEMY_001", "1.0.0-i01", PathId.DETECTIVE_ACADEMY, "Academy", "Training", CaseStatus.OPEN)


def valid_sequence(kind: ComicKind = ComicKind.OPENING) -> ComicSequence:
    return ComicSequence("SEQ", "ACADEMY_001", "1.0.0-i01", kind, True, (ComicPage("P1", 1, "Title", "Narration", "/image.svg", "Alt"),))


@pytest.mark.parametrize("mutator", [
    lambda sequence: replace(sequence, pages=()),
    lambda sequence: replace(sequence, pages=(replace(sequence.pages[0], position=0),)),
    lambda sequence: replace(sequence, pages=(replace(sequence.pages[0], title=""),)),
    lambda sequence: replace(sequence, pages=(replace(sequence.pages[0], image_url=""),)),
])
def test_invalid_published_sequence_is_rejected(mutator) -> None:
    sequence = mutator(valid_sequence())
    with pytest.raises(ValueError):
        NarrativeService(SingleSequenceRepository(sequence)).validate_case(valid_case())
