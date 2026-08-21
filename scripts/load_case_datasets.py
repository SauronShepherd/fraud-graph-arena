from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS
from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse

def main() -> int:
    p = argparse.ArgumentParser(description="Canonical v1 loader; targets are registry-controlled.")
    p.add_argument("package", type=Path); p.add_argument("--plan", action="store_true"); p.add_argument("--self-check", action="store_true"); args = p.parse_args()
    if args.plan:
        print(json.dumps({"package": str(args.package), "datasets": list(PHYSICAL_TARGETS), "targets": list(PHYSICAL_TARGETS.values())}, indent=2)); return 0
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(args.package)
    print(json.dumps(result.__dict__, default=str, indent=2)); return 0 if result.status.value in {"PUBLISHED", "REUSED"} else 1
if __name__ == "__main__": raise SystemExit(main())
