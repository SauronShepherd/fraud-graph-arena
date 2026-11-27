from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


class ReleaseManifestError(ValueError):
    """A release manifest is incomplete, inconsistent or not reproducible."""


UNIT_DEFINITIONS: tuple[tuple[str, str, str, str], ...] = (
    ("frontend", "fga19-web-v1", "apps/web/src", "frontend"),
    ("python_backend", "fga19-python-v1", "src/fraud_graph_arena", "backend"),
    ("database_migrations", "fga19-rounds-migration-v2", "src/fraud_graph_arena/release_engineering/migration.py", "migration"),
    ("case_packages", "fga13-package-v1", "case-packages", "case-content"),
    ("graph_assets", "fga02-board-assets-v1", "apps/web/public/assets/board/v1/manifest.json", "assets"),
    ("analytics_jobs", "fga10-analytics-v1", "src/fraud_graph_arena/graph_analytics/service.py", "analytics"),
)

CI_STAGES: tuple[dict[str, Any], ...] = (
    {"id": "lint", "command": "python -m compileall -q src scripts", "blocks": "merge"},
    {"id": "unit", "command": "python -m pytest -q tests/iteration_19", "blocks": "merge"},
    {"id": "contracts", "command": "python scripts/validate_fga19_release.py", "blocks": "merge"},
    {"id": "case-validation", "command": "python scripts/validate_case_packages.py", "blocks": "release"},
    {"id": "end-to-end", "command": "npm run test:e2e -- --workers=1", "blocks": "release"},
    {"id": "container-build", "command": "docker compose --profile local-build build web", "blocks": "release"},
    {"id": "deployment-smoke", "command": "python scripts/fga19_release_smoke.py", "blocks": "promotion"},
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _files_for(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and "__pycache__" not in candidate.parts
        and candidate.suffix not in {".pyc", ".pyo"}
        and ".pytest_cache" not in candidate.parts
    )


def tree_digest(root: Path, relative: str) -> str:
    target = (root / relative).resolve()
    if root.resolve() not in target.parents and target != root.resolve():
        raise ReleaseManifestError(f"release unit escapes repository root: {relative}")
    if not target.exists():
        raise ReleaseManifestError(f"release unit is missing: {relative}")
    entries = []
    for path in _files_for(target):
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path.read_bytes()),
            }
        )
    return _sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def package_digest(package_dir: Path) -> str:
    """Hash a case package's declared files without hashing runtime state."""

    package_dir = Path(package_dir).resolve()
    entries = []
    for path in _files_for(package_dir):
        entries.append(
            {
                "path": path.relative_to(package_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path.read_bytes()),
            }
        )
    return _sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "working-tree"


def build_release_manifest(
    root: Path,
    *,
    release_id: str = "fga19-mvp.1",
    source_revision: str | None = None,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    units = [
        {
            "id": unit_id,
            "version": version,
            "path": path,
            "kind": kind,
            "immutable": True,
            "digest_algorithm": "sha256-tree-v1",
            "digest": f"sha256:{tree_digest(root, path)}",
        }
        for unit_id, version, path, kind in UNIT_DEFINITIONS
    ]
    return {
        "schema_version": "fga19-release-v1",
        "release_id": release_id,
        "source_revision": source_revision or _git_revision(root),
        "generated_at_utc": generated_at_utc or datetime.now(UTC).isoformat(),
        "units": units,
        "contracts": {
            "api": "v1",
            "screen_set": "1.0",
            "case_package_schema": "fga13-case-package-v1",
            "canonical_model": "1.0.0",
            "analytics": "fga10-analytics-v1",
            "rules": "fga13-engine-v1",
            "scoring": "package-bound",
            "economy": "package-bound",
        },
        "compatibility": {
            "saved_rounds": "bind-or-freeze",
            "case_updates": "immutable-package-version",
            "database_migrations": "forward-only-expand-then-contract",
            "application_rollback": "separate-from-data-rollback",
        },
        "feature_flags": [
            {
                "id": "fga19.release_candidate",
                "enabled": False,
                "default": False,
                "owner": "release-engineering",
                "purpose": "Gate a candidate deployment without changing case rules.",
                "removal_condition": "Remove after the first stable promotion of the release line.",
            }
        ],
        "ci_stages": list(CI_STAGES),
    }


def _schema(root: Path) -> dict[str, Any]:
    path = root / "contracts/release/fga19-release.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_release_manifest(
    manifest: Mapping[str, Any],
    root: Path,
    *,
    check_digests: bool = True,
) -> list[str]:
    root = Path(root).resolve()
    errors = [error.message for error in Draft202012Validator(_schema(root)).iter_errors(manifest)]
    if errors:
        return sorted(errors)
    seen: set[str] = set()
    for unit in manifest["units"]:
        if unit["id"] in seen:
            errors.append(f"duplicate release unit: {unit['id']}")
        seen.add(unit["id"])
        if check_digests:
            try:
                actual = f"sha256:{tree_digest(root, unit['path'])}"
            except ReleaseManifestError as error:
                errors.append(str(error))
            else:
                if actual != unit["digest"]:
                    errors.append(f"digest mismatch for {unit['id']}: expected {unit['digest']}, got {actual}")
    if len({stage["id"] for stage in manifest["ci_stages"]}) != len(manifest["ci_stages"]):
        errors.append("CI stage identifiers must be unique")
    return sorted(errors)


def load_release_manifest(path: Path, *, root: Path | None = None, check_digests: bool = True) -> dict[str, Any]:
    path = Path(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    repository_root = Path(root).resolve() if root is not None else path.parents[2].resolve()
    errors = validate_release_manifest(manifest, repository_root, check_digests=check_digests)
    if errors:
        raise ReleaseManifestError("; ".join(errors))
    return manifest


@dataclass(frozen=True, slots=True)
class ReleaseBinding:
    release_id: str
    package_id: str
    package_version: str
    case_id: str
    case_version: str
    package_schema_version: str
    canonical_model_version: str
    engine_api_version: str
    scoring_version: str
    economy_version: str
    analytics_version: str
    screen_set_version: str
    api_contract_version: str
    package_digest: str

    @classmethod
    def from_package(cls, package: Any, *, release_id: str, contracts: Mapping[str, str], analytics_version: str) -> "ReleaseBinding":
        compatibility = package.compatibility
        return cls(
            release_id=release_id,
            package_id=package.package_id,
            package_version=package.package_version,
            case_id=package.case_id,
            case_version=package.case_version,
            package_schema_version=package.schema_version,
            canonical_model_version=str(compatibility.get("canonical_model", contracts["canonical_model"])),
            engine_api_version=str(compatibility.get("engine_api", contracts["rules"])),
            scoring_version=package.scoring_version,
            economy_version=package.economy_version,
            analytics_version=analytics_version,
            screen_set_version=contracts["screen_set"],
            api_contract_version=contracts["api"],
            package_digest=package_digest(package.package_dir),
        )
