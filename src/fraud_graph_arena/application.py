from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fraud_graph_arena.catalogue.adapters.memory import InMemoryCatalogueRepository
from fraud_graph_arena.catalogue.service import CatalogueService
from fraud_graph_arena.case_packages import CasePackage
from fraud_graph_arena.config import RuntimeRole, Settings
from fraud_graph_arena.investigation_commands.adapters.memory import InMemoryInvestigationCommandRepository
from fraud_graph_arena.investigation_commands.adapters.sqlite import SqliteInvestigationCommandRepository
from fraud_graph_arena.investigation_commands.ports import InvestigationCommandRepository
from fraud_graph_arena.investigation_commands.service import InvestigationCommandService
from fraud_graph_arena.narrative.adapters.memory import InMemoryNarrativeRepository
from fraud_graph_arena.narrative.service import NarrativeService
from fraud_graph_arena.rounds.adapters.memory import InMemoryRoundRepository
from fraud_graph_arena.rounds.adapters.sqlite import SqliteRoundRepository
from fraud_graph_arena.rounds.domain import Round
from fraud_graph_arena.rounds.ports import RoundRepository
from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.web.problem_handlers import register_problem_handlers
from fraud_graph_arena.web.routes import catalogue, health, rounds
from fraud_graph_arena.web.spa import SpaStaticFiles
from fraud_graph_arena.workspace import WorkspaceService
from fraud_graph_arena.workspace.graph_service import GraphInvestigationService
from fraud_graph_arena.entity_resolution import (
    EntityResolutionService,
    InMemoryEntityResolutionRepository,
    SqliteEntityResolutionRepository,
)
from fraud_graph_arena.graph_analytics import GraphAnalyticsService
from fraud_graph_arena.economy import EconomyService, InMemoryLedgerRepository, SqliteLedgerRepository
from fraud_graph_arena.case_resolution import CaseResolutionService, InMemorySubmissionRepository, SqliteSubmissionRepository


@dataclass(slots=True)
class Container:
    settings: Settings
    catalogue: CatalogueService
    narrative: NarrativeService
    rounds: RoundService
    round_repository: RoundRepository
    workspace: WorkspaceService
    graph: GraphInvestigationService
    investigation_commands: InvestigationCommandService
    entity_resolution: EntityResolutionService
    graph_analytics: GraphAnalyticsService
    economy: EconomyService
    case_resolution: CaseResolutionService


def build_web_container(settings: Settings) -> Container:
    if settings.runtime_role != RuntimeRole.WEB:
        raise RuntimeError("the public container is only valid for WEB runtime role")
    catalogue_repository = InMemoryCatalogueRepository()
    catalogue = CatalogueService(catalogue_repository)
    narrative = NarrativeService(InMemoryNarrativeRepository(catalogue_repository.package_registry))
    for case in catalogue.list_cases():
        narrative.validate_case(case)

    round_repository: RoundRepository
    if settings.round_repository == "memory":
        round_repository = InMemoryRoundRepository()
    else:
        round_repository = SqliteRoundRepository(settings.sqlite_path)
    round_service = RoundService(
        repository=round_repository,
        catalogue=catalogue,
        narrative=narrative,
    )
    def package_for_round(round_: Round) -> CasePackage | None:
        return catalogue.get_package(round_.case_id, round_.case_version)

    def package_cost(round_id: str, action: str) -> int | None:
        package = package_for_round(round_service.require(round_id))
        return None if package is None else package.economy.get("costs", {}).get(action)

    ledger_repository = InMemoryLedgerRepository() if settings.round_repository == "memory" else SqliteLedgerRepository(settings.sqlite_path)
    economy = EconomyService(
        round_service,
        ledger_repository,
        cost_provider=package_cost,
    )
    entity_repository = (
        InMemoryEntityResolutionRepository()
        if settings.round_repository == "memory"
        else SqliteEntityResolutionRepository(settings.sqlite_path)
    )
    entity_resolution = EntityResolutionService(round_service, entity_repository, economy=economy, package_provider=package_for_round)

    def graph_provider(round_id: str) -> dict:
        round_ = round_service.require(round_id)
        package = package_for_round(round_)
        graph = package.graph() if package is not None else {"nodes": (), "edges": (), "node_count": 0, "edge_count": 0, "projection_version": "empty"}
        return entity_resolution.graph_with_reviews(round_id, graph) if package is not None and package.supports("COMPARE_IDENTITIES") else graph

    command_repository: InvestigationCommandRepository
    if settings.round_repository == "memory":
        command_repository = InMemoryInvestigationCommandRepository()
    else:
        command_repository = SqliteInvestigationCommandRepository(settings.sqlite_path)

    submission_repository = InMemorySubmissionRepository() if settings.round_repository == "memory" else SqliteSubmissionRepository(settings.sqlite_path)
    return Container(
        settings=settings,
        catalogue=catalogue,
        narrative=narrative,
        rounds=round_service,
        round_repository=round_repository,
        workspace=WorkspaceService(round_service, catalogue, graph_provider=graph_provider),
        graph=GraphInvestigationService(graph_provider),
        investigation_commands=InvestigationCommandService(round_service, command_repository),
        entity_resolution=entity_resolution,
        graph_analytics=GraphAnalyticsService(round_service, graph_provider, economy=economy, package_provider=package_for_round),
        economy=economy,
        case_resolution=CaseResolutionService(round_service, economy, submission_repository, package_provider=package_for_round),
    )


def build_container(settings: Settings) -> Container:
    """Compatibility entry point for existing I01 tests and integrations."""
    return build_web_container(settings)


def create_app(
    settings: Settings | None = None,
    *,
    container: Container | None = None,
) -> FastAPI:
    resolved_settings = settings or Settings()
    if resolved_settings.runtime_role != RuntimeRole.WEB:
        raise RuntimeError(f"create_app is only available for WEB runtime role, got {resolved_settings.runtime_role.value}")
    resolved_container = container or build_web_container(resolved_settings)

    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.build_version,
        docs_url=f"{resolved_settings.api_prefix}/docs",
        openapi_url=f"{resolved_settings.api_prefix}/openapi.json",
        redoc_url=None,
    )
    app.state.container = resolved_container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Correlation-ID"],
        expose_headers=["X-Correlation-ID"],
    )

    @app.middleware("http")
    async def attach_correlation_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        supplied = request.headers.get("X-Correlation-ID", "").strip()
        request.state.correlation_id = supplied[:128] if supplied else str(uuid4())
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = request.state.correlation_id
        return response

    register_problem_handlers(app)
    for router in (health.router, catalogue.router, rounds.router):
        app.include_router(router, prefix=resolved_settings.api_prefix)

    frontend_dist = Path(resolved_settings.frontend_dist)
    if frontend_dist.is_dir():
        app.mount("/", SpaStaticFiles(directory=frontend_dist, html=True), name="frontend")

    return app
