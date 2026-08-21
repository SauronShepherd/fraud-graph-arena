"""Strict, write-free package preflight model."""
from __future__ import annotations

import hashlib, json
from dataclasses import dataclass
from pathlib import Path
from .identity import content_digest
from .registry import PHYSICAL_TARGETS

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
            if entry.get("bytes") != len(data) or entry.get("sha256") != hashlib.sha256(data).hexdigest():
                raise ValueError(f"manifest digest mismatch: {rel}")
        return cls(root, manifest["package_name"], manifest.get("package_version", ""), manifest["case_id"],
                   manifest["case_version"], manifest["snapshot_version"], manifest["canonical_model_version"],
                   content_digest(root), manifest)

