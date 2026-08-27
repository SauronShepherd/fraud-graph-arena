"""Normalize package table snapshot versions to the package control row."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def normalize(root: Path) -> int:
    changed = 0
    for package in sorted(path for path in root.iterdir() if path.is_dir()):
        control = package / "config/cases.csv"
        if not control.exists():
            continue
        with control.open(newline="", encoding="utf-8") as handle:
            snapshot = next(csv.DictReader(handle))["snapshot_version"]
        for path in sorted(package.rglob("*.csv")):
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
                fieldnames = handle.seek(0) or next(csv.reader(handle))
            if not rows or "snapshot_version" not in fieldnames:
                continue
            updates = sum(row.get("snapshot_version") not in ("", snapshot) for row in rows)
            if not updates:
                continue
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                for row in rows:
                    row["snapshot_version"] = snapshot
                    writer.writerow(row)
            changed += updates
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(f"normalized_rows={normalize(args.root)}")
