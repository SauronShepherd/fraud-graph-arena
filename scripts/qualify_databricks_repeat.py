from __future__ import annotations
import argparse, json
from pathlib import Path
from databricks_bulk_lifecycle import run_package

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package-root",type=Path,default=Path("case-data/canonical/v1")); p.add_argument("--profile",default="sda"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--repeats",type=int,default=10); p.add_argument("--report",type=Path,default=Path("reports/iteration-05/databricks-repeat.json")); a=p.parse_args(); root=Path(__file__).resolve().parents[1]; results=[]; failures=[]
    for attempt in range(1,a.repeats+1):
        for package in sorted(x for x in a.package_root.iterdir() if x.is_dir()):
            try: results.append({"attempt":attempt,"status":"pass",**run_package(package,root=root,profile=a.profile,catalog=a.catalog,schema=a.schema,warehouse=a.warehouse)})
            except Exception as exc: failures.append({"attempt":attempt,"package":package.name,"error":str(exc)[-1000:]})
    report={"status":"pass" if not failures else "fail","attempts":a.repeats,"package_count":len([x for x in a.package_root.iterdir() if x.is_dir()]),"results":results,"failures":failures}; a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if not failures else 1
if __name__=="__main__": raise SystemExit(main())
