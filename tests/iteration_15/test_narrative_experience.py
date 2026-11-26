from __future__ import annotations

import copy
import json

from fraud_graph_arena.case_packages import CasePackageRegistry, validate_all_case_packages
from fraud_graph_arena.narrative import CLOSURE_VARIANTS, ComicKind, validate_narrative_manifest
from fraud_graph_arena.narrative.adapters.memory import InMemoryNarrativeRepository


def active_t02(client) -> str:
    response = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"})
    assert response.status_code == 201, response.text
    round_id = response.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete").status_code == 200
    return round_id


def test_every_published_package_has_a_valid_spoiler_safe_experience_manifest() -> None:
    results = validate_all_case_packages()

    assert results
    assert all(errors == [] for errors in results.values()), results
    registry = CasePackageRegistry()
    for package in registry.published():
        assert package.narrative["schema_version"] == "fga15-narrative-v1"
        assert set(package.narrative["closing"]["variants"]) == set(CLOSURE_VARIANTS)
        assert not any("truth" in value.lower() for value in json.dumps(package.narrative).split())
        assert all(not item["enabled"] for item in package.narrative["audio"]["assets"])


def test_narrative_asset_references_cannot_escape_the_case_package() -> None:
    package = CasePackageRegistry().require("ACADEMY_T02")
    candidate = copy.deepcopy(package.narrative)
    candidate["opening"]["panels"][0]["asset_ref"] = "truth"

    errors = validate_narrative_manifest(candidate, package_assets=package.assets)

    assert any("asset_ref" in error for error in errors)


def test_enabled_audio_requires_approved_provenance() -> None:
    package = CasePackageRegistry().require("ACADEMY_T02")
    candidate = copy.deepcopy(package.narrative)
    candidate["audio"]["assets"][0].update({"enabled": True, "file": "audio/rejected.ogg", "license": "APPROVED", "approval_status": "REJECTED"})

    errors = validate_narrative_manifest(candidate, package_assets=package.assets)

    assert any("APPROVED" in error or "approval" in error.lower() for error in errors)


def test_narrative_repository_exposes_transcripts_and_three_closure_variants() -> None:
    package = CasePackageRegistry().require("ACADEMY_T02")
    repository = InMemoryNarrativeRepository(CasePackageRegistry())
    opening = repository.get_sequence(case_id=package.case_id, case_version=package.case_version, kind=ComicKind.OPENING)
    closing = repository.get_sequence(case_id=package.case_id, case_version=package.case_version, kind=ComicKind.CLOSING)

    assert opening is not None and closing is not None
    assert opening.pages[0].accessible_transcript
    assert closing.pages_for_variant("EXCELLENT") != closing.pages_for_variant("FAILED")
    assert set(closing.variants) == set(CLOSURE_VARIANTS)
    assert closing.fictionalization_statement


def test_closing_api_exposes_media_and_transcripts_for_each_variant(client) -> None:
    round_id = active_t02(client)
    submission = client.post(f"/api/v1/rounds/{round_id}/submission", json={"idempotency_key": "fga15-closing", "suspect_record_ids": [], "evidence_claim_ids": []})
    assert submission.status_code == 200, submission.text

    response = client.get(f"/api/v1/rounds/{round_id}/closing")
    assert response.status_code == 200, response.text
    variants = response.json()["sequence"]["variants"]
    assert set(variants) == set(CLOSURE_VARIANTS)
    for pages in variants.values():
        assert all(page["image_url"] and page["alt_text"] and page["caption"] and page["transcript"] for page in pages)
