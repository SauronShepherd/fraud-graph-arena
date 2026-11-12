"""Create the immutable FGA06 tag only after closure validation passes."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="fga-iteration-06-r1")
    args = parser.parse_args()
    existing = subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{args.tag}"], cwd=ROOT, capture_output=True, text=True)
    if existing.returncode == 0:
        print(f"Refusing to replace immutable tag {args.tag}.", file=sys.stderr)
        return 4
    validation = subprocess.run([sys.executable, str(ROOT / "scripts/validate_iteration_06_closure.py"), "--require-closure"], cwd=ROOT, capture_output=True, text=True)
    print(validation.stdout, end="")
    if validation.returncode != 0:
        print("Formal FGA06 closure did not pass; tag was not created.", file=sys.stderr)
        return validation.returncode
    created = subprocess.run(["git", "tag", "-a", args.tag, "-m", "Fraud Graph Arena Iteration 06 — qualified renderer and reproducible evidence closure"], cwd=ROOT)
    if created.returncode == 0:
        print(f"Created immutable annotated tag {args.tag} at HEAD.")
    return created.returncode


if __name__ == "__main__":
    raise SystemExit(main())
