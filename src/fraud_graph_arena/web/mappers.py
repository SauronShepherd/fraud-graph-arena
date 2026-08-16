from __future__ import annotations

from fraud_graph_arena.catalogue.domain import CaseSummary, CatalogueSection, PathDefinition
from fraud_graph_arena.narrative.domain import ComicPage, ComicSequence
from fraud_graph_arena.rounds.domain import Round
from fraud_graph_arena.rounds.service import Opening, Workspace
from fraud_graph_arena.workspace.service import WorkspaceProjection
from fraud_graph_arena.web.api_models import (
    CaseResponse,
    CatalogueSectionResponse,
    ComicPageResponse,
    ComicSequenceResponse,
    OpeningResponse,
    PathResponse,
    RoundResponse,
    WorkspaceResponse,
)


def map_path(value: PathDefinition) -> PathResponse:
    return PathResponse(
        id=value.id,
        name=value.name,
        description=value.description,
        ranked=value.ranked,
        status=value.status,
        access_message=value.access_message,
    )


def map_case(value: CaseSummary) -> CaseResponse:
    return CaseResponse(
        id=value.id,
        version=value.version,
        path_id=value.path_id,
        name=value.name,
        description=value.description,
        status=value.status,
    )


def map_section(value: CatalogueSection) -> CatalogueSectionResponse:
    return CatalogueSectionResponse(
        path=map_path(value.path),
        cases=[map_case(item) for item in value.cases],
    )


def map_round(value: Round) -> RoundResponse:
    return RoundResponse(
        id=value.id,
        player_id=value.player_id,
        path_id=value.path_id,
        case_id=value.case_id,
        case_version=value.case_version,
        status=value.status,
        created_at=value.created_at,
        started_at=value.started_at,
        intro_completed_at=value.intro_completed_at,
    )


def map_comic_page(value: ComicPage) -> ComicPageResponse:
    return ComicPageResponse(
        id=value.id,
        position=value.position,
        title=value.title,
        narration=value.narration,
        image_url=value.image_url,
        alt_text=value.alt_text,
    )


def map_comic_sequence(value: ComicSequence) -> ComicSequenceResponse:
    return ComicSequenceResponse(
        id=value.id,
        case_id=value.case_id,
        case_version=value.case_version,
        kind=value.kind,
        skippable=value.skippable,
        pages=[map_comic_page(item) for item in value.pages],
    )


def map_opening(value: Opening) -> OpeningResponse:
    return OpeningResponse(
        round=map_round(value.round),
        case=map_case(value.case),
        sequence=map_comic_sequence(value.sequence),
    )


def map_workspace(value: WorkspaceProjection | Workspace) -> WorkspaceResponse:
    if isinstance(value, WorkspaceProjection):
        return WorkspaceResponse(
            round=map_round(value.round), case=map_case(value.case), board_message="No evidence has been revealed.",
            evidence_count=value.evidence_count, suspect_count=value.suspect_count, path_name=value.path_name,
            empty_state_code=value.empty_state_code, actions=value.actions,
        )
    return WorkspaceResponse(
        round=map_round(value.round),
        case=map_case(value.case),
        board_message=value.board_message,
        evidence_count=value.evidence_count,
        suspect_count=value.suspect_count,
        path_name="Detective Academy", empty_state_code="NO_EVIDENCE_REVEALED", actions=[],
    )
