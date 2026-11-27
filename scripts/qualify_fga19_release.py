"""Qualify the FGA-19 release contract and Databricks public boundary."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.case_packages import CasePackageRegistry  # noqa: E402
from fraud_graph_arena.release_engineering import build_release_manifest, validate_release_manifest  # noqa: E402
from scripts.qualify_case_packages import qualify  # noqa: E402
from scripts.qualify_investigation_boundary import source_commit  # noqa: E402


def _profile_identity(profile: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["databricks", "current-user", "me", "--profile", profile, "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {"status": "fail", "profile": profile, "error": completed.stderr.strip() or completed.stdout.strip()}
    return {"status": "pass", "profile": profile, "authenticated": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--manifest", type=Path, default=Path("reports/iteration-19/fga19-release-manifest-current.json"))
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-19/databricks-fga19-release-current.json"))
    parser.add_argument("--skip-profile-check", action="store_true")
    args = parser.parse_args()
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = build_release_manifest(ROOT)
    manifest_errors = validate_release_manifest(manifest, ROOT)
    identity = {"status": "skipped", "profile": args.profile} if args.skip_profile_check else _profile_identity(args.profile)
    remote: list[dict[str, Any]] = []
    if identity["status"] == "pass":
        for package in CasePackageRegistry().published():
            if package.kind != "canonical":
                continue
            graph = package.graph()
            try:
                result = qualify(
                    args.profile,
                    args.warehouse_id,
                    args.catalog,
                    args.schema,
                    package.case_id,
                    expected_counts={"records": graph["node_count"], "relationships": graph["edge_count"]},
                )
            except Exception as exc:
                result = {"status": "fail", "read_only": True, "profile": args.profile, "case_id": package.case_id, "error": str(exc)}
            result["package_id"] = package.package_id
            result["qualification_scope"] = "SELECT-only public publication boundary; release manifest and rollback drill remain local"
            remote.append(result)
    remote_pass = bool(remote) and all(item.get("status") == "pass" for item in remote)
    status = "pass" if not manifest_errors and identity["status"] in {"pass", "skipped"} and (remote_pass or args.skip_profile_check) else "fail"
    report = {
        "status": status,
        "iteration": "FGA19",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": source_commit(),
        "profile": args.profile,
        "catalog": args.catalog,
        "schema": args.schema,
        "warehouse_id": args.warehouse_id,
        "read_only": True,
        "truth_source_queried": False,
        "actual_engine_run": False,
        "release_manifest": {
            "status": "pass" if not manifest_errors else "fail",
            "release_id": manifest.get("release_id"),
            "source_revision": manifest.get("source_revision"),
            "unit_count": len(manifest.get("units", [])),
            "errors": manifest_errors,
        },
        "profile_identity": identity,
        "docker_execution_on_databricks": False,
        "databricks_public_boundary": {
            "status": "pass" if remote_pass else ("skipped" if args.skip_profile_check else "fail"),
            "package_count": len(remote),
            "checks": "SELECT-only active publication, snapshot, count, endpoint and safe-column checks for every canonical case",
        },
        "cases": remote,
        "rollback_boundary": "local immutable application pointer drill; no Databricks publication mutation",
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
