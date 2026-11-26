"""Read-only FGA-11 qualification against the player-safe Databricks boundary.

The economy ledger and evaluator are application-owned state. Databricks is
qualified here as the immutable source projection they are allowed to inspect:
one active publication, the bounded graph counts, and no truth-bearing player
columns. Every statement is a SELECT against the allowlisted active tables.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.qualify_investigation_boundary import execute_sql, source_commit
except ModuleNotFoundError:
    from qualify_investigation_boundary import execute_sql, source_commit


FORBIDDEN_COLUMN_TOKENS = ("answer", "culprit", "evaluator", "guilt", "hidden", "solution", "truth", "verdict")
SAFE_TABLES = ("fga_active_publications", "fga_active_published_records_csv", "fga_active_published_relationships_csv")


def rows(response: dict[str, Any]) -> list[list[Any]]:
    data = response.get("result", {}).get("data_array", [])
    if not isinstance(data, list):
        raise ValueError("Databricks returned an unexpected result shape")
    return data


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def build_statements(catalog: str, schema: str, case_id: str) -> dict[str, str]:
    prefix = f"`{catalog}`.`{schema}`."
    case = sql_string(case_id)
    return {
        "publication": f"SELECT case_id, case_version, snapshot_version, active_publication_id FROM {prefix}`fga_active_publications` WHERE case_id = {case}",
        "records": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT record_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {prefix}`fga_active_published_records_csv` WHERE case_id = {case}",
        "relationships": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT relationship_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {prefix}`fga_active_published_relationships_csv` WHERE case_id = {case}",
        "columns": f"SELECT table_name, column_name FROM `{catalog}`.information_schema.columns WHERE table_schema = {sql_string(schema)} AND table_name IN ({', '.join(sql_string(table) for table in SAFE_TABLES)}) ORDER BY table_name, ordinal_position",
        "runtime_probe": "SELECT current_version() AS sql_warehouse_runtime",
    }


def qualify(profile: str, warehouse_id: str, catalog: str, schema: str, case_id: str, execute: Any = execute_sql) -> dict[str, Any]:
    statements = build_statements(catalog, schema, case_id)
    responses = {name: execute(profile, warehouse_id, catalog, schema, statement) for name, statement in statements.items()}
    publication = rows(responses["publication"])
    record_summary = rows(responses["records"])
    relationship_summary = rows(responses["relationships"])
    column_rows = rows(responses["columns"])
    record_row = record_summary[0] if record_summary else []
    relationship_row = relationship_summary[0] if relationship_summary else []
    columns = [str(row[1]) for row in column_rows if len(row) >= 2]
    forbidden = sorted(column for column in columns if any(token in column.lower() for token in FORBIDDEN_COLUMN_TOKENS))
    checks = {
        "one_active_publication": len(publication) == 1,
        "record_boundary": len(record_row) >= 3 and tuple(map(int, record_row[:3])) == (20, 20, 1),
        "relationship_boundary": len(relationship_row) >= 3 and tuple(map(int, relationship_row[:3])) == (21, 21, 1),
        "no_forbidden_player_columns": not forbidden,
        "only_allowlisted_read_queries": all(statement.lstrip().upper().startswith("SELECT") and not any(token in statement.lower() for token in ("insert", "update", "delete", "merge", "drop", "create")) for statement in statements.values()),
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "read_only": True,
        "profile": profile,
        "catalog": catalog,
        "schema": schema,
        "warehouse_id": warehouse_id,
        "case_id": case_id,
        "active_publication": publication[0] if len(publication) == 1 else None,
        "record_summary": record_row,
        "relationship_summary": relationship_row,
        "observed_columns": columns,
        "forbidden_columns": forbidden,
        "economy_contract": {"rules_version": "fga11-economy-v1", "initial_credits": 9, "paid_actions": {"COMPARE_IDENTITIES": 3, "RUN_GRAPH_ANALYSIS": 3}, "navigation_and_submission": 0},
        "scoring_contract": {"version": "fga11-scoring-v1", "max_score": 1000, "truth_source_queried": False},
        "graphframes_compatibility": {"status": "UNRESOLVED_SQL_WAREHOUSE_ONLY", "actual_engine_run": False, "fallback": "RUNTIME_DETERMINISTIC_FALLBACK"},
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--case-id", default="ACADEMY_T02")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    for label, value in (("catalog", args.catalog), ("schema", args.schema), ("warehouse-id", args.warehouse_id)):
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", value):
            raise SystemExit(f"invalid {label}")
    try:
        report = qualify(args.profile, args.warehouse_id, args.catalog, args.schema, args.case_id)
    except Exception as exc:
        report = {"status": "fail", "read_only": True, "profile": args.profile, "catalog": args.catalog, "schema": args.schema, "warehouse_id": args.warehouse_id, "case_id": args.case_id, "error": str(exc)}
    report["run_at_utc"] = datetime.now(UTC).isoformat()
    report["source_commit"] = source_commit()
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
