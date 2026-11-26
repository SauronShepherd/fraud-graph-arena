from __future__ import annotations

import json
from pathlib import Path

from fraud_graph_arena.case_packages import CasePackageRegistry, validate_all_case_packages, validate_case_package
from fraud_graph_arena.difficulty import validate_catalogue


def test_thirteen_packages_have_one_non_cumulative_difficulty_profile() -> None:
    registry = CasePackageRegistry()
    packages = registry.published()
    canonical = tuple(package for package in packages if package.kind == "canonical")
    assert len(packages) == 14
    assert len(canonical) == 13
    assert validate_catalogue(packages) == []
    assert {package.path_id.value for package in packages} == {"DETECTIVE_ACADEMY", "PUPPY", "ADULT_DOG", "SENIOR_DOG"}
    assert all(package.difficulty_profile.progression_mode == "PACKAGE_SINGLE_PROFILE" for package in packages)
    assert len({package.difficulty_profile.ambiguity for package in canonical}) >= 4
    assert all(package.difficulty_profile.legitimate_comparators >= 1 for package in canonical)


def test_package_schema_rejects_cumulative_levels_and_missing_comparator(tmp_path: Path) -> None:
    source = Path("case-packages/puppy-maddog/manifest.json")
    manifest = json.loads(source.read_text(encoding="utf-8"))
    manifest["difficulty_profile"]["progression_mode"] = "CUMULATIVE_LEVEL"
    manifest["difficulty_profile"]["legitimate_comparators"] = 0
    target = tmp_path / "puppy-maddog"
    target.mkdir()
    (target / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_case_package(target)
    assert any(error["check_id"] == "PACKAGE.SCHEMA" for error in errors)


def test_all_package_manifests_are_valid() -> None:
    results = validate_all_case_packages()
    assert len(results) == 14
    assert all(not errors for errors in results.values())
