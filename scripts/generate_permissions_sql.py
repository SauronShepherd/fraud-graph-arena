"""Generate WEB grants/revokes from the closed physical registry and layer policy."""
from __future__ import annotations
import argparse
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, OPERATIONAL_TARGETS

SAFE_LAYERS = ("published/", "genie/")
WEB_PRINCIPAL = "fga_web"

def render(principal: str = WEB_PRINCIPAL) -> str:
    lines = ["-- Generated from the Canonical Model v1 physical registry. Do not hand-edit.",
             "-- Deployment must substitute the approved principal before execution."]
    for path, table in PHYSICAL_TARGETS.items():
        if path.startswith(SAFE_LAYERS):
            lines.append(f"GRANT SELECT ON TABLE {table} TO `{principal}`;")
        else:
            lines.append(f"REVOKE ALL PRIVILEGES ON TABLE {table} FROM `{principal}`;")
    for table in OPERATIONAL_TARGETS:
        lines.append(f"REVOKE ALL PRIVILEGES ON TABLE {table} FROM `{principal}`;")
    return "\n".join(lines) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--principal", default=WEB_PRINCIPAL); args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(render(args.principal), encoding="utf-8"); return 0

if __name__ == "__main__": raise SystemExit(main())
