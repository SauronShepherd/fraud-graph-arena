from __future__ import annotations
import argparse, json, subprocess, tempfile

def main():
    p = argparse.ArgumentParser(); p.add_argument("table"); p.add_argument("source"); p.add_argument("--profile", default="sda"); p.add_argument("--warehouse", default="e444f39962128242"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--force", action="store_true"); args = p.parse_args()
    force = "true" if args.force else "false"
    statement = f"COPY INTO {args.table} FROM '/Volumes/{args.catalog}/{args.schema}/fga05_stage/{args.source}' FILEFORMAT = CSV FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false') COPY_OPTIONS ('mergeSchema' = 'false', 'force' = '{force}')"
    payload = {"statement": statement, "warehouse_id": args.warehouse, "wait_timeout": "30s", "catalog": args.catalog, "schema": args.schema}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh: json.dump(payload, fh); path = fh.name
    result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", args.profile, "--json", "@" + path], capture_output=True, text=True)
    print(result.stdout); print(result.stderr, end="")
    return result.returncode
if __name__ == "__main__": raise SystemExit(main())
