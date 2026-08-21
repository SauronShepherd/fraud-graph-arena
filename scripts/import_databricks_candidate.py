"""Build a write-time tagged Databricks candidate import plan.

The plan reads each source file into a temporary view and inserts rows into
the closed physical target with publication/run metadata in the same write.
No untagged target rows are created and no post-load UPDATE is required.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.identity import content_digest
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS
from fraud_graph_arena.case_data.registry import headers

def quote(value: str) -> str: return "'" + value.replace("'", "''") + "'"
def plan(package: Path, run_id: str, catalog: str, schema: str) -> list[str]:
    digest = content_digest(package); publication = "pub_" + hashlib.sha256((package.name + digest).encode()).hexdigest()
    statements = []
    for relative, table in PHYSICAL_TARGETS.items():
        view = "fga_stage_" + hashlib.sha256((run_id + relative).encode()).hexdigest()[:16]
        source = f"/Volumes/{catalog}/{schema}/fga05_stage/{package.name}/{relative}"
        columns = ", ".join(headers(relative))
        statements.append(f"CREATE OR REPLACE TEMPORARY VIEW {view} AS SELECT * FROM read_files({quote(source)}, format => 'csv', header => true)")
        statements.append(f"INSERT INTO {catalog}.{schema}.{table} ({columns}, _publication_id, _load_run_id) SELECT {columns}, {quote(publication)}, {quote(run_id)} FROM {view}")
    return statements

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("package", type=Path); parser.add_argument("--run-id", required=True); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    statements = plan(args.package, args.run_id, args.catalog, args.schema)
    args.output.write_text(";\n".join(statements) + ";\n", encoding="utf-8")
    print(json.dumps({"status": "planned", "statements": len(statements), "write_time_metadata": True}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
