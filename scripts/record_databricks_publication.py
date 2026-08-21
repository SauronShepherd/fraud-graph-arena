from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import Path
from fraud_graph_arena.canonical_persistence.identity import content_digest

def call(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False,encoding="utf-8") as fh: json.dump(payload,fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    output=json.loads(result.stdout)
    if output.get("status",{}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))
def q(value): return "NULL" if value is None else "'"+str(value).replace("'","''")+"'"
def main():
    p=argparse.ArgumentParser(); p.add_argument("package",type=Path); p.add_argument("--run-id",required=True); p.add_argument("--profile",default="sda"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); args=p.parse_args()
    import hashlib
    digest=content_digest(args.package); pub="pub_"+hashlib.sha256((args.package.name+digest).encode()).hexdigest()
    manifest=json.loads((args.package / "manifest.json").read_text(encoding="utf-8"))
    case_id=manifest["case_id"]; case_version=manifest.get("case_version", "1.0.0"); snapshot=manifest["snapshot_version"]; model=manifest["canonical_model_version"]
    call(args.profile,args.warehouse,args.catalog,args.schema,f"INSERT INTO fga_import_runs VALUES ({q(args.run_id)},{q(case_id)},{q(case_version)},{q(snapshot)},{q(digest)},'PUBLISHED',NULL,NULL,current_timestamp(),current_timestamp())")
    call(args.profile,args.warehouse,args.catalog,args.schema,f"INSERT INTO fga_import_publications VALUES ({q(pub)},{q(case_id)},{q(case_version)},{q(snapshot)},{q(model)},{q(digest)},NULL,'ACTIVE')")
    call(args.profile,args.warehouse,args.catalog,args.schema,f"INSERT INTO fga_active_publications VALUES ({q(case_id)},{q(case_version)},{q(snapshot)},{q(pub)},current_timestamp())")
    print(json.dumps({"status":"PUBLISHED","publication_id":pub,"run_id":args.run_id},indent=2))
if __name__ == "__main__": main()
