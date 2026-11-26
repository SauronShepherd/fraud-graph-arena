from __future__ import annotations

import copy
import json

from fraud_graph_arena.case_packages import CasePackageRegistry, validate_all_case_packages
from fraud_graph_arena.narrative import CLOSURE_VARIANTS, ComicKind, validate_narrative_manifest
from fraud_graph_arena.narrative.adapters.memory import InMemoryNarrativeRepository


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
