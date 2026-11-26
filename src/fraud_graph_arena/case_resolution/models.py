from __future__ import annotations

from dataclasses import dataclass


SCORING_VERSION = "fga11-scoring-v1"


@dataclass(frozen=True, slots=True)
class ScoreDimensions:
    conclusion_accuracy: int
    evidence_quality: int
    relationship_interpretation: int
    protected_actor_discipline: int
    efficiency: int

    @property
    def total(self) -> int:
        return sum((self.conclusion_accuracy, self.evidence_quality, self.relationship_interpretation, self.protected_actor_discipline, self.efficiency))

    def as_dict(self) -> dict[str, int]:
        return {
            "conclusion_accuracy": self.conclusion_accuracy,
            "evidence_quality": self.evidence_quality,
            "relationship_interpretation": self.relationship_interpretation,
            "protected_actor_discipline": self.protected_actor_discipline,
            "efficiency": self.efficiency,
        }


@dataclass(frozen=True, slots=True)
class SubmissionResult:
    submission_id: str
    round_id: str
    idempotency_key: str
    status: str
    score: int
    ending_code: str
    ending_title: str
    ending_narrative: str
    dimensions: ScoreDimensions
    false_accusations: int
    required_claims_complete: bool
    submitted_suspect_count: int
    credits_remaining: int
    scoring_version: str
    economy_version: str
    created_at: str
    request_hash: str
    replayed: bool = False
