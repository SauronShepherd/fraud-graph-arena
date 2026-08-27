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
)
from fraud_graph_arena.web.mappers import map_opening, map_round, map_workspace

router = APIRouter(prefix="/rounds", tags=["rounds"])


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
    return GraphResponse.model_validate(request.app.state.container.graph.initial(round_id, body.seeds, body.limit))

@router.post("/{round_id}/graph/expand", response_model=GraphResponse)
def expand_graph(round_id: str, request: Request, payload: GraphExpandRequest) -> GraphResponse:
    try:
        result = request.app.state.container.graph.expand(round_id, payload.visible.model_dump(), payload.node_id, payload.depth, payload.limit)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail="graph expansion is limited to visible nodes") from error
    except KeyError as error:
        raise HTTPException(status_code=404, detail="graph node was not found") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return GraphResponse.model_validate(result)

@router.post("/{round_id}/graph/filter", response_model=GraphResponse)
def filter_graph(round_id: str, request: Request, payload: GraphFilterRequest) -> GraphResponse:
    return GraphResponse.model_validate(request.app.state.container.graph.filter(round_id, payload.visible.model_dump(), payload.families))
