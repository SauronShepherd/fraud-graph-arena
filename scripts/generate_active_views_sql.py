from __future__ import annotations
import argparse
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, ACTIVE_VIEW_TARGETS

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    lines = ["-- Generated active-pointer serving views. Do not hand-edit."]
    for path, view in ACTIVE_VIEW_TARGETS.items():
        table = PHYSICAL_TARGETS[path]
        lines.append(f"CREATE OR REPLACE VIEW {view} AS SELECT source.* FROM {table} AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- {path}")
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text("\n\n".join(lines) + "\n", encoding="utf-8"); return 0
if __name__ == "__main__": raise SystemExit(main())
