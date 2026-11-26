"""Qualify the FGA-13 difficulty catalogue and its player-safe Databricks data.

All Databricks statements are delegated to the existing read-only package
qualification boundary.  The script adds the local difficulty contract and
checks every canonical package, not just one representative per path.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from fraud_graph_arena.case_packages import CasePackageRegistry
from fraud_graph_arena.difficulty import validate_catalogue
try:
    from scripts.qualify_case_packages import qualify
    from scripts.qualify_investigation_boundary import source_commit
except ModuleNotFoundError:
    from qualify_case_packages import qualify
    from qualify_investigation_boundary import source_commit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-13/databricks-fga13-difficulty-current.json"))
    args = parser.parse_args()
    registry = CasePackageRegistry()
    packages = tuple(package for package in registry.published() if package.kind == "canonical")
    difficulty_errors = validate_catalogue(packages)
    cases: list[dict[str, Any]] = []
    for package in packages:
        graph = package.graph()
        expected = {"records": graph["node_count"], "relationships": graph["edge_count"]}
        try:
            result = qualify(args.profile, args.warehouse_id, args.catalog, args.schema, package.case_id, expected_counts=expected)
        except Exception as exc:  # persist the external failure as a durable receipt
            result = {"status": "fail", "read_only": True, "profile": args.profile, "case_id": package.case_id, "error": str(exc)}
        result["package_id"] = package.package_id
        result["path_id"] = package.path_id.value
        result["difficulty_profile"] = package.difficulty_profile.as_dict()
        result["expected_graph"] = expected
        cases.append(result)
    report = {
        "status": "pass" if not difficulty_errors and cases and all(item["status"] == "pass" for item in cases) else "fail",
        "iteration": "FGA13",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": source_commit(),
        "profile": args.profile,
        "catalog": args.catalog,
        "schema": args.schema,
        "warehouse_id": args.warehouse_id,
        "read_only": True,
        "difficulty_contract": {"status": "pass" if not difficulty_errors else "fail", "errors": difficulty_errors, "package_count": len(packages)},
        "cases": cases,
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
