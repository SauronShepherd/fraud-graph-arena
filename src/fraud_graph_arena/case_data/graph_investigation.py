"""Bounded, renderer-neutral graph investigation operations.

This module deliberately operates on the published graph projection.  It has
no access to evaluator truth and cannot discover records outside its input.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable

MAX_GRAPH_NODES = 300
MAX_GRAPH_EDGES = 700
DEFAULT_INITIAL_NODES = 150
DEFAULT_INITIAL_EDGES = 300


def _plain(value: Any) -> dict[str, Any]:
    return asdict(value) if hasattr(value, "__dataclass_fields__") else dict(value)


def _graph(nodes: Iterable[Any], edges: Iterable[Any], *, node_limit: int = MAX_GRAPH_NODES, edge_limit: int = MAX_GRAPH_EDGES, partial: bool = False, omitted_nodes: int = 0, omitted_edges: int = 0, filters: tuple[str, ...] = ()) -> dict[str, Any]:
    if not 1 <= node_limit <= MAX_GRAPH_NODES:
        raise ValueError(f"node limit must be between 1 and {MAX_GRAPH_NODES}")
    if not 1 <= edge_limit <= MAX_GRAPH_EDGES:
        raise ValueError(f"edge limit must be between 1 and {MAX_GRAPH_EDGES}")
    node_list = sorted((_plain(node) for node in nodes), key=lambda item: item["record_id"])
    all_ids = {node["record_id"] for node in node_list}
    omitted_nodes += max(0, len(node_list) - node_limit)
    node_list = node_list[:node_limit]
    ids = {node["record_id"] for node in node_list}
    candidates = sorted((_plain(edge) for edge in edges if edge["source_record_id"] in all_ids and edge["target_record_id"] in all_ids), key=lambda item: item["relationship_id"])
    edge_list = [edge for edge in candidates if edge["source_record_id"] in ids and edge["target_record_id"] in ids]
    omitted_edges += len(candidates) - len(edge_list)
    omitted_edges += max(0, len(edge_list) - edge_limit)
    edge_list = edge_list[:edge_limit]
    return {
        "projection_version": "1",
        "nodes": node_list,
        "edges": edge_list,
        "node_count": len(node_list),
        "edge_count": len(edge_list),
        "partial": partial or omitted_nodes > 0 or omitted_edges > 0,
        "omitted_node_count": omitted_nodes,
        "omitted_edge_count": omitted_edges,
        "relationship_filters": list(filters),
    }


def initial_subset(graph: dict[str, Any], *, seeds: Iterable[str] | None = None, limit: int = DEFAULT_INITIAL_NODES, edge_limit: int = DEFAULT_INITIAL_EDGES) -> dict[str, Any]:
    """Return a deterministic bounded view of an already-authorized graph."""
    if not 1 <= limit <= MAX_GRAPH_NODES:
        raise ValueError(f"node limit must be between 1 and {MAX_GRAPH_NODES}")
    nodes = [_plain(node) for node in graph.get("nodes", ())]
    edges = [_plain(edge) for edge in graph.get("edges", ())]
    seed_ids = set(seeds or ())
    if seed_ids:
        selected = [node for node in nodes if node["record_id"] in seed_ids]
    else:
        selected = nodes
    selected = sorted(selected, key=lambda item: item["record_id"])
    return _graph(selected, edges, node_limit=limit, edge_limit=edge_limit)


def expand(graph: dict[str, Any], visible: dict[str, Any], node_id: str, *, depth: int = 1, limit: int = MAX_GRAPH_NODES, edge_limit: int = MAX_GRAPH_EDGES) -> dict[str, Any]:
    """Expand only through records already present in the authorized graph."""
    if depth != 1:
        raise ValueError("only one-hop expansion is supported")
    if not 1 <= limit <= MAX_GRAPH_NODES:
        raise ValueError(f"node limit must be between 1 and {MAX_GRAPH_NODES}")
    all_nodes = {_plain(node)["record_id"]: _plain(node) for node in graph.get("nodes", ())}
    all_edges = [_plain(edge) for edge in graph.get("edges", ())]
    if node_id not in all_nodes:
        raise KeyError(node_id)
    current = {_plain(node)["record_id"] for node in visible.get("nodes", ())}
    if not current.issubset(all_nodes):
        raise PermissionError("visible graph contains records outside the authorized projection")
    if node_id not in current:
        raise PermissionError("cannot expand a node outside the visible graph")
    neighbours = {edge["target_record_id"] if edge["source_record_id"] == node_id else edge["source_record_id"] for edge in all_edges if node_id in (edge["source_record_id"], edge["target_record_id"])}
    expanded_ids = current | neighbours
    selected = [all_nodes[item] for item in expanded_ids if item in all_nodes]
    return _graph(selected, all_edges, node_limit=limit, edge_limit=edge_limit)


def filter_relationships(graph: dict[str, Any], families: Iterable[str], *, node_ids: Iterable[str] | None = None, edge_limit: int = MAX_GRAPH_EDGES) -> dict[str, Any]:
    """Filter the view without changing the underlying authorized graph."""
    requested = tuple(sorted(set(families)))
    nodes = [_plain(node) for node in graph.get("nodes", ())]
    allowed_ids = set(node_ids) if node_ids is not None else {node["record_id"] for node in nodes}
    unknown_ids = allowed_ids - {node["record_id"] for node in nodes}
    if unknown_ids:
        raise PermissionError("visible graph contains records outside the authorized projection")
    nodes = [node for node in nodes if node["record_id"] in allowed_ids]
    edges = [_plain(edge) for edge in graph.get("edges", ())]
    if requested:
        edges = [edge for edge in edges if edge.get("relationship_family") in requested]
    return _graph(nodes, edges, edge_limit=edge_limit, filters=requested)
