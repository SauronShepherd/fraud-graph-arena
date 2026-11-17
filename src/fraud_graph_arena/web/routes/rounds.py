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
    EntityResolutionRequest, EntityResolutionResponse, IdentityCandidateResponse,
    ExactIdentityMatchResponse, EntityResolutionReviewRequest, EntityResolutionReviewResponse,
    EntityResolutionHistoryResponse,
)
from fraud_graph_arena.web.mappers import map_opening, map_round, map_workspace

router = APIRouter(prefix="/rounds", tags=["rounds"])


def _command_response(command, *, replayed: bool = False) -> InvestigationCommandResponse:
    return InvestigationCommandResponse(
        command_id=command.command_id,
        round_id=command.round_id,
        idempotency_key=command.idempotency_key,
        action=command.action,
        source_record_id=command.source_record_id,
        target_record_id=command.target_record_id,
        relationship_type=command.relationship_type,
        status=command.status,
        charged_credits=command.charged_credits,
        revealed_record_ids=list(command.revealed_record_ids),
        created_at=command.created_at,
        replayed=replayed,
    )


@router.post("/{round_id}/investigations/hypotheses", response_model=InvestigationCommandResponse)
def submit_hypothesis(round_id: str, payload: HypothesisRequest, request: Request) -> InvestigationCommandResponse:
    command, created = request.app.state.container.investigation_commands.submit_hypothesis(
        round_id,
        payload.idempotency_key,
        payload.source_record_id,
        payload.target_record_id,
        payload.relationship_type,
    )
    return _command_response(command, replayed=not created)


@router.get("/{round_id}/investigations/history", response_model=InvestigationCommandListResponse)
def investigation_history(round_id: str, request: Request) -> InvestigationCommandListResponse:
    commands = request.app.state.container.investigation_commands.list_for_round(round_id)
    return InvestigationCommandListResponse(commands=[_command_response(item) for item in commands])


def _candidate_response(candidate) -> IdentityCandidateResponse:
    return IdentityCandidateResponse(
        candidate_id=candidate.candidate_id,
        left_record_id=candidate.left_record_id,
        right_record_id=candidate.right_record_id,
        entity_type=candidate.entity_type,
        confidence_band=candidate.confidence_band,
        estimated_score=candidate.estimated_score,
        agreement_fields=list(candidate.agreement_fields),
        disagreement_fields=list(candidate.disagreement_fields),
        missing_fields=list(candidate.missing_fields),
        evidence_reasons=list(candidate.evidence_reasons),
        model_version=candidate.model_version,
        threshold_version=candidate.threshold_version,
        normalization_version=candidate.normalization_version,
        framework_semantics=candidate.framework_semantics,
        generation_mode=candidate.generation_mode,
        actual_engine_run=candidate.actual_engine_run,
        review_required=candidate.review_required,
        snapshot_version=candidate.snapshot_version,
    )


def _analysis_response(run, *, replayed: bool = False) -> EntityResolutionResponse:
    return EntityResolutionResponse(
        analysis_id=run.analysis_id,
        round_id=run.round_id,
        idempotency_key=run.idempotency_key,
        focus_record_id=run.focus_record_id,
        status=run.status,
        charged_credits=run.charged_credits,
        normalization_version=run.normalization_version,
        model_version=run.model_version,
        threshold_version=run.threshold_version,
        snapshot_version=run.snapshot_version,
        generation_mode=run.generation_mode,
        framework_semantics=run.framework_semantics,
        actual_engine_run=run.actual_engine_run,
        exact_matches=[ExactIdentityMatchResponse(
            match_id=item.match_id,
            left_record_id=item.left_record_id,
            right_record_id=item.right_record_id,
            entity_type=item.entity_type,
            rule_id=item.rule_id,
            evidence_fields=list(item.evidence_fields),
            evidence_reasons=list(item.evidence_reasons),
            normalization_version=item.normalization_version,
            snapshot_version=item.snapshot_version,
            provenance_refs=list(item.provenance_refs),
        ) for item in run.exact_matches],
        candidates=[_candidate_response(item) for item in run.candidates],
        replayed=replayed,
    )


def _review_response(review, *, replayed: bool = False) -> EntityResolutionReviewResponse:
    return EntityResolutionReviewResponse(
        review_id=review.review_id,
        round_id=review.round_id,
        candidate_id=review.candidate_id,
        outcome=review.outcome,
        status=review.status,
        created_at=review.created_at,
        replayed=replayed,
    )


@router.post("/{round_id}/investigations/entity-resolution", response_model=EntityResolutionResponse)
def entity_resolution(round_id: str, payload: EntityResolutionRequest, request: Request) -> EntityResolutionResponse:
    run, created = request.app.state.container.entity_resolution.analyze(
        round_id,
        payload.idempotency_key,
        payload.focus_record_id,
    )
    return _analysis_response(run, replayed=not created)


@router.post("/{round_id}/investigations/entity-resolution/{candidate_id}/review", response_model=EntityResolutionReviewResponse)
def entity_resolution_review(round_id: str, candidate_id: str, payload: EntityResolutionReviewRequest, request: Request) -> EntityResolutionReviewResponse:
    review, created = request.app.state.container.entity_resolution.review(
        round_id,
        candidate_id,
        payload.idempotency_key,
        payload.outcome,
    )
    return _review_response(review, replayed=not created)


@router.get("/{round_id}/investigations/entity-resolution/history", response_model=EntityResolutionHistoryResponse)
def entity_resolution_history(round_id: str, request: Request) -> EntityResolutionHistoryResponse:
    runs, reviews = request.app.state.container.entity_resolution.history(round_id)
    return EntityResolutionHistoryResponse(
        analyses=[_analysis_response(run) for run in runs],
        reviews=[_review_response(review) for review in reviews],
    )


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
