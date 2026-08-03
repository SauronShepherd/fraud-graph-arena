from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from fraud_graph_arena.catalogue.domain import CaseStatus, PathId, PathStatus
from fraud_graph_arena.narrative.domain import ComicKind
from fraud_graph_arena.rounds.domain import RoundStatus


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


class WorkspaceResponse(ApiModel):
    round: RoundResponse
    case: CaseResponse
    board_message: str
    evidence_count: int
    suspect_count: int


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
