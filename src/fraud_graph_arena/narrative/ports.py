from __future__ import annotations

from typing import Protocol

from fraud_graph_arena.narrative.domain import ComicKind, ComicSequence


class NarrativeRepository(Protocol):
    def get_sequence(
        self,
        *,
        case_id: str,
        case_version: str,
        kind: ComicKind,
    ) -> ComicSequence | None: ...
