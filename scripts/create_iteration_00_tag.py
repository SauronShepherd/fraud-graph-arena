#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAG = "fga-iteration-00"


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, capture_output=capture, check=False
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create the immutable Iteration-00 tag only after formal closure passes."
    )
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument(
        "--message",
        default="Fraud Graph Arena Iteration 00 — qualified normative baseline and delivery constitution",
    )
    args = parser.parse_args()

    existing = run("git", "rev-parse", "-q", "--verify", f"refs/tags/{args.tag}")
    if existing.returncode == 0:
        print(f"Refusing to replace existing immutable tag {args.tag}.", file=sys.stderr)
        return 4

    validation = run(
        sys.executable,
        str(ROOT / "scripts/validate_iteration_00.py"),
        "--require-closure",
        "--no-write-report",
        "--no-update-evidence",
        capture=True,
    )
    if validation.returncode != 0:
        sys.stderr.write(validation.stdout)
        sys.stderr.write(validation.stderr)
        print("Formal closure did not pass; tag was not created.", file=sys.stderr)
        return validation.returncode

    created = run("git", "tag", "-a", args.tag, "-m", args.message)
    if created.returncode != 0:
        return created.returncode
    print(f"Created immutable annotated tag {args.tag} at HEAD.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
