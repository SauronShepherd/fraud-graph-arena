from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from fraud_graph_arena.catalogue.domain import CaseStatus, PathId, PathStatus
from fraud_graph_arena.narrative.domain import ComicKind
from fraud_graph_arena.rounds.domain import IntroCompletion, RoundStatus


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PathResponse(ApiModel):
    id: PathId
    name: str
    description: str
    ranked: bool
    status: PathStatus
    access_message: str


class CaseResponse(ApiModel):
    id: str
    version: str
    path_id: PathId
    name: str
    description: str
    status: CaseStatus


class CatalogueSectionsResponse(ApiModel):
    sections: list[PathResponse]


class CatalogueSectionResponse(ApiModel):
    path: PathResponse
    cases: list[CaseResponse]


class CreateRoundRequest(ApiModel):
    player_id: str = Field(default="demo-hercule", min_length=1, max_length=100)
    path_id: str = Field(min_length=1, max_length=64)
    case_id: str = Field(min_length=1, max_length=64)


class RoundResponse(ApiModel):
    id: str
    player_id: str
    path_id: PathId
    case_id: str
    case_version: str
    status: RoundStatus
    created_at: datetime
    started_at: datetime | None
    intro_completed_at: datetime | None
    credits_remaining: int = Field(ge=0)
    version: int = Field(ge=1)


class ComicPageResponse(ApiModel):
    id: str
    position: int
    title: str
    narration: str
    image_url: str
    alt_text: str


class ComicSequenceResponse(ApiModel):
    id: str
    case_id: str
    case_version: str
    kind: ComicKind
    skippable: bool
    pages: list[ComicPageResponse]


class OpeningResponse(ApiModel):
    round: RoundResponse
    case: CaseResponse
    sequence: ComicSequenceResponse

class IntroCompletionRequest(ApiModel):
    completion: IntroCompletion = IntroCompletion.FINISHED

class ActionAvailability(ApiModel):
    id: str
    state: str
    reason_code: str
    reason: str

class GraphNodeResponse(ApiModel):
    record_id: str = Field(max_length=128)
    record_type: str = Field(max_length=64)
    label: str = Field(max_length=256)
    safe_summary: str = Field(max_length=2048)
    record_subtype: str = Field(max_length=128)
    source_system_id: str = Field(max_length=128)
    provenance_ref: str = Field(max_length=512)

class GraphEdgeResponse(ApiModel):
    relationship_id: str = Field(max_length=128)
    source_record_id: str = Field(max_length=128)
    target_record_id: str = Field(max_length=128)
    relationship_family: str = Field(max_length=128)
    relationship_type: str = Field(max_length=128)
    directed: bool
    provenance: str = Field(max_length=512)
    player_safe_summary: str = Field(max_length=2048)
    event_time: str = Field(max_length=64)

class GraphResponse(ApiModel):
    projection_version: str
    nodes: list[GraphNodeResponse] = Field(max_length=300)
    edges: list[GraphEdgeResponse] = Field(max_length=700)
    node_count: int
    edge_count: int
    partial: bool = False
    omitted_node_count: int = 0
    omitted_edge_count: int = 0
    relationship_filters: list[str] = Field(default_factory=list)

class GraphViewRequest(ApiModel):
    seeds: list[str] = Field(default_factory=list, max_length=100)
    limit: int = Field(default=150, ge=1, le=300)
    edge_limit: int = Field(default=300, ge=1, le=700)

class GraphExpandRequest(ApiModel):
    visible: GraphResponse
    node_id: str = Field(min_length=1, max_length=128)
    depth: int = Field(default=1, ge=1, le=1)
    limit: int = Field(default=300, ge=1, le=300)
    edge_limit: int = Field(default=700, ge=1, le=700)

class GraphFilterRequest(ApiModel):
    visible: GraphResponse
    families: list[str] = Field(default_factory=list, max_length=32)


class GraphAnalysisRequest(ApiModel):
    algorithm: str = Field(pattern=r"^(NEIGHBOURHOOD|SHORTEST_PATH|CONNECTED_COMPONENTS|CENTRALITY|MOTIF|CIRCULAR_FLOW)$")
    seed_record_id: str | None = Field(default=None, min_length=1, max_length=128)
    source_record_id: str | None = Field(default=None, min_length=1, max_length=128)
    target_record_id: str | None = Field(default=None, min_length=1, max_length=128)
    max_hops: int = Field(default=1, ge=1, le=3)
    max_path_length: int = Field(default=4, ge=1, le=6)
    result_limit: int = Field(default=10, ge=1, le=20)
    directed: bool = True
    centrality_metric: str = Field(default="degree", pattern=r"^(degree|pagerank|betweenness)$")
    relationship_families: list[str] = Field(default_factory=list, max_length=16)
    relationship_types: list[str] = Field(default_factory=list, max_length=16)
    time_from: str | None = Field(default=None, max_length=64)
    time_to: str | None = Field(default=None, max_length=64)
    visible_record_ids: list[str] = Field(default_factory=list, max_length=300)


class GraphAnalysisPathResponse(ApiModel):
    record_ids: list[str]
    relationship_ids: list[str]
    length: int = Field(ge=0)


class GraphAnalysisComponentResponse(ApiModel):
    component_id: str
    record_ids: list[str]
    node_count: int = Field(ge=0)
    edge_count: int = Field(ge=0)


class GraphAnalysisLeadResponse(ApiModel):
    rank: int = Field(ge=1)
    record_id: str
    metric: str
    score: float
    supporting_relationship_ids: list[str]


class GraphAnalysisMotifResponse(ApiModel):
    motif_type: str
    record_ids: list[str]
    relationship_ids: list[str]
    length: int = Field(ge=1)
    event_times: list[str]
    time_span: str | None = None
    chronology_observed: bool


class GraphAnalysisResponse(ApiModel):
    analysis_id: str
    round_id: str
    algorithm: str
    status: str
    result_type: str
    parameters: dict[str, Any]
    snapshot_version: str
    projection_version: str
    graph_engine: str
    framework_semantics: str
    generation_mode: str
    actual_engine_run: bool
    input_node_count: int = Field(ge=0)
    input_edge_count: int = Field(ge=0)
    nodes: list[GraphNodeResponse] = Field(max_length=300)
    edges: list[GraphEdgeResponse] = Field(max_length=700)
    paths: list[GraphAnalysisPathResponse] = Field(max_length=20)
    components: list[GraphAnalysisComponentResponse] = Field(max_length=20)
    ranked_leads: list[GraphAnalysisLeadResponse] = Field(max_length=20)
    motifs: list[GraphAnalysisMotifResponse] = Field(max_length=20)
    supporting_relationship_ids: list[str] = Field(max_length=700)
    partial: bool
    omitted_result_count: int = Field(ge=0)
    interpretation: str = Field(max_length=2048)
    limitations: list[str] = Field(max_length=16)
    cache_key: str
    cached: bool = False
    execution_millis: int = Field(ge=0)


class GraphAnalysisHistoryResponse(ApiModel):
    analyses: list[GraphAnalysisResponse]


class HypothesisRequest(ApiModel):
    idempotency_key: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    source_record_id: str = Field(min_length=1, max_length=128)
    target_record_id: str = Field(min_length=1, max_length=128)
    relationship_type: str = Field(min_length=1, max_length=64)


class InvestigationCommandResponse(ApiModel):
    command_id: str
    round_id: str
    idempotency_key: str
    action: str
    source_record_id: str
    target_record_id: str
    relationship_type: str
    status: str
    charged_credits: int = Field(ge=0)
    revealed_record_ids: list[str]
    created_at: datetime
    replayed: bool = False


class InvestigationCommandListResponse(ApiModel):
    commands: list[InvestigationCommandResponse]


class EntityResolutionRequest(ApiModel):
    idempotency_key: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    focus_record_id: str | None = Field(default=None, min_length=1, max_length=128)


class IdentityCandidateResponse(ApiModel):
    candidate_id: str
    left_record_id: str
    right_record_id: str
    entity_type: str
    confidence_band: str
    estimated_score: float = Field(ge=0, le=1)
    agreement_fields: list[str]
    disagreement_fields: list[str]
    missing_fields: list[str]
    evidence_reasons: list[str]
    model_version: str
    threshold_version: str
    normalization_version: str
    framework_semantics: str
    generation_mode: str
    actual_engine_run: bool
    review_required: bool
    snapshot_version: str


class ExactIdentityMatchResponse(ApiModel):
    match_id: str
    left_record_id: str
    right_record_id: str
    entity_type: str
    rule_id: str
    evidence_fields: list[str]
    evidence_reasons: list[str]
    normalization_version: str
    snapshot_version: str
    provenance_refs: list[str]


class EntityResolutionResponse(ApiModel):
    analysis_id: str
    round_id: str
    idempotency_key: str
    focus_record_id: str | None
    status: str
    charged_credits: int = Field(ge=0)
    normalization_version: str
    model_version: str
    threshold_version: str
    snapshot_version: str
    generation_mode: str
    framework_semantics: str
    actual_engine_run: bool
    exact_matches: list[ExactIdentityMatchResponse]
    candidates: list[IdentityCandidateResponse]
    replayed: bool = False


class EntityResolutionReviewRequest(ApiModel):
    idempotency_key: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    outcome: str = Field(pattern=r"^(ACCEPTED|REJECTED|UNRESOLVED)$")


class EntityResolutionReviewResponse(ApiModel):
    review_id: str
    round_id: str
    candidate_id: str
    outcome: str
    status: str
    created_at: datetime
    replayed: bool = False


class EntityResolutionHistoryResponse(ApiModel):
    analyses: list[EntityResolutionResponse]
    reviews: list[EntityResolutionReviewResponse]


class WorkspaceResponse(ApiModel):
    round: RoundResponse
    case: CaseResponse
    board_message: str
    evidence_count: int
    suspect_count: int
    path_name: str
    empty_state_code: str
    actions: list[ActionAvailability]
    graph: GraphResponse


class LiveHealthResponse(ApiModel):
    status: str = "alive"


class ReadyHealthResponse(ApiModel):
    status: str
    checks: dict[str, str]


class VersionResponse(ApiModel):
    build_version: str
    contract_version: str
    runtime_role: str
    environment: str


class ProblemDetails(ApiModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    code: str
    correlation_id: str
    recovery: str | None = None
    errors: list[dict[str, Any]] | None = None
