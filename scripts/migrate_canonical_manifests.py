"""Normalize checked-in canonical manifests to the single package contract."""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path
from fraud_graph_arena.case_data.registry import TABLE_PATHS
FAMILY_BY_PREFIX = {"T": "ACADEMY", "P": "PUPPY", "A": "ADULT", "S": "SENIOR"}
MAPPINGS = json.loads((Path(__file__).resolve().parents[1] / "config/converters/family-mappings.v1.json").read_text(encoding="utf-8"))["families"]
def migrate(package: Path) -> None:
    path = package / "manifest.json"; manifest = json.loads(path.read_text(encoding="utf-8"))
    with (package / "config/cases.csv").open(newline="", encoding="utf-8") as handle: row = next(csv.DictReader(handle))
    manifest["case_id"] = row["case_id"]; manifest["case_version"] = row["case_version"]
    manifest["family"] = manifest.get("family") or manifest.get("profile_code") or FAMILY_BY_PREFIX[package.name[0]]
    mapping = MAPPINGS[manifest["family"]]
    manifest["canonical_model_version"] = "1.0.0"; manifest["canonical_csv_table_count"] = len(TABLE_PATHS); manifest["converter"] = mapping["converter"]
    manifest["package_name"] = package.name; manifest["package_version"] = manifest.get("package_version") or "1.0.0"
    manifest["converter_version"] = manifest.get("converter_version") or "v1"
    manifest["mapping_version"] = manifest.get("mapping_version") or "family-mappings.v1"
    manifest["source_dialect"] = mapping["source_dialect"]
    receipts = []
    for rel in TABLE_PATHS:
        data = (package / rel).read_bytes()
        with (package / rel).open(newline="", encoding="utf-8") as handle: rows = max(0, sum(1 for _ in csv.reader(handle)) - 1)
        receipts.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "rows": rows})
    manifest["files"] = receipts; manifest["source_inputs"] = manifest.get("source_inputs") or []
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("root", type=Path); args = parser.parse_args()
    packages = sorted(path for path in args.root.iterdir() if path.is_dir())
    for package in packages: migrate(package)
    print(json.dumps({"package_count": len(packages), "status": "pass"}, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
