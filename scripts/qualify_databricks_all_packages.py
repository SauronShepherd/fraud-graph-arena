from __future__ import annotations
import argparse, json, subprocess, uuid
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS

def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.DEVNULL)

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package-root",type=Path,default=Path("case-data/canonical/v1")); p.add_argument("--profile",default="sda"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--stage-volume",default="fga05_stage"); p.add_argument("--all-rows",action="store_true"); p.add_argument("--report",type=Path,default=Path("reports/iteration-05/databricks-all-packages.json")); args=p.parse_args()
    root=Path(__file__).resolve().parents[1]; results=[]
    if args.report.exists():
        try: results=json.loads(args.report.read_text(encoding="utf-8")).get("results", [])
        except json.JSONDecodeError: results=[]
    completed={item.get("package") for item in results}
    for package in sorted(x for x in args.package_root.iterdir() if x.is_dir()):
        if package.name in completed: continue
        args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps({"status":"in_progress","current_package":package.name,"phase":"STAGING","package_count":len(results),"results":results},indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"package":package.name,"phase":"STAGING"}), flush=True)
        stage=f"dbfs:/Volumes/{args.catalog}/{args.schema}/{args.stage_volume}/{package.name}"
        run(["databricks","fs","cp",str(package),stage,"--profile",args.profile,"-r","--overwrite"],root)
        args.report.write_text(json.dumps({"status":"in_progress","current_package":package.name,"phase":"COPY_INTO","package_count":len(results),"results":results},indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"package":package.name,"phase":"COPY_INTO"}), flush=True)
        files=sorted(package.rglob("*.csv")); copied=0
        for file in files:
            rel=file.relative_to(package).as_posix(); table="fga_"+rel.replace("/","_").replace(".","_")
            run(["python","scripts/databricks_copy_into.py",table,f"{package.name}/{rel}","--profile",args.profile,"--catalog",args.catalog,"--schema",args.schema,"--warehouse",args.warehouse],root); copied+=1
        run_id="dbx_run_"+uuid.uuid4().hex
        tag=subprocess.run(["python","scripts/tag_databricks_publication.py",str(package),"--run-id",run_id,"--profile",args.profile,"--catalog",args.catalog,"--schema",args.schema,"--warehouse",args.warehouse],cwd=root,capture_output=True,text=True,check=True)
        results.append({"package":package.name,"status":"BULK_LOADED","csv_count":copied,"run_id":run_id,"tag":json.loads(tag.stdout)})
        args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps({"status":"in_progress","package_count":len(results),"results":results},indent=2)+"\n",encoding="utf-8")
    final={"status":"pass" if len(results)==len([x for x in args.package_root.iterdir() if x.is_dir()]) else "in_progress","package_count":len(results),"results":results}; args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(final,indent=2)+"\n",encoding="utf-8"); print(json.dumps(final,indent=2)); return 0 if final["status"]=="pass" else 1
if __name__ == "__main__": raise SystemExit(main())
