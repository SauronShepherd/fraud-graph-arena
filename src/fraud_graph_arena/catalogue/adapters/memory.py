from __future__ import annotations

from fraud_graph_arena.catalogue.domain import (
    CaseStatus,
    CaseSummary,
    CatalogueSection,
    PathDefinition,
    PathId,
    PathStatus,
)


class InMemoryCatalogueRepository:
    """Deterministic, spoiler-free Iteration-01 catalogue.

    Detective Academy is the only playable route. Ranked paths are visible through
    server-owned catalogue state, but no real anthology case names or details are
    published by the walking skeleton.
    """

    def __init__(self) -> None:
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
                description="The first ranked trail through the anthology.",
                ranked=True,
                status=PathStatus.COMING_SOON,
                access_message="Ranked cases remain sealed while the Academy is being built.",
            ),
            PathDefinition(
                id=PathId.ADULT_DOG,
                name="Adult Dog",
                description="A later ranked entry point for experienced investigators.",
                ranked=True,
                status=PathStatus.LOCKED,
                access_message="Complete the required ranked progression when the anthology opens.",
            ),
            PathDefinition(
                id=PathId.SENIOR_DOG,
                name="Senior Dog",
                description="The advanced ranked entry point. Trench coat not included.",
                ranked=True,
                status=PathStatus.LOCKED,
                access_message="Advanced entry remains locked until its release requirements exist.",
            ),
        )
        self._cases = (
            CaseSummary(
                id="ACADEMY_001",
                version="1.0.0-i01",
                path_id=PathId.DETECTIVE_ACADEMY,
                name="The Case of the Empty Evidence Board",
                description=(
                    "A spoiler-free training file whose only mystery is whether the application "
                    "can carry it safely from catalogue to board."
                ),
                status=CaseStatus.OPEN,
            ),
        )

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
