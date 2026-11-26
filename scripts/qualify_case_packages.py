"""Qualify published case-package projections through Databricks, read-only.

The package manifest and application own the mechanics. Databricks is checked only
at the player-safe boundary: one active publication, one immutable snapshot, the
expected public record/relationship counts and an allowlisted column surface.
The SQL Warehouse is intentionally reported as a compatibility boundary; this
script does not claim to have executed GraphFrames, Zingg or any mutating command.
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
SAFE_TABLES = (
    "fga_active_publications",
    "fga_active_published_records_csv",
    "fga_active_published_relationships_csv",
)
DEFAULT_EXPECTED_COUNTS = {
    "ACADEMY_T02": {"records": 20, "relationships": 21},
    "ACADEMY_T03": {"records": 23, "relationships": 27},
}


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


def qualify(
    profile: str,
    warehouse_id: str,
    catalog: str,
    schema: str,
    case_id: str,
    execute: Any = execute_sql,
    expected_counts: dict[str, int] | None = None,
) -> dict[str, Any]:
    normalized_case_id = case_id.strip().upper()
    expected = expected_counts or DEFAULT_EXPECTED_COUNTS.get(normalized_case_id, {})
    statements = build_statements(catalog, schema, normalized_case_id)
    responses = {name: execute(profile, warehouse_id, catalog, schema, statement) for name, statement in statements.items()}
    publication_rows = rows(responses["publication"])
    record_rows = rows(responses["records"])
    relationship_rows = rows(responses["relationships"])
    column_rows = rows(responses["columns"])
    publication = publication_rows[0] if len(publication_rows) == 1 else None
    record_summary = record_rows[0] if record_rows else []
    relationship_summary = relationship_rows[0] if relationship_rows else []
    columns = [str(row[1]) for row in column_rows if len(row) >= 2]
    forbidden_columns = sorted(column for column in columns if any(token in column.lower() for token in FORBIDDEN_COLUMN_TOKENS))
    expected_records = int(expected.get("records", -1))
    expected_relationships = int(expected.get("relationships", -1))
    active_snapshot = str(publication[2]) if publication is not None and len(publication) >= 3 else None
    checks = {
        "one_active_publication": publication is not None,
        "records_match_package": len(record_summary) >= 3 and tuple(map(int, record_summary[:3])) == (expected_records, expected_records, 1),
        "relationships_match_package": len(relationship_summary) >= 3 and tuple(map(int, relationship_summary[:3])) == (expected_relationships, expected_relationships, 1),
        "one_snapshot_matches_publication": active_snapshot is not None and len(record_summary) >= 3 and len(relationship_summary) >= 3 and int(record_summary[2]) == 1 and int(relationship_summary[2]) == 1,
        "no_forbidden_player_columns": not forbidden_columns,
        "only_allowlisted_read_queries": all(
            statement.lstrip().upper().startswith("SELECT")
            and not any(token in statement.lower() for token in ("insert", "update", "delete", "merge", "drop", "create", "alter", "truncate"))
            for statement in statements.values()
        ),
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "read_only": True,
        "profile": profile,
        "catalog": catalog,
        "schema": schema,
        "warehouse_id": warehouse_id,
        "case_id": normalized_case_id,
        "active_publication": publication,
        "record_summary": record_summary,
        "relationship_summary": relationship_summary,
        "expected_counts": {"records": expected_records, "relationships": expected_relationships},
        "observed_columns": columns,
        "forbidden_columns": forbidden_columns,
        "package_boundary": {
            "manifest_is_application_owned": True,
            "truth_source_queried": False,
            "graphframes_compatibility": "UNRESOLVED_SQL_WAREHOUSE_ONLY",
            "actual_engine_run": False,
            "fallback": "RUNTIME_DETERMINISTIC_FALLBACK",
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--case-id", action="append", dest="case_ids")
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-12/databricks-fga12-packages-current.json"))
    args = parser.parse_args()
    for label, value in (("catalog", args.catalog), ("schema", args.schema), ("warehouse-id", args.warehouse_id)):
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", value):
            raise SystemExit(f"invalid {label}")
    case_ids = [item.upper() for item in (args.case_ids or list(DEFAULT_EXPECTED_COUNTS))]
    reports: list[dict[str, Any]] = []
    for case_id in case_ids:
        try:
            reports.append(qualify(args.profile, args.warehouse_id, args.catalog, args.schema, case_id))
        except Exception as exc:  # keep the external boundary as a durable receipt
            reports.append({"status": "fail", "read_only": True, "profile": args.profile, "catalog": args.catalog, "schema": args.schema, "warehouse_id": args.warehouse_id, "case_id": case_id, "error": str(exc)})
    report = {
        "status": "pass" if reports and all(item["status"] == "pass" for item in reports) else "fail",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": source_commit(),
        "profile": args.profile,
        "catalog": args.catalog,
        "schema": args.schema,
        "warehouse_id": args.warehouse_id,
        "read_only": True,
        "cases": reports,
    }
    rendered = json.dumps(report, indent=2, default=str) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

