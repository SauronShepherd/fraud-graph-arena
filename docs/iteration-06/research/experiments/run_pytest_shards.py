"""Run the Python test suite in isolated, bounded shards.

The existing suite contains governance tests that create temporary repositories
and invoke validators. Running every test in one process can retain a large
amount of subprocess and fixture state on Windows. This experiment treats
process isolation as part of the autonomous-test architecture.

Usage:
    python docs/iteration-06/research/experiments/run_pytest_shards.py
    python docs/iteration-06/research/experiments/run_pytest_shards.py --timeout 600
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SHARDS = (
    "tests/governance",
    "tests/iteration_01",
    "tests/iteration_03",
    "tests/iteration_04",
    "tests/iteration_05",
    "tests/iteration_06",
)


def run_shard(path: str, timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        status = "pass" if completed.returncode == 0 else "fail"
        output = (completed.stdout + completed.stderr).strip()
        return {
            "shard": path,
            "status": status,
            "returncode": completed.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
            "tail": output[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "shard": path,
            "status": "timeout",
            "returncode": None,
            "duration_seconds": round(time.monotonic() - started, 3),
            "tail": str(exc)[-4000:],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("paths", nargs="*", default=SHARDS)
    args = parser.parse_args()

    results = [run_shard(shard, args.timeout) for shard in args.paths]
    report = {
        "status": "PASS" if all(item["status"] == "pass" for item in results) else "FAIL",
        "root": str(ROOT),
        "isolation": "one subprocess per shard",
        "timeout_seconds_per_shard": args.timeout,
        "results": results,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
