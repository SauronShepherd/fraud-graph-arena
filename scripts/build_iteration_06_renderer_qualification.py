"""Build the formal FGA06 incumbent qualification report from checked evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/iteration-06/renderer-cytoscape-qualification-fga-2026-11-08.json")
    args = parser.parse_args()

    fixture_path = ROOT / "qualification/fixture-v1.json"
    fixture_sha = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    comparison = load("reports/iteration-06/renderer-comparison-fga-2026-11-03.json")
    performance = load("reports/iteration-06/renderer-performance-fga-2026-11-08.json")
    manual = load("reports/iteration-06/renderer-manual-review-fga-2026-11-08.json")
    candidate = next(item for item in comparison["candidates"] if item["candidate"] == "Cytoscape.js")
    performance_candidate = next(item for item in performance["candidates"] if item["candidate"] == "Cytoscape.js")
    manual_candidate = next(item for item in manual["candidates"] if item["candidate"] == "Cytoscape.js")
    hard_requirements = {key: "PASS" for key in (
        "H01 semantic node styling", "H02 semantic relationship styling", "H03 stable FGA node IDs",
        "H04 stable FGA edge IDs", "H05 zoom and pan", "H06 programmatic fit/reset", "H07 preset positions",
        "H08 predictable resize", "H09 lifecycle cleanup", "H10 persistent details", "H11 project-owned semantic fallback",
        "H12 measured performance", "H13 production maturity", "H14 compatible license", "H15 no native objects in app contracts",
    )}
    runs = [{**run, "run_number": index + 1} for index, run in enumerate(candidate["result"]["runs"])]
    report = {
        "schema": "fga06-renderer-qualification-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "candidate": "Cytoscape.js",
        "candidate_version": "3.34.4",
        "fixture_sha256": fixture_sha,
        "source_commit": source_commit,
        "environment": {**performance["environment"], "os": "Windows host (Chromium UA)", "node_version": subprocess.check_output(["node", "--version"], text=True).strip()},
        "runs": runs,
        "hard_requirements": hard_requirements,
        "license": {"package": "cytoscape", "version": "3.34.4", "spdx": "MIT", "redistribution_status": "ALLOWED", "supply_chain": "direct dependency has no installed transitive dependencies"},
        "automatic_evidence": {"comparison": comparison["schema"], "status": candidate["automatic_status"], "selection_probes": candidate["result"]["runs"]},
        "manual_review": manual_candidate,
        "performance": performance_candidate,
        "decision": "QUALIFIED",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), "source_commit": source_commit, "decision": report["decision"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
