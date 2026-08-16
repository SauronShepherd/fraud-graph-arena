from __future__ import annotations

import subprocess
import sys
import json

def run(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT).strip()

def main() -> int:
    try:
        run("rev-parse", "--verify", "fga-iteration-00-r1^{commit}")
        candidate = run("rev-parse", "HEAD")
        run("merge-base", "--is-ancestor", "fga-iteration-00-r1", candidate)
        evidence = json.loads(run("show", "fga-iteration-00-r1:reports/iteration-00/evidence.json"))
        if evidence.get("status") != "passing" or evidence.get("closure_eligible") is not True:
            raise ValueError("I00 tag does not contain passing closure evidence")
        tagged_commit = run("rev-parse", "fga-iteration-00-r1^{commit}")
        source_commit = evidence.get("source_commit")
        if not source_commit or not run("merge-base", "--is-ancestor", source_commit, tagged_commit) == "":
            raise ValueError("I00 evidence does not identify an ancestor of the immutable tag")
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(exc.output or "release lineage verification failed", file=sys.stderr)
        return 1
    print(f"fga-iteration-00-r1 is an ancestor of {candidate}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
