"""Small, allowlisted Databricks SQL adapter used by qualification scripts."""
from __future__ import annotations
import json
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Sequence
from .registry import expected_topology

class DatabricksWarehouseError(RuntimeError): pass

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

    def select(self, columns: Sequence[str], table: str, predicate: str | None = None) -> dict[str, Any]:
        projection = ", ".join(columns)
        statement = f"SELECT {projection} FROM {self.qualify_table(table)}"
        if predicate: statement += f" WHERE {predicate}"
        return self.execute(statement)
