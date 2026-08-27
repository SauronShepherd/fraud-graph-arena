"""Bounded, renderer-neutral graph investigation operations.

This module deliberately operates on the published graph projection.  It has
no access to evaluator truth and cannot discover records outside its input.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable


def _plain(value: Any) -> dict[str, Any]:
    return asdict(value) if hasattr(value, "__dataclass_fields__") else dict(value)


def _graph(nodes: Iterable[Any], edges: Iterable[Any], *, partial: bool = False, omitted_nodes: int = 0, omitted_edges: int = 0, filters: tuple[str, ...] = ()) -> dict[str, Any]:
    node_list = sorted((_plain(node) for node in nodes), key=lambda item: item["record_id"])
    ids = {node["record_id"] for node in node_list}
    edge_list = sorted((_plain(edge) for edge in edges if edge["source_record_id"] in ids and edge["target_record_id"] in ids), key=lambda item: item["relationship_id"])
    return {
        "projection_version": "1",
        "nodes": node_list,
        "edges": edge_list,
        "node_count": len(node_list),
        "edge_count": len(edge_list),
        "partial": partial,
        "omitted_node_count": omitted_nodes,
        "omitted_edge_count": omitted_edges,
        "relationship_filters": list(filters),
    }


def initial_subset(graph: dict[str, Any], *, seeds: Iterable[str] | None = None, limit: int = 100) -> dict[str, Any]:
    """Return a deterministic bounded view of an already-authorized graph."""
    if limit < 1:
        raise ValueError("graph limit must be positive")
    nodes = [_plain(node) for node in graph.get("nodes", ())]
    edges = [_plain(edge) for edge in graph.get("edges", ())]
    seed_ids = set(seeds or ())
    if seed_ids:
        selected = [node for node in nodes if node["record_id"] in seed_ids]
    else:
        selected = nodes
    selected = sorted(selected, key=lambda item: item["record_id"])
    omitted = max(0, len(selected) - limit)
    selected = selected[:limit]
    return _graph(selected, edges, partial=omitted > 0, omitted_nodes=omitted)


def expand(graph: dict[str, Any], visible: dict[str, Any], node_id: str, *, depth: int = 1, limit: int = 100) -> dict[str, Any]:
    """Expand only through records already present in the authorized graph."""
    if depth != 1:
        raise ValueError("only one-hop expansion is supported")
    if limit < 1:
        raise ValueError("graph limit must be positive")
    all_nodes = {_plain(node)["record_id"]: _plain(node) for node in graph.get("nodes", ())}
    all_edges = [_plain(edge) for edge in graph.get("edges", ())]
    if node_id not in all_nodes:
        raise KeyError(node_id)
    current = {_plain(node)["record_id"] for node in visible.get("nodes", ())}
    if node_id not in current:
        raise PermissionError("cannot expand a node outside the visible graph")
    neighbours = {edge["target_record_id"] if edge["source_record_id"] == node_id else edge["source_record_id"] for edge in all_edges if node_id in (edge["source_record_id"], edge["target_record_id"])}
    expanded_ids = current | neighbours
    selected = [all_nodes[item] for item in expanded_ids if item in all_nodes]
    omitted = max(0, len(selected) - limit)
    selected = sorted(selected, key=lambda item: item["record_id"])[:limit]
    return _graph(selected, all_edges, partial=omitted > 0, omitted_nodes=omitted)


def filter_relationships(graph: dict[str, Any], families: Iterable[str]) -> dict[str, Any]:
    """Filter the view without changing the underlying authorized graph."""
    requested = tuple(sorted(set(families)))
    edges = [_plain(edge) for edge in graph.get("edges", ())]
    if requested:
        edges = [edge for edge in edges if edge.get("relationship_family") in requested]
    return _graph(graph.get("nodes", ()), edges, filters=requested)
