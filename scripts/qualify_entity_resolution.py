"""Read-only FGA-09 entity-resolution qualification against Databricks.

The script verifies the active T02 publication, the player-safe candidate and
exact-match projections, and the two deliberately difficult person pairs. It
never installs a library, starts a job, writes a row, or updates a publication.
The current FGA runtime uses a deterministic local fallback when a Zingg
runtime is not available; the receipt says so explicitly instead of upgrading
curated rows into a claim that Zingg ran.
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
except ModuleNotFoundError:  # direct `python scripts/qualify_entity_resolution.py`
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
    candidates = prefix + "`fga_active_published_entity_resolution_candidates_csv`"
    exact = prefix + "`fga_active_published_exact_matches_csv`"
    publications = prefix + "`fga_active_publications`"
    return {
        "publication": f"SELECT case_id, case_version, snapshot_version, active_publication_id FROM {publications} WHERE case_id = {case}",
        "candidate_pairs": f"SELECT candidate_id, left_record_id, right_record_id, entity_type, confidence_band, actual_engine_run, generation_mode, framework_semantics, snapshot_version FROM {candidates} WHERE case_id = {case} ORDER BY candidate_id",
        "candidate_count": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT candidate_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {candidates} WHERE case_id = {case}",
        "exact_count": f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT match_id) AS distinct_ids, COUNT(DISTINCT snapshot_version) AS snapshot_count FROM {exact} WHERE case_id = {case}",
        "exact_pair_types": f"SELECT match_id, relationship_type, left_record_id, right_record_id, exact_field, actual_engine_run, snapshot_version FROM {exact} WHERE case_id = {case} ORDER BY match_id",
        "columns": f"SELECT table_name, column_name FROM `{catalog}`.information_schema.columns WHERE table_schema = {sql_string(schema)} AND table_name IN ('fga_active_published_entity_resolution_candidates_csv','fga_active_published_exact_matches_csv') ORDER BY table_name, ordinal_position",
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
    candidate_rows = rows(responses["candidate_pairs"])
    candidate_summary = rows(responses["candidate_count"])
    exact_summary = rows(responses["exact_count"])
    exact_rows = rows(responses["exact_pair_types"])
    column_rows = rows(responses["columns"])
    runtime_rows = rows(responses["runtime_probe"])

    columns = [str(row[1]) for row in column_rows if len(row) >= 2]
    forbidden_columns = sorted(column for column in columns if any(token in column.lower() for token in FORBIDDEN_COLUMN_TOKENS))
    candidate_summary_row = candidate_summary[0] if candidate_summary else []
    exact_summary_row = exact_summary[0] if exact_summary else []
    pairs = {(str(row[1]), str(row[2])) for row in candidate_rows if len(row) >= 3}
    normalized_pairs = {tuple(sorted(pair)) for pair in pairs}
    golden_pair = tuple(sorted(("T2-P-CIPHER-A", "T2-P-CIPHER-B")))
    hard_negative_pair = tuple(sorted(("T2-P-CIPHER-A", "T2-P-CYPHER")))
    active_snapshot = str(publication_rows[0][2]) if len(publication_rows) == 1 and len(publication_rows[0]) >= 3 else None
    candidate_entity_types = [str(row[3]).upper() for row in candidate_rows if len(row) >= 4]
    candidate_snapshots = [str(row[8]) for row in candidate_rows if len(row) >= 9]
    exact_relationship_types = [str(row[1]).upper() for row in exact_rows if len(row) >= 2]
    exact_snapshots = [str(row[6]) for row in exact_rows if len(row) >= 7]
    candidate_ids = [str(row[0]) for row in candidate_rows if len(row) >= 1]
    candidate_bands = [str(row[4]).upper() for row in candidate_rows if len(row) >= 5]
    candidate_generation_modes = [str(row[6]) for row in candidate_rows if len(row) >= 7]
    candidate_frameworks = [str(row[7]) for row in candidate_rows if len(row) >= 8]
    candidate_engine_flags = [str(row[5]).lower() for row in candidate_rows if len(row) >= 6]
    exact_engine_flags = [str(row[5]).lower() for row in exact_rows if len(row) >= 6]
    checks = {
        "one_active_publication": len(publication_rows) == 1,
        "candidate_rows": len(candidate_summary_row) >= 3 and int(candidate_summary_row[0]) == 2,
        "candidate_ids_unique": len(candidate_summary_row) >= 3 and int(candidate_summary_row[1]) == 2,
        "candidate_ids_nonempty": bool(candidate_ids) and all(candidate_ids),
        "candidate_bands_supported": bool(candidate_bands) and all(band in {"HIGH", "MEDIUM", "LOW"} for band in candidate_bands),
        "candidate_one_snapshot": len(candidate_summary_row) >= 3 and int(candidate_summary_row[2]) == 1,
        "candidate_snapshot_matches_publication": active_snapshot is not None and bool(candidate_snapshots) and all(snapshot == active_snapshot for snapshot in candidate_snapshots),
        "candidate_entities_are_person": bool(candidate_entity_types) and all(entity_type == "PERSON" for entity_type in candidate_entity_types),
        "candidate_generation_is_explicit": bool(candidate_generation_modes) and all(candidate_generation_modes),
        "candidate_framework_is_explicit": bool(candidate_frameworks) and all(candidate_frameworks),
        "golden_pair_present": golden_pair in normalized_pairs,
        "hard_negative_present": hard_negative_pair in normalized_pairs,
        "exact_rows": len(exact_summary_row) >= 3 and int(exact_summary_row[0]) == 5,
        "exact_ids_unique": len(exact_summary_row) >= 3 and int(exact_summary_row[1]) == 5,
        "exact_one_snapshot": len(exact_summary_row) >= 3 and int(exact_summary_row[2]) == 1,
        "exact_snapshot_matches_publication": active_snapshot is not None and bool(exact_snapshots) and all(snapshot == active_snapshot for snapshot in exact_snapshots),
        "exact_relationships_are_associations": bool(exact_relationship_types) and all("IDENTITY" not in relationship_type for relationship_type in exact_relationship_types),
        "no_candidate_zingg_claim": all(flag == "false" for flag in candidate_engine_flags),
        "no_exact_engine_claim": all(flag == "false" for flag in exact_engine_flags),
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
        "candidate_summary": candidate_summary_row,
        "candidate_pairs": candidate_rows,
        "exact_summary": exact_summary_row,
        "exact_rows": exact_rows,
        "observed_columns": columns,
        "forbidden_columns": forbidden_columns,
        "runtime_probe": runtime_rows,
        "zingg_compatibility": {
            "status": "UNRESOLVED_SQL_WAREHOUSE_ONLY",
            "actual_zingg_run": False,
            "reason": "The fga profile reaches a SQL Warehouse; no cluster library installation or Zingg job was requested or performed.",
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
    except Exception as exc:  # the receipt is still useful when the external warehouse is unavailable
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
