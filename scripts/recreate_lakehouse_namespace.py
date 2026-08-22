from __future__ import annotations
import argparse, json, re, subprocess, tempfile
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import expected_topology

POLICY_PATH = Path(__file__).resolve().parents[1] / "config/lakehouse/destructive-environments.v1.json"

def approved_tuple(environment: str, catalog: str, schema: str, workspace_host: str = "") -> dict:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    for item in policy.get("approved", []):
        if (item.get("environment"), item.get("catalog"), item.get("schema")) == (environment, catalog, schema) and (not item.get("workspace_host") or item.get("workspace_host") == workspace_host):
            return item
    raise SystemExit("refusing destructive recreation: environment/catalog/schema tuple is not allowlisted")

def validate_identifier(label: str, value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", value):
        raise SystemExit(f"refusing destructive recreation: invalid {label}")
    return value

def execute(profile, warehouse, catalog, schema, statement):
    payload={"statement":statement,"warehouse_id":warehouse,"wait_timeout":"30s","catalog":catalog,"schema":schema}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump(payload, fh); path=fh.name
    result=subprocess.run(["databricks","api","post","/api/2.0/sql/statements","--profile",profile,"--json","@"+path],capture_output=True,text=True,check=True)
    output=json.loads(result.stdout)
    if output.get("status",{}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))
    return output

def main() -> int:
    p=argparse.ArgumentParser(description="Recreate only the explicitly approved disposable FGA namespace")
    p.add_argument("--environment",required=True); p.add_argument("--profile",default="sda"); p.add_argument("--workspace-host",default=""); p.add_argument("--catalog",default="sda_dev"); p.add_argument("--schema",default="sandbox"); p.add_argument("--warehouse",default="e444f39962128242"); p.add_argument("--dry-run",action="store_true"); p.add_argument("--apply",action="store_true"); p.add_argument("--confirm",type=str); p.add_argument("--report",type=Path)
    args=p.parse_args()
    validate_identifier("catalog", args.catalog); validate_identifier("schema", args.schema); validate_identifier("warehouse", args.warehouse)
    policy = approved_tuple(args.environment, args.catalog, args.schema, args.workspace_host)
    confirmation = f"{args.environment}:{args.catalog}:{args.schema}"
    if not args.dry_run and (not args.apply or args.confirm != confirmation):
        raise SystemExit(f"refusing destructive execution: require --apply --confirm {confirmation}")
    expected=set(expected_topology()); report={"environment":args.environment,"catalog":args.catalog,"schema":args.schema,"destructive_unit":policy["destructive_unit"],"dry_run":args.dry_run,"expected_count":len(expected),"statements":[]}
    if not args.dry_run:
        inventory=execute(args.profile,args.warehouse,args.catalog,args.schema,f"SHOW TABLES IN `{args.catalog}`.`{args.schema}`")
        actual={row[1] for row in inventory.get("result",{}).get("data_array",[])}
        views=execute(args.profile,args.warehouse,args.catalog,args.schema,f"SHOW VIEWS IN `{args.catalog}`.`{args.schema}`")
        actual_views={row[1] for row in views.get("result",{}).get("data_array",[])}
        report["before"] = sorted(actual)
        report["before_views"] = sorted(actual_views)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        for name in sorted(actual_views): execute(args.profile,args.warehouse,args.catalog,args.schema,f"DROP VIEW IF EXISTS `{name}`"); report["statements"].append("DROP VIEW "+name)
        for name in sorted(actual-expected): execute(args.profile,args.warehouse,args.catalog,args.schema,f"DROP TABLE IF EXISTS `{name}`"); report["statements"].append("DROP "+name)
        for name in sorted(actual&expected): execute(args.profile,args.warehouse,args.catalog,args.schema,f"TRUNCATE TABLE `{name}`"); report["statements"].append("TRUNCATE "+name)
        root=Path(__file__).resolve().parents[1]
        ddl=(root/"sql/lakehouse/fga_canonical_persistence_v1.sql").read_text(encoding="utf-8")+"\n"+(root/"sql/lakehouse/fga_import_ledger_v1.sql").read_text(encoding="utf-8")+"\n"+(root/"sql/lakehouse/fga_active_views_v1.sql").read_text(encoding="utf-8")
        for statement in (part.strip() for part in ddl.split(";") if part.strip()): execute(args.profile,args.warehouse,args.catalog,args.schema,statement); report["statements"].append("CREATE")
        final=execute(args.profile,args.warehouse,args.catalog,args.schema,f"SHOW TABLES IN `{args.catalog}`.`{args.schema}`")
        report["actual"] = sorted(row[1] for row in final.get("result",{}).get("data_array",[])); report["status"] = "pass" if set(report["actual"]) == expected else "fail"
    else:
        report["status"]="dry_run"; report["would_recreate"]=sorted(expected)
    rendered=json.dumps(report,indent=2)+"\n"; print(rendered,end="")
    if args.report: args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(rendered,encoding="utf-8")
    return 0 if report["status"] in {"pass","dry_run"} else 1
if __name__=="__main__": raise SystemExit(main())
