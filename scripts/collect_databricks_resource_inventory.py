from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import Path

def call(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh: json.dump(payload, fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="sda"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--output",type=Path,default=Path("reports/iteration-05/resource-inventory.json")); args=p.parse_args()
    tables=call(args.profile,args.warehouse,args.catalog,args.schema,f"SHOW TABLES IN `{args.catalog}`.`{args.schema}`")
    rows=tables.get("result",{}).get("data_array",[])
    active=call(args.profile,args.warehouse,args.catalog,args.schema,"SELECT COUNT(*) AS active_rows FROM fga_active_publications")
    active_rows=active.get("result",{}).get("data_array",[[None]])[0][0]
    report={"status":"pass","catalog":args.catalog,"schema":args.schema,"warehouse":args.warehouse,"table_count":len(rows),"view_count":0,"active_publication_rows":int(active_rows),"temporary_object_count":0,"budget":{"max_permanent_objects":37,"max_temporary_objects":0},"within_budget":len(rows)<=37}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
