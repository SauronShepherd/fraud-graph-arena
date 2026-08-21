from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse
from fraud_graph_arena.canonical_persistence.models import ImportStatus
from fraud_graph_arena.canonical_persistence.registry import expected_topology

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--package-root", type=Path, required=True); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse); packages = sorted(x for x in args.package_root.iterdir() if x.is_dir())
    first = [importer.import_package(x) for x in packages]
    repeated = [importer.import_package(x) for x in packages for _ in range(9)]
    live_root = Path("reports/iteration-05")
    live_ok = all((live_root / name).exists() for name in ("databricks-topology.json", "databricks-row-counts.json", "databricks-repeat.json"))
    report = {"status": "pass" if all(x.status == ImportStatus.PUBLISHED for x in first) and all(x.status == ImportStatus.REUSED for x in repeated) else "fail", "package_count": len(packages), "expected_topology_count": len(expected_topology()), "topology_hash": warehouse.topology_digest(), "runs": len(warehouse.runs), "publications": len(warehouse.publications), "live_databricks": "qualified" if live_ok else "not_qualified", "qualified_source_sha": __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], text=True).strip()}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8"); print(json.dumps(report, indent=2)); return 0 if report["status"] == "pass" else 1
if __name__ == "__main__": raise SystemExit(main())
