"""Qualify FGA-18's observability contract and public Databricks boundary."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from jsonschema import validate


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.case_packages import CasePackageRegistry  # noqa: E402
from fraud_graph_arena.observability import load_instrumentation_config  # noqa: E402
from scripts.fga17_compose_contract import validate as validate_compose  # noqa: E402
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


def _observability_contract() -> dict[str, Any]:
    config_path = ROOT / "contracts" / "observability" / "fga18-instrumentation.json"
    schema_path = ROOT / "contracts" / "observability" / "fga18-instrumentation.schema.json"
    document = json.loads(config_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=document, schema=schema)
    config = load_instrumentation_config(config_path)
    identifiers = {entry.identifier for entry in config.entries}
    required = {
        "http.request",
        "domain.graph-analytics.analyze",
        "repository.economy.reserve",
        "repository.sqlite.round.charge",
        "repository.sqlite.ledger.add",
        "test.async-probe",
    }
    return {
        "status": "pass" if required <= identifiers else "fail",
        "schema_version": config.schema_version,
        "entry_count": len(config.entries),
        "required_entries_present": sorted(required & identifiers),
        "declarative_only": True,
        "redaction_policy": config.default_redaction_policy,
        "runtime_scope": "local in-process recorder; no observability rows written to the public case tables",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-18/databricks-fga18-observability-current.json"))
    parser.add_argument("--skip-profile-check", action="store_true")
    args = parser.parse_args()

    compose_errors = validate_compose(ROOT)
    observability = _observability_contract()
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
            result["qualification_scope"] = "SELECT-only public publication boundary; observability and Docker remain local"
            remote.append(result)

    remote_pass = bool(remote) and all(item.get("status") == "pass" for item in remote)
    status = "pass" if not compose_errors and observability["status"] == "pass" and identity["status"] in {"pass", "skipped"} and (remote_pass or args.skip_profile_check) else "fail"
    report = {
        "status": status,
        "iteration": "FGA18",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": source_commit(),
        "profile": args.profile,
        "catalog": args.catalog,
        "schema": args.schema,
        "warehouse_id": args.warehouse_id,
        "read_only": True,
        "truth_source_queried": False,
        "actual_engine_run": False,
        "compose_contract": {"status": "pass" if not compose_errors else "fail", "errors": compose_errors},
        "observability_contract": observability,
        "profile_identity": identity,
        "docker_execution_on_databricks": False,
        "databricks_public_boundary": {
            "status": "pass" if remote_pass else ("skipped" if args.skip_profile_check else "fail"),
            "package_count": len(remote),
            "checks": "SELECT-only active publication, snapshot, count, endpoint and safe-column checks for every canonical case",
        },
        "cases": remote,
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
