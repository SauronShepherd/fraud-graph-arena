from __future__ import annotations
import argparse, json, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS
from fraud_graph_arena.canonical_persistence.identity import content_digest
from pathlib import Path

def execute(profile, warehouse, catalog, schema, statement):
    payload = {"statement": statement, "warehouse_id": warehouse, "wait_timeout": "30s", "catalog": catalog, "schema": schema}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh: json.dump(payload, fh); path = fh.name
    result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", profile, "--json", "@" + path], capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    if output.get("status", {}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))

def main():
    raise SystemExit("post-load tagging is retired; use scripts/import_databricks_candidate.py")
    p = argparse.ArgumentParser(); p.add_argument("package", type=Path); p.add_argument("--run-id", required=True); p.add_argument("--profile", default="sda"); p.add_argument("--warehouse", default="e444f39962128242"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--workers", type=int, default=8); args = p.parse_args()
    import hashlib
    publication = "pub_" + hashlib.sha256((args.package.name + content_digest(args.package)).encode()).hexdigest()
    def tag(table): execute(args.profile, args.warehouse, args.catalog, args.schema, f"UPDATE {table} SET _publication_id = '{publication}', _load_run_id = '{args.run_id}' WHERE _publication_id IS NULL")
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool: list(pool.map(tag, PHYSICAL_TARGETS.values()))
    print(json.dumps({"status": "TAGGED", "publication_id": publication, "run_id": args.run_id, "tables": len(PHYSICAL_TARGETS)}, indent=2))
if __name__ == "__main__": main()
