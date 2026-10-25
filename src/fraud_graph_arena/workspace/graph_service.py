from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fraud_graph_arena.case_data.graph_investigation import DEFAULT_INITIAL_EDGES, DEFAULT_INITIAL_NODES, MAX_GRAPH_EDGES, MAX_GRAPH_NODES, expand, filter_relationships, initial_subset

_FORBIDDEN_PLAYER_KEYS = {"truth", "culpability", "protected_notes", "expected_classification", "scoring_rules", "ending_rules", "mastermind"}

def _assert_safe(value: object) -> None:
    if isinstance(value, str):
        if "DO_NOT_SHOW_HERCULE_THIS" in value:
            raise PermissionError("protected evaluator sentinel cannot enter the graph projection")
    elif isinstance(value, dict):
        forbidden = _FORBIDDEN_PLAYER_KEYS.intersection(str(key).lower() for key in value)
        if forbidden:
            raise PermissionError("protected evaluator fields cannot enter the graph projection")
        for item in value.values():
            _assert_safe(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _assert_safe(item)


@dataclass(frozen=True, slots=True)
class GraphInvestigationService:
    """Authorizes graph operations against a published, player-safe graph."""

    graph_provider: object

    def _graph(self, round_id: str) -> dict:
        graph = self.graph_provider(round_id)
        if graph is None:
            raise KeyError(round_id)
        _assert_safe(graph)
        return graph

    def initial(self, round_id: str, seeds: Iterable[str] = (), limit: int = DEFAULT_INITIAL_NODES, edge_limit: int = DEFAULT_INITIAL_EDGES) -> dict:
        return initial_subset(self._graph(round_id), seeds=seeds, limit=limit, edge_limit=edge_limit)

    def expand(self, round_id: str, visible: dict, node_id: str, depth: int = 1, limit: int = MAX_GRAPH_NODES, edge_limit: int = MAX_GRAPH_EDGES) -> dict:
        _assert_safe(visible)
        return expand(self._graph(round_id), visible, node_id, depth=depth, limit=limit, edge_limit=edge_limit)

    def filter(self, round_id: str, visible: dict, families: Iterable[str]) -> dict:
        _assert_safe(visible)
        graph = self._graph(round_id)
        visible_ids = {node["record_id"] for node in visible.get("nodes", ())}
        return filter_relationships(graph, families, node_ids=visible_ids)
