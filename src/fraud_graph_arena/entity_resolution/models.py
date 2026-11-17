from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NormalizedValue:
    field: str
    original_present: bool
    normalized: str | None
    valid: bool
    placeholder: bool
    classification: str
    original: str | None = None


@dataclass(frozen=True, slots=True)
class NormalizedRecord:
    record_id: str
    entity_type: str
    label: str
    provenance_ref: str
    snapshot_version: str
    fields: dict[str, NormalizedValue]
    identifier_validated: bool = False


@dataclass(frozen=True, slots=True)
class ExactIdentityMatch:
    match_id: str
    left_record_id: str
    right_record_id: str
    entity_type: str
    rule_id: str
    evidence_fields: tuple[str, ...]
    evidence_reasons: tuple[str, ...]
    normalization_version: str
    snapshot_version: str
    provenance_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IdentityCandidate:
    candidate_id: str
    left_record_id: str
    right_record_id: str
    entity_type: str
    confidence_band: str
    estimated_score: float
    agreement_fields: tuple[str, ...]
    disagreement_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    evidence_reasons: tuple[str, ...]
    model_version: str
    threshold_version: str
    normalization_version: str
    framework_semantics: str
    generation_mode: str
    actual_engine_run: bool
    review_required: bool
    snapshot_version: str


@dataclass(frozen=True, slots=True)
class ResolutionRun:
    analysis_id: str
    round_id: str
    idempotency_key: str
    request_hash: str
    focus_record_id: str | None
    status: str
    charged_credits: int
    normalization_version: str
    model_version: str
    threshold_version: str
    snapshot_version: str
    generation_mode: str
    framework_semantics: str
    actual_engine_run: bool
    exact_matches: tuple[ExactIdentityMatch, ...]
    candidates: tuple[IdentityCandidate, ...]
    created_at: str


@dataclass(frozen=True, slots=True)
class IdentityReview:
    review_id: str
    round_id: str
    candidate_id: str
    idempotency_key: str
    request_hash: str
    outcome: str
    status: str
    created_at: str
