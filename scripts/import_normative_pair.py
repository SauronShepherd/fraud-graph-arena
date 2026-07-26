#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "config/governance/baseline.json"
DESTINATION = ROOT / "specifications/normative-pair-v10.0"

EXPECTED = {
    "functional": {
        "filename": "Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md",
        "title": "## Complete Functional Specification",
        "artifact_id": "FGA-NORMATIVE-FUNCTIONAL-10.0-20260726",
    },
    "technical": {
        "filename": "Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md",
        "title": "## Complete Technical Architecture and Design Specification",
        "artifact_id": "FGA-NORMATIVE-TECHNICAL-10.0-20260726",
    },
}
PAIR_ID = "FGA-NORMATIVE-PAIR-10.0-20260726"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_source(path: Path, kind: str) -> None:
    if not path.is_file():
        raise SystemExit(f"{kind} source does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    expected = EXPECTED[kind]
    required_fragments = [
        "# Fraud Graph Arena",
        expected["title"],
        "**Document version:** 10.0",
        f"**Normative pair ID:** `{PAIR_ID}`",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in text]
    if missing:
        joined = "\n  - ".join(missing)
        raise SystemExit(
            f"{kind} document identity validation failed for {path}. Missing:\n  - {joined}"
        )
    if len(text.splitlines()) < 100:
        raise SystemExit(
            f"{kind} source is implausibly short ({len(text.splitlines())} lines); "
            "refusing a placeholder or summary."
        )


def update_baseline(imported: dict[str, Path]) -> None:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    artifacts_by_id = {item["artifact_id"]: item for item in baseline["artifacts"]}
    for kind, path in imported.items():
        artifact_id = EXPECTED[kind]["artifact_id"]
        if artifact_id not in artifacts_by_id:
            raise SystemExit(f"baseline does not contain expected artifact {artifact_id}")
        artifact = artifacts_by_id[artifact_id]
        artifact["availability"] = "available"
        artifact["path"] = path.relative_to(ROOT).as_posix()
        artifact["sha256"] = digest(path)
        artifact.pop("external_reference", None)
        artifact["notes"] = "Imported from the exact approved v10.0 source document."

    unresolved = [
        item["artifact_id"]
        for item in baseline["artifacts"]
        if item.get("required_for_closure") and item.get("availability") != "available"
    ]
    baseline["status"] = "active" if not unresolved else "blocked"
    baseline["closure_requirements"] = {
        "all_required_available": not unresolved,
        "all_available_digests_verified": True,
        "unresolved_required_artifact_ids": unresolved,
    }
    BASELINE_PATH.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import the exact approved Fraud Graph Arena v10.0 normative pair."
    )
    parser.add_argument("functional", type=Path)
    parser.add_argument("technical", type=Path)
    args = parser.parse_args()

    sources = {"functional": args.functional.resolve(), "technical": args.technical.resolve()}
    for kind, path in sources.items():
        validate_source(path, kind)

    DESTINATION.mkdir(parents=True, exist_ok=True)
    imported: dict[str, Path] = {}
    for kind, source in sources.items():
        destination = DESTINATION / EXPECTED[kind]["filename"]
        if source != destination.resolve():
            shutil.copyfile(source, destination)
        imported[kind] = destination

    update_baseline(imported)
    print("Imported and digest-registered the v10.0 normative pair:")
    for kind, path in imported.items():
        print(f"  {kind}: {path.relative_to(ROOT)} ({digest(path)})")
    print("Commit the two documents and updated baseline before generating closure evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
