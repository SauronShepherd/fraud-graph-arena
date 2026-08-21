"""Closed canonical import planning; package paths never determine targets."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from .registry import PHYSICAL_TARGETS, validate_registry

@dataclass(frozen=True)
class DatasetPlan:
    canonical_path: str
    physical_target: str
    layer: str

def build_plan(paths: list[str] | tuple[str, ...] | None = None) -> tuple[DatasetPlan, ...]:
    validate_registry()
    requested = set(paths if paths is not None else PHYSICAL_TARGETS)
    unknown = requested - set(PHYSICAL_TARGETS)
    if unknown:
        raise ValueError(f"unexpected canonical paths: {sorted(unknown)}")
    return tuple(DatasetPlan(p, PHYSICAL_TARGETS[p], p.split("/", 1)[0]) for p in PHYSICAL_TARGETS if p in requested)

def reject_dynamic_path(path: str | Path) -> None:
    if str(path).replace("\\", "/") not in PHYSICAL_TARGETS:
        raise ValueError("path is not an approved canonical registry path")

