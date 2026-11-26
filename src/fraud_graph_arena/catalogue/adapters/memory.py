from __future__ import annotations

from fraud_graph_arena.catalogue.domain import (
    CaseStatus,
    CaseSummary,
    CatalogueSection,
    PathDefinition,
    PathId,
    PathStatus,
)
from fraud_graph_arena.case_packages import CasePackage, CasePackageRegistry


class InMemoryCatalogueRepository:
    """Deterministic catalogue backed by the published FGA-13 packages.

    The same repository and round engine serve Academy, Puppy, Adult Dog and
    Senior Dog.  Path access is catalogue state; case difficulty lives in each
    package and is never inferred from the number of graph rows.
    """

    def __init__(self, package_registry: CasePackageRegistry | None = None) -> None:
        self.package_registry = package_registry or CasePackageRegistry()
        self._paths = (
            PathDefinition(
                id=PathId.DETECTIVE_ACADEMY,
                name="Detective Academy",
                description="The unranked training route where every mechanic can be learned safely.",
                ranked=False,
                status=PathStatus.OPEN,
                access_message="Academy doors are open. No real-case spoilers beyond this point.",
            ),
            PathDefinition(
                id=PathId.PUPPY,
                name="Puppy",
                description="The first ranked trail: the full loop with room to learn.",
                ranked=True,
                status=PathStatus.OPEN,
                access_message="Puppy cases are open. Learn the loop, then question the shortcut.",
            ),
            PathDefinition(
                id=PathId.ADULT_DOG,
                name="Adult Dog",
                description="Organisational complexity, incomplete evidence and resource trade-offs.",
                ranked=True,
                status=PathStatus.OPEN,
                access_message="Adult Dog cases are open. Mixed roles and polished paperwork await.",
            ),
            PathDefinition(
                id=PathId.SENIOR_DOG,
                name="Senior Dog",
                description="Temporal, identity and role ambiguity with legitimate alternatives.",
                ranked=True,
                status=PathStatus.OPEN,
                access_message="Senior Dog cases are open. The obvious story is only a lead.",
            ),
        )
        self._cases = tuple(package.summary() for package in self.package_registry.published())

    def list_paths(self) -> tuple[PathDefinition, ...]:
        return self._paths

    def get_section(self, path_id: PathId) -> CatalogueSection | None:
        path = next((item for item in self._paths if item.id == path_id), None)
        if path is None:
            return None
        cases = tuple(item for item in self._cases if item.path_id == path_id)
        return CatalogueSection(path=path, cases=cases)

    def get_case(self, case_id: str, version: str | None = None) -> CaseSummary | None:
        normalized = case_id.strip().upper()
        return next(
            (
                item
                for item in self._cases
                if item.id == normalized and (version is None or item.version == version)
            ),
            None,
        )

    def get_package(self, case_id: str, version: str | None = None) -> CasePackage | None:
        return self.package_registry.get(case_id, version)
