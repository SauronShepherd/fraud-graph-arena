"""Qualify the FGA-16 Academy contract and published cases with Databricks ``fga``."""

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

from fraud_graph_arena.academy import AcademyValidationRunner  # noqa: E402
from fraud_graph_arena.case_packages import CasePackageRegistry  # noqa: E402
from scripts.qualify_case_packages import qualify  # noqa: E402
from scripts.qualify_investigation_boundary import source_commit  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-16/databricks-fga16-academy-current.json"))
    args = parser.parse_args()

    local_report = AcademyValidationRunner().run()
    remote: list[dict[str, Any]] = []
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
        except Exception as exc:  # persist external failures as a durable receipt
            result = {
                "status": "fail",
                "read_only": True,
                "profile": args.profile,
                "case_id": package.case_id,
                "error": str(exc),
            }
        result["package_id"] = package.package_id
        result["academy_regression_scope"] = "published-case-smoke-and-public-boundary"
        remote.append(result)

    remote_pass = bool(remote) and all(item.get("status") == "pass" for item in remote)
    report = {
        "status": "pass" if local_report.status == "PASS" and remote_pass else "fail",
        "iteration": "FGA16",
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
        "local_academy_validation": local_report.as_dict(),
        "databricks_public_boundary": {
            "status": "pass" if remote_pass else "fail",
            "package_count": len(remote),
            "checks": "SELECT-only active publication, snapshot, count, endpoint and safe-column checks for every canonical case",
        },
        "cases": remote,
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
