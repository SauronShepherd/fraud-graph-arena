"""Validate one renderer report against the frozen FGA06 evidence rules."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RUN_MODES = {"A_RENDERER", "B_SOLUTION"}
REQUIRED_REPORT_KEYS = {"candidate", "candidate_version", "fixture_sha256", "environment", "runs", "hard_requirements", "license"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(report: dict, fixture_path: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_REPORT_KEYS - report.keys()
    if missing:
        errors.append(f"missing report fields: {', '.join(sorted(missing))}")
    expected_sha = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    if report.get("fixture_sha256") != expected_sha:
        errors.append("fixture_sha256 does not match qualification/fixture-v1.json")
    environment = report.get("environment", {})
    for key in ("browser", "os", "viewport", "node_version"):
        if not environment.get(key):
            errors.append(f"environment.{key} is required")
    runs = report.get("runs", [])
    modes = {run.get("mode") for run in runs}
    if not REQUIRED_RUN_MODES.issubset(modes):
        errors.append("reports must include both A_RENDERER and B_SOLUTION runs")
    numbers = [run.get("run_number") for run in runs]
    if any(not isinstance(number, int) or number < 1 for number in numbers):
        errors.append("run_number must be a positive integer")
    requirements = report.get("hard_requirements", {})
    if not requirements:
        errors.append("hard_requirements must not be empty")
    elif any(value == "NOT_MEASURED" for value in requirements.values()):
        errors.append("all hard requirements must be measured before a candidate report is qualified")
    license_data = report.get("license", {})
    if license_data.get("redistribution_status") != "ALLOWED":
        errors.append("redistribution_status must be ALLOWED for a production candidate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--fixture", type=Path, default=ROOT / "qualification" / "fixture-v1.json")
    args = parser.parse_args()
    errors = validate(load(args.report), args.fixture)
    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, indent=2))
        return 1
    print(json.dumps({"status": "valid", "report": str(args.report)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
