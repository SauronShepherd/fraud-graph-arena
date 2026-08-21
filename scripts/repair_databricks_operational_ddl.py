from __future__ import annotations
import json, subprocess, tempfile

TABLES = {
"fga_import_runs": ["import_run_id", "case_id", "case_version", "snapshot_version", "package_content_digest", "status", "retry_of", "error_code", "started_at_utc", "finished_at_utc"],
"fga_import_run_files": ["import_run_id", "relative_path", "byte_length", "sha256", "observed_at_utc"],
"fga_import_run_datasets": ["import_run_id", "dataset_path", "source_row_count", "staged_row_count", "validated_row_count", "phase"],
"fga_import_publications": ["publication_id", "case_id", "case_version", "snapshot_version", "canonical_model_version", "package_content_digest", "semantic_hash", "status"],
"fga_active_publications": ["case_id", "case_version", "snapshot_version", "active_publication_id", "activated_at_utc"],
}
def execute(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False,encoding="utf-8") as fh: json.dump(payload,fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    output=json.loads(result.stdout)
    if output.get("status",{}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))
def main():
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="sda"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); args=p.parse_args()
    for table in TABLES: execute(args.profile,args.warehouse,args.catalog,args.schema,f"DROP TABLE IF EXISTS {table}")
    for table, columns in TABLES.items(): execute(args.profile,args.warehouse,args.catalog,args.schema,f"CREATE TABLE {table} (" + ",".join(f"{column} STRING" for column in columns) + ") USING DELTA")
    print(json.dumps({"status":"pass","tables":list(TABLES)}))
if __name__ == "__main__": main()
