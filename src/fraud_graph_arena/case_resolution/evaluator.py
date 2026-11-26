from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from fraud_graph_arena.economy.models import LedgerEntryType
from fraud_graph_arena.economy.service import EconomyService
from fraud_graph_arena.paths import project_root
from fraud_graph_arena.rounds.domain import Round

from .models import SCORING_VERSION, ScoreDimensions


T02_TRUTH = project_root() / "case-data/canonical/v1/T2_THE_CIRCULAR_COLLAR_canonical_case_data_v3/truth"
REQUIRED_CLAIMS = frozenset({"IDENTITY_MERGE", "FALSE_MERGE_REJECTION", "DIRECTED_PAYMENT_CYCLE", "COORDINATED_ADMINISTRATION", "BENIGN_SHARED_INFRASTRUCTURE"})
PRIMARY = frozenset({"T2-P-CIPHER-A", "T2-P-CIPHER-B"})
PROTECTED = frozenset({"T2-P-CYPHER", "T2-O-BAKERY"})
ALL_PUBLISHED = frozenset({"T2-P-CIPHER-A", "T2-P-CIPHER-B", "T2-P-CYPHER", "T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA", "T2-O-BAKERY"})


def _truth_rows(name: str) -> list[dict[str, str]]:
    with (T02_TRUTH / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def required_claims() -> frozenset[str]:
    return frozenset(row["claim_id"] for row in _truth_rows("claims.csv") if row.get("required", "").lower() == "true")


def evaluate(round_: Round, ledger: tuple[Any, ...], suspects: list[str], claims: list[str]) -> tuple[int, str, ScoreDimensions, int, bool, str, str]:
    selected = frozenset(str(item) for item in suspects)
    submitted_claims = frozenset(str(item) for item in claims)
    required = required_claims()
    complete = required.issubset(submitted_claims)
    false_accusations = len(selected & PROTECTED)
    paid = [entry for entry in ledger if entry.entry_type == LedgerEntryType.CHARGE and entry.status == "SETTLED"]
    paid_count = len(paid)
    identity_runs = sum(entry.action == "COMPARE_IDENTITIES" for entry in paid)
    graph_runs = sum(entry.action == "RUN_GRAPH_ANALYSIS" for entry in paid)

    if selected == PRIMARY and complete and false_accusations == 0 and identity_runs == 1 and graph_runs == 1:
        score = 1000
        dimensions = ScoreDimensions(350, 250, 150, 150, 100)
        ending = "CLEAN_COLLAR"
        title = "Clean Collar"
        narrative = "The case closes cleanly: the supported identity joins, the false merge stays rejected, and the graph never got to call shared infrastructure guilty."
    elif PRIMARY.issubset(selected) and "T2-O-BAKERY" in selected and false_accusations == 1:
        score = 760
        dimensions = ScoreDimensions(350, 200, 130, 40, 40)
        ending = "CASE_CLOSED_KENNEL_WRECKED"
        title = "Case Closed, Kennel Wrecked"
        narrative = "The controller was found, but a legitimate tenant was dragged into the accusation. Correct direction; unnecessary collateral."
    elif not selected and complete:
        score = 520
        dimensions = ScoreDimensions(0, 250, 150, 100, 20)
        ending = "THE_SCENT_WENT_COLD"
        title = "The Scent Went Cold"
        narrative = "The connections made sense, but nobody was submitted as the controller. The evidence survived; the conclusion never arrived."
    elif not selected and round_.credits_remaining == 0:
        score = 280
        dimensions = ScoreDimensions(0, 100, 100, 80, 0)
        ending = "BISCUIT_BUDGET_BLOWN"
        title = "Biscuit Budget Blown"
        narrative = "The last credit went on another question and the case was submitted without a defensible conclusion. Even Hercule cannot spend the same biscuit twice."
    elif len(selected & PROTECTED) >= 2 or len(selected) >= 6:
        score = 120
        dimensions = ScoreDimensions(40, 30, 30, 0, 20)
        ending = "CHASED_EVERY_SQUIRREL"
        title = "Chased Every Squirrel"
        narrative = "Every connected actor became a suspect. The graph supplied context; the submission supplied a kennel-wide indictment."
    elif "T2-P-CYPHER" in selected and not PRIMARY.issubset(selected):
        score = 40
        dimensions = ScoreDimensions(0, 20, 0, 20, 0)
        ending = "BARKING_UP_THE_WRONG_TREE"
        title = "Barking Up the Wrong Tree"
        narrative = "A similar name won the final line. The records did not agree, and the submission ignored them."
    else:
        conclusion = 350 if PRIMARY.issubset(selected) else 0
        evidence = 250 if complete else min(250, len(submitted_claims & required) * 50)
        relationship = 150 if "DIRECTED_PAYMENT_CYCLE" in submitted_claims else 0
        discipline = max(0, 150 - false_accusations * 110)
        efficiency = 100 if paid_count <= 2 else max(0, 100 - (paid_count - 2) * 50)
        dimensions = ScoreDimensions(conclusion, evidence, relationship, discipline, efficiency)
        score = dimensions.total
        ending = "CLEAN_COLLAR" if score >= 850 and complete and false_accusations == 0 else "THE_SCENT_WENT_COLD" if score >= 400 else "BARKING_UP_THE_WRONG_TREE"
        title = ending.replace("_", " ").title()
        narrative = "The board recorded a partial answer. The evidence is explicit; the unresolved parts remain unresolved."
    return score, ending, dimensions, false_accusations, complete, title, narrative
