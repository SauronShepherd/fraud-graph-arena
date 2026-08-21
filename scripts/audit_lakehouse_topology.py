from __future__ import annotations
import argparse, json
from fraud_graph_arena.canonical_persistence.registry import expected_topology

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=str); args = parser.parse_args()
    report = {"expected": list(expected_topology()), "count": len(expected_topology()), "case_specific": []}
    text = json.dumps(report, indent=2) + "\n"
    if args.output: open(args.output, "w", encoding="utf-8").write(text)
    else: print(text, end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())
