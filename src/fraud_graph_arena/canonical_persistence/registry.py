from __future__ import annotations
import re
from fraud_graph_arena.case_data.registry import TABLE_PATHS, headers

PHYSICAL_TARGETS = {path: "fga_" + re.sub(r"[^a-z0-9]+", "_", path.lower()).strip("_") for path in TABLE_PATHS}
OPERATIONAL_TARGETS = ("fga_import_runs", "fga_import_run_files", "fga_import_run_datasets", "fga_import_publications", "fga_active_publications")

def expected_topology() -> tuple[str, ...]: return tuple(PHYSICAL_TARGETS.values()) + OPERATIONAL_TARGETS

def validate_registry() -> None:
    if len(TABLE_PATHS) != 32 or len(PHYSICAL_TARGETS) != 32 or len(set(PHYSICAL_TARGETS.values())) != 32:
        raise ValueError("canonical registry must contain exactly 32 unique physical targets")
    for path in TABLE_PATHS:
        if not headers(path) or "snapshot_version" not in headers(path):
            raise ValueError(f"invalid canonical header: {path}")
