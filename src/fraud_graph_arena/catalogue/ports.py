from __future__ import annotations

from typing import Protocol

from fraud_graph_arena.catalogue.domain import CaseSummary, CatalogueSection, PathDefinition, PathId


class CatalogueRepository(Protocol):
    def list_paths(self) -> tuple[PathDefinition, ...]: ...

    def get_section(self, path_id: PathId) -> CatalogueSection | None: ...

    def get_case(self, case_id: str, version: str | None = None) -> CaseSummary | None: ...
