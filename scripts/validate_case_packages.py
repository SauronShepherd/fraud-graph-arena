"""Validate every declarative FGA-12 case package and its canonical reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fraud_graph_arena.case_packages import validate_all_case_packages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("case-packages"))
    args = parser.parse_args()
    results = validate_all_case_packages(args.root)
    output = {"status": "pass" if all(not errors for errors in results.values()) else "fail", "packages": results}
    print(json.dumps(output, indent=2))
    return 0 if output["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
