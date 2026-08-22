"""Complete the live publication lifecycle after candidate rows are staged."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse, _literal
from fraud_graph_arena.canonical_persistence.identity import publication_id
from fraud_graph_arena.canonical_persistence.models import PackageIdentity
from fraud_graph_arena.canonical_persistence.package import CanonicalPackage
from fraud_graph_arena.canonical_persistence.security import redact_error
from validate_databricks_candidate import validate_results

PUBLICATION_TABLE = "fga_import_publications"
ACTIVE_POINTER_TABLE = "fga_active_publications"

q = _literal

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("package", type=Path); parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); parser.add_argument("--execute", action="store_true"); parser.add_argument("--report", type=Path); args = parser.parse_args()
    report = {"status": "planned", "run_id": args.run_id, "lifecycle": ["STARTED", "PREFLIGHTED", "STAGING", "STAGED", "VALIDATING", "VALIDATED", "PUBLISHING", "PUBLISHED"]}
    try:
        package = CanonicalPackage.read(args.package)
    except Exception as exc:
        report.update({"status": "fail", "error_code": "PACKAGE_PREFLIGHT_FAILED", "error_summary": redact_error(str(exc), (str(args.profile), str(args.warehouse), str(args.catalog), str(args.schema)))})
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
            existing = warehouse.execute(f"SELECT publication_id,status,package_content_digest FROM {publications} WHERE publication_id={q(publication)}")
            existing_rows = existing.get("result", {}).get("data_array", [])
            if existing_rows:
                report.update({"status": "REUSED", "retry": "REUSED", "existing_status": existing_rows[0][1]})
                rendered = json.dumps(report, indent=2) + "\n"; print(rendered, end="")
                if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
                return 0
            conflict = warehouse.execute(f"SELECT publication_id,status FROM {publications} WHERE case_id={q(identity.case_id)} AND case_version={q(identity.case_version)} AND snapshot_version={q(identity.snapshot_version)} AND canonical_model_version={q(identity.canonical_model_version)} AND package_content_digest<>{q(identity.content_digest)}")
            if conflict.get("result", {}).get("data_array", []):
                raise ValueError("IMMUTABLE_SNAPSHOT_CONFLICT")
            for statement in statements: warehouse.execute(statement)
            for phase in ("PREFLIGHTED", "STAGING", "STAGED", "VALIDATING"):
                warehouse.execute(f"UPDATE {runs} SET status={q(phase)} WHERE import_run_id={q(args.run_id)}")
            validate_results(warehouse.validate_candidate(publication, args.run_id), publication, args.run_id)
            warehouse.execute(f"UPDATE {publications} SET status='VALIDATED' WHERE publication_id={q(publication)} AND status='CANDIDATE'")
            warehouse.execute(f"UPDATE {runs} SET status='VALIDATED' WHERE import_run_id={q(args.run_id)}")
            warehouse.execute(f"UPDATE {runs} SET status='PUBLISHING' WHERE import_run_id={q(args.run_id)}")
            warehouse.activate_publication(identity.case_id, identity.case_version, identity.snapshot_version, identity.canonical_model_version, publication, args.run_id)
            warehouse.execute(f"UPDATE {publications} SET status='ACTIVE' WHERE publication_id={q(publication)}")
            warehouse.execute(f"UPDATE {runs} SET status='PUBLISHED', finished_at_utc=current_timestamp() WHERE import_run_id={q(args.run_id)}")
            report["status"] = "pass"
        except Exception as exc:
            secrets = (str(args.profile), str(args.warehouse), str(args.catalog), str(args.schema))
            error_summary = redact_error(str(exc), secrets)
            cleanup_ok = True
            try:
                warehouse.execute(f"UPDATE {publications} SET status='REJECTED' WHERE publication_id={q(publication)} AND status IN ('CANDIDATE','VALIDATED')")
                warehouse.cleanup_candidate(publication)
            except Exception as cleanup_exc:
                cleanup_ok = False
                error_summary = f"{error_summary}; cleanup: {redact_error(str(cleanup_exc), secrets)}"[-1024:]
            terminal = "FAILED_CLEANUP" if not cleanup_ok else "FAILED"
            warehouse.execute(f"UPDATE {runs} SET status={q(terminal)}, error_code={q('CANDIDATE_CLEANUP_FAILED' if not cleanup_ok else 'LIVE_PUBLICATION_FAILED')}, error_summary={q(error_summary)}, finished_at_utc=current_timestamp() WHERE import_run_id={q(args.run_id)}")
            report.update({"status": "fail", "terminal_run_status": terminal, "error_code": "CANDIDATE_CLEANUP_FAILED" if not cleanup_ok else "LIVE_PUBLICATION_FAILED", "error_summary": error_summary})
    rendered = json.dumps(report, indent=2) + "\n"; print(rendered, end="")
    if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
    return 0

if __name__ == "__main__": raise SystemExit(main())
