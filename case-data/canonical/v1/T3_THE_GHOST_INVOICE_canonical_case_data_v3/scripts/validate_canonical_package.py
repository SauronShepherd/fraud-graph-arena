#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

FORBIDDEN_SAFE_HEADERS = {
    "content_role", "expected_truth", "expected_classification", "culpability",
    "harm_status", "fraud_network_membership", "protected_notes", "score_weight",
    "forbidden_conclusion", "penalty",
}
FORBIDDEN_SAFE_JSON_KEYS = FORBIDDEN_SAFE_HEADERS | {
    "primary_suspect", "is_fraudulent", "truth_role", "evaluator_truth",
}
PROFILE_CODES = {"ACADEMY", "PUPPY", "ADULT", "SENIOR"}
CASE_PREFIX = re.compile(r"(^|/)(bone|crypto|downline|hydrant|maddog|relief|ceo|phantom|love|panama)_", re.I)


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")
    if path.stat().st_size == 0:
        raise AssertionError(f"Zero-byte CSV is forbidden: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise AssertionError(f"CSV has no header: {path}")
        return list(reader.fieldnames), list(reader)


def canonical_json(value: str, location: str) -> None:
    if value == "":
        return
    try:
        json.loads(value)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON at {location}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", type=Path)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "fga_canonical_schema_registry_v1.json",
    )
    args = parser.parse_args()
    root = args.package_root.resolve()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))

    failures: list[str] = []
    loaded: dict[str, list[dict[str, str]]] = {}
    for rel, spec in registry["tables"].items():
        try:
            header, rows = read_rows(root / rel)
            expected = [column["name"] for column in spec["columns"]]
            if header != expected:
                raise AssertionError(
                    f"Header mismatch in {rel}: expected={expected}, actual={header}"
                )
            if CASE_PREFIX.search(rel):
                raise AssertionError(f"Case-specific canonical path is forbidden: {rel}")
            loaded[rel] = rows

            pk = spec["primary_key"]
            seen: set[tuple[str, ...]] = set()
            for index, row in enumerate(rows, start=2):
                key = tuple(row.get(name, "") for name in pk)
                if "" in key:
                    raise AssertionError(f"Blank primary-key value in {rel}:{index}: {key}")
                if key in seen:
                    raise AssertionError(f"Duplicate primary key in {rel}:{index}: {key}")
                seen.add(key)
                for name, value in row.items():
                    if name.endswith("_json") and value:
                        canonical_json(value, f"{rel}:{index}:{name}")
                if rel.startswith(("published/", "genie/")):
                    leaked = FORBIDDEN_SAFE_HEADERS.intersection(row)
                    if leaked:
                        raise AssertionError(f"Protected headers in {rel}: {sorted(leaked)}")
                    for name, value in row.items():
                        if name.endswith("_json") and value:
                            payload = json.loads(value)
                            if isinstance(payload, dict):
                                keys = {str(k).casefold() for k in payload}
                                bad = keys.intersection(FORBIDDEN_SAFE_JSON_KEYS)
                                if bad:
                                    raise AssertionError(
                                        f"Protected JSON keys in {rel}:{index}:{name}: {sorted(bad)}"
                                    )
        except AssertionError as exc:
            failures.append(str(exc))

    expected_paths = set(registry["tables"])
    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.csv")
    }
    extras = actual_paths - expected_paths
    if extras:
        failures.append(f"Unexpected canonical CSV files: {sorted(extras)}")

    # Package-level constraints.
    case_rows = loaded.get("config/cases.csv", [])
    profile_rows = loaded.get("config/case_profiles.csv", [])
    if len(case_rows) != 1:
        failures.append(f"config/cases.csv must contain exactly one row; found {len(case_rows)}")
    if len(profile_rows) != 1:
        failures.append(
            f"config/case_profiles.csv must contain exactly one row; found {len(profile_rows)}"
        )
    if profile_rows:
        profile = profile_rows[0]
        if profile.get("profile_code") not in PROFILE_CODES:
            failures.append(f"Invalid profile_code: {profile.get('profile_code')}")
        if profile.get("cumulative", "").casefold() != "false":
            failures.append("Canonical profiles must have cumulative=false")

    # Safe graph referential integrity.
    published_records = {
        (r["case_id"], r["profile_code"], r["record_id"])
        for r in loaded.get("published/records.csv", [])
    }
    for rel in (
        "published/relationships.csv",
        "published/entity_resolution_candidates.csv",
        "published/exact_matches.csv",
    ):
        for row in loaded.get(rel, []):
            left_name = "source_record_id" if "source_record_id" in row else "left_record_id"
            right_name = "target_record_id" if "target_record_id" in row else "right_record_id"
            for field in (left_name, right_name):
                key = (row["case_id"], row["profile_code"], row[field])
                if key not in published_records:
                    failures.append(f"Missing published endpoint {key} referenced by {rel}")

    genie_records = {
        (r["case_id"], r["profile_code"], r["record_id"])
        for r in loaded.get("genie/records.csv", [])
    }
    for row in loaded.get("genie/record_attributes.csv", []):
        key = (row["case_id"], row["profile_code"], row["record_id"])
        if key not in genie_records:
            failures.append(f"Missing Genie record for attribute: {key}")
    for row in loaded.get("genie/relationships.csv", []):
        for field in ("source_record_id", "target_record_id"):
            key = (row["case_id"], row["profile_code"], row[field])
            if key not in genie_records:
                failures.append(f"Missing Genie endpoint {key}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    print(f"Canonical model: {registry['canonical_model_version']}")
    print(f"Validated tables: {len(registry['tables'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
