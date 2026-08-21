"""Candidate validation independent of publication activation."""
from __future__ import annotations
import json
from .identity import semantic_hash
from .registry import PHYSICAL_TARGETS

class CandidateValidationError(ValueError): pass

def validate_candidate(rows: dict[str, list[dict]], *, case_id: str, snapshot_version: str) -> str:
    if set(rows) != set(PHYSICAL_TARGETS):
        raise CandidateValidationError("candidate does not contain exactly the canonical registry set")
    for path, values in rows.items():
        for row in values:
            if row.get("case_id") not in (None, case_id):
                raise CandidateValidationError(f"case mismatch in {path}")
            if row.get("snapshot_version") not in (None, snapshot_version):
                raise CandidateValidationError(f"snapshot mismatch in {path}")
        # A persisted candidate must not contain duplicate complete rows.
        if len(values) != len({json.dumps(item, sort_keys=True, ensure_ascii=False) for item in values}):
            raise CandidateValidationError(f"duplicate candidate rows in {path}")
    return semantic_hash(rows)
