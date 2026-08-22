"""Complete the live publication lifecycle after candidate rows are staged."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from fraud_graph_arena.canonical_persistence.identity import publication_id
from fraud_graph_arena.canonical_persistence.models import PackageIdentity
from fraud_graph_arena.canonical_persistence.package import CanonicalPackage
from fraud_graph_arena.canonical_persistence.security import redact_error
from validate_databricks_candidate import validate_results

PUBLICATION_TABLE = "fga_import_publications"
ACTIVE_POINTER_TABLE = "fga_active_publications"

def q(value: object) -> str:
    if value is None: return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("package", type=Path); parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); parser.add_argument("--execute", action="store_true"); parser.add_argument("--report", type=Path); args = parser.parse_args()
    report = {"status": "planned", "run_id": args.run_id, "lifecycle": ["STARTED", "PREFLIGHTED", "STAGING", "STAGED", "VALIDATING", "VALIDATED", "PUBLISHING", "PUBLISHED"]}
    try:
        package = CanonicalPackage.read(args.package)
    except Exception as exc:
        report.update({"status": "fail", "error_code": "PACKAGE_PREFLIGHT_FAILED", "error_summary": redact_error(str(exc))})
        rendered = json.dumps(report, indent=2) + "\n"; print(rendered, end="")
        if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
        return 1
    identity = PackageIdentity(package.case_id, package.case_version, package.snapshot_version, package.canonical_model_version, package.content_digest)
    publication = publication_id(identity); warehouse = DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema)
    runs = warehouse.qualify_table("fga_import_runs"); publications = warehouse.qualify_table(PUBLICATION_TABLE); active_pointer = warehouse.qualify_table(ACTIVE_POINTER_TABLE)
    statements = [
        f"INSERT INTO {runs} (import_run_id,case_id,case_version,snapshot_version,package_content_digest,status,retry_of,error_code,error_summary,started_at_utc,finished_at_utc,actor,load_policy) VALUES ({q(args.run_id)},{q(identity.case_id)},{q(identity.case_version)},{q(identity.snapshot_version)},{q(identity.content_digest)},'STARTED',NULL,NULL,NULL,current_timestamp(),NULL,'record-publication','FULL_INTERNAL')",
        f"INSERT INTO {publications} (publication_id,case_id,case_version,snapshot_version,canonical_model_version,package_content_digest,semantic_hash,status) VALUES ({q(publication)},{q(identity.case_id)},{q(identity.case_version)},{q(identity.snapshot_version)},{q(identity.canonical_model_version)},{q(identity.content_digest)},NULL,'CANDIDATE')",
    ]
    report.update({"publication_id": publication, "identity": identity.__dict__, "statements": len(statements)})
    if args.execute:
        try:
            for statement in statements: warehouse.execute(statement)
            validate_results(warehouse.validate_candidate(publication, args.run_id), publication, args.run_id)
            warehouse.execute(f"UPDATE {runs} SET status='VALIDATED' WHERE import_run_id={q(args.run_id)}")
            warehouse.execute(f"UPDATE {runs} SET status='PUBLISHING' WHERE import_run_id={q(args.run_id)}")
            warehouse.activate_publication(identity.case_id, identity.case_version, identity.snapshot_version, identity.canonical_model_version, publication, args.run_id)
            warehouse.execute(f"UPDATE {publications} SET status='ACTIVE' WHERE publication_id={q(publication)}")
            warehouse.execute(f"UPDATE {runs} SET status='PUBLISHED', finished_at_utc=current_timestamp() WHERE import_run_id={q(args.run_id)}")
            report["status"] = "pass"
        except Exception as exc:
            report.update({"status": "fail", "error_code": "LIVE_PUBLICATION_FAILED", "error_summary": redact_error(str(exc))})
    rendered = json.dumps(report, indent=2) + "\n"; print(rendered, end="")
    if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
    return 0

if __name__ == "__main__": raise SystemExit(main())
