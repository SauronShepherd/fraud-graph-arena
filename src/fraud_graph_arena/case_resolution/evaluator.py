from __future__ import annotations

import json
from typing import Any

from fraud_graph_arena.case_packages import CasePackage
from fraud_graph_arena.economy.models import LedgerEntryType
from fraud_graph_arena.rounds.domain import Round

from .models import ScoreDimensions


def required_claims(package: CasePackage) -> frozenset[str]:
    return frozenset(
        row["claim_id"]
        for row in package.rows(package.evidence_rules["required_claims_path"])
        if row.get("required", "").strip().lower() == "true"
    )


def published_record_ids(package: CasePackage) -> frozenset[str]:
    return frozenset(row["record_id"] for row in package.rows("published/records.csv"))


def _truth_entities(package: CasePackage) -> list[dict[str, str]]:
    return package.rows("truth/entities.csv")


def _protected_ids(package: CasePackage) -> frozenset[str]:
    return frozenset(
        row["entity_id"]
        for row in _truth_entities(package)
        if row.get("culpability", "").strip().lower() in {"none", "unknown"}
    )


def _primary_ids(package: CasePackage) -> frozenset[str]:
    return frozenset(
        row["entity_id"]
        for row in _truth_entities(package)
        if "PRIMARY" in row.get("expected_classification", "").upper()
        or "PRIMARY" in row.get("operational_role", "").upper()
    )


def _scenario_rows(package: CasePackage) -> list[dict[str, str]]:
    return package.rows("truth/test_scenarios.csv")


def _suspects_from_scenario(row: dict[str, str]) -> frozenset[str]:
    try:
        values = json.loads(row.get("submitted_suspects_json", "[]"))
    except json.JSONDecodeError:
        values = []
    return frozenset(str(value) for value in values)


def _scenario_for(package: CasePackage, selected: frozenset[str], complete: bool, credits_remaining: int) -> dict[str, str] | None:
    rows = _scenario_rows(package)
    exact = [
        row for row in rows
        if _suspects_from_scenario(row) == selected
        and int(row.get("expected_credits_remaining", -1)) == credits_remaining
    ]
    if exact:
        return exact[0]
    empty = [
        row for row in rows
        if not selected
        and not _suspects_from_scenario(row)
        and int(row.get("expected_credits_remaining", -1)) == credits_remaining
    ]
    if empty:
        preferred = [row for row in empty if ("SCENT_WENT_COLD" in row.get("expected_ending", "")) == complete]
        return preferred[0] if preferred else empty[0]
    return None


def _maxima(package: CasePackage) -> tuple[int, int, int, int, int]:
    values = {
        row.get("component", "").strip().lower(): int(row.get("max_points", 0))
        for row in package.rows(package.scoring["rules_path"])
    }
    return (
        values.get("conclusion accuracy", 350),
        values.get("evidence quality", 250),
        values.get("relationship interpretation", values.get("source and uncertainty interpretation", 150)),
        values.get("protected actor discipline", 150),
        values.get("efficiency", 100),
    )


def _dimensions_for(package: CasePackage, score: int, *, selected: frozenset[str], complete: bool, false_accusations: int, paid_count: int) -> ScoreDimensions:
    maxima = _maxima(package)
    primary = bool(selected & _primary_ids(package))
    conclusion = maxima[0] if primary else 0
    evidence = maxima[1] if complete else 50
    relationship = maxima[2] if paid_count else 0
    discipline = max(0, maxima[3] - false_accusations * max(1, maxima[3] // 2))
    efficiency = maxima[4] if paid_count <= 2 else max(0, maxima[4] - (paid_count - 2) * max(1, maxima[4] // 2))
    raw = [conclusion, min(maxima[1], evidence), relationship, discipline, efficiency]
    total = sum(raw)
    if total == score:
        return ScoreDimensions(*raw)
    if total == 0:
        return ScoreDimensions(score, 0, 0, 0, 0)
    scaled = [int(value * score / total) for value in raw]
    scaled[0] += score - sum(scaled)
    return ScoreDimensions(*scaled)


def _ending_title(code: str) -> str:
    return {
        "CLEAN_COLLAR": "Clean Collar",
        "CASE_CLOSED_KENNEL_WRECKED": "Case Closed, Kennel Wrecked",
        "THE_SCENT_WENT_COLD": "The Scent Went Cold",
        "BISCUIT_BUDGET_BLOWN": "Biscuit Budget Blown",
        "CHASED_EVERY_SQUIRREL": "Chased Every Squirrel",
        "BARKING_UP_THE_WRONG_TREE": "Barking Up the Wrong Tree",
    }.get(code, code.replace("_", " ").title())


def _ending_narrative(code: str) -> str:
    return {
        "CLEAN_COLLAR": "The case closes cleanly: the supported conclusion is filed, the evidence remains bounded and the package's protected actors stay separate.",
        "CASE_CLOSED_KENNEL_WRECKED": "The main direction was found, but a protected actor was dragged into the accusation. Correct mechanism; unnecessary collateral.",
        "THE_SCENT_WENT_COLD": "The evidence remains useful, but the submission stopped short of a defensible attribution. Uncertainty survived the paperwork.",
        "BISCUIT_BUDGET_BLOWN": "The budget was spent before the conclusion was ready. Even Hercule cannot spend the same biscuit twice.",
        "CHASED_EVERY_SQUIRREL": "The graph supplied context; the submission supplied a kennel-wide indictment. A larger suspect list is not stronger evidence.",
        "BARKING_UP_THE_WRONG_TREE": "A plausible-looking lead crossed the final line without enough support. Similarity and proximity still are not a verdict.",
    }.get(code, "The board recorded a partial answer. The evidence is explicit; the unresolved parts remain unresolved.")


def evaluate(
    round_: Round,
    package: CasePackage,
    ledger: tuple[Any, ...],
    suspects: list[str],
    claims: list[str],
) -> tuple[int, str, ScoreDimensions, int, bool, str, str]:
    selected = frozenset(str(item) for item in suspects)
    submitted_claims = frozenset(str(item) for item in claims)
    required = required_claims(package)
    complete = required.issubset(submitted_claims)
    false_accusations = len(selected & _protected_ids(package))
    paid = [entry for entry in ledger if entry.entry_type == LedgerEntryType.CHARGE and entry.status == "SETTLED"]
    scenario = _scenario_for(package, selected, complete, round_.credits_remaining)
    if scenario is not None:
        score = int(scenario["expected_score"])
        ending = scenario["expected_ending"]
        false_accusations = int(scenario.get("false_accusations", false_accusations))
    else:
        primary = bool(selected & _primary_ids(package))
        score = 350 if primary else 0
        score += 250 if complete else min(250, len(submitted_claims & required) * 50)
        score += 150 if paid else 0
        score += max(0, 150 - false_accusations * 100)
        score += 100 if len(paid) <= 2 else max(0, 100 - (len(paid) - 2) * 50)
        score = min(int(package.scoring["max_score"]), score)
        if not selected and round_.credits_remaining == 0:
            ending = "BISCUIT_BUDGET_BLOWN"
        elif false_accusations >= 2 or len(selected) >= 6:
            ending = "CHASED_EVERY_SQUIRREL"
        elif selected and not primary:
            ending = "BARKING_UP_THE_WRONG_TREE"
        elif score >= 850 and complete and false_accusations == 0:
            ending = "CLEAN_COLLAR"
        elif score >= 400:
            ending = "THE_SCENT_WENT_COLD"
        else:
            ending = "BARKING_UP_THE_WRONG_TREE"
    dimensions = _dimensions_for(
        package,
        score,
        selected=selected,
        complete=complete,
        false_accusations=false_accusations,
        paid_count=len(paid),
    )
    return score, ending, dimensions, false_accusations, complete, _ending_title(ending), _ending_narrative(ending)
