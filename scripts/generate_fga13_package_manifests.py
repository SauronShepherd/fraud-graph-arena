"""Generate the FGA-13 package catalogue from the approved canonical corpus.

The canonical CSV packages remain the data authority.  This authoring step adds
the player-facing package contract and one non-cumulative difficulty vector per
dataset; it never copies protected truth into the package manifest.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from generate_fga15_narrative_manifests import narrative as fga15_narrative

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ROOT = ROOT / "case-data/canonical/v1"
ASSET_PREFIX = "fga/13-puppy-love-adult-problems"
PATH_IDS = {
    "ACADEMY": "DETECTIVE_ACADEMY",
    "PUPPY": "PUPPY",
    "ADULT": "ADULT_DOG",
    "SENIOR": "SENIOR_DOG",
}
PACKAGE_IDS = {
    "ACADEMY_T01": "academy-t01",
    "ACADEMY_T02": "academy-t02",
    "ACADEMY_T03": "academy-t03",
    "MADDOG": "puppy-maddog",
    "CEO_BARKED_TWICE": "puppy-ceo-barked-twice",
    "BISCUIT_RELIEF": "puppy-biscuit-relief",
    "BONE_LEDGER": "adult-bone-ledger",
    "DOWNLINE": "adult-downline",
    "PHANTOM_VET": "adult-phantom-vet",
    "GOLDEN_HYDRANT": "adult-golden-hydrant",
    "LOVE_LEASHES_OFFSHORE": "senior-love-leashes-offshore",
    "CRYPTO_KENNEL_LONG_CON": "senior-crypto-kennel-long-con",
    "PANAMA_PAWPERS": "senior-panama-pawpers",
}
LEGACY_PACKAGE_VERSIONS = {"ACADEMY_T02": "1.0.0-fga06", "ACADEMY_T03": "1.0.0-fga12"}
LEGACY_ECONOMY_VERSIONS = {"ACADEMY_T02": "fga11-economy-v1", "ACADEMY_T03": "fga12-economy-v1"}
LEGACY_SCORING_VERSIONS = {"ACADEMY_T02": "fga11-scoring-v1", "ACADEMY_T03": "fga12-scoring-v1"}

# These are authoring expectations, not an attempt to hide the dimensions behind
# a score.  They are intentionally per case so a larger graph cannot automatically
# win the difficulty argument.
DIFFICULTY = {
    "ACADEMY_T01": dict(ambiguity=0, noise=0, graph_depth=1, evidence_quality="GUIDED", resource_pressure=0, mixed_roles=False, legitimate_comparators=1, session_minutes=10, action_budget=5, graph_node_limit=20, hypothesis_target=0, evidence_threshold=2),
    "ACADEMY_T02": dict(ambiguity=1, noise=1, graph_depth=2, evidence_quality="CLEAR", resource_pressure=1, mixed_roles=False, legitimate_comparators=1, session_minutes=15, action_budget=8, graph_node_limit=30, hypothesis_target=1, evidence_threshold=3),
    "ACADEMY_T03": dict(ambiguity=2, noise=2, graph_depth=3, evidence_quality="MIXED", resource_pressure=2, mixed_roles=False, legitimate_comparators=2, session_minutes=20, action_budget=10, graph_node_limit=40, hypothesis_target=1, evidence_threshold=4),
    "MADDOG": dict(ambiguity=2, noise=1, graph_depth=2, evidence_quality="CLEAR", resource_pressure=1, mixed_roles=False, legitimate_comparators=1, session_minutes=20, action_budget=10, graph_node_limit=100, hypothesis_target=1, evidence_threshold=3),
    "CEO_BARKED_TWICE": dict(ambiguity=2, noise=2, graph_depth=2, evidence_quality="CLEAR", resource_pressure=2, mixed_roles=True, legitimate_comparators=1, session_minutes=22, action_budget=12, graph_node_limit=120, hypothesis_target=1, evidence_threshold=3),
    "BISCUIT_RELIEF": dict(ambiguity=3, noise=2, graph_depth=3, evidence_quality="MIXED", resource_pressure=2, mixed_roles=True, legitimate_comparators=2, session_minutes=24, action_budget=13, graph_node_limit=140, hypothesis_target=2, evidence_threshold=4),
    "BONE_LEDGER": dict(ambiguity=3, noise=3, graph_depth=3, evidence_quality="MIXED", resource_pressure=3, mixed_roles=True, legitimate_comparators=2, session_minutes=30, action_budget=16, graph_node_limit=180, hypothesis_target=2, evidence_threshold=5),
    "DOWNLINE": dict(ambiguity=4, noise=3, graph_depth=4, evidence_quality="MIXED", resource_pressure=3, mixed_roles=True, legitimate_comparators=2, session_minutes=32, action_budget=18, graph_node_limit=220, hypothesis_target=2, evidence_threshold=5),
    "PHANTOM_VET": dict(ambiguity=4, noise=4, graph_depth=4, evidence_quality="CONFLICTED", resource_pressure=4, mixed_roles=True, legitimate_comparators=3, session_minutes=34, action_budget=20, graph_node_limit=240, hypothesis_target=3, evidence_threshold=6),
    "GOLDEN_HYDRANT": dict(ambiguity=3, noise=3, graph_depth=4, evidence_quality="MIXED", resource_pressure=3, mixed_roles=True, legitimate_comparators=2, session_minutes=30, action_budget=17, graph_node_limit=200, hypothesis_target=2, evidence_threshold=5),
    "LOVE_LEASHES_OFFSHORE": dict(ambiguity=5, noise=4, graph_depth=5, evidence_quality="CONFLICTED", resource_pressure=3, mixed_roles=True, legitimate_comparators=3, session_minutes=38, action_budget=22, graph_node_limit=260, hypothesis_target=3, evidence_threshold=7),
    "CRYPTO_KENNEL_LONG_CON": dict(ambiguity=4, noise=5, graph_depth=5, evidence_quality="CONFLICTED", resource_pressure=4, mixed_roles=True, legitimate_comparators=3, session_minutes=40, action_budget=24, graph_node_limit=280, hypothesis_target=3, evidence_threshold=7),
    "PANAMA_PAWPERS": dict(ambiguity=5, noise=5, graph_depth=5, evidence_quality="FRAGMENTED", resource_pressure=5, mixed_roles=True, legitimate_comparators=4, session_minutes=42, action_budget=26, graph_node_limit=300, hypothesis_target=4, evidence_threshold=8),
}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _canonical_cases() -> dict[str, tuple[Path, dict[str, str], dict[str, str], dict[str, str]]]:
    found: dict[str, tuple[Path, dict[str, str], dict[str, str], dict[str, str]]] = {}
    for root in sorted(CANONICAL_ROOT.iterdir()):
        if not root.is_dir():
            continue
        cases = _read_rows(root / "config/cases.csv")
        profiles = _read_rows(root / "config/case_profiles.csv")
        if len(cases) != 1 or len(profiles) != 1:
            raise ValueError(f"expected one case and one profile in {root.name}")
        canonical_manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        found[cases[0]["case_id"]] = (root, cases[0], profiles[0], canonical_manifest)
    return found


def _profile(case_id: str, path_id: str) -> dict[str, object]:
    values = {"profile_version": "fga13-difficulty-profile-v1", "path_id": path_id, **DIFFICULTY[case_id], "progression_mode": "PACKAGE_SINGLE_PROFILE"}
    return values


def _manifest(case_id: str, root: Path, case: dict[str, str], profile: dict[str, str], canonical: dict[str, str]) -> dict[str, object]:
    path_code = case["path_code"]
    path_id = PATH_IDS[path_code]
    package_version = "1.0.0-fga13" if path_code != "PUPPY" else "1.1.0-fga13"
    case_version = LEGACY_PACKAGE_VERSIONS.get(case_id, f"{case['case_version']}-fga13")
    supported = ["COMPARE_IDENTITIES", "CREATE_HYPOTHESIS", "RUN_GRAPH_ANALYSIS", "SUBMIT"]
    if path_code == "ACADEMY":
        supported = {"ACADEMY_T01": ["RUN_GRAPH_ANALYSIS", "SUBMIT"], "ACADEMY_T02": supported, "ACADEMY_T03": ["RUN_GRAPH_ANALYSIS", "SUBMIT"]}[case_id]
    costs: dict[str, int] = {}
    if "COMPARE_IDENTITIES" in supported and int(profile["zingg_cost"]):
        costs["COMPARE_IDENTITIES"] = int(profile["zingg_cost"])
    if "RUN_GRAPH_ANALYSIS" in supported and int(profile["graphframes_cost"]):
        costs["RUN_GRAPH_ANALYSIS"] = int(profile["graphframes_cost"])
    descriptions = {
        "ACADEMY_T01": "A guided Academy file for learning a bounded evidence trail without treating a first lead as a verdict.",
        "ACADEMY_T02": "A spoiler-free graph lesson about records, organizations, and directed source relationships.",
        "ACADEMY_T03": "An advanced Academy file where chronology, unavailable evidence and uncertainty matter more than a loud accusation.",
    }
    description = descriptions.get(case_id, f"A synthetic {path_code.title()} case whose challenge is described by a tested difficulty profile, not by row count.")
    manifest = {
        "schema_version": "fga13-case-package-v1",
        "package_id": PACKAGE_IDS[case_id],
        "package_version": package_version,
        "case_id": case_id,
        "case_version": case_version,
        "path_id": path_id,
        "title": case["title"],
        "description": description,
        "kind": "canonical",
        "briefing": {"opening_sequence_id": f"{case_id}_OPENING", "closing_sequence_id": f"{case_id}_CLOSING"},
        "canonical": {"root": f"case-data/canonical/v1/{root.name}", "case_id": canonical["case_id"], "case_version": canonical["case_version"], "snapshot_version": canonical["snapshot_version"], "model_version": canonical["canonical_model_version"]},
        "objectives": [
            "Inspect the published evidence and its provenance.",
            "Compare competing explanations without treating similarity as guilt.",
            "Submit a reproducible conclusion that leaves legitimate comparators visible.",
        ],
        "supported_actions": supported,
        "economy": {"version": LEGACY_ECONOMY_VERSIONS.get(case_id, "fga13-economy-v1"), "initial_credits": int(profile["starting_credits"]), "costs": costs},
        "evidence_rules": {"public_projection": "published", "protected_truth": "truth", "required_claims_path": "truth/claims.csv"},
        "scoring": {"version": LEGACY_SCORING_VERSIONS.get(case_id, "fga13-scoring-v1"), "rules_path": "truth/scoring_rules.csv", "ending_rules_path": "truth/ending_rules.csv", "max_score": 1000},
        "assets": {"cover": f"{ASSET_PREFIX}/1.png", "infographic": f"{ASSET_PREFIX}/2.png"},
        "difficulty_profile": _profile(case_id, path_id),
        "compatibility": {"engine_api": "fga13-engine-v1", "canonical_model": "1.0.0", "package_schema": "fga13-case-package-v1"},
        "publication": {"state": "PUBLISHED", "published_at": "2026-11-26"},
    }
    manifest["narrative"] = fga15_narrative(manifest)
    return manifest


def build(*, write: bool) -> dict[str, object]:
    cases = _canonical_cases()
    expected = set(PACKAGE_IDS) - {"ACADEMY_001"}
    if set(cases) != expected:
        raise ValueError(f"canonical corpus mismatch: {sorted(set(cases) ^ expected)}")
    package_root = ROOT / "case-packages"
    # The empty Academy shell is still a package, so it receives the same contract.
    empty_path = package_root / "academy-001" / "manifest.json"
    empty = json.loads(empty_path.read_text(encoding="utf-8"))
    empty.update({"schema_version": "fga13-case-package-v1", "assets": {"cover": f"{ASSET_PREFIX}/1.png", "infographic": f"{ASSET_PREFIX}/2.png"}, "difficulty_profile": _profile("ACADEMY_T01", "DETECTIVE_ACADEMY"), "compatibility": {"engine_api": "fga13-engine-v1", "canonical_model": "1.0.0", "package_schema": "fga13-case-package-v1"}})
    empty["narrative"] = fga15_narrative(empty)
    manifests = {"academy-001": empty}
    for case_id, (root, case, profile, canonical) in cases.items():
        manifests[PACKAGE_IDS[case_id]] = _manifest(case_id, root, case, profile, canonical)
    if write:
        for package_id, manifest in manifests.items():
            target = package_root / package_id / "manifest.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"packages": len(manifests), "package_ids": sorted(manifests), "written": write}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(write=args.write), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
