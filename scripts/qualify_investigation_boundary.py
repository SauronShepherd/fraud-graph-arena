"""Qualify the player-safe T02 publication boundary with read-only SQL.

This check deliberately does not create tables, mutate publications, or store
manual hypotheses in Databricks.  FGA-08 stores the command history in the
application persistence boundary; Databricks is qualified here as the source
of the safe, active graph projection consumed by that command.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any


SQL_CLI_TIMEOUT_SECONDS = 75
SQL_STATEMENT_TIMEOUT_SECONDS = 180
SAFE_TABLES = (
    "fga_active_published_records_csv",
    "fga_active_published_relationships_csv",
)
FORBIDDEN_COLUMN_TOKENS = (
    "answer",
    "culprit",
    "evaluator",
    "guilt",
    "hidden",
    "solution",
    "truth",
    "verdict",
)


class DatabricksBoundaryError(RuntimeError):
    """Raised when the read-only qualification cannot complete."""


def validate_identifier(label: str, value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", value):
        raise ValueError(f"invalid {label}: only approved SQL identifier characters are allowed")
    return value


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def data_rows(response: dict[str, Any]) -> list[list[Any]]:
    result = response.get("result", {})
    rows = result.get("data_array", [])
    if not isinstance(rows, list):
        raise DatabricksBoundaryError("Databricks returned an unexpected result shape")
    return rows


def execute_sql(profile: str, warehouse_id: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
    payload = {
        "statement": statement,
        "warehouse_id": warehouse_id,
        "wait_timeout": "30s",
        "catalog": catalog,
        "schema": schema,
    }
    try:
        submitted = subprocess.run(
            [
                "databricks",
                "api",
                "post",
                "/api/2.0/sql/statements",
                "--profile",
                profile,
                "--json",
                json.dumps(payload),
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=SQL_CLI_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise DatabricksBoundaryError("Databricks SQL submission timed out") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "Databricks SQL submission failed").strip()
        raise DatabricksBoundaryError(detail[-512:]) from exc

    try:
        response = json.loads(submitted.stdout)
    except json.JSONDecodeError as exc:
        raise DatabricksBoundaryError("Databricks returned invalid JSON") from exc

    state = response.get("status", {}).get("state")
    statement_id = response.get("statement_id")
    deadline = time.monotonic() + SQL_STATEMENT_TIMEOUT_SECONDS
    while state in {"PENDING", "RUNNING"} and statement_id and time.monotonic() < deadline:
        time.sleep(1)
        try:
            polled = subprocess.run(
                [
                    "databricks",
                    "api",
                    "get",
                    f"/api/2.0/sql/statements/{statement_id}",
                    "--profile",
                    profile,
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=SQL_CLI_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            raise DatabricksBoundaryError("Databricks SQL polling timed out") from exc
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "Databricks SQL polling failed").strip()
            raise DatabricksBoundaryError(detail[-512:]) from exc
        try:
            response = json.loads(polled.stdout)
        except json.JSONDecodeError as exc:
            raise DatabricksBoundaryError("Databricks returned invalid polling JSON") from exc
        state = response.get("status", {}).get("state")

    if state != "SUCCEEDED":
        detail = response.get("status", {}).get("error", response.get("status", {}))
        raise DatabricksBoundaryError(f"Databricks statement did not succeed: {detail}")
    return response


def build_statements(catalog: str, schema: str, case_id: str) -> dict[str, str]:
    qualified_records = f"`{catalog}`.`{schema}`.`fga_active_published_records_csv`"
    qualified_relationships = f"`{catalog}`.`{schema}`.`fga_active_published_relationships_csv`"
    qualified_publications = f"`{catalog}`.`{schema}`.`fga_active_publications`"
    case = sql_string(case_id)
    return {
        "publication": (
            f"SELECT case_id, case_version, snapshot_version, active_publication_id "
            f"FROM {qualified_publications} WHERE case_id = {case}"
        ),
        "records": (
            f"SELECT COUNT(*) AS record_count, COUNT(DISTINCT record_id) AS distinct_record_ids, "
            f"COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {qualified_records} WHERE case_id = {case}"
        ),
        "relationships": (
            f"SELECT COUNT(*) AS relationship_count, COUNT(DISTINCT relationship_id) AS distinct_relationship_ids, "
            f"COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {qualified_relationships} WHERE case_id = {case}"
        ),
        "dangling_endpoints": (
            f"SELECT COUNT(*) AS dangling_endpoint_count FROM {qualified_relationships} AS relationship "
            f"WHERE relationship.case_id = {case} AND ("
            f"NOT EXISTS (SELECT 1 FROM {qualified_records} AS source_record "
            f"WHERE source_record.case_id = relationship.case_id AND source_record.record_id = relationship.source_record_id) "
            f"OR NOT EXISTS (SELECT 1 FROM {qualified_records} AS target_record "
            f"WHERE target_record.case_id = relationship.case_id AND target_record.record_id = relationship.target_record_id))"
        ),
        "columns": (
            f"SELECT table_name, column_name FROM `{catalog}`.information_schema.columns "
            f"WHERE table_schema = {sql_string(schema)} AND table_name IN "
            f"({', '.join(sql_string(table) for table in SAFE_TABLES)}) ORDER BY table_name, ordinal_position"
        ),
    }


def qualify(
    profile: str,
    warehouse_id: str,
    catalog: str,
    schema: str,
    case_id: str,
    expected_records: int,
    expected_relationships: int,
    execute: Any = execute_sql,
) -> dict[str, Any]:
    statements = build_statements(catalog, schema, case_id)
    responses = {
        name: execute(profile, warehouse_id, catalog, schema, statement)
        for name, statement in statements.items()
    }
    publication_rows = data_rows(responses["publication"])
    record_rows = data_rows(responses["records"])
    relationship_rows = data_rows(responses["relationships"])
    dangling_rows = data_rows(responses["dangling_endpoints"])
    column_rows = data_rows(responses["columns"])

    columns = [str(row[1]) for row in column_rows if len(row) >= 2]
    forbidden_columns = sorted(
        column for column in columns
        if any(token in column.lower() for token in FORBIDDEN_COLUMN_TOKENS)
    )
    record_summary = record_rows[0] if record_rows else []
    relationship_summary = relationship_rows[0] if relationship_rows else []
    dangling_count = int(dangling_rows[0][0]) if dangling_rows else -1
    checks = {
        "one_active_publication": len(publication_rows) == 1,
        "record_count": len(record_summary) >= 3 and int(record_summary[0]) == expected_records,
        "distinct_record_ids": len(record_summary) >= 3 and int(record_summary[1]) == expected_records,
        "record_snapshot_count": len(record_summary) >= 3 and int(record_summary[2]) == 1,
        "relationship_count": len(relationship_summary) >= 3 and int(relationship_summary[0]) == expected_relationships,
        "distinct_relationship_ids": len(relationship_summary) >= 3 and int(relationship_summary[1]) == expected_relationships,
        "relationship_snapshot_count": len(relationship_summary) >= 3 and int(relationship_summary[2]) == 1,
        "no_dangling_endpoints": dangling_count == 0,
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
        "active_publication": publication_rows[0] if len(publication_rows) == 1 else None,
        "record_summary": record_summary,
        "relationship_summary": relationship_summary,
        "dangling_endpoint_count": dangling_count,
        "observed_columns": columns,
        "forbidden_columns": forbidden_columns,
        "checks": checks,
    }


def source_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    value = result.stdout.strip()
    return value or None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="fga")
    parser.add_argument("--catalog", default="sda_dev")
    parser.add_argument("--schema", default="sandbox")
    parser.add_argument("--warehouse-id", default="eded42c9d0a69b84")
    parser.add_argument("--case-id", default="ACADEMY_T02")
    parser.add_argument("--expected-records", type=int, default=20)
    parser.add_argument("--expected-relationships", type=int, default=21)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    for label, value in (("catalog", args.catalog), ("schema", args.schema), ("warehouse-id", args.warehouse_id)):
        validate_identifier(label, value)
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", args.case_id):
        raise SystemExit("invalid case-id")

    try:
        report = qualify(
            args.profile,
            args.warehouse_id,
            args.catalog,
            args.schema,
            args.case_id,
            args.expected_records,
            args.expected_relationships,
        )
    except (DatabricksBoundaryError, ValueError) as exc:
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
