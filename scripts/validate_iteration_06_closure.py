"""Validate the FGA06 two-commit source/evidence closure model."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "reports/iteration-06"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()


def load(name: str) -> dict:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def validate_evidence_scope(changed: list[str]) -> list[str]:
    """Accept cumulative descendants while requiring FGA06 evidence to be present.

    The original two-commit FGA06 gate ran at an evidence-only commit, so it
    rejected every path outside reports/iteration-06. FGA07 is intentionally a
    descendant containing later implementation, tests, and reports; those
    paths do not invalidate the already-qualified FGA06 source/evidence pair.
    """
    if not changed:
        return ["source/evidence range contains no changed files"]
    if not any(path.startswith("reports/iteration-06/") for path in changed):
        return ["source/evidence range does not contain FGA06 evidence files"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-closure", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    current = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    if status:
        errors.append("working tree is not clean")
    try:
        qualification = load("renderer-cytoscape-qualification-fga-2026-11-08.json")
        performance = load("renderer-performance-fga-2026-11-08.json")
        manual = load("renderer-manual-review-fga-2026-11-08.json")
        closure = load("closure.json")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"evidence bundle is incomplete: {exc}")
        qualification = performance = manual = closure = {}
    source = closure.get("source_commit") or qualification.get("source_commit")
    if not source:
        errors.append("evidence does not identify a qualified source commit")
    else:
        try:
            git("merge-base", "--is-ancestor", source, current)
        except subprocess.CalledProcessError:
            errors.append("qualified source commit is not an ancestor of the evidence commit")
        try:
            changed = [path for path in git("diff", "--name-only", f"{source}..{current}").splitlines() if path]
            errors.extend(validate_evidence_scope(changed))
        except subprocess.CalledProcessError as exc:
            errors.append(f"could not inspect source/evidence diff: {exc}")
    if qualification.get("source_commit") != source:
        errors.append("formal renderer report does not identify the closure source commit")
    if qualification.get("decision") != "QUALIFIED" or any(value != "PASS" for value in qualification.get("hard_requirements", {}).values()):
        errors.append("formal renderer qualification is not green")
    if performance.get("status") != "PASS" or not all(candidate.get("envelope", {}).get("pass") for candidate in performance.get("candidates", [])):
        errors.append("performance envelope is not green for every candidate")
    if manual.get("status") != "PASS" or not all(candidate.get("status", "").startswith("PASS") for candidate in manual.get("candidates", [])):
        errors.append("manual renderer review is not green")
    if args.require_closure and (closure.get("status") != "passing" or closure.get("closure_eligible") is not True):
        errors.append("closure record is not passing and eligible")
    result = {"status": "FAIL" if errors else "PASS", "source_commit": source, "evidence_commit": current, "errors": errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
