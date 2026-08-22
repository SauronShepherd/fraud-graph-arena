"""Deterministic, governed multi-package reference importer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
from fraud_graph_arena.canonical_persistence.models import LoadPolicy
from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("config/canonical-corpus.v1.json"))
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stop-on-failure", action="store_true")
    parser.add_argument("--load-policy", choices=[p.value for p in LoadPolicy], default=LoadPolicy.SAFE_ONLY.value)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    root = args.root or Path(manifest["root"])
    packages = [root / name for name in manifest["order"]]
    warehouse = MemoryWarehouse()
    importer = CanonicalImporter(warehouse)
    results = []
    for package in packages:
        try:
            result = importer.import_package(package, load_policy=LoadPolicy(args.load_policy))
            item = {"package": package.name, "status": result.status.value, "run_id": result.run_id, "publication_id": result.publication_id}
        except Exception as exc:
            item = {"package": package.name, "status": "FAILED", "error_code": type(exc).__name__, "error_summary": str(exc)[-512:]}
        results.append(item)
        if item["status"] not in {"PUBLISHED", "REUSED", "VALIDATED"} and args.stop_on_failure:
            break
    report = {"schema_version": "1.0", "manifest": str(args.manifest), "model_version": manifest["model_version"], "package_count": len(packages), "processed_count": len(results), "results": results, "status": "pass" if len(results) == len(packages) and all(item["status"] in {"PUBLISHED", "REUSED", "VALIDATED"} for item in results) else "fail", "evidence_scope": "local-reference"}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
