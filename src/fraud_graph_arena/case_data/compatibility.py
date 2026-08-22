"""Cross-package compatibility checks against the canonical registry."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .registry import TABLE_PATHS, headers, MODEL_VERSION


@dataclass(frozen=True)
class CompatibilityReport:
    compatible: bool
    model_version: str
    missing_tables: tuple[str, ...] = ()
    extra_tables: tuple[str, ...] = ()
    header_mismatches: tuple[str, ...] = ()


def compare_package_tables(root: Path, *, model_version: str = MODEL_VERSION) -> CompatibilityReport:
    root = Path(root)
    expected = set(TABLE_PATHS)
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*.csv")}
    missing = tuple(sorted(expected - actual))
    extra = tuple(sorted(actual - expected))
    mismatches: list[str] = []
    for table in sorted(expected & actual):
        with (root / table).open(encoding="utf-8", newline="") as handle:
            line = handle.readline().rstrip("\r\n")
        if tuple(line.split(",")) != headers(table):
            mismatches.append(table)
    return CompatibilityReport(
        compatible=model_version == MODEL_VERSION and not (missing or extra or mismatches),
        model_version=model_version,
        missing_tables=missing,
        extra_tables=extra,
        header_mismatches=tuple(mismatches),
    )
