from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fraud_graph_arena.case_data.graph_investigation import initial_subset


@dataclass(frozen=True, slots=True)
class GraphInvestigationService:
    """Authorizes graph operations against a published, player-safe graph."""

    graph_provider: object

    def _graph(self, round_id: str) -> dict:
        graph = self.graph_provider(round_id)
        if graph is None:
            raise KeyError(round_id)
        return graph

    def initial(self, round_id: str, seeds: Iterable[str] = (), limit: int = 100) -> dict:
        return initial_subset(self._graph(round_id), seeds=seeds, limit=limit)
