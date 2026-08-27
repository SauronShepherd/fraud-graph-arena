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
    record_id: str
    record_type: str
    label: str
    safe_summary: str
    record_subtype: str
    source_system_id: str
    provenance_ref: str

class GraphEdgeResponse(ApiModel):
    relationship_id: str
    source_record_id: str
    target_record_id: str
    relationship_family: str
    relationship_type: str
    directed: bool
    provenance: str
    player_safe_summary: str
    event_time: str

class GraphResponse(ApiModel):
    projection_version: str
    nodes: list[GraphNodeResponse]
    edges: list[GraphEdgeResponse]
    node_count: int
    edge_count: int
    partial: bool = False
    omitted_node_count: int = 0
    omitted_edge_count: int = 0
    relationship_filters: list[str] = Field(default_factory=list)

class GraphViewRequest(ApiModel):
    seeds: list[str] = Field(default_factory=list, max_length=100)
    limit: int = Field(default=100, ge=1, le=1000)

class GraphExpandRequest(ApiModel):
    visible: GraphResponse
    node_id: str = Field(min_length=1, max_length=128)
    depth: int = Field(default=1, ge=1, le=1)
    limit: int = Field(default=100, ge=1, le=1000)

class GraphFilterRequest(ApiModel):
    visible: GraphResponse
    families: list[str] = Field(default_factory=list, max_length=32)


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
