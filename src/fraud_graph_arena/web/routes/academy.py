from __future__ import annotations

from fastapi import APIRouter, Request

from fraud_graph_arena.web.api_models import AcademyCurriculumResponse


router = APIRouter(prefix="/academy", tags=["academy"])


@router.get("/curriculum", response_model=AcademyCurriculumResponse)
def curriculum(request: Request) -> AcademyCurriculumResponse:
    return AcademyCurriculumResponse.model_validate(request.app.state.container.academy.public_curriculum())
