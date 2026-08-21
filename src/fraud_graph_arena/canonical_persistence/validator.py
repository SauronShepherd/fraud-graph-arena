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
    typed_registry = load_typed_registry()
    for path, values in rows.items():
        for row in values:
            if row.get("case_id") not in (None, case_id):
                raise CandidateValidationError(f"case mismatch in {path}")
            row_snapshot = row.get("snapshot_version")
            if row_snapshot not in (None, snapshot_version) and not str(row_snapshot).startswith(f"{snapshot_version}-"):
                raise CandidateValidationError(f"snapshot mismatch in {path}")
        # A persisted candidate must not contain duplicate complete rows.
        if len(values) != len({json.dumps(item, sort_keys=True, ensure_ascii=False) for item in values}):
            raise CandidateValidationError(f"duplicate candidate rows in {path}")
        primary_key = typed_registry[path].get("primary_key", [])
        if primary_key:
            keys = [tuple(row.get(column) for column in primary_key) for row in values]
            if len(keys) != len(set(keys)):
                raise CandidateValidationError(f"duplicate primary key in {path}")
    record_ids = {row.get("record_id") for row in rows.get("authoring/records.csv", [])}
    for relationship in rows.get("authoring/relationships.csv", []):
        for field in ("source_record_id", "target_record_id"):
            value = relationship.get(field)
            if value and value not in record_ids:
                raise CandidateValidationError(f"foreign key {field} missing in authoring/relationships.csv")
    return semantic_hash(rows)
