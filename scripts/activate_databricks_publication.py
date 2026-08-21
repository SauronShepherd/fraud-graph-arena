"""Guarded case-version-scoped activation for a validated candidate."""
from __future__ import annotations
import argparse, json
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def activation_statement(catalog: str, schema: str) -> str:
    table = f"{catalog}.{schema}.fga_active_publications"
    return f"MERGE INTO {table} AS target USING (SELECT :case_id AS case_id, :case_version AS case_version, :snapshot_version AS snapshot_version, :publication_id AS active_publication_id, current_timestamp() AS activated_at_utc) AS source ON target.case_id = source.case_id AND target.case_version = source.case_version WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--case-id", required=True); parser.add_argument("--case-version", required=True); parser.add_argument("--snapshot-version", required=True); parser.add_argument("--publication-id", required=True); parser.add_argument("--execute", action="store_true"); parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); args = parser.parse_args()
    statement = activation_statement(args.catalog, args.schema)
    if args.execute: DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema).execute(statement)
    print(json.dumps({"status": "activated" if args.execute else "planned", "case_id": args.case_id, "case_version": args.case_version, "publication_id": args.publication_id}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
