from __future__ import annotations

import csv
import hashlib
from difflib import SequenceMatcher
import json
from pathlib import Path
from typing import Any, Iterable

from fraud_graph_arena.paths import project_root

from .models import ExactIdentityMatch, IdentityCandidate, NormalizedRecord, ResolutionRun
from .normalization import NORMALIZATION_VERSION, normalize_record, value

MODEL_VERSION = "fga09-deterministic-fallback-v1"
THRESHOLD_VERSION = "fga09-review-thresholds-v1"
FEATURE_CONFIG_VERSION = "fga09-identity-fields-v1"
IDENTIFIER_VALIDATION_VERSION = "fga09-identifier-contract-v1"
IDENTITY_FEATURE_FIELDS = ("given_name", "surname", "email", "phone", "identifier")
FRAMEWORK_SEMANTICS = "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE"
GENERATION_MODE = "RUNTIME_DETERMINISTIC_FALLBACK"


def load_t02_identity_records() -> list[dict[str, Any]]:
    root = project_root() / "case-data" / "canonical" / "v1" / "T2_THE_CIRCULAR_COLLAR_canonical_case_data_v3" / "published"
    with (root / "records.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _pair_id(prefix: str, left: str, right: str) -> str:
    digest = hashlib.sha256(f"{left}|{right}".encode("utf-8")).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


class EntityResolutionEngine:
    """Deterministic fallback used when a Zingg job is not available in the runtime.

    It deliberately emits player-safe reasons and never carries labels, truth, fraud
    roles, or evaluator metadata into a resolution run.
    """

    def analyze(
        self,
        raw_records: Iterable[dict[str, Any]],
        *,
        analysis_id: str,
        round_id: str,
        idempotency_key: str,
        request_hash: str,
        focus_record_id: str | None,
        charged_credits: int,
        created_at: str,
    ) -> ResolutionRun:
        records = [normalize_record(raw) for raw in raw_records]
        records = [record for record in records if record.entity_type == "PERSON"]
        records.sort(key=lambda record: record.record_id)
        if focus_record_id is not None:
            focus = next((record for record in records if record.record_id == focus_record_id), None)
            if focus is not None:
                allowed = {focus.record_id, *self._candidate_neighbours(focus, records)}
                records = [record for record in records if record.record_id in allowed]
        exact_matches: list[ExactIdentityMatch] = []
        candidates: list[IdentityCandidate] = []
        for index, left in enumerate(records):
            for right in records[index + 1 :]:
                exact_fields = self._strict_exact_fields(left, right)
                comparison = self._compare(left, right)
                candidate_signal = comparison["name_signal"] or bool(
                    set(comparison["agreements"]) & {"email", "phone", "identifier"}
                )
                if not exact_fields and not candidate_signal:
                    continue
                if exact_fields:
                    exact_matches.append(
                        ExactIdentityMatch(
                            match_id=_pair_id("EXACT", left.record_id, right.record_id),
                            left_record_id=left.record_id,
                            right_record_id=right.record_id,
                            entity_type=left.entity_type,
                            rule_id="STRICT_CONTACT_PAIR_MATCH" if "identifier" not in exact_fields else "VALIDATED_IDENTIFIER_MATCH",
                            evidence_fields=tuple(exact_fields),
                            evidence_reasons=("At least two normalized contact fields agree under the strict identity rule." if "identifier" not in exact_fields else "A validated unique identifier agrees under the strict identity rule.", "This is an identity rule match, not a fraud verdict."),
                            normalization_version=NORMALIZATION_VERSION,
                            snapshot_version=left.snapshot_version,
                            provenance_refs=tuple(ref for ref in (left.provenance_ref, right.provenance_ref) if ref),
                        )
                    )
                score = 0.99 if exact_fields else round(comparison["score"], 3)
                band = "HIGH" if score >= 0.85 else "MEDIUM" if score >= 0.40 else "LOW"
                reasons = list(comparison["reasons"])
                if exact_fields:
                    reasons.insert(0, "Strict normalized contact agreement supports an identity observation.")
                candidates.append(
                    IdentityCandidate(
                        candidate_id=_pair_id("CAND", left.record_id, right.record_id),
                        left_record_id=left.record_id,
                        right_record_id=right.record_id,
                        entity_type=left.entity_type,
                        confidence_band=band,
                        estimated_score=score,
                        agreement_fields=tuple(comparison["agreements"]),
                        disagreement_fields=tuple(comparison["disagreements"]),
                        missing_fields=tuple(comparison["missing"]),
                        evidence_reasons=tuple(reasons),
                        model_version=MODEL_VERSION,
                        threshold_version=THRESHOLD_VERSION,
                        normalization_version=NORMALIZATION_VERSION,
                        framework_semantics=FRAMEWORK_SEMANTICS,
                        generation_mode=GENERATION_MODE,
                        actual_engine_run=False,
                        review_required=not bool(exact_fields),
                        snapshot_version=left.snapshot_version,
                    )
                )
        return ResolutionRun(
            analysis_id=analysis_id,
            round_id=round_id,
            idempotency_key=idempotency_key,
            request_hash=request_hash,
            focus_record_id=focus_record_id,
            status="COMPLETED",
            charged_credits=charged_credits,
            normalization_version=NORMALIZATION_VERSION,
            model_version=MODEL_VERSION,
            threshold_version=THRESHOLD_VERSION,
            snapshot_version=records[0].snapshot_version if records else "",
            generation_mode=GENERATION_MODE,
            framework_semantics=FRAMEWORK_SEMANTICS,
            actual_engine_run=False,
            exact_matches=tuple(exact_matches),
            candidates=tuple(candidates),
            created_at=created_at,
        )

    @staticmethod
    def _candidate_neighbours(
        focus: NormalizedRecord,
        records: list[NormalizedRecord],
    ) -> set[str]:
        neighbours: set[str] = set()
        for record in records:
            if record.record_id == focus.record_id:
                continue
            exact_fields = EntityResolutionEngine._strict_exact_fields(focus, record)
            comparison = EntityResolutionEngine._compare(focus, record)
            candidate_signal = comparison["name_signal"] or bool(
                set(comparison["agreements"]) & {"email", "phone", "identifier"}
            )
            if exact_fields or candidate_signal:
                neighbours.add(record.record_id)
        return neighbours

    @staticmethod
    def _strict_exact_fields(left: NormalizedRecord, right: NormalizedRecord) -> list[str]:
        fields: list[str] = []
        for field in ("email", "phone"):
            left_value, right_value = value(left, field), value(right, field)
            if left_value is not None and left_value == right_value:
                fields.append(field)
        # A single shared contact field is a candidate signal, not an exact
        # identity assertion. T02's golden pair has both contact fields; a
        # validated unique identifier is the only single-field exception.
        identifier_left, identifier_right = value(left, "identifier"), value(right, "identifier")
        if (
            identifier_left is not None
            and identifier_left == identifier_right
            and left.identifier_validated
            and right.identifier_validated
        ):
            fields.append("identifier")
        return fields if len(fields) >= 2 or "identifier" in fields else []

    @staticmethod
    def _compare(left: NormalizedRecord, right: NormalizedRecord) -> dict[str, Any]:
        agreements: list[str] = []
        disagreements: list[str] = []
        missing: list[str] = []
        name_signal = False
        surname = value(left, "surname"), value(right, "surname")
        if surname[0] is None or surname[1] is None:
            missing.append("surname")
        elif surname[0] == surname[1]:
            agreements.append("surname")
            name_signal = True
        else:
            disagreements.append("surname")
        given = value(left, "given_name"), value(right, "given_name")
        if given[0] is None or given[1] is None:
            missing.append("given_name")
        else:
            ratio = SequenceMatcher(None, given[0], given[1]).ratio()
            if ratio >= 0.72:
                agreements.append("similar_given_name")
                name_signal = True
            else:
                disagreements.append("given_name")
        for field in ("email", "phone", "identifier"):
            left_value, right_value = value(left, field), value(right, field)
            if left_value is None or right_value is None:
                missing.append(field)
            elif left_value == right_value:
                agreements.append(field)
            else:
                disagreements.append(field)
        name_score = 0.0
        if "surname" in agreements:
            name_score += 0.25
        if "similar_given_name" in agreements:
            name_score += 0.25
        contact_score = 0.0
        if "email" in agreements:
            contact_score += 0.25
        if "phone" in agreements:
            contact_score += 0.25
        score = min(1.0, name_score + contact_score)
        reasons = []
        if name_signal:
            reasons.append("Normalized name fields are similar.")
        if "email" in disagreements or "phone" in disagreements:
            reasons.append("Contact fields disagree; review is required.")
        if not reasons:
            reasons.append("No sufficient shared identity evidence was found.")
        return {
            "agreements": agreements,
            "disagreements": disagreements,
            "missing": missing,
            "score": score,
            "name_signal": name_signal,
            "reasons": reasons,
        }

