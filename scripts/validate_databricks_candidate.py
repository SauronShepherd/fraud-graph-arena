"""Validate a write-time tagged candidate before publication activation."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS

def validation_queries(publication_id: str, run_id: str, catalog: str, schema: str) -> list[str]:
    prefix = f"{catalog}.{schema}."
    queries = []
    for path, table in PHYSICAL_TARGETS.items():
        qualified = prefix + table
        queries.append(f"SELECT COUNT(*) AS rows, COUNT_IF(_publication_id = '{publication_id}') AS tagged, COUNT_IF(_load_run_id = '{run_id}') AS correlated FROM {qualified}")
        queries.append(f"SELECT COUNT(*) AS missing_snapshot FROM {qualified} WHERE _publication_id = '{publication_id}' AND snapshot_version IS NULL")
    return queries

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--publication-id", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--execute", action="store_true"); parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); args = parser.parse_args()
    queries = validation_queries(args.publication_id, args.run_id, args.catalog, args.schema)
    if args.execute:
        warehouse = DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema)
        for query in queries: warehouse.execute(query)
    print(json.dumps({"status": "pass", "checks": len(queries), "publication_id": args.publication_id, "run_id": args.run_id}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
