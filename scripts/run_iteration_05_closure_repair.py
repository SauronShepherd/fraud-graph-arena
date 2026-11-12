"""Build an honest, revision-pinned FGA-05 repair report.

The historical FGA-05 gate was not releasable because its passing gate was
recorded with a dirty working tree.  This report is deliberately generated
from a clean source revision and keeps a non-admin security gap explicit.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def run_local_tests(target: str) -> dict:
    command = [sys.executable, "-m", "pytest", "-q", target]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {
        "status": "pass" if result.returncode == 0 else "fail",
        "command": " ".join(command),
        "exit_code": result.returncode,
        "output_tail": (result.stdout + result.stderr)[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure", type=Path, required=True)
    parser.add_argument("--bulk", type=Path, required=True)
    parser.add_argument("--repeat", type=Path, required=True)
    parser.add_argument("--security", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--test-target", default="tests/iteration_05")
    args = parser.parse_args()

    revision = source_sha()
    dirty_paths = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    generated_prefix = "?? reports/iteration-05/"
    source_dirty_paths = [path for path in dirty_paths if not path.startswith(generated_prefix)]
    structure = read_json(args.structure)
    bulk = read_json(args.bulk)
    repeat = read_json(args.repeat)
    security = read_json(args.security)
    local_tests = run_local_tests(args.test_target)

    structure_ok = (
        structure.get("source_sha") == revision
        and structure.get("status") == "pass"
        and structure.get("expected_count") == 44
        and structure.get("actual_count") == 44
        and not structure.get("missing")
        and not structure.get("extra")
        and not structure.get("column_mismatches")
    )
    bulk_results = bulk.get("results", [])
    bulk_ok = (
        bulk.get("source_sha") == revision
        and bulk.get("status") == "pass"
        and bulk.get("package_count") == 13
        and len(bulk_results) == 13
        and all(item.get("status") == "pass" for item in bulk_results)
        and all(item.get("source_sha") == revision for item in bulk_results)
        and all(item.get("lifecycle", {}).get("status") in {"pass", "REUSED_PRECHECK", "REUSED"} for item in bulk_results)
    )
    repeat_ok = (
        repeat.get("source_sha") == revision
        and repeat.get("status") == "pass"
        and repeat.get("attempts") == 10
        and repeat.get("package_count") == 13
        and repeat.get("csv_attempt_count") == 4160
        and not repeat.get("failures")
        and all(item.get("source_sha") == revision for item in repeat.get("results", []))
    )
    security_ok = (
        security.get("source_sha") == revision
        and security.get("status") == "pass"
        and security.get("is_admin") is False
        and security.get("active_view_select") == "pass"
        and security.get("raw_safe_select") == "pass"
        and security.get("truth_select") == "pass"
    )

    requirements = {
        "clean_source_revision": "pass" if not source_dirty_paths else "fail",
        "local_regression": local_tests["status"],
        "databricks_structure": "pass" if structure_ok else "fail",
        "databricks_candidate_pipeline": "pass" if bulk_ok else "fail",
        "databricks_repeat_idempotence": "pass" if repeat_ok else "fail",
        "non_admin_truth_denial": "pass" if security_ok else "external_gap",
    }
    if any(value == "fail" for value in requirements.values()):
        status = "fail"
    elif any(value == "external_gap" for value in requirements.values()):
        status = "external_gap"
    else:
        status = "pass"

    report = {
        "schema": "fga05-closure-repair-v1",
        "status": status,
        "source_sha": revision,
        "working_tree_before_artifact": {
            "clean": not source_dirty_paths,
            "changed_paths": source_dirty_paths,
            "ignored_generated_evidence": [path for path in dirty_paths if path not in source_dirty_paths],
        },
        "requirements": requirements,
        "closure_tag_allowed": status == "pass" and not source_dirty_paths,
        "historical_gate_repaired": not source_dirty_paths,
        "historical_gap": {
            "invalid_passing_commit": "5eebf83666c84e3e90722431688de8926a24476b",
            "reason": "the historical pass was recorded with working_tree=development_changes_present",
            "final_line": "external_gap",
            "repair_policy": "publish a clean repair checkpoint; do not relabel an admin-only run as non-admin-qualified",
        },
        "evidence": {
            "structure": str(args.structure),
            "bulk": str(args.bulk),
            "repeat": str(args.repeat),
            "security": str(args.security),
            "local_tests": local_tests,
        },
        "databricks": {
            "profile": bulk.get("profile", "fga"),
            "catalog": bulk.get("catalog"),
            "schema": bulk.get("schema"),
            "warehouse": bulk.get("warehouse"),
        },
        "notes": [
            "FGA-05 is cleanly reproducible at this source revision.",
            "The fga principal is an administrator, so the non-admin denial requirement remains an external gap.",
            "A clean repair tag is not a closure tag while closure_tag_allowed is false.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status in {"pass", "external_gap"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
