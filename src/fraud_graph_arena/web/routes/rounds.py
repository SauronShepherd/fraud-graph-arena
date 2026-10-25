from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status
from fraud_graph_arena.rounds.domain import IntroCompletion

from fraud_graph_arena.web.api_models import (
    CreateRoundRequest,
    IntroCompletionRequest,
    OpeningResponse,
    RoundResponse,
    WorkspaceResponse,
    GraphViewRequest, GraphExpandRequest, GraphFilterRequest, GraphResponse,
    HypothesisRequest, InvestigationCommandResponse, InvestigationCommandListResponse,
)
from fraud_graph_arena.web.mappers import map_opening, map_round, map_workspace

router = APIRouter(prefix="/rounds", tags=["rounds"])


@router.post("/{round_id}/investigations/hypotheses", response_model=InvestigationCommandResponse)
def submit_hypothesis(round_id: str, payload: HypothesisRequest, request: Request) -> InvestigationCommandResponse:
    command, created = request.app.state.container.investigation_commands.submit_hypothesis(
        round_id, payload.idempotency_key, payload.source_record_id, payload.target_record_id,
        payload.relationship_type,
    )
    return InvestigationCommandResponse(
        command_id=command.command_id, round_id=command.round_id, idempotency_key=command.idempotency_key,
        action=command.action, source_record_id=command.source_record_id, target_record_id=command.target_record_id,
        relationship_type=command.relationship_type, status=command.status, charged_credits=command.charged_credits,
        revealed_record_ids=list(command.revealed_record_ids), created_at=command.created_at, replayed=not created,
    )


@router.get("/{round_id}/investigations/history", response_model=InvestigationCommandListResponse)
def investigation_history(round_id: str, request: Request) -> InvestigationCommandListResponse:
    commands = request.app.state.container.investigation_commands.list_for_round(round_id)
    return InvestigationCommandListResponse(commands=[
        InvestigationCommandResponse(
            command_id=item.command_id, round_id=item.round_id, idempotency_key=item.idempotency_key,
            action=item.action, source_record_id=item.source_record_id, target_record_id=item.target_record_id,
            relationship_type=item.relationship_type, status=item.status, charged_credits=item.charged_credits,
            revealed_record_ids=list(item.revealed_record_ids), created_at=item.created_at,
        ) for item in commands
    ])


@router.post("", response_model=RoundResponse, status_code=status.HTTP_201_CREATED)
def create_round(payload: CreateRoundRequest, request: Request) -> RoundResponse:
    round_ = request.app.state.container.rounds.create(
        player_id=payload.player_id,
        path_id=payload.path_id,
        case_id=payload.case_id,
    )
    return map_round(round_)


@router.post("/{round_id}/start", response_model=RoundResponse)
def start_round(round_id: str, request: Request) -> RoundResponse:
    return map_round(request.app.state.container.rounds.start(round_id))


@router.get("/{round_id}/opening", response_model=OpeningResponse)
def opening(round_id: str, request: Request) -> OpeningResponse:
    return map_opening(request.app.state.container.rounds.opening(round_id))


@router.post("/{round_id}/opening/complete", response_model=RoundResponse)
def complete_opening(round_id: str, request: Request, payload: IntroCompletionRequest | None = None) -> RoundResponse:
    completion = payload.completion if payload else IntroCompletion.FINISHED
    return map_round(request.app.state.container.rounds.complete_opening(round_id, completion=completion))


@router.get("/{round_id}/workspace", response_model=WorkspaceResponse)
def workspace(round_id: str, request: Request) -> WorkspaceResponse:
    return map_workspace(request.app.state.container.workspace.get(round_id))

@router.post("/{round_id}/graph/initial", response_model=GraphResponse)
def initial_graph(round_id: str, request: Request, payload: GraphViewRequest | None = None) -> GraphResponse:
    body = payload or GraphViewRequest()
    return GraphResponse.model_validate(request.app.state.container.graph.initial(round_id, body.seeds, body.limit, body.edge_limit))

@router.post("/{round_id}/graph/expand", response_model=GraphResponse)
def expand_graph(round_id: str, request: Request, payload: GraphExpandRequest) -> GraphResponse:
    try:
        result = request.app.state.container.graph.expand(round_id, payload.visible.model_dump(), payload.node_id, payload.depth, payload.limit, payload.edge_limit)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail="graph expansion is limited to visible nodes") from error
    except KeyError as error:
        raise HTTPException(status_code=404, detail="graph node was not found") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return GraphResponse.model_validate(result)

@router.post("/{round_id}/graph/filter", response_model=GraphResponse)
def filter_graph(round_id: str, request: Request, payload: GraphFilterRequest) -> GraphResponse:
    try:
        result = request.app.state.container.graph.filter(round_id, payload.visible.model_dump(), payload.families)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail="graph filters must reference authorized visible records") from error
    return GraphResponse.model_validate(result)
