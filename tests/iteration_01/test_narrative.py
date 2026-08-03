from fraud_graph_arena.application import build_container
from fraud_graph_arena.config import Settings
from fraud_graph_arena.narrative import ComicKind


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
