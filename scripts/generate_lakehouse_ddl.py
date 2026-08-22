from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, OPERATIONAL_TARGETS
from fraud_graph_arena.case_data.registry import headers, sql_types
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_REGISTRY_PATH

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    registry_digest = hashlib.sha256(PHYSICAL_REGISTRY_PATH.read_bytes()).hexdigest()
    parts = [f"-- Generated from Canonical Model v1 registry. Do not hand-edit.\n-- physical_registry_sha256: {registry_digest}\n"]
    for path, table in PHYSICAL_TARGETS.items():
        cols = ", ".join(f"{column} {sql_type}" for column, sql_type in zip(headers(path), sql_types(path), strict=True))
        cols += ", _publication_id STRING, _load_run_id STRING"
        parts.append(f"CREATE TABLE IF NOT EXISTS {table} ({cols}); -- {path}\n")
    parts.append("-- Operational DDL: sql/lakehouse/fga_import_ledger_v1.sql\n")
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text("\n".join(parts), encoding="utf-8"); return 0
if __name__ == "__main__": raise SystemExit(main())
