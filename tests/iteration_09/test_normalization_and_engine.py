from __future__ import annotations

from dataclasses import asdict

from fraud_graph_arena.entity_resolution import evaluation as evaluation_module
from fraud_graph_arena.entity_resolution.engine import (
    FEATURE_CONFIG_VERSION,
    IDENTIFIER_VALIDATION_VERSION,
    IDENTITY_FEATURE_FIELDS,
    EntityResolutionEngine,
    load_t02_identity_records,
)
from fraud_graph_arena.entity_resolution.evaluation import EvaluationExample, evaluate_t02
from fraud_graph_arena.entity_resolution.normalization import (
    NORMALIZATION_VERSION,
    PLACEHOLDER_REGISTRY_VERSION,
    normalize_record,
    normalize_value,
)


def test_normalization_is_unicode_aware_idempotent_and_preserves_invalid_classification() -> None:
    value = normalize_value("given_name", "  C.  ")
    assert value.normalized == "c"
    assert value.original == "  C.  "
    assert normalize_value("given_name", value.normalized).normalized == value.normalized
    accented = normalize_value("given_name", " Élodie ")
    assert accented.normalized == "élodie"
    assert normalize_value("given_name", accented.normalized).normalized == accented.normalized
    compatibility_variant = normalize_value("given_name", " Ｆｌｕｆｆｙ ")
    assert compatibility_variant.normalized == "fluffy"
    ligature = normalize_value("given_name", "Oﬃcer")
    assert ligature.normalized == "officer"
    assert normalize_value("email", "not-an-email").classification == "INVALID"
    assert normalize_value("phone", "123").classification == "INVALID"
    assert normalize_value("phone", "+1 (555) 0204").normalized == "15550204"
    assert normalize_value("phone", "000000").classification == "PLACEHOLDER"
    assert NORMALIZATION_VERSION.startswith("fga09-")
    assert PLACEHOLDER_REGISTRY_VERSION.startswith("fga09-")
    assert FEATURE_CONFIG_VERSION == "fga09-identity-fields-v1"
    assert IDENTIFIER_VALIDATION_VERSION == "fga09-identifier-contract-v1"
    assert IDENTITY_FEATURE_FIELDS == ("given_name", "surname", "email", "phone", "identifier")


def test_placeholders_never_become_contact_agreement_or_exact_identity() -> None:
    records = [
        {
            "record_id": "P-PLACEHOLDER-A",
            "record_type": "PERSON_RECORD",
            "display_label": "Luna Corgi",
            "snapshot_version": "snap-1",
            "safe_attributes_json": '{"given_name":"Luna","surname":"Corgi","email":"N/A","phone":"000-000-0000"}',
        },
        {
            "record_id": "P-PLACEHOLDER-B",
            "record_type": "PERSON_RECORD",
            "display_label": "L. Corgi",
            "snapshot_version": "snap-1",
            "safe_attributes_json": '{"given_name":"L.","surname":"Corgi","email":"n / a","phone":"0000000000"}',
        },
    ]
    run = EntityResolutionEngine().analyze(
        records,
        analysis_id="placeholder-analysis",
        round_id="round-1",
        idempotency_key="placeholder-key",
        request_hash="placeholder-hash",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert run.exact_matches == ()
    candidate = next(item for item in run.candidates)
    assert "email" not in candidate.agreement_fields
    assert "phone" not in candidate.agreement_fields


def test_record_keeps_only_identity_features_and_original_presence_without_player_values() -> None:
    record = normalize_record({
        "record_id": "P1",
        "record_type": "PERSON_RECORD",
        "display_label": "C. Corgi",
        "provenance_ref": "source:P1",
        "snapshot_version": "snap-1",
        "safe_attributes_json": '{"given_name":"C.","email":"cipher@example.test","device_id":"dev-1","fraud_role":"hidden"}',
    })
    assert record.fields["given_name"].original_present is True
    assert "fraud_role" not in record.fields
    assert "device_id" in record.fields


def test_golden_match_and_hard_negative_are_separate_player_safe_observations() -> None:
    engine = EntityResolutionEngine()
    run = engine.analyze(
        load_t02_identity_records(),
        analysis_id="analysis-1",
        round_id="round-1",
        idempotency_key="key-1",
        request_hash="hash-1",
        focus_record_id="T2-P-CIPHER-A",
        charged_credits=3,
        created_at="2026-11-16T00:00:00+00:00",
    )
    golden = next(item for item in run.candidates if {item.left_record_id, item.right_record_id} == {"T2-P-CIPHER-A", "T2-P-CIPHER-B"})
    hard_negative = next(item for item in run.candidates if {item.left_record_id, item.right_record_id} == {"T2-P-CIPHER-A", "T2-P-CYPHER"})
    assert golden.confidence_band == "HIGH"
    assert {"email", "phone"}.issubset(golden.agreement_fields)
    assert hard_negative.confidence_band == "MEDIUM"
    assert {"email", "phone"}.issubset(hard_negative.disagreement_fields)
    assert hard_negative.review_required is True
    assert run.actual_engine_run is False
    assert not any("truth" in key.lower() or "fraud" in key.lower() for key in asdict(hard_negative))
    first_feature_fields = set(IDENTITY_FEATURE_FIELDS)
    assert not first_feature_fields.intersection({"address", "device_id", "ip", "fraud_role", "culpability"})


def test_single_shared_contact_field_is_a_review_candidate_not_an_exact_match() -> None:
    run = EntityResolutionEngine().analyze(
        [
            {
                "record_id": "P-SHARED-EMAIL-A",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Corgi","email":"shared@example.test","phone":"+1-555-0001"}',
            },
            {
                "record_id": "P-SHARED-EMAIL-B",
                "record_type": "PERSON_RECORD",
                "display_label": "Bert Hound",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Bert","surname":"Hound","email":"shared@example.test","phone":"+1-555-0002"}',
            },
        ],
        analysis_id="shared-email-analysis",
        round_id="round-1",
        idempotency_key="shared-email-key",
        request_hash="shared-email-hash",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert run.exact_matches == ()
    candidate = next(item for item in run.candidates)
    assert candidate.agreement_fields == ("email",)
    assert candidate.review_required is True
    assert candidate.confidence_band == "LOW"

    missing_phone_run = EntityResolutionEngine().analyze(
        [
            {
                "record_id": "P-MISSING-PHONE-A",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Corgi","email":"shared@example.test"}',
            },
            {
                "record_id": "P-MISSING-PHONE-B",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Hound",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Hound","email":"shared@example.test","phone":"+1-555-0002"}',
            },
        ],
        analysis_id="missing-phone-analysis",
        round_id="round-1",
        idempotency_key="missing-phone-key",
        request_hash="missing-phone-hash",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    missing_phone_candidate = next(item for item in missing_phone_run.candidates)
    assert "phone" in missing_phone_candidate.missing_fields
    assert "phone" not in missing_phone_candidate.disagreement_fields


def test_focused_analysis_keeps_cross_surname_shared_contact_candidates() -> None:
    run = EntityResolutionEngine().analyze(
        [
            {
                "record_id": "P-CROSS-SURNAME-A",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Corgi","email":"shared@example.test","phone":"+1-555-0001"}',
            },
            {
                "record_id": "P-CROSS-SURNAME-B",
                "record_type": "PERSON_RECORD",
                "display_label": "Bert Hound",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Bert","surname":"Hound","email":"shared@example.test","phone":"+1-555-0002"}',
            },
        ],
        analysis_id="cross-surname-analysis",
        round_id="round-1",
        idempotency_key="cross-surname-key",
        request_hash="cross-surname-hash",
        focus_record_id="P-CROSS-SURNAME-A",
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert len(run.candidates) == 1
    assert {run.candidates[0].left_record_id, run.candidates[0].right_record_id} == {
        "P-CROSS-SURNAME-A",
        "P-CROSS-SURNAME-B",
    }
    assert run.exact_matches == ()


def test_duplicate_identifier_is_candidate_evidence_not_a_validated_exact_match() -> None:
    run = EntityResolutionEngine().analyze(
        [
            {
                "record_id": "P-DUPLICATE-ID-A",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Corgi","identifier":"shared-id","email":"ada@example.test","phone":"+1-555-0001"}',
            },
            {
                "record_id": "P-DUPLICATE-ID-B",
                "record_type": "PERSON_RECORD",
                "display_label": "Bert Hound",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Bert","surname":"Hound","identifier":"shared-id","email":"bert@example.test","phone":"+1-555-0002"}',
            },
        ],
        analysis_id="duplicate-identifier-analysis",
        round_id="round-1",
        idempotency_key="duplicate-identifier-key",
        request_hash="duplicate-identifier-hash",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert run.exact_matches == ()
    assert len(run.candidates) == 1
    assert run.candidates[0].agreement_fields == ("identifier",)
    assert run.candidates[0].review_required is True


def test_source_validated_identifier_can_be_a_single_field_exact_match() -> None:
    run = EntityResolutionEngine().analyze(
        [
            {
                "record_id": "P-VALIDATED-ID-A",
                "record_type": "PERSON_RECORD",
                "display_label": "Ada Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"Ada","surname":"Corgi","identifier":"verified-id","identifier_validated":true,"email":"ada@example.test"}',
            },
            {
                "record_id": "P-VALIDATED-ID-B",
                "record_type": "PERSON_RECORD",
                "display_label": "A. Corgi",
                "snapshot_version": "snap-1",
                "safe_attributes_json": '{"given_name":"A.","surname":"Corgi","identifier":"verified-id","identifier_validated":true,"email":"other@example.test"}',
            },
        ],
        analysis_id="validated-identifier-analysis",
        round_id="round-1",
        idempotency_key="validated-identifier-key",
        request_hash="validated-identifier-hash",
        focus_record_id=None,
        charged_credits=0,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert len(run.exact_matches) == 1
    assert run.exact_matches[0].rule_id == "VALIDATED_IDENTIFIER_MATCH"
    assert run.exact_matches[0].evidence_fields == ("identifier",)


def test_shared_infrastructure_is_not_an_exact_identity_rule() -> None:
    run = EntityResolutionEngine().analyze(
        load_t02_identity_records(),
        analysis_id="analysis-2",
        round_id="round-1",
        idempotency_key="key-2",
        request_hash="hash-2",
        focus_record_id=None,
        charged_credits=3,
        created_at="2026-11-16T00:00:00+00:00",
    )
    assert all(match.left_record_id.startswith("T2-P-") and match.right_record_id.startswith("T2-P-") for match in run.exact_matches)
    assert all(match.left_record_id < match.right_record_id for match in run.exact_matches)
    assert len({match.match_id for match in run.exact_matches}) == len(run.exact_matches)
    assert not any("address" in field or "device" in field or "ip" in field for match in run.exact_matches for field in match.evidence_fields)


def test_offline_evaluation_is_reproducible_and_keeps_hard_negative_clean() -> None:
    first = evaluate_t02()
    second = evaluate_t02()
    assert first == second
    assert first.precision == 1.0
    assert first.recall == 1.0
    assert first.false_merges == 0
    assert first.false_splits == 0
    assert first.training_label_count == 2
    assert first.training_positive_count == first.training_negative_count == 1
    assert first.balanced_training_labels is True
    assert first.leakage_safe is True
    assert first.identifier_validation_version == "fga09-identifier-contract-v1"
    assert first.per_difficulty["HARD_NEGATIVE"]["false_merges"] == 0
    assert first.regression_pass is True
    assert first.actual_engine_run is False


def test_regression_gate_rejects_unbalanced_training_manifest(monkeypatch) -> None:
    monkeypatch.setattr(
        evaluation_module,
        "t02_training_examples",
        lambda: (
            EvaluationExample("TRAINING", "TRAIN-PERSON-A", "TRAIN-PERSON-B", True, "TRAIN_POSITIVE"),
            EvaluationExample("TRAINING", "TRAIN-PERSON-C", "TRAIN-PERSON-D", True, "TRAIN_POSITIVE"),
        ),
    )
    metrics = evaluation_module.evaluate_t02()

    assert metrics.balanced_training_labels is False
    assert metrics.leakage_safe is True
    assert metrics.regression_pass is False


def test_regression_gate_rejects_a_pair_leaky_training_manifest(monkeypatch) -> None:
    monkeypatch.setattr(
        evaluation_module,
        "t02_training_examples",
        lambda: (
            EvaluationExample("TRAINING", "T2-P-CIPHER-A", "T2-P-CIPHER-B", True, "TRAIN_POSITIVE"),
            EvaluationExample("TRAINING", "TRAIN-PERSON-C", "TRAIN-PERSON-D", False, "TRAIN_HARD_NEGATIVE"),
        ),
    )
    metrics = evaluation_module.evaluate_t02()

    assert metrics.balanced_training_labels is True
    assert metrics.leakage_safe is False
    assert metrics.regression_pass is False


def test_regression_gate_rejects_record_id_leakage_even_when_pairs_are_disjoint(monkeypatch) -> None:
    monkeypatch.setattr(
        evaluation_module,
        "t02_training_examples",
        lambda: (
            EvaluationExample("TRAINING", "T2-P-CIPHER-A", "TRAIN-PERSON-B", True, "TRAIN_POSITIVE"),
            EvaluationExample("TRAINING", "TRAIN-PERSON-C", "TRAIN-PERSON-D", False, "TRAIN_HARD_NEGATIVE"),
        ),
    )
    metrics = evaluation_module.evaluate_t02()

    assert metrics.balanced_training_labels is True
    assert metrics.leakage_safe is False
    assert metrics.regression_pass is False
