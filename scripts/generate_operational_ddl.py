from __future__ import annotations
import argparse
from pathlib import Path
from fraud_graph_arena.canonical_persistence.operational_registry import ddl, registry

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("-- Generated from the FGA-05 operational registry.\n" + "\n\n".join(ddl(table) + ";" for table in registry()) + "\n", encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())
