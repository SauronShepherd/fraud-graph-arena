"""Generate the repository-authoritative Canonical Model v1 typed registry."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.case_data.registry import load_typed_registry

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    tables = load_typed_registry()
    output = {"model_version": "1.0.0", "physical_table_count": 32, "package_rule": "Every canonical case package contains exactly these CSV paths.", "tables": tables}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "table_count": len(tables)}, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
