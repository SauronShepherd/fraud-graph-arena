"""Candidate validation independent of publication activation."""
from __future__ import annotations
import json
from .identity import semantic_hash
from .registry import PHYSICAL_TARGETS
from fraud_graph_arena.case_data.registry import load_typed_registry

class CandidateValidationError(ValueError): pass

def validate_candidate(rows: dict[str, list[dict]], *, case_id: str, snapshot_version: str) -> str:
    if set(rows) != set(PHYSICAL_TARGETS):
        raise CandidateValidationError("candidate does not contain exactly the canonical registry set")
    typed_registry = load_typed_registry(include_references=True)
    for path, values in rows.items():
        for row in values:
            if row.get("case_id") not in (None, case_id):
                raise CandidateValidationError(f"case mismatch in {path}")
            row_snapshot = row.get("snapshot_version")
            if row_snapshot not in (None, snapshot_version) and not str(row_snapshot).startswith(f"{snapshot_version}-"):
                raise CandidateValidationError(f"snapshot mismatch in {path}")
        # A persisted candidate must not contain duplicate complete rows.
        if len(values) != len({json.dumps(item, sort_keys=True, ensure_ascii=False, default=lambda value: value.isoformat().replace("+00:00", "Z") if hasattr(value, "isoformat") else str(value)) for item in values}):
            raise CandidateValidationError(f"duplicate candidate rows in {path}")
        primary_key = typed_registry[path].get("primary_key", [])
        if primary_key:
            keys = [tuple(row.get(column) for column in primary_key) for row in values]
            if len(keys) != len(set(keys)):
                raise CandidateValidationError(f"duplicate primary key in {path}")
    identities: dict[tuple[str, str], set[object]] = {}
    for path, values in rows.items():
        for column in typed_registry[path].get("columns", []):
            name = column["name"]
            if name.endswith("_id"):
                identities[(path, name)] = {item.get(name) for item in values if item.get(name) is not None}
    for path, values in rows.items():
        for rule in typed_registry[path].get("references", []):
            source_column = rule["column"]
            targets = identities.get((rule["to"], rule["target_column"]), set())
            for row in values:
                value = row.get(source_column)
                if value is None or value in targets:
                    continue
                if (path == "authoring/relationships.csv" and source_column == "target_record_id"
                        and row.get("relationship_type") == "MENTIONS" and str(value).startswith("CE-")):
                    continue
                raise CandidateValidationError(f"foreign key {source_column} missing in {path}")
    return semantic_hash(rows)
