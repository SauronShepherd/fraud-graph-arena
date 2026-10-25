"""Deterministic player-safe graph projection helpers for FGA06."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable


def _plain(value: Any) -> dict[str, Any]:
    return asdict(value) if hasattr(value, "__dataclass_fields__") else dict(value)


def _graph(nodes: Iterable[Any], edges: Iterable[Any], *, partial: bool = False, omitted_nodes: int = 0) -> dict[str, Any]:
    node_list = sorted((_plain(node) for node in nodes), key=lambda item: item["record_id"])
    ids = {node["record_id"] for node in node_list}
    edge_list = sorted(
        (_plain(edge) for edge in edges if edge["source_record_id"] in ids and edge["target_record_id"] in ids),
        key=lambda item: item["relationship_id"],
    )
    return {
        "projection_version": "1",
        "nodes": node_list,
        "edges": edge_list,
        "node_count": len(node_list),
        "edge_count": len(edge_list),
        "partial": partial,
        "omitted_node_count": omitted_nodes,
        "omitted_edge_count": 0,
        "relationship_filters": [],
    }


def initial_subset(graph: dict[str, Any], *, seeds: Iterable[str] | None = None, limit: int = 100) -> dict[str, Any]:
    """Return a deterministic bounded projection of an already-authorized graph."""
    if limit < 1:
        raise ValueError("graph limit must be positive")
    nodes = [_plain(node) for node in graph.get("nodes", ())]
    edges = [_plain(edge) for edge in graph.get("edges", ())]
    seed_ids = set(seeds or ())
    selected = [node for node in nodes if not seed_ids or node["record_id"] in seed_ids]
    selected = sorted(selected, key=lambda item: item["record_id"])
    omitted = max(0, len(selected) - limit)
    return _graph(selected[:limit], edges, partial=omitted > 0, omitted_nodes=omitted)
