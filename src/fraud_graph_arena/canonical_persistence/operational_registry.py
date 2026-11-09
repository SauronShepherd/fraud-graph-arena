"""Single executable registry for the five durable FGA-05 operational tables."""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

@lru_cache(maxsize=1)
def registry() -> dict[str, dict]:
    data = json.loads((ROOT / "contracts/canonical/v1/operational-registry.json").read_text(encoding="utf-8"))
    tables = data.get("tables", {})
    if set(tables) != {"fga_import_runs", "fga_import_run_files", "fga_import_run_datasets", "fga_import_publications", "fga_active_publications"}:
        raise ValueError("operational registry must contain exactly five tables")
    for name, table in tables.items():
        if not table.get("primary_key") or not set(table["primary_key"]).issubset(table.get("columns", {})):
            raise ValueError(f"invalid operational primary key: {name}")
    return tables

def columns(table: str) -> dict[str, str]:
    try: return dict(registry()[table]["columns"])
    except KeyError as exc: raise ValueError("unregistered operational table") from exc

def sql_types(table: str) -> tuple[str, ...]:
    return tuple(columns(table).values())

def ddl(table: str) -> str:
    definition = registry()[table]
    cols = ",\n  ".join(f"{name} {sql_type}" for name, sql_type in definition["columns"].items())
    return f"CREATE TABLE IF NOT EXISTS {table} (\n  {cols}\n) USING DELTA"
