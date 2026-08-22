from __future__ import annotations
import argparse, json
import subprocess
from pathlib import Path
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse
from fraud_graph_arena.canonical_persistence.models import ImportStatus
from fraud_graph_arena.canonical_persistence.registry import expected_topology

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--package-root", type=Path, required=True); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse); packages = sorted(x for x in args.package_root.iterdir() if x.is_dir())
    first = [importer.import_package(x) for x in packages]
    repeated = [importer.import_package(x) for x in packages for _ in range(9)]
    failures = []
    for package, result in zip(packages, first):
        run = warehouse.runs.get(result.run_id)
        if result.status not in {ImportStatus.PUBLISHED, ImportStatus.REUSED, ImportStatus.VALIDATED} and run is not None:
            failures.append({"package": package.name, "run_id": result.run_id, "error_code": run.error_code, "error_summary": run.error_summary})
    live_root = Path("reports/iteration-05")
    current_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    unified = json.loads((live_root / "unified-audit-current.json").read_text(encoding="utf-8")) if (live_root / "unified-audit-current.json").exists() else {}
    live_ok = unified.get("live_databricks", {}).get("status") == "qualified" and unified.get("source_sha") == current_sha and unified.get("live_databricks", {}).get("source_sha") == current_sha
    local_ok = all(x.status == ImportStatus.PUBLISHED for x in first) and all(x.status == ImportStatus.REUSED for x in repeated)
    report = {"status": "pass" if local_ok else "fail", "package_count": len(packages), "expected_topology_count": len(expected_topology()), "topology_hash": warehouse.topology_digest(), "runs": len(warehouse.runs), "publications": len(warehouse.publications), "failures": failures, "evidence_scope": "local-reference", "live_databricks": "qualified" if live_ok else "not_qualified", "qualified_source_sha": current_sha, "closure_allowed": local_ok and live_ok}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8"); print(json.dumps(report, indent=2)); return 0 if report["status"] == "pass" else 1
if __name__ == "__main__": raise SystemExit(main())
