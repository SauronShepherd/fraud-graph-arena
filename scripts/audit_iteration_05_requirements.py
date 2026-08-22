from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

def load(path: Path) -> dict:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError): return {}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path("reports/iteration-05")); p.add_argument("--output",type=Path,default=Path("reports/iteration-05/requirement-audit.json")); args=p.parse_args()
    root=args.root; gate=load(root/"gate.json"); validation=load(root/"canonical-package-validation.json"); topology=load(root/"databricks-topology.json"); rows=load(root/"databricks-row-counts.json"); repeat=load(root/"databricks-repeat.json"); resources=load(root/"resource-inventory.json"); security=load(root/"security/qualification-gap.json"); unified=load(root/"unified-audit-current.json")
    evidence_sha = unified.get("source_sha") or gate.get("qualified_source_sha")
    closure_reports = [gate, validation, topology, rows, repeat, resources, security, unified]
    observed_shas = {value for report in closure_reports for value in (report.get("qualified_source_sha"), report.get("source_sha")) if value}
    observed_registry_digests = {value for report in closure_reports for value in (report.get("registry_digest"), report.get("canonical_registry_digest")) if value}
    mixed_revision = len(observed_shas) > 1 or len(observed_registry_digests) > 1
    def fresh(report: dict) -> bool:
        return report.get("qualified_source_sha", report.get("source_sha")) == evidence_sha
    requirements={
        "canonical_packages": "pass" if validation.get("valid") and validation.get("package_count")==13 else "fail",
        "bounded_topology": "pass" if topology.get("status")=="pass" and topology.get("actual_count")==44 else "fail",
        "live_rows_and_receipts": "pass" if rows.get("status")=="pass" and fresh(rows) else "external_gap",
        "repeat_qualification": "pass" if repeat.get("status")=="pass" and repeat.get("csv_attempt_count")==416 and fresh(repeat) else "external_gap",
        "resource_budget": "pass" if resources.get("within_budget") else "fail",
        "failure_isolation": "pass" if load(root/"imports/failure-injection-summary.json").get("status")=="pass" and fresh(load(root/"imports/failure-injection-summary.json")) else "external_gap",
        "local_regression_gate": "pass" if gate.get("status")=="pass" else "fail",
        "non_admin_truth_denial": security.get("status","missing") if fresh(security) else "external_gap",
        "live_candidate_pipeline": "pass" if unified.get("live_databricks", {}).get("status")=="qualified" else "external_gap",
    }
    if mixed_revision:
        requirements["evidence_revision_consistency"] = "fail"
    else:
        requirements["evidence_revision_consistency"] = "pass"
    report={"status":"external_gap" if "external_gap" in requirements.values() else ("pass" if all(v=="pass" for v in requirements.values()) else "fail"),"qualified_source_sha":evidence_sha,"observed_source_shas":sorted(observed_shas),"observed_registry_digests":sorted(observed_registry_digests),"mixed_revision":mixed_revision,"requirements":requirements,"closure_tag_allowed":all(v=="pass" for v in requirements.values())}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if report["status"] in {"pass","external_gap"} else 1
if __name__=="__main__": raise SystemExit(main())
