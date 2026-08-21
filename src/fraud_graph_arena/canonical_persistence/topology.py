"""Topology identity and resource-budget helpers."""
from __future__ import annotations
from .identity import topology_hash
from .registry import expected_topology, OPERATIONAL_TARGETS

def audit_objects(objects: set[str] | list[str] | tuple[str, ...]) -> dict:
    actual = set(objects); expected = set(expected_topology())
    return {"status": "pass" if actual == expected else "fail", "missing": sorted(expected - actual),
            "extra": sorted(actual - expected), "object_count": len(actual), "topology_hash": topology_hash(actual)}

def permanent_topology_hash(objects) -> str:
    return topology_hash(set(objects))

def operational_object_names() -> tuple[str, ...]: return OPERATIONAL_TARGETS

