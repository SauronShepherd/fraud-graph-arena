from __future__ import annotations
import json, subprocess, tempfile
from fraud_graph_arena.canonical_persistence.operational_registry import ddl, registry
# Registry tables: fga_import_runs, fga_import_run_files, fga_import_run_datasets,
# fga_import_publications, fga_active_publications.
def execute(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False,encoding="utf-8") as fh: json.dump(payload,fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    output=json.loads(result.stdout)
    if output.get("status",{}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))
def main():
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="sda"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--apply",action="store_true"); p.add_argument("--confirm"); args=p.parse_args()
    token=f"{args.catalog}:{args.schema}"
    if not args.apply or args.confirm != token: raise SystemExit(f"refusing operational DDL repair; require --apply --confirm {token}")
    for table in registry(): execute(args.profile,args.warehouse,args.catalog,args.schema,ddl(table))
    print(json.dumps({"status":"pass","tables":list(registry())}))
if __name__ == "__main__": main()
