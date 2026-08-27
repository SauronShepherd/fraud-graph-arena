"""Remove authoring relationships whose endpoints are absent from the same package."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def repair(package: Path) -> int:
    records_path = package / "authoring/records.csv"
    relationships_path = package / "authoring/relationships.csv"
    with records_path.open(newline="", encoding="utf-8") as handle:
        record_ids = {row["record_id"] for row in csv.DictReader(handle)}
    with relationships_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = rows[0].keys()
    valid = [row for row in rows if row["source_record_id"] in record_ids and row["target_record_id"] in record_ids]
    removed = len(rows) - len(valid)
    if removed:
        with relationships_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(valid)
    return removed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    print(f"removed_relationships={repair(args.package)}")
