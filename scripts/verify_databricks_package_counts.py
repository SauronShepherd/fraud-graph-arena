from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=Path("case-data/canonical/v1"))
    parser.add_argument("--profile", default="sda")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse", default="e444f39962128242")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-05/databricks-row-counts.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    counts: dict[str, int] = {}
    for package in sorted(args.package_root.iterdir()):
        if not package.is_dir():
            continue
        for csv_path in sorted(package.rglob("*.csv")):
            table = "fga_" + csv_path.relative_to(package).as_posix().replace("/", "_").replace(".", "_")
            with csv_path.open(newline="", encoding="utf-8") as fh:
                counts[table] = counts.get(table, 0) + max(0, sum(1 for _ in fh) - 1)

    selects = [f"SELECT '{table}' AS table_name, COUNT(*) AS row_count, COUNT(_publication_id) AS publication_rows, COUNT(_load_run_id) AS run_rows FROM {table}" for table in sorted(counts)]
    payload = {"statement": " UNION ALL ".join(selects), "warehouse_id": args.warehouse, "wait_timeout": "50s", "catalog": args.catalog, "schema": args.schema}
    response = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", args.profile, "--json", json.dumps(payload)], cwd=root, capture_output=True, text=True, check=True)
    body = json.loads(response.stdout)
    if body.get("status", {}).get("state") != "SUCCEEDED":
        raise SystemExit(json.dumps(body))
    observed = {row[0]: {"live_rows": int(row[1]), "publication_rows": int(row[2]), "run_rows": int(row[3])} for row in body.get("result", {}).get("data_array", [])}
    mismatches = []
    for table, expected in counts.items():
        actual = observed.get(table, {"live_rows": -1, "publication_rows": -1, "run_rows": -1})
        if actual["live_rows"] != expected or actual["publication_rows"] != expected or actual["run_rows"] != expected:
            mismatches.append({"table": table, "expected_rows": expected, **actual})
    report = {"status": "pass" if not mismatches else "fail", "table_count": len(counts), "mismatch_count": len(mismatches), "mismatches": mismatches}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
