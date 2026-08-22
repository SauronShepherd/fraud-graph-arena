from __future__ import annotations
import argparse, json
from pathlib import Path
from databricks_bulk_lifecycle import run_package

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package-root",type=Path,default=Path("case-data/canonical/v1")); p.add_argument("--profile",default="sda"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--report",type=Path,default=Path("reports/iteration-05/databricks-all-packages.json")); a=p.parse_args(); root=Path(__file__).resolve().parents[1]; results=[]
    for package in sorted(x for x in a.package_root.iterdir() if x.is_dir()):
        try: results.append({"status":"pass",**run_package(package,root=root,profile=a.profile,catalog=a.catalog,schema=a.schema,warehouse=a.warehouse)})
        except Exception as exc: results.append({"package":package.name,"status":"fail","error":str(exc)[-1000:]}); break
    status="pass" if len(results)==len([x for x in a.package_root.iterdir() if x.is_dir()]) and all(x["status"]=="pass" for x in results) else "fail"; report={"status":status,"package_count":len(results),"results":results}; a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if status=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
