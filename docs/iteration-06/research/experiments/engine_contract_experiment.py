"""Small, dependency-free experiment for the proposed FGA graph-engine contract.

This is research tooling, not production code. It checks a few architectural
properties that should remain true when the eventual engine gains different
renderers or worker implementations:

* filters are projections and never invent edges;
* stable IDs survive projection;
* a deterministic layout is reproducible for the same snapshot, seed and pins;
* command replay is deterministic;
* capability tokens prevent presentation code from invoking unauthorized work;
* the semantic mirror contains the same stable IDs as the visual projection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
import random
from typing import Any, Iterable


@dataclass(frozen=True)
class GraphSnapshot:
    nodes: tuple[dict[str, Any], ...]
    edges: tuple[dict[str, Any], ...]
    version: str

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "GraphSnapshot":
        nodes = tuple(sorted((dict(node) for node in payload["nodes"]), key=lambda n: n["id"]))
        node_ids = {node["id"] for node in nodes}
        edges = tuple(
            sorted(
                (
                    dict(edge)
                    for edge in payload["edges"]
                    if edge["source"] in node_ids and edge["target"] in node_ids
                ),
                key=lambda e: e["id"],
            )
        )
        return cls(nodes=nodes, edges=edges, version=str(payload["version"]))

    def project(self, visible_ids: Iterable[str]) -> "GraphSnapshot":
        allowed = set(visible_ids)
        return GraphSnapshot.from_payload(
            {
                "version": f"{self.version}:project:{','.join(sorted(allowed))}",
                "nodes": [node for node in self.nodes if node["id"] in allowed],
                "edges": [edge for edge in self.edges if edge["source"] in allowed and edge["target"] in allowed],
            }
        )


def deterministic_layout(
    snapshot: GraphSnapshot,
    seed: int,
    pinned: dict[str, tuple[float, float]] | None = None,
) -> dict[str, tuple[float, float]]:
    """Produce stable exploratory positions without claiming layout quality."""

    pinned = pinned or {}
    rng = random.Random(f"{snapshot.version}:{seed}")
    positions: dict[str, tuple[float, float]] = {}
    count = max(1, len(snapshot.nodes))
    for index, node in enumerate(snapshot.nodes):
        node_id = node["id"]
        if node_id in pinned:
            positions[node_id] = pinned[node_id]
            continue
        angle = (2 * math.pi * index) / count
        radius = 100.0 + rng.random() * 3.0
        positions[node_id] = (round(math.cos(angle) * radius, 6), round(math.sin(angle) * radius, 6))
    return positions


@dataclass
class InteractionState:
    selected: tuple[str, ...] = ()
    pinned: dict[str, tuple[float, float]] = field(default_factory=dict)
    open_menu: str | None = None
    notes: tuple[str, ...] = ()

    def digest(self) -> str:
        payload = {
            "selected": self.selected,
            "pinned": sorted((key, value) for key, value in self.pinned.items()),
            "open_menu": self.open_menu,
            "notes": self.notes,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def replay(
    commands: Iterable[dict[str, Any]],
    capabilities: set[str],
) -> InteractionState:
    state = InteractionState()
    for command in commands:
        kind = command["kind"]
        capability = command.get("capability")
        if capability and capability not in capabilities:
            continue
        if kind == "select":
            state.selected = tuple(sorted(set(command["ids"])))
        elif kind == "open-menu":
            state.open_menu = command["target"]
        elif kind == "pin":
            state.pinned[command["id"]] = (float(command["x"]), float(command["y"]))
        elif kind == "note":
            state.notes = (*state.notes, command["text"])
        elif kind == "dismiss-menu":
            state.open_menu = None
        else:
            raise ValueError(f"unknown command: {kind}")
    return state


def semantic_mirror(snapshot: GraphSnapshot) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "role": "graph-node",
            "id": node["id"],
            "name": node.get("label", node["id"]),
            "relationship_count": sum(
                edge["source"] == node["id"] or edge["target"] == node["id"]
                for edge in snapshot.edges
            ),
        }
        for node in snapshot.nodes
    )


def main() -> None:
    snapshot = GraphSnapshot.from_payload(
        {
            "version": "T02:v1",
            "nodes": [
                {"id": "FGA:N:01", "label": "Account"},
                {"id": "FGA:N:02", "label": "Device"},
                {"id": "FGA:N:03", "label": "Merchant"},
            ],
            "edges": [
                {"id": "FGA:E:01", "source": "FGA:N:01", "target": "FGA:N:02"},
                {"id": "FGA:E:02", "source": "FGA:N:02", "target": "FGA:N:03"},
                {"id": "FGA:E:orphan", "source": "FGA:N:03", "target": "missing"},
            ],
        }
    )
    projected = snapshot.project({"FGA:N:01", "FGA:N:02"})
    assert {node["id"] for node in projected.nodes} == {"FGA:N:01", "FGA:N:02"}
    assert all(
        edge["source"] in {node["id"] for node in projected.nodes}
        and edge["target"] in {node["id"] for node in projected.nodes}
        for edge in projected.edges
    )

    pins = {"FGA:N:01": (0.0, 0.0)}
    layout_a = deterministic_layout(projected, seed=7, pinned=pins)
    layout_b = deterministic_layout(projected, seed=7, pinned=pins)
    assert layout_a == layout_b
    assert layout_a["FGA:N:01"] == (0.0, 0.0)

    commands = [
        {"kind": "select", "ids": ["FGA:N:02"]},
        {"kind": "open-menu", "target": "FGA:N:02", "capability": "inspect"},
        {"kind": "pin", "id": "FGA:N:02", "x": 12, "y": -4, "capability": "move"},
        {"kind": "note", "text": "presentation-only note", "capability": "annotate"},
    ]
    state_a = replay(commands, {"inspect", "move"})
    state_b = replay(json.loads(json.dumps(commands)), {"inspect", "move"})
    assert state_a.digest() == state_b.digest()
    assert state_a.notes == ()

    semantic_ids = {item["id"] for item in semantic_mirror(projected)}
    visual_ids = {node["id"] for node in projected.nodes}
    assert semantic_ids == visual_ids

    print(
        json.dumps(
            {
                "status": "PASS",
                "snapshot_version": snapshot.version,
                "projected_nodes": len(projected.nodes),
                "projected_edges": len(projected.edges),
                "layout_digest": hashlib.sha256(repr(layout_a).encode()).hexdigest()[:16],
                "replay_digest": state_a.digest()[:16],
                "unauthorized_command_dropped": True,
                "semantic_visual_id_sets_equal": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
