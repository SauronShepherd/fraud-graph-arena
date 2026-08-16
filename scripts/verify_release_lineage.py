from __future__ import annotations

import subprocess
import sys

def run(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT).strip()

def main() -> int:
    try:
        run("rev-parse", "--verify", "fga-iteration-00-r1^{commit}")
        candidate = run("rev-parse", "HEAD")
        run("merge-base", "--is-ancestor", "fga-iteration-00-r1", candidate)
    except subprocess.CalledProcessError as exc:
        print(exc.output or "release lineage verification failed", file=sys.stderr)
        return 1
    print(f"fga-iteration-00-r1 is an ancestor of {candidate}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
