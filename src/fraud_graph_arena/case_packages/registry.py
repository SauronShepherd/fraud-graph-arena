from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fraud_graph_arena.catalogue.domain import PathId
from fraud_graph_arena.paths import project_root

from .models import CasePackage


def _package_from_manifest(package_dir: Path) -> CasePackage:
    manifest_path = package_dir / "manifest.json"
    raw: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    return CasePackage(
        package_dir=package_dir,
        package_id=str(raw["package_id"]),
        schema_version=str(raw["schema_version"]),
        package_version=str(raw["package_version"]),
        case_id=str(raw["case_id"]),
        case_version=str(raw["case_version"]),
        path_id=PathId(str(raw["path_id"])),
        title=str(raw["title"]),
        description=str(raw["description"]),
        kind=str(raw["kind"]),
        briefing=dict(raw["briefing"]),
        canonical=None if raw.get("canonical") is None else dict(raw["canonical"]),
        objectives=tuple(str(item) for item in raw["objectives"]),
        supported_actions=tuple(str(item) for item in raw["supported_actions"]),
        economy=dict(raw["economy"]),
        evidence_rules=dict(raw["evidence_rules"]),
        scoring=dict(raw["scoring"]),
        assets=dict(raw["assets"]),
        compatibility=dict(raw["compatibility"]),
        publication=dict(raw["publication"]),
    )


class CasePackageRegistry:
    """Discover published case packages without case IDs in application branches."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or project_root() / "case-packages").resolve()
        self._packages = tuple(
            _package_from_manifest(directory)
            for directory in sorted(self.root.iterdir())
            if directory.is_dir() and (directory / "manifest.json").is_file()
        )
        self._by_key = {(item.case_id, item.case_version): item for item in self._packages}
        self._by_case_id = {item.case_id: item for item in self._packages}

    def all(self) -> tuple[CasePackage, ...]:
        return self._packages

    def published(self) -> tuple[CasePackage, ...]:
        return tuple(item for item in self._packages if item.is_published)

    def get(self, case_id: str, case_version: str | None = None) -> CasePackage | None:
        normalized = case_id.strip().upper()
        if case_version is not None:
            return self._by_key.get((normalized, case_version))
        return self._by_case_id.get(normalized)

    def require(self, case_id: str, case_version: str | None = None) -> CasePackage:
        package = self.get(case_id, case_version)
        if package is None:
            suffix = f" version '{case_version}'" if case_version else ""
            raise LookupError(f"case package '{case_id}'{suffix} was not discovered")
        return package
