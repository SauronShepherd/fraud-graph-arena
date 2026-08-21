from __future__ import annotations
import argparse, json, shutil, tempfile
from pathlib import Path
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse
from fraud_graph_arena.canonical_persistence.models import ImportStatus

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package-root",type=Path,default=Path("case-data/canonical/v1")); p.add_argument("--output",type=Path,default=Path("reports/iteration-05/imports")); a=p.parse_args()
    packages=sorted(x for x in a.package_root.iterdir() if x.is_dir()); warehouse=MemoryWarehouse(); importer=CanonicalImporter(warehouse)
    first=importer.import_package(packages[0]); old=warehouse.active[warehouse.publications[first.publication_id].identity.key]
    failed=importer.import_package(packages[1], retry_of=first.run_id, fail_after=17)
    retry=importer.import_package(packages[1], retry_of=failed.run_id)
    with tempfile.TemporaryDirectory() as temp:
        mutated=Path(temp)/packages[0].name; shutil.copytree(packages[0], mutated)
        target=mutated/"config/cases.csv"; raw=target.read_text(encoding="utf-8"); target.write_text(raw.replace(",", ",", 1)+"\n", encoding="utf-8")
        # Recompute only the manifest entry so the failure reaches immutable identity checking.
        import hashlib
        manifest=json.loads((mutated/"manifest.json").read_text(encoding="utf-8")); entry=next(x for x in manifest["files"] if x["path"]=="config/cases.csv"); data=target.read_bytes(); entry["bytes"]=len(data); entry["sha256"]=hashlib.sha256(data).hexdigest(); (mutated/"manifest.json").write_text(json.dumps(manifest),encoding="utf-8")
        conflict=importer.import_package(mutated)
    conflict_code=warehouse.runs[conflict.run_id].error_code
    report={"status":"pass" if first.status==ImportStatus.PUBLISHED and failed.status==ImportStatus.FAILED and retry.status==ImportStatus.PUBLISHED and warehouse.active[warehouse.publications[first.publication_id].identity.key]==old and conflict_code=="IMMUTABLE_SNAPSHOT_CONFLICT" else "fail", "first":first.status, "failed":failed.status, "retry":retry.status, "conflict":conflict_code, "active_unchanged":warehouse.active[warehouse.publications[first.publication_id].identity.key]==old}
    a.output.mkdir(parents=True,exist_ok=True); (a.output/"recovery-comparison.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); (a.output/"immutable-conflict-summary.json").write_text(json.dumps({"status":"pass" if conflict_code=="IMMUTABLE_SNAPSHOT_CONFLICT" else "fail","error_code":conflict_code},indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if report["status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
