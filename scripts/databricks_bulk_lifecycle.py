"""Shared live bulk/repeat lifecycle for candidate publications."""
from __future__ import annotations
import json, subprocess, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from fraud_graph_arena.canonical_persistence.identity import publication_id
from fraud_graph_arena.canonical_persistence.models import PackageIdentity
from fraud_graph_arena.canonical_persistence.package import CanonicalPackage
from import_databricks_candidate import plan

def run_package(package: Path, *, root: Path, profile: str, catalog: str, schema: str, warehouse: str) -> dict:
    preflight = CanonicalPackage.read(package)
    identity = PackageIdentity(preflight.case_id, preflight.case_version, preflight.snapshot_version, preflight.canonical_model_version, preflight.content_digest)
    publication = publication_id(identity)
    client = DatabricksWarehouse(profile, warehouse, catalog, schema)
    existing = client.execute(f"SELECT status FROM {client.qualify_table('fga_import_publications')} WHERE publication_id = '{publication}'")
    existing_rows = existing.get("result", {}).get("data_array", [])
    if existing_rows and existing_rows[0][0] == "ACTIVE":
        return {"package": package.name, "run_id": None, "statements": 0, "lifecycle": {"status": "REUSED_PRECHECK", "publication_id": publication, "existing_status": "ACTIVE", "reason": "publication already active; no candidate rows inserted"}}
    run_id = "dbx_run_" + uuid.uuid4().hex
    stage = f"dbfs:/Volumes/{catalog}/{schema}/fga05_stage/{package.name}"
    subprocess.run(["databricks", "fs", "cp", str(package), stage, "--profile", profile, "-r", "--overwrite", "--concurrency", "1"], cwd=root, check=True, capture_output=True, text=True, timeout=600)
    statements = plan(package, run_id, catalog, schema)
    def execute_statement(statement: str) -> None:
        client.execute(statement)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(execute_statement, statements))
    result = subprocess.run(["python", "scripts/record_databricks_publication.py", str(package), "--run-id", run_id, "--profile", profile, "--warehouse", warehouse, "--catalog", catalog, "--schema", schema, "--execute"], cwd=root, check=True, capture_output=True, text=True)
    return {"package": package.name, "run_id": run_id, "statements": len(statements), "lifecycle": json.loads(result.stdout)}
