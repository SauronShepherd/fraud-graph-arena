"""Guarded case-version-scoped activation for a validated candidate."""
from __future__ import annotations
import argparse, json
import re
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse, _literal

def activation_statement(catalog: str, schema: str, case_id: str, case_version: str, snapshot_version: str, publication_id: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", catalog) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
        raise ValueError("catalog and schema must be registered SQL identifiers")
    table = DatabricksWarehouse(catalog=catalog, schema=schema).qualify_table("fga_active_publications")
    q = _literal
    return f"MERGE INTO {table} AS target USING (SELECT {q(case_id)} AS case_id, {q(case_version)} AS case_version, {q(snapshot_version)} AS snapshot_version, {q(publication_id)} AS active_publication_id, current_timestamp() AS activated_at_utc) AS source ON target.case_id = source.case_id AND target.case_version = source.case_version WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--case-id", required=True); parser.add_argument("--case-version", required=True); parser.add_argument("--snapshot-version", required=True); parser.add_argument("--publication-id", required=True); parser.add_argument("--execute", action="store_true"); parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); args = parser.parse_args()
    statement = activation_statement(args.catalog, args.schema, args.case_id, args.case_version, args.snapshot_version, args.publication_id)
    if args.execute: DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema).execute(statement)
    print(json.dumps({"status": "activated" if args.execute else "planned", "case_id": args.case_id, "case_version": args.case_version, "publication_id": args.publication_id}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
