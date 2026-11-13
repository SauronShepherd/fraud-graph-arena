from __future__ import annotations
import argparse, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from databricks_bulk_lifecycle import run_package

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package-root",type=Path,default=Path("case-data/canonical/v1")); p.add_argument("--profile",default="sda"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--package-workers",type=int,default=2); p.add_argument("--report",type=Path,default=Path("reports/iteration-05/databricks-all-packages.json")); a=p.parse_args(); root=Path(__file__).resolve().parents[1]; packages=sorted(x for x in a.package_root.iterdir() if x.is_dir())
    if not 1 <= a.package_workers <= 4: raise SystemExit("package-workers must be between 1 and 4")
    def qualify(package: Path) -> dict:
        try:
            result = run_package(package,root=root,profile=a.profile,catalog=a.catalog,schema=a.schema,warehouse=a.warehouse)
            if result.get("lifecycle", {}).get("status") not in {"pass", "REUSED"}:
                raise RuntimeError(f"publication lifecycle did not pass: {result.get('lifecycle', {})}")
            return {"status":"pass",**result}
        except Exception as exc:
            return {"package":package.name,"status":"fail","error":str(exc)[-1000:]}
    with ThreadPoolExecutor(max_workers=a.package_workers) as executor:
        results=list(executor.map(qualify, packages))
    status="pass" if len(results)==len(packages) and all(x["status"]=="pass" for x in results) else "fail"; report={"status":status,"package_count":len(results),"package_workers":a.package_workers,"results":results}; a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if status=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
