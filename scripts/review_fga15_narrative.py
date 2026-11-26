"""Run the FGA-15 narrative manifest, accessibility and fallback review locally."""

from __future__ import annotations

from datetime import UTC, datetime
import copy
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.case_packages import CasePackageRegistry, validate_case_package  # noqa: E402
from fraud_graph_arena.narrative import CLOSURE_VARIANTS, ComicKind  # noqa: E402
from fraud_graph_arena.narrative.adapters.memory import InMemoryNarrativeRepository  # noqa: E402
from fraud_graph_arena.narrative.manifest import validate_narrative_manifest  # noqa: E402


def _fixture_errors() -> list[str]:
    package = CasePackageRegistry().require("ACADEMY_T02")
    missing_asset = copy.deepcopy(package.narrative)
    missing_asset["opening"]["panels"][0]["asset_ref"] = "not-declared"
    missing_file = copy.deepcopy(package.narrative)
    missing_file["audio"]["assets"][0].update({"enabled": True, "file": None, "license": "NOT_SHIPPED"})
    errors: list[str] = []
    if not any("asset_ref" in item for item in validate_narrative_manifest(missing_asset, package_assets=package.assets)):
        errors.append("undeclared asset reference was accepted")
    if not any("enabled audio requires a shipped file" in item for item in validate_narrative_manifest(missing_file, package_assets=package.assets)):
        errors.append("enabled audio without a file was accepted")
    return errors


def review_packages() -> list[dict[str, Any]]:
    registry = CasePackageRegistry()
    repository = InMemoryNarrativeRepository(registry)
    reports: list[dict[str, Any]] = []
    for package in registry.published():
        errors = validate_case_package(package.package_dir)
        opening = repository.get_sequence(case_id=package.case_id, case_version=package.case_version, kind=ComicKind.OPENING)
        closing = repository.get_sequence(case_id=package.case_id, case_version=package.case_version, kind=ComicKind.CLOSING)
        checks = {
            "manifest_valid": not errors,
            "opening_transcripts": opening is not None and all(page.accessible_transcript for page in opening.pages),
            "opening_alt_text": opening is not None and all(page.alt_text for page in opening.pages),
            "closure_variants": closing is not None and set(closing.variants) == set(CLOSURE_VARIANTS),
            "closure_variants_are_distinct": closing is not None and len({page.accessible_transcript for pages in closing.variants.values() for page in pages}) == len(closing.variants),
            "fictionalization_boundary": bool(opening and closing and opening.fictionalization_statement == closing.fictionalization_statement),
            "optional_audio_is_safe": all(not item["enabled"] or (item["file"] and item["license"] == "APPROVED") for item in package.narrative["audio"]["assets"]),
        }
        reports.append({"package_id": package.package_id, "case_id": package.case_id, "status": "PASS" if all(checks.values()) and not errors else "FAIL", "checks": checks, "manifest_errors": errors})
    return reports


def main() -> int:
    reports = review_packages()
    fixture_errors = _fixture_errors()
    payload = {
        "status": "pass" if not fixture_errors and all(item["status"] == "PASS" for item in reports) else "fail",
        "iteration": "FGA15",
        "review_version": "fga15-narrative-review-v1",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "package_count": len(reports),
        "fixture_errors": fixture_errors,
        "packages": reports,
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    report_path = ROOT / "reports/iteration-15/fga15-narrative-review.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
