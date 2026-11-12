from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Add parsed CSV data-row counts to canonical package receipts.")
    parser.add_argument("--root", type=Path, default=Path("case-data/canonical/v1"))
    parser.add_argument("--write", action="store_true", help="Persist the calculated row counts.")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"package root does not exist: {root}")

    updated = 0
    missing: list[str] = []
    for manifest_path in sorted(root.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        receipts = {
            item.get("path"): item
            for item in manifest.get("files", [])
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        changed = False
        for csv_path in sorted(manifest_path.parent.rglob("*.csv")):
            relative = csv_path.relative_to(manifest_path.parent).as_posix()
            receipt = receipts.get(relative)
            if receipt is None:
                missing.append(f"{manifest_path.parent.name}:{relative}")
                continue
            with csv_path.open(encoding="utf-8", newline="") as stream:
                reader = csv.reader(stream, strict=True)
                next(reader, None)
                rows = sum(1 for _ in reader)
            if receipt.get("rows") != rows:
                receipt["rows"] = rows
                changed = True
        if changed:
            updated += 1
        if args.write:
            serialized = json.dumps(manifest, indent=2, sort_keys=False) + "\n"
            manifest_path.write_bytes(serialized.encode("utf-8"))
    print(json.dumps({"manifests_updated": updated, "written": args.write, "missing_csv_receipts": missing}))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
