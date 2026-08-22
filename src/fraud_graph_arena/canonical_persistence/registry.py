from __future__ import annotations
import json
from fraud_graph_arena.case_data.registry import TABLE_PATHS, headers

_ROOT = __import__("pathlib").Path(__file__).resolve().parents[3]
_PHYSICAL_REGISTRY = _ROOT / "contracts/canonical/v1/physical-registry.json"
PHYSICAL_TARGETS = json.loads(_PHYSICAL_REGISTRY.read_text(encoding="utf-8"))["tables"]
OPERATIONAL_TARGETS = ("fga_import_runs", "fga_import_run_files", "fga_import_run_datasets", "fga_import_publications", "fga_active_publications")

def expected_topology() -> tuple[str, ...]: return tuple(PHYSICAL_TARGETS.values()) + OPERATIONAL_TARGETS

def validate_registry() -> None:
    if len(TABLE_PATHS) != 32 or len(PHYSICAL_TARGETS) != 32 or len(set(PHYSICAL_TARGETS.values())) != 32:
        raise ValueError("canonical registry must contain exactly 32 unique physical targets")
    for path in TABLE_PATHS:
        if not headers(path) or "snapshot_version" not in headers(path):
            raise ValueError(f"invalid canonical header: {path}")
    if set(PHYSICAL_TARGETS) != set(TABLE_PATHS):
        raise ValueError("physical registry must map exactly the canonical table paths")
