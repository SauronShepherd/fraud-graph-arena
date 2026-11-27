from __future__ import annotations

from fastapi import APIRouter, Request

from fraud_graph_arena.web.api_models import CatalogueSectionResponse, CatalogueSectionsResponse
from fraud_graph_arena.web.mappers import map_path, map_section

router = APIRouter(prefix="/catalogue", tags=["catalogue"])


@router.get("/sections", response_model=CatalogueSectionsResponse)
def list_sections(request: Request) -> CatalogueSectionsResponse:
    paths = request.app.state.container.catalogue.list_paths()
    return CatalogueSectionsResponse(sections=[map_path(item) for item in paths])


@router.get("/{section}", response_model=CatalogueSectionResponse)
def get_section(section: str, request: Request) -> CatalogueSectionResponse:
    value = request.app.state.container.catalogue.get_section(section)
    curriculum = request.app.state.container.academy.public_curriculum() if str(value.path.id) == "DETECTIVE_ACADEMY" else None
    return map_section(value, academy_curriculum=curriculum)
