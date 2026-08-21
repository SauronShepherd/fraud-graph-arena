from __future__ import annotations
import argparse
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, OPERATIONAL_TARGETS
from fraud_graph_arena.case_data.registry import headers

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    parts = ["-- Generated from Canonical Model v1 registry. Do not hand-edit.\n"]
    for path, table in PHYSICAL_TARGETS.items():
        cols = ", ".join(f"{column} STRING" for column in headers(path))
        parts.append(f"CREATE TABLE IF NOT EXISTS {table} ({cols}); -- {path}\n")
    parts.append("-- Operational DDL: sql/lakehouse/fga_import_ledger_v1.sql\n")
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text("\n".join(parts), encoding="utf-8"); return 0
if __name__ == "__main__": raise SystemExit(main())
