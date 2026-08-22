"""Safely repoint the live active publication for one case-version scope."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse, _literal
from fraud_graph_arena.case_data.registry import supported_model_versions

q = _literal

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--case-id", required=True); parser.add_argument("--case-version", required=True); parser.add_argument("--publication-id", required=True); parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); parser.add_argument("--execute", action="store_true"); parser.add_argument("--confirm"); parser.add_argument("--report", type=Path); args = parser.parse_args()
    warehouse = DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema)
    publications = warehouse.qualify_table("fga_import_publications"); pointer = warehouse.qualify_table("fga_active_publications")
    report = {"status": "planned", "scope": {"case_id": args.case_id, "case_version": args.case_version}, "publication_id": args.publication_id, "run_id": args.run_id, "supported_model_versions": sorted(supported_model_versions())}
    if args.execute:
        if args.confirm != f"{args.case_id}:{args.case_version}:{args.publication_id}": raise SystemExit("refusing rollback: confirmation must match exact scope and publication")
        rows = warehouse.execute(f"SELECT status, canonical_model_version, case_id, case_version FROM {publications} WHERE publication_id={q(args.publication_id)}")
        data = rows.get("result", {}).get("data_array", [])
        if len(data) != 1: raise SystemExit("rollback target publication does not exist uniquely")
        status, model, case_id, case_version = data[0]
        if status not in {"ACTIVE", "SUPERSEDED"} or model not in supported_model_versions() or case_id != args.case_id or case_version != args.case_version:
            raise SystemExit("rollback target is not an eligible compatible publication in the requested scope")
        warehouse.execute(f"MERGE INTO {pointer} AS target USING (SELECT {q(args.case_id)} AS case_id, {q(args.case_version)} AS case_version, active.snapshot_version, active.canonical_model_version, {q(args.publication_id)} AS active_publication_id, current_timestamp() AS activated_at_utc, {q(args.run_id)} AS activating_run_id FROM {publications} active WHERE active.publication_id={q(args.publication_id)}) AS source ON target.case_id=source.case_id AND target.case_version=source.case_version WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *")
        warehouse.execute(f"INSERT INTO {warehouse.qualify_table('fga_import_runs')} (import_run_id,case_id,case_version,snapshot_version,package_content_digest,status,retry_of,error_code,error_summary,started_at_utc,finished_at_utc,actor,load_policy) SELECT {q(args.run_id)},case_id,case_version,snapshot_version,package_content_digest,'PUBLISHED',NULL,NULL,NULL,current_timestamp(),current_timestamp(),'rollback','FULL_INTERNAL' FROM {publications} WHERE publication_id={q(args.publication_id)}")
        report["status"] = "pass"
    rendered=json.dumps(report, indent=2)+"\n"; print(rendered,end="")
    if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())
