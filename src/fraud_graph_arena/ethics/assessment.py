from __future__ import annotations

import json
from typing import Iterable

from fraud_graph_arena.case_packages import CasePackage

from .models import IMPACT_DIMENSIONS, ROLE_DIMENSIONS, EvidenceStatement, EthicalAssessment


CLAIM_TYPES = frozenset(
    {
        "ACTOR",
        "AFFECTED_PARTY",
        "BEHAVIOUR",
        "BENEFICIARY",
        "CYCLE",
        "EVIDENCE",
        "GENERAL",
        "IDENTITY",
        "MECHANISM",
        "ROLE",
        "SHARED_INFRASTRUCTURE",
    }
)


def normalize_claim_type(raw: str) -> str:
    """Map a case-specific evidence label to a small ethical vocabulary."""

    value = str(raw or "").strip().upper()
    if value in CLAIM_TYPES:
        return value
    if any(token in value for token in ("IDENTITY", "NOMINEE", "KYC")):
        return "ACTOR"
    if any(token in value for token in ("CONTROL", "ROLE", "PERMISSION", "AUTHORITY", "CUSTODY", "OWNER")):
        return "ROLE"
    if any(token in value for token in ("BENEFIT", "PROCEEDS", "PAYMENT", "FUNDS", "DONATION", "GRANT", "BENEFICIARY")):
        return "BENEFICIARY"
    if any(token in value for token in ("LOSS", "VICTIM", "HARM", "COMPLAINT", "WHISTLEBLOWER")):
        return "AFFECTED_PARTY"
    if value:
        return "EVIDENCE"
    return "GENERAL"


def _rows(package: CasePackage, relative_path: str) -> list[dict[str, str]]:
    root = package.canonical_root
    if root is None or not (root / relative_path).is_file():
        return []
    return package.rows(relative_path)


def _json_list(raw: str) -> tuple[str, ...]:
    try:
        value = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return ()
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)


def _claim_rows(package: CasePackage) -> dict[str, dict[str, str]]:
    return {row["claim_id"]: row for row in _rows(package, package.evidence_rules["required_claims_path"])}


def _requirements(package: CasePackage) -> dict[str, tuple[dict[str, str], ...]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in _rows(package, "truth/evidence_requirements.csv"):
        grouped.setdefault(row.get("claim_id", ""), []).append(row)
    return {key: tuple(value) for key, value in grouped.items()}


def assess_submission(
    package: CasePackage,
    *,
    suspect_record_ids: Iterable[str],
    evidence_claim_ids: Iterable[str],
    evidence_record_ids: Iterable[str],
    required_claims_complete: bool,
    unsupported_accusation_count: int,
    has_supported_actor: bool,
) -> EthicalAssessment:
    """Assess support and harm using only facts the player can cite.

    The evaluator may use protected truth to calculate the score. This object never
    serialises that truth: it reports only submitted claims, published evidence
    anchors and category-level consequences.
    """

    selected = tuple(str(item) for item in suspect_record_ids)
    claims = frozenset(str(item) for item in evidence_claim_ids)
    records = frozenset(str(item) for item in evidence_record_ids)
    claim_rows = _claim_rows(package)
    requirements = _requirements(package)
    public_ids = frozenset(row["record_id"] for row in _rows(package, "published/records.csv"))
    valid_claims = claims & claim_rows.keys()
    unknown_claims = claims - claim_rows.keys()
    explicit_records = records & public_ids
    evidence_mode = "EXPLICIT_ANCHORS" if records else "CLAIM_DECLARATIONS"
    statements: list[EvidenceStatement] = []
    matched_total = 0
    supported_total = 0
    for claim_id in sorted(valid_claims):
        row = claim_rows[claim_id]
        requirement_rows = requirements.get(claim_id, ())
        refs = frozenset(ref for requirement in requirement_rows for ref in _json_list(requirement.get("record_ids_json", "")))
        required_count = max((int(item.get("minimum_distinct_items", 0) or 0) for item in requirement_rows), default=0)
        matched = len(refs & explicit_records) if records else 0
        anchored = not records or matched >= required_count
        if anchored:
            supported_total += 1
        matched_total += matched
        family = ", ".join(sorted({item.get("evidence_family", "GENERAL") for item in requirement_rows})) or "GENERAL"
        support = "ANCHORED" if records and anchored else "DECLARED" if not records else "INSUFFICIENT"
        statements.append(
            EvidenceStatement(
                claim_id=claim_id,
                claim_type=normalize_claim_type(row.get("claim_type", "GENERAL")),
                evidence_family=family,
                support=support,
                matched_record_count=matched,
                required_record_count=required_count,
                explanation=(
                    "The submitted claim is paired with enough player-visible evidence anchors."
                    if support == "ANCHORED"
                    else "The submitted claim is recorded, but its raw evidence anchors were not included."
                    if support == "DECLARED"
                    else "The submitted claim does not yet meet its declared evidence-anchor threshold."
                ),
            )
        )
    threshold_met = required_claims_complete and not unknown_claims and all(item.support != "INSUFFICIENT" for item in statements)
    unsupported_selection = bool(has_supported_actor is False and selected)
    if unsupported_accusation_count > 0 or unsupported_selection:
        status = "UNSUPPORTED"
    elif not threshold_met:
        status = "INCOMPLETE"
    else:
        status = "SUPPORTED"
    harm_penalty = min(300, unsupported_accusation_count * 150)
    missing_count = len(set(row["claim_id"] for row in claim_rows.values() if row.get("required", "").lower() == "true") - claims)
    explanation = {
        "SUPPORTED": "The conclusion met the evidence threshold and did not turn a protected actor into an accusation. Support is not the same as guilt.",
        "INCOMPLETE": f"The submission leaves {missing_count} required evidence claim(s) unresolved. Missing evidence remains uncertainty; it does not become guilt by default.",
        "UNSUPPORTED": "The submission crossed the support boundary. Similarity, proximity or a central graph position cannot substitute for an explicit responsibility finding.",
    }[status]
    if evidence_mode == "CLAIM_DECLARATIONS" and status == "SUPPORTED":
        explanation += " The result records the submitted claim contract; a later client may add raw evidence anchors for a stronger audit trail."
    return EthicalAssessment(
        status=status,
        evidence_mode=evidence_mode,
        evidence_threshold=max(1, int(package.difficulty_profile.evidence_threshold)),
        submitted_claim_count=len(claims),
        supported_claim_count=supported_total,
        missing_claim_count=missing_count,
        unsupported_claim_count=len(unknown_claims) + sum(item.support == "INSUFFICIENT" for item in statements),
        submitted_record_count=len(explicit_records),
        matched_record_count=matched_total,
        unsupported_accusation_count=unsupported_accusation_count,
        harm_penalty=harm_penalty,
        responsibility_rule="CONTROL_AND_ROLE_REQUIRED",
        evidence_boundary="PLAYER_VISIBLE_ONLY",
        role_dimensions=ROLE_DIMENSIONS,
        impact_dimensions=IMPACT_DIMENSIONS,
        explanation=explanation,
        statements=tuple(statements),
    )
