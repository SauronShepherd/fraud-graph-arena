from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, validate_registry, expected_topology
from fraud_graph_arena.canonical_persistence.identity import publication_id
from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse
from fraud_graph_arena.canonical_persistence.models import LoadPolicy

def main() -> int:
    p = argparse.ArgumentParser(description="Canonical v1 loader; targets are registry-controlled.")
    p.add_argument("package", type=Path); p.add_argument("--plan", action="store_true"); p.add_argument("--self-check", action="store_true"); p.add_argument("--adapter", choices=("memory", "databricks"), default="memory"); p.add_argument("--load-policy", choices=[policy.value for policy in LoadPolicy], default=LoadPolicy.SAFE_ONLY.value); p.add_argument("--json-report", type=Path); p.add_argument("--profile", default="sda"); p.add_argument("--warehouse", default="e444f39962128242"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--run-id"); p.add_argument("--execute", action="store_true"); args = p.parse_args()
    if args.self_check:
        validate_registry()
        report = {"schema_version":"1.0", "status":"pass", "check":"self-check", "canonical_table_count":len(PHYSICAL_TARGETS), "operational_table_count":5, "topology_count":len(expected_topology()), "adapter":args.adapter}
        rendered=json.dumps(report, indent=2)+"\n"; print(rendered,end="")
        if args.json_report: args.json_report.write_text(rendered,encoding="utf-8")
        return 0
    if args.adapter == "databricks":
        if args.plan:
            report = {"schema_version":"1.0", "status":"planned", "adapter":"databricks", "package":str(args.package), "delegated_engine":"record_databricks_publication.py", "write_free":True, "requires_execute":True}
            rendered=json.dumps(report, indent=2)+"\n"; print(rendered,end="")
            if args.json_report: args.json_report.write_text(rendered,encoding="utf-8")
            return 0
        if not args.execute:
            raise SystemExit("databricks execution requires explicit --execute; use --plan for a write-free plan")
        command=[sys.executable, "scripts/record_databricks_publication.py", str(args.package), "--run-id", args.run_id or "dbx_cli_run", "--profile", args.profile, "--warehouse", args.warehouse, "--catalog", args.catalog, "--schema", args.schema, "--execute"]
        result=subprocess.run(command, capture_output=True, text=True)
        if result.stdout: print(result.stdout, end="")
        if result.returncode != 0 and result.stderr: print(result.stderr, file=sys.stderr, end="")
        return result.returncode
    if args.plan:
        warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse); identity = importer._identity(args.package); active=warehouse.active.get(identity.key)
        report={"schema_version":"1.0","status":"planned","package":str(args.package),"case_id":identity.case_id,"case_version":identity.case_version,"snapshot_version":identity.snapshot_version,"canonical_model_version":identity.canonical_model_version,"content_digest":identity.content_digest,"publication_id":publication_id(identity),"datasets":list(PHYSICAL_TARGETS),"targets":list(PHYSICAL_TARGETS.values()),"active_publication_id":active,"classification":"new_publication"}
        rendered=json.dumps(report, indent=2)+"\n"; print(rendered,end="")
        if args.json_report: args.json_report.write_text(rendered,encoding="utf-8")
        return 0
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(args.package, load_policy=LoadPolicy(args.load_policy))
    report={"schema_version":"1.0", **result.__dict__}; rendered=json.dumps(report, default=str, indent=2)+"\n"; print(rendered,end="")
    if args.json_report: args.json_report.write_text(rendered,encoding="utf-8")
    return 0 if result.status.value in {"PUBLISHED", "REUSED", "VALIDATED"} else 1
if __name__ == "__main__": raise SystemExit(main())
