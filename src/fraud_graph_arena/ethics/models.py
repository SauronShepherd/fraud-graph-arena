from __future__ import annotations

from dataclasses import dataclass


ETHICS_VERSION = "fga14-ethics-v1"
REVIEW_VERSION = "fga14-publication-review-v1"
ROLE_DIMENSIONS = (
    "OWNERSHIP",
    "CONTROL",
    "AUTHORISATION",
    "CUSTODY",
    "PROFESSIONAL_RESPONSIBILITY",
)
IMPACT_DIMENSIONS = ("BENEFIT", "HARM")


@dataclass(frozen=True, slots=True)
class EvidenceStatement:
    """A player-safe account of one submitted evidence claim."""

    claim_id: str
    claim_type: str
    evidence_family: str
    support: str
    matched_record_count: int
    required_record_count: int
    explanation: str


@dataclass(frozen=True, slots=True)
class EthicalAssessment:
    """The ethical boundary of a conclusion, without revealing evaluator truth."""

    status: str
    evidence_mode: str
    evidence_threshold: int
    submitted_claim_count: int
    supported_claim_count: int
    missing_claim_count: int
    unsupported_claim_count: int
    submitted_record_count: int
    matched_record_count: int
    unsupported_accusation_count: int
    harm_penalty: int
    responsibility_rule: str
    evidence_boundary: str
    role_dimensions: tuple[str, ...]
    impact_dimensions: tuple[str, ...]
    explanation: str
    statements: tuple[EvidenceStatement, ...]
    version: str = ETHICS_VERSION
