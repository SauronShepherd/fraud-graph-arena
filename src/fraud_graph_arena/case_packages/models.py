from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fraud_graph_arena.catalogue.domain import CaseSummary, CaseStatus, PathId
from fraud_graph_arena.case_data.graph_data import project_graph
from fraud_graph_arena.difficulty import DifficultyProfile


PACKAGE_SCHEMA_VERSION = "fga13-case-package-v1"


@dataclass(frozen=True, slots=True)
class CasePackage:
    """The declarative, versioned contract that selects reusable game mechanics."""

    package_dir: Path
    package_id: str
    schema_version: str
    package_version: str
    case_id: str
    case_version: str
    path_id: PathId
    title: str
    description: str
    kind: str
    briefing: dict[str, str]
    canonical: dict[str, str] | None
    objectives: tuple[str, ...]
    supported_actions: tuple[str, ...]
    economy: dict[str, Any]
    evidence_rules: dict[str, str]
    scoring: dict[str, Any]
    assets: dict[str, str]
    difficulty_profile: DifficultyProfile
    compatibility: dict[str, str]
    publication: dict[str, Any]
    narrative: dict[str, Any] = field(default_factory=dict)

    @property
    def initial_credits(self) -> int:
        return int(self.economy["initial_credits"])

    @property
    def economy_version(self) -> str:
        return str(self.economy["version"])

    @property
    def scoring_version(self) -> str:
        return str(self.scoring["version"])

    @property
    def canonical_root(self) -> Path | None:
        if self.canonical is None:
            return None
        return (self.package_dir.parent.parent / self.canonical["root"]).resolve()

    @property
    def is_published(self) -> bool:
        return self.publication.get("state") == "PUBLISHED"

    def supports(self, action: str) -> bool:
        return action in self.supported_actions

    def summary(self) -> CaseSummary:
        return CaseSummary(
            id=self.case_id,
            version=self.case_version,
            path_id=self.path_id,
            name=self.title,
            description=self.description,
            status=CaseStatus.OPEN if self.is_published else CaseStatus.LOCKED,
        )

    def rows(self, relative_path: str) -> list[dict[str, str]]:
        import csv

        root = self.canonical_root
        if root is None:
            return []
        candidate = (root / relative_path).resolve()
        if root not in candidate.parents:
            raise ValueError("case package path escapes its canonical root")
        with candidate.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def graph(self) -> dict[str, Any]:
        records = self.rows("published/records.csv")
        relationships = self.rows("published/relationships.csv")
        if not records:
            return {"projection_version": "empty", "snapshot_version": "empty", "nodes": (), "edges": (), "node_count": 0, "edge_count": 0}
        snapshots = {row.get("snapshot_version") for row in records + relationships}
        if len(snapshots) != 1 or None in snapshots:
            raise ValueError(f"case {self.case_id} must expose one complete published snapshot")
        return {**project_graph(records, relationships), "snapshot_version": next(iter(snapshots))}
