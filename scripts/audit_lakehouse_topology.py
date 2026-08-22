from __future__ import annotations
import argparse, json
from fraud_graph_arena.canonical_persistence.registry import expected_topology
from fraud_graph_arena.canonical_persistence.topology import classify_objects

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=str); parser.add_argument("--observed", type=str, help="JSON file containing observed object names"); parser.add_argument("--case-id", action="append", default=[]); args = parser.parse_args()
    observed = json.loads(open(args.observed, encoding="utf-8").read()) if args.observed else list(expected_topology())
    report = {"expected": list(expected_topology()), "count": len(expected_topology()), **classify_objects(observed, case_ids=args.case_id)}
    text = json.dumps(report, indent=2) + "\n"
    if args.output: open(args.output, "w", encoding="utf-8").write(text)
    else: print(text, end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())
