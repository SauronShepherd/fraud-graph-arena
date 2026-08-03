from __future__ import annotations

from fraud_graph_arena.catalogue.domain import (
    CaseSummary,
    CatalogueSection,
    PathDefinition,
    PathId,
    PathStatus,
)
from fraud_graph_arena.catalogue.ports import CatalogueRepository
from fraud_graph_arena.shared.errors import ConflictError, InvalidRequestError, NotFoundError


class CatalogueService:
    def __init__(self, repository: CatalogueRepository) -> None:
        self._repository = repository

    def list_paths(self) -> tuple[PathDefinition, ...]:
        return self._repository.list_paths()

    def list_cases(self) -> tuple[CaseSummary, ...]:
        cases: list[CaseSummary] = []
        for path in self.list_paths():
            section = self._repository.get_section(path.id)
            if section is not None:
                cases.extend(section.cases)
        return tuple(cases)

    def get_section(self, raw_path_id: str) -> CatalogueSection:
        try:
            path_id = PathId(raw_path_id.strip().upper())
        except ValueError as exc:
            raise InvalidRequestError(
                code="INVALID_PATH_ID",
                title="Invalid path identifier",
                detail=f"'{raw_path_id}' is not a recognised investigation path.",
                recovery="Refresh the path catalogue and choose one of the returned identifiers.",
            ) from exc
        section = self._repository.get_section(path_id)
        if section is None:
            raise NotFoundError(
                code="PATH_NOT_FOUND",
                title="Path not found",
                detail=f"Path '{path_id}' is not available.",
            )
        return section

    def require_case_for_path(
        self,
        *,
        raw_path_id: str,
        case_id: str,
        case_version: str | None = None,
    ) -> CaseSummary:
        section = self.get_section(raw_path_id)
        if section.path.status != PathStatus.OPEN:
            raise ConflictError(
                code="PATH_NOT_OPEN",
                title="Path is not open",
                detail=f"Path '{section.path.id}' cannot start a new investigation yet.",
                recovery=section.path.access_message,
            )
        case = self._repository.get_case(case_id, case_version)
        if case is None:
            raise NotFoundError(
                code="CASE_NOT_FOUND",
                title="Case not found",
                detail=(
                    f"Case '{case_id}'"
                    + (f" version '{case_version}'" if case_version else "")
                    + " does not exist in the catalogue."
                ),
            )
        if case.path_id != section.path.id:
            raise InvalidRequestError(
                code="CASE_PATH_MISMATCH",
                title="Case does not belong to path",
                detail=f"Case '{case.id}' is not part of path '{section.path.id}'.",
                recovery="Refresh the selected path catalogue before opening a case.",
            )
        return case
