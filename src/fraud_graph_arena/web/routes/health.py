from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

from fraud_graph_arena.web.api_models import LiveHealthResponse, ReadyHealthResponse, VersionResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=LiveHealthResponse)
def live() -> LiveHealthResponse:
    return LiveHealthResponse()


@router.get("/ready", response_model=ReadyHealthResponse)
def ready(request: Request, response: Response) -> ReadyHealthResponse:
    repository_ready = request.app.state.container.round_repository.is_ready()
    frontend_ready = True
    settings = request.app.state.container.settings
    if settings.environment == "production":
        frontend_ready = settings.frontend_dist.is_dir() and (settings.frontend_dist / "index.html").is_file()
    if not repository_ready or not frontend_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadyHealthResponse(
        status="ready" if repository_ready and frontend_ready else "not_ready",
        checks={"round_repository": "ready" if repository_ready else "unavailable", "frontend_distribution": "ready" if frontend_ready else "unavailable"},
    )


@router.get("/version", response_model=VersionResponse)
def version(request: Request) -> VersionResponse:
    settings = request.app.state.container.settings
    return VersionResponse(
        build_version=settings.build_version,
        contract_version=settings.contract_version,
        runtime_role=settings.runtime_role.value,
        environment=settings.environment,
    )
