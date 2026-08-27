from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, tempfile
from pathlib import Path

def sql(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False,encoding="utf-8") as fh: json.dump(payload,fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--profile",required=True); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--output",type=Path,default=Path("reports/iteration-05/security/truth-access-negative.json")); args=p.parse_args()
    cli = shutil.which("databricks")
    if not cli:
        report={"profile":args.profile,"principal_fingerprint":None,"is_admin":None,"active_view_select":"not_run","raw_safe_select":"not_run","truth_select":"not_run","status":"not_qualified","reason":"databricks_cli_unavailable"}
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0
    try:
        identity=json.loads(subprocess.check_output([cli,"current-user","me","--profile",args.profile],text=True))
    except (OSError, subprocess.CalledProcessError) as exc:
        report={"profile":args.profile,"principal_fingerprint":None,"is_admin":None,"active_view_select":"not_run","raw_safe_select":"not_run","truth_select":"not_run","status":"not_qualified","reason":"databricks_cli_unlaunchable","error_type":type(exc).__name__}
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0
    groups={item.get("display") for item in identity.get("groups",[])}; user=identity.get("userName")
    principal_fingerprint = hashlib.sha256((user or "unknown").encode()).hexdigest()[:16]
    report={"profile":args.profile,"principal_fingerprint":principal_fingerprint,"is_admin":"admins" in groups,"active_view_select":"not_run","raw_safe_select":"not_run","truth_select":"not_run"}
    if report["is_admin"]:
        report.update(status="not_qualified",reason="identity is a member of admins; admin sessions cannot prove denial")
    else:
        safe=sql(args.profile,args.warehouse,args.catalog,args.schema,f"SELECT COUNT(*) FROM fga_active_published_records_csv")
        raw_safe=sql(args.profile,args.warehouse,args.catalog,args.schema,f"SELECT COUNT(*) FROM fga_published_records_csv")
        truth=sql(args.profile,args.warehouse,args.catalog,args.schema,f"SELECT COUNT(*) FROM fga_truth_entities_csv")
        report["active_view_select"]="pass" if safe.get("status",{}).get("state")=="SUCCEEDED" else "fail"
        report["raw_safe_select"]="pass" if raw_safe.get("status",{}).get("state")=="FAILED" else "fail"
        report["truth_select"]="pass" if truth.get("status",{}).get("state")=="FAILED" else "fail"
        report["status"]="pass" if report["active_view_select"]=="pass" and report["raw_safe_select"]=="pass" and report["truth_select"]=="pass" else "fail"
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if report["status"] in {"pass","not_qualified"} else 1
if __name__=="__main__": raise SystemExit(main())
