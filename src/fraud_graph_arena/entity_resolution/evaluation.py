"""Offline-only evaluation fixtures for the FGA-09 identity slice.

This module is intentionally not imported by the web application. Its labels
are synthetic canonical truth for regression measurement, not player evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .engine import (
    FEATURE_CONFIG_VERSION,
    IDENTIFIER_VALIDATION_VERSION,
    EntityResolutionEngine,
    MODEL_VERSION,
    THRESHOLD_VERSION,
    load_t02_identity_records,
)
from .normalization import NORMALIZATION_VERSION

LABEL_SET_VERSION = "fga09-t02-labels-v1"
EVALUATION_SEED = 90209


@dataclass(frozen=True, slots=True)
class EvaluationExample:
    case_id: str
    left_record_id: str
    right_record_id: str
    expected_same_entity: bool
    difficulty: str

    @property
    def pair(self) -> tuple[str, str]:
        return tuple(sorted((self.left_record_id, self.right_record_id)))


@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    dataset_version: str
    label_set_version: str
    feature_config_version: str
    identifier_validation_version: str
    seed: int
    normalization_version: str
    model_version: str
    threshold_version: str
    threshold_band: str
    actual_engine_run: bool
    training_label_count: int
    training_positive_count: int
    training_negative_count: int
    balanced_training_labels: bool
    leakage_safe: bool
    true_positives: int
    true_negatives: int
    false_merges: int
    false_splits: int
    precision: float
    recall: float
    per_case: dict[str, dict[str, float | int]]
    per_difficulty: dict[str, dict[str, float | int]]
    regression_pass: bool


def t02_evaluation_examples() -> tuple[EvaluationExample, ...]:
    """Return synthetic labels kept outside the player-facing path."""
    return (
        EvaluationExample("ACADEMY_T02", "T2-P-CIPHER-A", "T2-P-CIPHER-B", True, "GOLDEN_MATCH"),
        EvaluationExample("ACADEMY_T02", "T2-P-CIPHER-A", "T2-P-CYPHER", False, "HARD_NEGATIVE"),
        EvaluationExample("ACADEMY_T02", "T2-P-CIPHER-B", "T2-P-CYPHER", False, "HARD_NEGATIVE"),
    )


def t02_training_examples() -> tuple[EvaluationExample, ...]:
    """Return a balanced synthetic training-label manifest, never player data."""
    return (
        EvaluationExample("FGA09_TRAINING_FIXTURE", "TRAIN-PERSON-A", "TRAIN-PERSON-B", True, "TRAIN_POSITIVE"),
        EvaluationExample("FGA09_TRAINING_FIXTURE", "TRAIN-PERSON-A", "TRAIN-PERSON-C", False, "TRAIN_HARD_NEGATIVE"),
    )


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 3) if denominator else 0.0


def _summary(examples: Iterable[EvaluationExample], predictions: dict[tuple[str, str], bool]) -> dict[str, float | int]:
    items = tuple(examples)
    true_positives = sum(predictions.get(item.pair, False) and item.expected_same_entity for item in items)
    true_negatives = sum((not predictions.get(item.pair, False)) and (not item.expected_same_entity) for item in items)
    false_merges = sum(predictions.get(item.pair, False) and not item.expected_same_entity for item in items)
    false_splits = sum((not predictions.get(item.pair, False)) and item.expected_same_entity for item in items)
    correct = true_positives + true_negatives
    return {
        "total": len(items),
        "correct": int(correct),
        "true_positives": int(true_positives),
        "true_negatives": int(true_negatives),
        "false_merges": int(false_merges),
        "false_splits": int(false_splits),
        "precision": _rate(int(true_positives), int(true_positives + false_merges)),
        "recall": _rate(int(true_positives), int(true_positives + false_splits)),
        "accuracy": _rate(int(correct), len(items)),
    }


def _bucket(examples: Iterable[EvaluationExample], predictions: dict[tuple[str, str], bool], field: str) -> dict[str, dict[str, float | int]]:
    result: dict[str, list[EvaluationExample]] = {}
    for example in examples:
        result.setdefault(getattr(example, field), []).append(example)
    return {key: _summary(items, predictions) for key, items in result.items()}


def evaluate_t02() -> EvaluationMetrics:
    training_examples = t02_training_examples()
    examples = t02_evaluation_examples()
    run = EntityResolutionEngine().analyze(
        load_t02_identity_records(),
        analysis_id="offline-evaluation",
        round_id="offline",
        idempotency_key="offline-evaluation",
        request_hash="offline-evaluation",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-01-01T00:00:00+00:00",
    )
    candidates = {tuple(sorted((candidate.left_record_id, candidate.right_record_id))): candidate for candidate in run.candidates}
    predictions = {
        example.pair: bool(candidates.get(example.pair) and candidates[example.pair].confidence_band == "HIGH")
        for example in examples
    }
    true_positives = sum(predictions[example.pair] and example.expected_same_entity for example in examples)
    true_negatives = sum((not predictions[example.pair]) and (not example.expected_same_entity) for example in examples)
    false_merges = sum(predictions[example.pair] and not example.expected_same_entity for example in examples)
    false_splits = sum((not predictions[example.pair]) and example.expected_same_entity for example in examples)
    per_case = _bucket(examples, predictions, "case_id")
    per_difficulty = _bucket(examples, predictions, "difficulty")
    training_positive_count = sum(example.expected_same_entity for example in training_examples)
    training_negative_count = len(training_examples) - training_positive_count
    training_pairs = {example.pair for example in training_examples}
    matching_pairs = {example.pair for example in examples}
    training_record_ids = {
        record_id
        for example in training_examples
        for record_id in (example.left_record_id, example.right_record_id)
    }
    matching_record_ids = {
        record_id
        for example in examples
        for record_id in (example.left_record_id, example.right_record_id)
    }
    balanced_training_labels = training_positive_count == training_negative_count
    leakage_safe = (
        training_pairs.isdisjoint(matching_pairs)
        and training_record_ids.isdisjoint(matching_record_ids)
    )
    return EvaluationMetrics(
        dataset_version="fga09-t02-matching-dataset-v1",
        label_set_version=LABEL_SET_VERSION,
        feature_config_version=FEATURE_CONFIG_VERSION,
        identifier_validation_version=IDENTIFIER_VALIDATION_VERSION,
        seed=EVALUATION_SEED,
        normalization_version=NORMALIZATION_VERSION,
        model_version=MODEL_VERSION,
        threshold_version=THRESHOLD_VERSION,
        threshold_band="HIGH",
        actual_engine_run=run.actual_engine_run,
        training_label_count=len(training_examples),
        training_positive_count=int(training_positive_count),
        training_negative_count=int(training_negative_count),
        balanced_training_labels=balanced_training_labels,
        leakage_safe=leakage_safe,
        true_positives=int(true_positives),
        true_negatives=int(true_negatives),
        false_merges=int(false_merges),
        false_splits=int(false_splits),
        precision=_rate(int(true_positives), int(true_positives + false_merges)),
        recall=_rate(int(true_positives), int(true_positives + false_splits)),
        per_case=per_case,
        per_difficulty=per_difficulty,
        regression_pass=(
            balanced_training_labels
            and leakage_safe
            and true_positives == 1
            and false_merges == 0
            and false_splits == 0
        ),
    )


def metrics_to_dict(metrics: EvaluationMetrics) -> dict:
    return asdict(metrics)

