"""Typed, lossless provenance helpers for canonical source records.

These helpers describe lineage only; they never claim that an engine executed
or that a source value is safe to publish.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


@dataclass(frozen=True)
class Provenance:
    source_system: str
    dataset: str
    record_key: str
    snapshot_version: str
    derivation: str = "DIRECT_SOURCE"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Provenance":
        required = ("source_system_id", "source_dataset", "source_record_key", "snapshot_version")
        missing = [key for key in required if str(row.get(key, "")).strip() == ""]
        if missing:
            raise ValueError(f"MISSING_PROVENANCE_FIELDS:{','.join(missing)}")
        return cls(
            source_system=str(row["source_system_id"]),
            dataset=str(row["source_dataset"]),
            record_key=str(row["source_record_key"]),
            snapshot_version=str(row["snapshot_version"]),
            derivation=str(row.get("generation_mode") or row.get("derivation") or "DIRECT_SOURCE"),
        )


def provenance_from_row(row: Mapping[str, Any]) -> Provenance:
    return Provenance.from_row(row)
