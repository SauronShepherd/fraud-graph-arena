"""Validate a write-time tagged candidate before publication activation."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS
from fraud_graph_arena.case_data.registry import load_typed_registry

def q(value: object) -> str:
    if value is None: return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def validation_queries(publication_id: str, run_id: str, catalog: str, schema: str) -> list[str]:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", catalog) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
        raise ValueError("catalog and schema must be registered SQL identifiers")
    prefix = f"{catalog}.{schema}."
    queries = []
    for path, table in PHYSICAL_TARGETS.items():
        qualified = prefix + table
        queries.append(f"SELECT COUNT(*) AS rows, COUNT_IF(_publication_id = {q(publication_id)}) AS tagged, COUNT_IF(_load_run_id = {q(run_id)}) AS correlated FROM {qualified}")
        queries.append(f"SELECT COUNT(*) AS missing_snapshot FROM {qualified} WHERE _publication_id = {q(publication_id)} AND snapshot_version IS NULL")
    return queries

def _rows(response: dict) -> list[list[object]]:
    """Normalize the Databricks SQL statement response to its row array."""
    result = response.get("result", response)
    data = result.get("data_array", []) if isinstance(result, dict) else []
    if not isinstance(data, list):
        raise ValueError("Databricks validation response has no data_array")
    return data

def validate_results(responses: list[dict], publication_id: str, run_id: str) -> dict:
    """Fail closed unless every table has tagged, correlated rows and no null snapshots."""
    expected = sum((5 if path == "authoring/relationships.csv" else 4 if load_typed_registry()[path].get("primary_key") else 3) for path in PHYSICAL_TARGETS)
    if len(responses) != expected: raise ValueError(f"expected {expected} validation responses, got {len(responses)}")
    failures = []
    cursor = 0
    for path in PHYSICAL_TARGETS:
        counts = _rows(responses[cursor]); missing = _rows(responses[cursor + 1]); cursor += 2
        if len(counts) != 1 or len(counts[0]) < 3:
            failures.append(f"{path}: malformed row-count response")
            continue
        total, tagged, correlated = (int(value or 0) for value in counts[0][:3])
        missing_snapshot = int(missing[0][0] or 0) if len(missing) == 1 and missing[0] else -1
        if tagged != total or correlated != tagged or missing_snapshot != 0:
            failures.append(f"{path}: rows={total}, tagged={tagged}, correlated={correlated}, missing_snapshot={missing_snapshot}")
        if load_typed_registry()[path].get("primary_key"):
            duplicate = _rows(responses[cursor]); cursor += 1
            if not duplicate or int(duplicate[0][0] or 0) != 0: failures.append(f"{path}: duplicate primary key")
        mismatch = _rows(responses[cursor]); cursor += 1
        if not mismatch or int(mismatch[0][0] or 0) != 0: failures.append(f"{path}: case identity mismatch")
        if path == "authoring/relationships.csv":
            dangling = _rows(responses[cursor]); cursor += 1
            if not dangling or int(dangling[0][0] or 0) != 0: failures.append(f"{path}: dangling relationship endpoint")
    if failures:
        raise ValueError("candidate validation failed: " + "; ".join(failures))
    return {"status": "pass", "checks": expected, "publication_id": publication_id, "run_id": run_id}

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--publication-id", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--execute", action="store_true"); parser.add_argument("--profile", default="sda"); parser.add_argument("--warehouse", default="e444f39962128242"); parser.add_argument("--catalog", default="sda_dev"); parser.add_argument("--schema", default="sandbox"); args = parser.parse_args()
    queries = validation_queries(args.publication_id, args.run_id, args.catalog, args.schema)
    if args.execute:
        warehouse = DatabricksWarehouse(args.profile, args.warehouse, args.catalog, args.schema)
        responses = [warehouse.execute(query) for query in queries]
        report = validate_results(responses, args.publication_id, args.run_id)
    else:
        report = {"status": "planned", "checks": len(queries), "publication_id": args.publication_id, "run_id": args.run_id}
    print(json.dumps(report, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
