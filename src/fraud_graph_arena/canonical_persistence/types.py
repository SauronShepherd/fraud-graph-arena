from __future__ import annotations
from fraud_graph_arena.case_data.registry import load_typed_registry
from fraud_graph_arena.case_data.types import coerce_sql_value

def coerce_row(row: dict[str, str], path: str, *, require_complete: bool = True) -> dict:
    """Return storage-ready values using the authoritative column registry."""
    specs = {column["name"]: column for column in load_typed_registry()[path]["columns"]}
    unknown = set(row) - set(specs)
    if unknown: raise ValueError(f"{path}: unknown columns: {sorted(unknown)}")
    result = {}
    for field, value in row.items():
        try: result[field] = coerce_sql_value(value, specs[field]["sql_type"], f"{path}.{field}")
        except ValueError:
            raise
    if require_complete:
        missing = [field for field, spec in specs.items() if not spec["nullable"] and result.get(field) is None]
        if missing: raise ValueError(f"{path}: missing non-nullable fields: {','.join(missing)}")
    return result

def validate_row_types(row: dict[str, str], path: str) -> None:
    coerce_row(row, path)
