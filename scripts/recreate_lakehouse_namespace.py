from __future__ import annotations
import argparse, json
from fraud_graph_arena.canonical_persistence.registry import expected_topology

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--environment", required=True); p.add_argument("--dry-run", action="store_true"); args = p.parse_args()
    if args.environment != "fga_dev": raise SystemExit("refusing destructive recreation outside approved fga_dev")
    print(json.dumps({"environment": args.environment, "dry_run": args.dry_run, "recreated": [] if args.dry_run else list(expected_topology())}, indent=2))
    return 0
if __name__ == "__main__": raise SystemExit(main())
