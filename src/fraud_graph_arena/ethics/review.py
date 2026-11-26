from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fraud_graph_arena.case_packages import CasePackage, CasePackageRegistry
from fraud_graph_arena.paths import project_root

from .assessment import _json_list, normalize_claim_type
from .models import IMPACT_DIMENSIONS, REVIEW_VERSION, ROLE_DIMENSIONS


@dataclass(frozen=True, slots=True)
class EthicsReviewCheck:
    check_id: str
    status: str
    message: str


@dataclass(frozen=True, slots=True)
class EthicsReviewReport:
    package_id: str
    status: str
    checks: tuple[EthicsReviewCheck, ...]
    adversarial_case_count: int
    version: str = REVIEW_VERSION

    @property
    def failures(self) -> tuple[EthicsReviewCheck, ...]:
        return tuple(item for item in self.checks if item.status == "FAIL")


def _check(check_id: str, passed: bool, message: str) -> EthicsReviewCheck:
    return EthicsReviewCheck(check_id, "PASS" if passed else "FAIL", message)


def _adversarial_cases(path: Path | None = None) -> list[dict[str, Any]]:
    fixture = path or project_root() / "contracts/ethics/fga14-adversarial-cases.json"
    raw = json.loads(fixture.read_text(encoding="utf-8"))
    return list(raw.get("cases", []))


def _ethical_contract(path: Path | None = None) -> dict[str, Any]:
    contract = path or project_root() / "contracts/ethics/fga14-ethical-contract.json"
    return json.loads(contract.read_text(encoding="utf-8"))


def validate_ethical_contract(path: Path | None = None) -> list[str]:
    contract = _ethical_contract(path)
    errors: list[str] = []
    if contract.get("version") != "fga14-ethics-v1":
        errors.append("ethical contract has an unsupported version")
    if set(contract.get("claim_types", [])) != {"ACTOR", "AFFECTED_PARTY", "BEHAVIOUR", "BENEFICIARY", "EVIDENCE", "MECHANISM", "ROLE"}:
        errors.append("ethical contract claim types are incomplete")
    if tuple(contract.get("role_dimensions", [])) != ("OWNERSHIP", "CONTROL", "AUTHORISATION", "CUSTODY", "PROFESSIONAL_RESPONSIBILITY"):
        errors.append("ethical contract role dimensions are incomplete or reordered")
    if tuple(contract.get("impact_dimensions", [])) != ("BENEFIT", "HARM"):
        errors.append("ethical contract must keep benefit and harm distinct")
    if set(contract.get("outcomes", [])) != {"SUPPORTED", "INCOMPLETE", "UNSUPPORTED"}:
        errors.append("ethical contract outcomes are incomplete")
    if set(contract.get("evidence_modes", [])) != {"EXPLICIT_ANCHORS", "CLAIM_DECLARATIONS"}:
        errors.append("ethical contract evidence modes are incomplete")
    if contract.get("responsibility_rule") != "CONTROL_AND_ROLE_REQUIRED":
        errors.append("ethical contract responsibility rule is unsafe")
    if contract.get("evidence_boundary") != "PLAYER_VISIBLE_ONLY":
        errors.append("ethical contract evidence boundary is unsafe")
    return errors


def validate_adversarial_cases(path: Path | None = None) -> list[str]:
    cases = _adversarial_cases(path)
    expected = {
        "INNOCENT_SUPERNODE",
        "SHARED_ADDRESS_TRAP",
        "FALSE_IDENTITY_MATCH",
        "VICTIM_RECRUITER",
        "PROFESSIONAL_PROXIMITY",
        "MISLEADING_ALGORITHM_RESULT",
    }
    errors: list[str] = []
    actual = {str(item.get("case_id")) for item in cases}
    if actual != expected:
        errors.append("adversarial fixture set must cover the six FGA14 traps exactly")
    for item in cases:
        if item.get("expected_disposition") != "DO_NOT_ACCUSE_WITHOUT_ROLE_EVIDENCE":
            errors.append(f"adversarial case {item.get('case_id')} has an unsafe expected disposition")
        if not item.get("protected_reason") or not item.get("trap"):
            errors.append(f"adversarial case {item.get('case_id')} is missing its safety rationale")
    return errors


def review_package(package: CasePackage, *, adversarial_case_count: int | None = None) -> EthicsReviewReport:
    if package.kind != "canonical":
        checks = (_check("ETHICS.EMPTY_PACKAGE", True, "Empty package has no player-facing conclusion to adjudicate."),)
        return EthicsReviewReport(package.package_id, "PASS", checks, adversarial_case_count or 0)
    published = {row["record_id"] for row in package.rows("published/records.csv")}
    claims = package.rows(package.evidence_rules["required_claims_path"])
    requirements = package.rows("truth/evidence_requirements.csv")
    entities = package.rows("truth/entities.csv")
    required_claim_ids = {row["claim_id"] for row in claims if row.get("required", "").lower() == "true"}
    requirement_claim_ids = {row.get("claim_id", "") for row in requirements}
    all_refs = {ref for row in requirements for ref in _json_list(row.get("record_ids_json", ""))}
    protected = [row for row in entities if row.get("culpability", "").lower() in {"none", "unknown"}]
    types_ok = all(bool(normalize_claim_type(row.get("claim_type", ""))) for row in claims)
    role_columns_ok = bool(entities) and all(
        all(column in row for column in ("operational_role", "harm_status", "fraud_network_membership")) for row in entities
    ) and bool(ROLE_DIMENSIONS) and bool(IMPACT_DIMENSIONS)
    contract_errors = validate_ethical_contract()
    checks = (
        _check("ETHICS.CONTRACT", not contract_errors, "Versioned role, impact, outcome and evidence dimensions are complete." if not contract_errors else "; ".join(contract_errors)),
        _check("ETHICS.PUBLIC_PROJECTION", bool(published), "Published evidence is non-empty."),
        _check("ETHICS.CLAIM_TYPES", types_ok, "Every claim uses a controlled ethical claim type."),
        _check("ETHICS.REQUIRED_EVIDENCE", required_claim_ids <= requirement_claim_ids, "Every required claim has an evidence requirement."),
        _check("ETHICS.EVIDENCE_REFERENCES", all_refs <= published, "Evidence requirements point only to published records."),
        _check("ETHICS.PROTECTED_ACTORS", bool(protected), "The case contains at least one protected actor for benign adversarial review."),
        _check("ETHICS.ROLE_SEMANTICS", role_columns_ok, "Role semantics and the separate benefit/harm impact dimensions are declared by the FGA-14 contract."),
        _check("ETHICS.TRUTH_BOUNDARY", not any("culpability" in row or "expected_classification" in row for row in package.rows("published/records.csv")), "Published records contain no evaluator truth fields."),
    )
    return EthicsReviewReport(package.package_id, "PASS" if not any(item.status == "FAIL" for item in checks) else "FAIL", checks, adversarial_case_count or 0)


def review_all_packages(root: Path | None = None) -> tuple[EthicsReviewReport, ...]:
    adversarial_path = project_root() / "contracts/ethics/fga14-adversarial-cases.json"
    adversarial_errors = validate_adversarial_cases(adversarial_path)
    count = len(_adversarial_cases(adversarial_path))
    reports = list(review_package(item, adversarial_case_count=count) for item in CasePackageRegistry(root).all())
    if adversarial_errors:
        failed = EthicsReviewCheck("ETHICS.ADVERSARIAL_FIXTURES", "FAIL", "; ".join(adversarial_errors))
        reports = [EthicsReviewReport(item.package_id, "FAIL", item.checks + (failed,), item.adversarial_case_count) for item in reports]
    return tuple(reports)
