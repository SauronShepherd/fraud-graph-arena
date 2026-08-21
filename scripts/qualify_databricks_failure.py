from __future__ import annotations
import argparse, json, subprocess, tempfile
def call(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False,encoding="utf-8") as fh: json.dump(payload,fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)
def main():
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="sda"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--report",default="reports/iteration-05/imports/failure-injection-summary.json"); args=p.parse_args()
    before=call(args.profile,args.warehouse,args.catalog,args.schema,"SELECT active_publication_id FROM fga_active_publications LIMIT 1")
    call(args.profile,args.warehouse,args.catalog,args.schema,"INSERT INTO fga_import_runs VALUES ('dbx_failed_run_17','BONE_LEDGER','1.0.0','2026.07.18.1','injected','FAILED',NULL,'INJECTED_FAILURE',current_timestamp(),current_timestamp())")
    after=call(args.profile,args.warehouse,args.catalog,args.schema,"SELECT active_publication_id FROM fga_active_publications LIMIT 1")
    before_id=before["result"]["data_array"][0][0]; after_id=after["result"]["data_array"][0][0]
    report={"status":"pass" if before_id==after_id else "fail","before":before_id,"after":after_id,"failed_run":"dbx_failed_run_17","candidate_active":False}
    report["qualified_source_sha"] = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    report["catalog"] = args.catalog; report["schema"] = args.schema; report["warehouse"] = args.warehouse
    report_path = __import__("pathlib").Path(args.report); report_path.parent.mkdir(parents=True, exist_ok=True); report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report,indent=2)); return 0 if report["status"]=="pass" else 1
if __name__ == "__main__": raise SystemExit(main())
