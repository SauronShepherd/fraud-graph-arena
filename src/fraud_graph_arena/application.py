from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fraud_graph_arena.catalogue.adapters.memory import InMemoryCatalogueRepository
from fraud_graph_arena.catalogue.service import CatalogueService
from fraud_graph_arena.academy import ScenarioRegistry
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
from fraud_graph_arena.web.routes import academy, catalogue, health, rounds
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
from fraud_graph_arena.case_data.graph_investigation import MAX_GRAPH_EDGES, MAX_GRAPH_NODES, initial_subset
from fraud_graph_arena.observability import ObservabilityRecorder
from fraud_graph_arena.release_engineering.runtime import load_runtime_context


_UUID_PATH_SEGMENT = re.compile(r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?=/|$)", re.IGNORECASE)
_SAFE_HEADER_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def _safe_route(path: str) -> str:
    return _UUID_PATH_SEGMENT.sub("/:id", path)


def _safe_header_id(value: str) -> str:
    lowered = value.lower()
    suspicious = ("token", "secret", "bearer", "password", "credential", "email")
    return value if _SAFE_HEADER_ID.fullmatch(value) and not any(marker in lowered for marker in suspicious) else str(uuid4())


@dataclass(slots=True)
class Container:
    settings: Settings
    academy: ScenarioRegistry
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
    academy_registry = ScenarioRegistry()
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
        release_context=load_runtime_context(),
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
        if package is None or package.kind != "canonical":
            return graph
        authorized = entity_resolution.graph_with_reviews(round_id, graph) if package.supports("COMPARE_IDENTITIES") else graph
        # The package owns the learning-sized initial view; the API retains the
        # renderer hard ceiling.  The omitted counts make truncation explicit.
        limit = min(package.difficulty_profile.graph_node_limit, MAX_GRAPH_NODES)
        return initial_subset(authorized, limit=limit, edge_limit=MAX_GRAPH_EDGES)

    command_repository: InvestigationCommandRepository
    if settings.round_repository == "memory":
        command_repository = InMemoryInvestigationCommandRepository()
    else:
        command_repository = SqliteInvestigationCommandRepository(settings.sqlite_path)

    submission_repository = InMemorySubmissionRepository() if settings.round_repository == "memory" else SqliteSubmissionRepository(settings.sqlite_path)
    return Container(
        settings=settings,
        academy=academy_registry,
        catalogue=catalogue,
        narrative=narrative,
        rounds=round_service,
        round_repository=round_repository,
        workspace=WorkspaceService(round_service, catalogue, graph_provider=graph_provider),
        graph=GraphInvestigationService(graph_provider),
        investigation_commands=InvestigationCommandService(
            round_service,
            command_repository,
            package_provider=package_for_round,
        ),
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
    app.state.observability = ObservabilityRecorder(
        resolved_settings.instrumentation_config,
        log_level=resolved_settings.log_level,
        enabled=resolved_settings.observability_enabled,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Correlation-ID", "X-Trace-ID"],
        expose_headers=["X-Correlation-ID", "X-Trace-ID"],
    )

    @app.middleware("http")
    async def attach_correlation_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        supplied = request.headers.get("X-Correlation-ID", "").strip()
        request_id = _safe_header_id(supplied) if supplied else str(uuid4())
        trace = request.headers.get("X-Trace-ID", "").strip()
        trace_id = _safe_header_id(trace) if trace else str(uuid4())
        request.state.correlation_id = request_id
        request.state.trace_id = trace_id
        observability = app.state.observability
        with observability.request_context(request_id, trace_id):
            with observability.span(
                "http.request",
                {"http_method": request.method, "route": _safe_route(request.url.path)},
            ) as span:
                response = await call_next(request)
                span["status"] = "error" if response.status_code >= 400 else "ok"
                span["result"] = {"http_status": response.status_code}
        response.headers["X-Correlation-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        return response

    register_problem_handlers(app)
    for router in (health.router, academy.router, catalogue.router, rounds.router):
        app.include_router(router, prefix=resolved_settings.api_prefix)

    frontend_dist = Path(resolved_settings.frontend_dist)
    if frontend_dist.is_dir():
        app.mount("/", SpaStaticFiles(directory=frontend_dist, html=True), name="frontend")

    return app
