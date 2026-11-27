"""Generate the immutable FGA-19 release manifest and its unit digests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.release_engineering import build_release_manifest, validate_release_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/iteration-19/fga19-release-manifest-current.json")
    parser.add_argument("--release-id", default="fga19-mvp.1")
    parser.add_argument("--source-revision")
    args = parser.parse_args()
    if not args.output.is_absolute():
        args.output = ROOT / args.output
    manifest = build_release_manifest(ROOT, release_id=args.release_id, source_revision=args.source_revision)
    errors = validate_release_manifest(manifest, ROOT)
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, indent=2))
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "output": str(args.output), "release_id": manifest["release_id"], "source_revision": manifest["source_revision"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
