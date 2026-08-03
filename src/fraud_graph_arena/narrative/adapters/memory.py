from __future__ import annotations

from fraud_graph_arena.narrative.domain import ComicKind, ComicPage, ComicSequence


class InMemoryNarrativeRepository:
    """Spoiler-free Academy narrative fixtures for the walking skeleton.

    Both opening and closing sequences are registered now so case-package completeness
    is enforced before the evaluator and ending flow exist. Only the opening sequence
    is player-reachable in Iteration 01.
    """

    def __init__(self) -> None:
        self._sequences = (
            ComicSequence(
                id="ACADEMY_001_OPENING",
                case_id="ACADEMY_001",
                case_version="1.0.0-i01",
                kind=ComicKind.OPENING,
                skippable=True,
                pages=(
                    ComicPage(
                        id="ACADEMY_001_OPENING_01",
                        position=1,
                        title="The Academy Door",
                        narration=(
                            "Hercule Perrot reports for training. The ranked case files remain "
                            "sealed upstairs, where spoilers cannot develop bad habits."
                        ),
                        image_url="/assets/academy-intro-01.svg",
                        alt_text=(
                            "Hercule Perrot, a curly Spanish Water Dog detective, standing outside "
                            "the Detective Academy beneath a rain-darkened lamp."
                        ),
                    ),
                    ComicPage(
                        id="ACADEMY_001_OPENING_02",
                        position=2,
                        title="A Board with Nothing to Hide",
                        narration=(
                            "Inside waits an empty evidence board. The first lesson is not to solve "
                            "a fraud, but to prove the whole journey reaches the correct room."
                        ),
                        image_url="/assets/academy-intro-02.svg",
                        alt_text=(
                            "Hercule facing an almost empty evidence board marked Academy 001, with "
                            "one folder and no real-case clues."
                        ),
                    ),
                ),
            ),
            ComicSequence(
                id="ACADEMY_001_CLOSING",
                case_id="ACADEMY_001",
                case_version="1.0.0-i01",
                kind=ComicKind.CLOSING,
                skippable=True,
                pages=(
                    ComicPage(
                        id="ACADEMY_001_CLOSING_01",
                        position=1,
                        title="Lesson Reserved",
                        narration=(
                            "The Academy conclusion is registered with the case package, but its "
                            "runtime door remains closed until submission and evaluation exist."
                        ),
                        image_url="/assets/academy-closing-01.svg",
                        alt_text=(
                            "A closed Academy case file stamped Conclusion Reserved for a later "
                            "iteration."
                        ),
                    ),
                ),
            ),
        )

    def get_sequence(
        self,
        *,
        case_id: str,
        case_version: str,
        kind: ComicKind,
    ) -> ComicSequence | None:
        normalized_case_id = case_id.strip().upper()
        return next(
            (
                item
                for item in self._sequences
                if item.case_id == normalized_case_id
                and item.case_version == case_version
                and item.kind == kind
            ),
            None,
        )
