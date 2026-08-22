"""Expected and observed bounded-persistence topology checks."""
from __future__ import annotations
import hashlib, json
from .identity import topology_hash
from .registry import expected_topology, OPERATIONAL_TARGETS

def classify_objects(objects, *, case_ids=(), temporary_prefixes=("fga_stage_", "fga_tmp_")) -> dict:
    actual = set(objects); expected = set(expected_topology()); case_tokens = tuple(str(token).lower() for token in case_ids)
    temporary = sorted(name for name in actual if name.startswith(temporary_prefixes))
    permanent = actual - set(temporary)
    case_specific = sorted(name for name in permanent if any(token and token in name.lower() for token in case_tokens))
    return {"permanent": sorted(permanent), "temporary": temporary, "case_specific": case_specific, "unexpected": sorted(permanent - expected), "missing": sorted(expected - permanent), "topology_hash": topology_hash(permanent), "status": "pass" if permanent == expected and not case_specific and not temporary else "fail"}

def audit_objects(objects, *, case_ids=()) -> dict:
    return classify_objects(objects, case_ids=case_ids)

def permanent_topology_hash(objects) -> str: return topology_hash(set(objects))
def operational_object_names() -> tuple[str, ...]: return OPERATIONAL_TARGETS
