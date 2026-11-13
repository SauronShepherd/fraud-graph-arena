"""Shared live bulk/repeat lifecycle for candidate publications."""
from __future__ import annotations
import json, subprocess, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS
from fraud_graph_arena.canonical_persistence.identity import publication_id
from fraud_graph_arena.canonical_persistence.models import PackageIdentity
from fraud_graph_arena.canonical_persistence.package import CanonicalPackage
from import_databricks_candidate import plan

TRANSFER_TIMEOUT_SECONDS = 120
TRANSFER_RETRIES = 3


def transfer_package(package: Path, *, root: Path, profile: str, catalog: str, schema: str) -> None:
    """Upload a package file-by-file so one stalled recursive copy cannot hang a run."""
    stage = f"dbfs:/Volumes/{catalog}/{schema}/fga05_stage/{package.name}"
    expected = {Path(relative) for relative in PHYSICAL_TARGETS}
    files = sorted(package / relative for relative in expected)
    missing = [relative.as_posix() for relative in expected if not (package / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"package is missing registered physical files: {sorted(missing)}")
    directories = sorted({f"{stage}/{source.relative_to(package).parent.as_posix()}" for source in files})
    for directory in directories:
        result = subprocess.run(
            ["databricks", "fs", "mkdirs", directory, "--profile", profile],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=TRANSFER_TIMEOUT_SECONDS,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
            raise RuntimeError(f"failed to create staging directory {directory}: {detail[-1000:]}")
    for source in files:
        relative = source.relative_to(package).as_posix()
        destination = f"{stage}/{relative}"
        last_error = ""
        for attempt in range(1, TRANSFER_RETRIES + 1):
            try:
                result = subprocess.run(
                    ["databricks", "fs", "cp", str(source), destination, "--profile", profile, "--overwrite"],
                    cwd=root,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=TRANSFER_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                last_error = f"timeout after {TRANSFER_TIMEOUT_SECONDS}s"
                continue
            if result.returncode == 0:
                break
            last_error = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
        else:
            raise RuntimeError(f"failed to transfer {relative} after {TRANSFER_RETRIES} attempts: {last_error[-1000:]}")

def run_package(package: Path, *, root: Path, profile: str, catalog: str, schema: str, warehouse: str) -> dict:
    run_id = "dbx_run_" + uuid.uuid4().hex
    preflight = CanonicalPackage.read(package)
    identity = PackageIdentity(preflight.case_id, preflight.case_version, preflight.snapshot_version, preflight.canonical_model_version, preflight.content_digest)
    candidate_id = publication_id(identity)
    client = DatabricksWarehouse(profile, warehouse, catalog, schema)
    publications = client.qualify_table("fga_import_publications")
    existing = client.execute(f"SELECT status FROM {publications} WHERE publication_id = '{candidate_id}'")
    existing_rows = existing.get("result", {}).get("data_array", [])
    if existing_rows and existing_rows[0][0] in {"ACTIVE", "PUBLISHED", "VALIDATED"}:
        return {"package": package.name, "run_id": run_id, "statements": 0, "lifecycle": {"status": "REUSED", "publication_id": candidate_id, "existing_status": existing_rows[0][0]}}
    if existing_rows and existing_rows[0][0] == "REJECTED":
        client.execute(f"DELETE FROM {publications} WHERE publication_id = '{candidate_id}' AND status = 'REJECTED'")
    transfer_package(package, root=root, profile=profile, catalog=catalog, schema=schema)
    statements = plan(package, run_id, catalog, schema)
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(client.execute, statements))
    result = subprocess.run(["python", "scripts/record_databricks_publication.py", str(package), "--run-id", run_id, "--profile", profile, "--warehouse", warehouse, "--catalog", catalog, "--schema", schema, "--execute"], cwd=root, check=True, capture_output=True, text=True)
    return {"package": package.name, "run_id": run_id, "statements": len(statements), "lifecycle": json.loads(result.stdout)}
