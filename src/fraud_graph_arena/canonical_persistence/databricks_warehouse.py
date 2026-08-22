"""Small, allowlisted Databricks SQL adapter used by qualification scripts."""
from __future__ import annotations
import json
import subprocess
import tempfile
import re
from datetime import date, datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Any, Sequence
from .registry import expected_topology, PHYSICAL_TARGETS, OPERATIONAL_TARGETS
from fraud_graph_arena.case_data.registry import headers
from fraud_graph_arena.canonical_persistence.types import coerce_row
from .operational_registry import columns as operational_columns

class DatabricksWarehouseError(RuntimeError): pass

def _literal(value: object) -> str:
    if value is None or value == "": return "NULL"
    if isinstance(value, bool): return "TRUE" if value else "FALSE"
    if isinstance(value, Decimal): return format(value, "f")
    if isinstance(value, date):
        if isinstance(value, datetime): return f"TIMESTAMP '{value.isoformat().replace('+00:00', 'Z')}'"
        return f"DATE '{value.isoformat()}'"
    return "'" + str(value).replace("'", "''") + "'"

@dataclass(frozen=True)
class DatabricksWarehouse:
    profile: str = "sda"
    warehouse_id: str = "e444f39962128242"
    catalog: str = "sda_dev"
    schema: str = "sandbox"
    wait_timeout: str = "50s"

    def qualify_table(self, table: str) -> str:
        if table not in expected_topology():
            raise ValueError(f"table is outside the closed persistence registry: {table}")
        return f"{self.catalog}.{self.schema}.{table}"

    def execute(self, statement: str) -> dict[str, Any]:
        payload = {"statement": statement, "warehouse_id": self.warehouse_id, "wait_timeout": self.wait_timeout, "catalog": self.catalog, "schema": self.schema}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(payload, handle); request_path = handle.name
        result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", self.profile, "--json", "@" + request_path], capture_output=True, text=True)
        if result.returncode:
            raise DatabricksWarehouseError(result.stderr.strip()[-512:])
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise DatabricksWarehouseError("Databricks returned invalid JSON") from exc
        if response.get("status", {}).get("state") == "FAILED":
            raise DatabricksWarehouseError(str(response.get("status", {}).get("error", "statement failed"))[-512:])
        return response

    def select(self, columns: Sequence[str], table: str, predicate: tuple[str, str, object] | None = None) -> dict[str, Any]:
        """Select registered columns with a structured, non-injectable predicate."""
        allowed = set(operational_columns(table)) if table in OPERATIONAL_TARGETS else set(headers(next(path for path, target in PHYSICAL_TARGETS.items() if target == table)))
        if any(column not in allowed or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", column) for column in columns):
            raise ValueError("projection contains an unregistered column")
        projection = ", ".join(columns)
        statement = f"SELECT {projection} FROM {self.qualify_table(table)}"
        if predicate:
            column, operator, value = predicate
            if column not in allowed or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", column):
                raise ValueError("predicate column is not registered")
            if operator not in {"=", "!=", "<>", "IS", "IS NOT"}:
                raise ValueError("predicate operator is not allowlisted")
            if operator in {"IS", "IS NOT"} and value is not None:
                raise ValueError("IS predicates only accept NULL")
            statement += f" WHERE {column} {operator} {_literal(value)}"
        return self.execute(statement)

    def insert_candidate(self, path: str, rows: Sequence[dict[str, Any]], publication_id: str, run_id: str) -> dict[str, Any]:
        """Insert rows only into a registry-resolved table with write-time metadata."""
        if path not in PHYSICAL_TARGETS: raise ValueError("canonical path is not registered")
        table = PHYSICAL_TARGETS[path]; columns = list(headers(path)) + ["_publication_id", "_load_run_id"]
        if not rows: return {"status": "skipped", "row_count": 0}
        values = []
        for raw_row in rows:
            row = coerce_row(dict(raw_row), path)
            values.append("(" + ", ".join([_literal(row.get(column)) for column in headers(path)] + [_literal(publication_id), _literal(run_id)]) + ")")
        return self.execute(f"INSERT INTO {self.qualify_table(table)} ({', '.join(columns)}) VALUES {', '.join(values)}")

    def validate_candidate(self, publication_id: str, run_id: str) -> list[dict[str, Any]]:
        queries = []
        for path, table in PHYSICAL_TARGETS.items():
            qualified = self.qualify_table(table)
            queries.extend([
                f"SELECT COUNT(*) AS rows, COUNT_IF(_publication_id = {_literal(publication_id)}) AS tagged, COUNT_IF(_load_run_id = {_literal(run_id)}) AS correlated FROM {qualified}",
                f"SELECT COUNT(*) AS missing_snapshot FROM {qualified} WHERE _publication_id = {_literal(publication_id)} AND snapshot_version IS NULL",
            ])
        return [self.execute(query) for query in queries]

    def cleanup_candidate(self, publication_id: str) -> list[dict[str, Any]]:
        return [self.execute(f"DELETE FROM {self.qualify_table(table)} WHERE _publication_id = {_literal(publication_id)}") for table in PHYSICAL_TARGETS.values()]

    def activate_publication(self, case_id: str, case_version: str, snapshot_version: str, model_version: str, publication_id: str, run_id: str) -> dict[str, Any]:
        table = self.qualify_table("fga_active_publications")
        values = ", ".join((_literal(case_id), _literal(case_version), _literal(snapshot_version), _literal(model_version), _literal(publication_id), "current_timestamp()", _literal(run_id)))
        return self.execute(f"MERGE INTO {table} AS target USING (SELECT {values}) AS source ON target.case_id = source.case_id AND target.case_version = source.case_version WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *")
