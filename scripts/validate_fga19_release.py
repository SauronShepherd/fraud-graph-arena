"""Validate the FGA-19 release contract, unit digests and blocking stages."""

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
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.manifest is None:
        manifest = build_release_manifest(ROOT)
        source = "generated"
    else:
        if not args.manifest.is_absolute():
            args.manifest = ROOT / args.manifest
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        source = str(args.manifest)
    errors = validate_release_manifest(manifest, ROOT)
    stage_ids = [stage["id"] for stage in manifest.get("ci_stages", [])]
    required = ["lint", "unit", "contracts", "case-validation", "end-to-end", "container-build", "deployment-smoke"]
    if stage_ids != required:
        errors.append(f"CI stages must be ordered as {required}")
    flag_ids = [flag["id"] for flag in manifest.get("feature_flags", [])]
    if len(flag_ids) != len(set(flag_ids)):
        errors.append("feature flag identifiers must be unique")
    report = {
        "status": "pass" if not errors else "fail",
        "source": source,
        "release_id": manifest.get("release_id"),
        "source_revision": manifest.get("source_revision"),
        "unit_count": len(manifest.get("units", [])),
        "ci_stage_ids": stage_ids,
        "feature_flags": flag_ids,
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
