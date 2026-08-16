from __future__ import annotations

from fastapi import APIRouter, Request, status
from fraud_graph_arena.rounds.domain import IntroCompletion

from fraud_graph_arena.web.api_models import (
    CreateRoundRequest,
    IntroCompletionRequest,
    OpeningResponse,
    RoundResponse,
    WorkspaceResponse,
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
