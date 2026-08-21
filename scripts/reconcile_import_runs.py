from __future__ import annotations
import argparse, json

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--state", required=True); args = p.parse_args()
    with open(args.state, encoding="utf-8") as fh: state = json.load(fh)
    state["reconciled"] = True
    print(json.dumps(state, indent=2))
    return 0
if __name__ == "__main__": raise SystemExit(main())
