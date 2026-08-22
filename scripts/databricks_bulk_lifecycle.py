"""Shared live bulk/repeat lifecycle for candidate publications."""
from __future__ import annotations
import json, subprocess, uuid
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from import_databricks_candidate import plan

def run_package(package: Path, *, root: Path, profile: str, catalog: str, schema: str, warehouse: str) -> dict:
    run_id = "dbx_run_" + uuid.uuid4().hex
    stage = f"dbfs:/Volumes/{catalog}/{schema}/fga05_stage/{package.name}"
    subprocess.run(["databricks", "fs", "cp", str(package), stage, "--profile", profile, "-r", "--overwrite"], cwd=root, check=True, capture_output=True, text=True)
    statements = plan(package, run_id, catalog, schema)
    client = DatabricksWarehouse(profile, warehouse, catalog, schema)
    for statement in statements: client.execute(statement)
    result = subprocess.run(["python", "scripts/record_databricks_publication.py", str(package), "--run-id", run_id, "--profile", profile, "--warehouse", warehouse, "--catalog", catalog, "--schema", schema, "--execute"], cwd=root, check=True, capture_output=True, text=True)
    return {"package": package.name, "run_id": run_id, "statements": len(statements), "lifecycle": json.loads(result.stdout)}
