"""Read-only FGA-10 graph-analytics qualification against Databricks.

The qualification proves the published graph boundary and known-answer source
fixture. It does not call a GraphFrames job: the current ``fga`` target is a SQL
Warehouse, so the runtime result remains an explicit deterministic fallback.
No table, publication, cluster or library is created or changed.
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
except ModuleNotFoundError:  # direct ``python scripts/qualify_graph_analytics.py``
    from qualify_investigation_boundary import execute_sql, source_commit


FORBIDDEN_COLUMN_TOKENS = ("answer", "culprit", "evaluator", "guilt", "hidden", "solution", "truth", "verdict")


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def rows(response: dict[str, Any]) -> list[list[Any]]:
    data = response.get("result", {}).get("data_array", [])
    if not isinstance(data, list):
        raise ValueError("Databricks returned an unexpected result shape")
    return data


def build_statements(catalog: str, schema: str, case_id: str) -> dict[str, str]:
    prefix = f"`{catalog}`.`{schema}`."
    case = sql_string(case_id)
    records = prefix + "`fga_active_published_records_csv`"
    relationships = prefix + "`fga_active_published_relationships_csv`"
    publications = prefix + "`fga_active_publications`"
    return {
        "publication": f"SELECT case_id, case_version, snapshot_version, active_publication_id FROM {publications} WHERE case_id = {case}",
        "records": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT record_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {records} WHERE case_id = {case}",
        "relationships": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT relationship_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {relationships} WHERE case_id = {case}",
        "dangling_endpoints": f"SELECT COUNT(*) AS dangling_count FROM {relationships} AS relationship WHERE relationship.case_id = {case} AND (NOT EXISTS (SELECT 1 FROM {records} AS source_record WHERE source_record.case_id = relationship.case_id AND source_record.record_id = relationship.source_record_id) OR NOT EXISTS (SELECT 1 FROM {records} AS target_record WHERE target_record.case_id = relationship.case_id AND target_record.record_id = relationship.target_record_id))",
        "known_cycle": f"SELECT relationship_id, relationship_type, source_record_id, target_record_id, event_time, snapshot_version FROM {relationships} WHERE case_id = {case} AND relationship_type = 'PAYS' ORDER BY event_time, relationship_id",
        "columns": f"SELECT table_name, column_name FROM `{catalog}`.information_schema.columns WHERE table_schema = {sql_string(schema)} AND table_name IN ('fga_active_published_records_csv','fga_active_published_relationships_csv') ORDER BY table_name, ordinal_position",
        "runtime_probe": "SELECT current_version() AS sql_warehouse_runtime",
    }


def qualify(
    profile: str,
    warehouse_id: str,
    catalog: str,
    schema: str,
    case_id: str,
    execute: Any = execute_sql,
) -> dict[str, Any]:
    statements = build_statements(catalog, schema, case_id)
    responses = {name: execute(profile, warehouse_id, catalog, schema, statement) for name, statement in statements.items()}
    publication_rows = rows(responses["publication"])
    record_summary = rows(responses["records"])
    relationship_summary = rows(responses["relationships"])
    dangling_rows = rows(responses["dangling_endpoints"])
    cycle_rows = rows(responses["known_cycle"])
    column_rows = rows(responses["columns"])
    runtime_rows = rows(responses["runtime_probe"])

    publication = publication_rows[0] if len(publication_rows) == 1 else None
    active_snapshot = str(publication[2]) if publication and len(publication) >= 3 else None
    record_row = record_summary[0] if record_summary else []
    relationship_row = relationship_summary[0] if relationship_summary else []
    dangling_count = int(dangling_rows[0][0]) if dangling_rows else -1
    columns = [str(row[1]) for row in column_rows if len(row) >= 2]
    forbidden_columns = sorted(column for column in columns if any(token in column.lower() for token in FORBIDDEN_COLUMN_TOKENS))
    cycle_snapshots = [str(row[5]) for row in cycle_rows if len(row) >= 6]
    cycle_types = [str(row[1]).upper() for row in cycle_rows if len(row) >= 2]
    checks = {
        "one_active_publication": publication is not None,
        "record_count": len(record_row) >= 3 and int(record_row[0]) == 20,
        "distinct_record_ids": len(record_row) >= 3 and int(record_row[1]) == 20,
        "record_one_snapshot": len(record_row) >= 3 and int(record_row[2]) == 1,
        "relationship_count": len(relationship_row) >= 3 and int(relationship_row[0]) == 21,
        "distinct_relationship_ids": len(relationship_row) >= 3 and int(relationship_row[1]) == 21,
        "relationship_one_snapshot": len(relationship_row) >= 3 and int(relationship_row[2]) == 1,
        "no_dangling_endpoints": dangling_count == 0,
        "known_payment_cycle_fixture": len(cycle_rows) == 3 and all(kind == "PAYS" for kind in cycle_types),
        "cycle_snapshot_matches_publication": active_snapshot is not None and bool(cycle_snapshots) and all(snapshot == active_snapshot for snapshot in cycle_snapshots),
        "no_forbidden_player_columns": not forbidden_columns,
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "read_only": True,
        "profile": profile,
        "catalog": catalog,
        "schema": schema,
        "warehouse_id": warehouse_id,
        "case_id": case_id,
        "active_publication": publication,
        "record_summary": record_row,
        "relationship_summary": relationship_row,
        "dangling_endpoint_count": dangling_count,
        "known_cycle_rows": cycle_rows,
        "observed_columns": columns,
        "forbidden_columns": forbidden_columns,
        "runtime_probe": runtime_rows,
        "graphframes_compatibility": {
            "status": "UNRESOLVED_SQL_WAREHOUSE_ONLY",
            "actual_engine_run": False,
            "reason": "The fga profile reaches a SQL Warehouse; no cluster library installation or GraphFrames job was requested or performed.",
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
    parser.add_argument("--case-id", default="ACADEMY_T02")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    for label, value in (("catalog", args.catalog), ("schema", args.schema), ("warehouse-id", args.warehouse_id)):
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", value):
            raise SystemExit(f"invalid {label}")
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", args.case_id):
        raise SystemExit("invalid case-id")
    try:
        report = qualify(args.profile, args.warehouse_id, args.catalog, args.schema, args.case_id)
    except Exception as exc:  # keep the failed external boundary as a receipt
        report = {
            "status": "fail",
            "read_only": True,
            "profile": args.profile,
            "catalog": args.catalog,
            "schema": args.schema,
            "warehouse_id": args.warehouse_id,
            "case_id": args.case_id,
            "error": str(exc),
        }
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
