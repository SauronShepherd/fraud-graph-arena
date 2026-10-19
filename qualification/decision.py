"""Apply the FGA06 renderer decision rule without selecting by popularity."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NORMATIVE = "Cytoscape.js"


def decide(reports: list[dict]) -> tuple[str, list[str]]:
    incumbent = next((report for report in reports if report.get("candidate") == NORMATIVE), None)
    if incumbent is None:
        return "BLOCKED_PENDING_QUALIFICATION", ["no Cytoscape.js report exists"]
    requirements = incumbent.get("hard_requirements", {})
    failed = sorted(name for name, value in requirements.items() if value == "FAIL")
    unmeasured = sorted(name for name, value in requirements.items() if value != "PASS")
    if failed:
        return "NORMATIVE_CHANGE_REQUIRED", [f"Cytoscape.js failed: {', '.join(failed)}"]
    if unmeasured or incumbent.get("license", {}).get("redistribution_status") != "ALLOWED":
        return "BLOCKED_PENDING_QUALIFICATION", ["Cytoscape.js evidence is incomplete or not redistributable"]
    return "QUALIFIED", []


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("reports", type=Path, nargs="+")
    args = parser.parse_args()
    status, reasons = decide([json.loads(path.read_text(encoding="utf-8")) for path in args.reports])
    print(json.dumps({"decision": status, "reasons": reasons}, indent=2))
    return 0 if status == "QUALIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
