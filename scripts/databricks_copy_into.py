from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import PurePosixPath
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS

def main():
    p = argparse.ArgumentParser(); p.add_argument("canonical_path", choices=tuple(PHYSICAL_TARGETS)); p.add_argument("source"); p.add_argument("--profile", default="sda"); p.add_argument("--warehouse", default="e444f39962128242"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--force", action="store_true"); args = p.parse_args()
    source_path = PurePosixPath(args.source)
    if source_path.is_absolute() or ".." in source_path.parts:
        raise SystemExit("source must remain inside the approved staging volume")
    table = PHYSICAL_TARGETS[args.canonical_path]
    force = "true" if args.force else "false"
    statement = f"COPY INTO {table} FROM '/Volumes/{args.catalog}/{args.schema}/fga05_stage/{source_path.as_posix()}' FILEFORMAT = CSV FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false') COPY_OPTIONS ('mergeSchema' = 'false', 'force' = '{force}')"
    payload = {"statement": statement, "warehouse_id": args.warehouse, "wait_timeout": "30s", "catalog": args.catalog, "schema": args.schema}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh: json.dump(payload, fh); path = fh.name
    result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", args.profile, "--json", "@" + path], capture_output=True, text=True)
    print(result.stdout); print(result.stderr, end="")
    return result.returncode
if __name__ == "__main__": raise SystemExit(main())
