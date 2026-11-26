"""Qualify the FGA-15 narrative boundary with Databricks profile ``fga``."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.case_packages import CasePackageRegistry  # noqa: E402
from scripts.qualify_case_packages import qualify  # noqa: E402
from scripts.qualify_investigation_boundary import source_commit  # noqa: E402
from scripts.review_fga15_narrative import review_packages, _fixture_errors  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-15/databricks-fga15-narrative-current.json"))
    args = parser.parse_args()
    registry = CasePackageRegistry()
    published = registry.published()
    canonical = tuple(package for package in published if package.kind == "canonical")
    local_reviews = review_packages()
    fixture_errors = _fixture_errors()
    remote: list[dict[str, Any]] = []
    for package in canonical:
        graph = package.graph()
        try:
            result = qualify(args.profile, args.warehouse_id, args.catalog, args.schema, package.case_id, expected_counts={"records": graph["node_count"], "relationships": graph["edge_count"]})
        except Exception as exc:
            result = {"status": "fail", "read_only": True, "profile": args.profile, "case_id": package.case_id, "error": str(exc)}
        result["package_id"] = package.package_id
        result["narrative_manifest_version"] = package.narrative.get("schema_version")
        remote.append(result)
    local_pass = not fixture_errors and all(item["status"] == "PASS" for item in local_reviews)
    remote_pass = bool(remote) and all(item.get("status") == "pass" for item in remote)
    report = {
        "status": "pass" if local_pass and remote_pass else "fail",
        "iteration": "FGA15",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": source_commit(),
        "profile": args.profile,
        "catalog": args.catalog,
        "schema": args.schema,
        "warehouse_id": args.warehouse_id,
        "read_only": True,
        "truth_source_queried": False,
        "actual_engine_run": False,
        "graphframes_compatibility": "UNRESOLVED_SQL_WAREHOUSE_ONLY",
        "local_narrative_review": {"status": "pass" if local_pass else "fail", "package_count": len(local_reviews), "fixture_errors": fixture_errors},
        "databricks_public_boundary": {"status": "pass" if remote_pass else "fail", "package_count": len(remote), "checks": "SELECT-only active publication, snapshot, count, endpoint and safe-column checks"},
        "cases": remote,
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
