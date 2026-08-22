"""Strict, write-free package preflight model."""
from __future__ import annotations

import csv, hashlib, json
from dataclasses import dataclass
from pathlib import Path
from .identity import content_digest
from .registry import PHYSICAL_TARGETS
from fraud_graph_arena.case_data.registry import supported_model_versions

@dataclass(frozen=True)
class CanonicalPackage:
    root: Path
    package_name: str
    package_version: str
    case_id: str
    case_version: str
    snapshot_version: str
    canonical_model_version: str
    content_digest: str
    manifest: dict

    @classmethod
    def read(cls, root: str | Path) -> "CanonicalPackage":
        root = Path(root); manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        files = {x.get("path"): x for x in manifest.get("files", [])}
        expected = set(PHYSICAL_TARGETS)
        if set(files) != expected:
            raise ValueError("manifest does not contain exactly the canonical registry paths")
        for rel in sorted(expected):
            path = root / rel
            if not path.is_file() or path.stat().st_size == 0:
                raise ValueError(f"missing or zero-byte canonical file: {rel}")
            data = path.read_bytes(); entry = files[rel]
            row_count = max(0, data.count(b"\n") - 1)
            if entry.get("bytes") != len(data) or entry.get("sha256") != hashlib.sha256(data).hexdigest() or entry.get("rows") != row_count:
                raise ValueError(f"manifest digest mismatch: {rel}")
        if manifest.get("canonical_model_version") not in supported_model_versions():
            raise ValueError(f"unsupported canonical model version: {manifest.get('canonical_model_version')}")
        converter = str(manifest.get("converter", ""))
        if not converter or not manifest.get("converter_version") or not manifest.get("mapping_version"):
            raise ValueError("manifest is missing converter provenance metadata")
        with (root / "config/cases.csv").open(newline="", encoding="utf-8") as handle:
            cases = list(csv.DictReader(handle))
        matching = [row for row in cases if row.get("case_id") == manifest.get("case_id")]
        if len(matching) != 1:
            raise ValueError("manifest case_id must match exactly one config/cases.csv row")
        case = matching[0]
        for field in ("case_version", "snapshot_version", "canonical_model_version"):
            if case.get(field) != manifest.get(field):
                raise ValueError(f"manifest {field} disagrees with config/cases.csv")
        with (root / "config/case_profiles.csv").open(newline="", encoding="utf-8") as handle:
            profiles = [row for row in csv.DictReader(handle) if row.get("case_id") == manifest.get("case_id")]
        if len(profiles) != 1:
            raise ValueError("package must contain exactly one case profile for the manifest case")
        if str(profiles[0].get("cumulative", "")).lower() != "false":
            raise ValueError("canonical package profile must have cumulative=false")
        return cls(root, manifest["package_name"], manifest.get("package_version", ""), manifest["case_id"],
                   manifest["case_version"], manifest["snapshot_version"], manifest["canonical_model_version"],
                   content_digest(root), manifest)
