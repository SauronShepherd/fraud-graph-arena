from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fraud_graph_arena.case_data.validator import validate_package as validate_canonical_package
from fraud_graph_arena.paths import project_root

from .models import PACKAGE_SCHEMA_VERSION


def _error(check_id: str, location: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "location": location, "message": message}


def validate_case_package(package_dir: Path) -> list[dict[str, str]]:
    package_dir = Path(package_dir)
    manifest_path = package_dir / "manifest.json"
    errors: list[dict[str, str]] = []
    if not manifest_path.is_file():
        return [_error("PACKAGE.MANIFEST.MISSING", "manifest.json", "A case package requires manifest.json.")]
    try:
        manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [_error("PACKAGE.MANIFEST.JSON", "manifest.json", str(exc))]
    schema_path = project_root() / "contracts/case-packages/fga12-case-package.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors.extend(
        _error("PACKAGE.SCHEMA", "manifest.json", error.message)
        for error in Draft202012Validator(schema).iter_errors(manifest)
    )
    if errors:
        return errors
    if manifest["package_id"] != package_dir.name:
        errors.append(_error("PACKAGE.ID.DIRECTORY", "manifest.json", "package_id must match its directory name."))
    if manifest["schema_version"] != PACKAGE_SCHEMA_VERSION:
        errors.append(_error("PACKAGE.SCHEMA.VERSION", "manifest.json", "Unsupported case package schema version."))
    canonical = manifest.get("canonical")
    if manifest["kind"] == "canonical":
        if canonical is None:
            errors.append(_error("PACKAGE.CANONICAL.MISSING", "manifest.json", "Canonical packages require a canonical reference."))
        else:
            root = (project_root() / canonical["root"]).resolve()
            if not root.is_dir():
                errors.append(_error("PACKAGE.CANONICAL.ROOT", "manifest.json", f"Canonical root does not exist: {canonical['root']}"))
            else:
                errors.extend(
                    _error(item["check_id"], f"canonical/{item.get('table', 'package')}", item["message"])
                    for item in validate_canonical_package(root)
                )
                canonical_manifest_path = root / "manifest.json"
                if canonical_manifest_path.is_file():
                    canonical_manifest = json.loads(canonical_manifest_path.read_text(encoding="utf-8"))
                    for field in ("case_id", "snapshot_version"):
                        if canonical_manifest.get(field) != canonical[field]:
                            errors.append(_error("PACKAGE.CANONICAL.IDENTITY", "manifest.json", f"canonical.{field} disagrees with the canonical manifest."))
    elif canonical is not None:
        errors.append(_error("PACKAGE.EMPTY.CANONICAL", "manifest.json", "An empty package must not reference canonical data."))
    if manifest["publication"]["state"] == "PUBLISHED" and "SUBMIT" not in manifest["supported_actions"] and manifest["kind"] == "canonical":
        errors.append(_error("PACKAGE.PUBLISH.SUBMISSION", "manifest.json", "A published playable package must expose SUBMIT."))
    costs = manifest["economy"]["costs"]
    for action in costs:
        if action not in manifest["supported_actions"]:
            errors.append(_error("PACKAGE.ECONOMY.UNSUPPORTED_ACTION", "economy.costs", f"Cost declared for unsupported action {action}."))
    for action in manifest["supported_actions"]:
        if action in costs and action != "SUBMIT" and costs[action] <= 0:
            errors.append(_error("PACKAGE.ECONOMY.COST", "manifest.json", f"Supported paid action {action} must cost more than zero."))
    evidence = manifest["evidence_rules"]
    if evidence["public_projection"] == evidence["protected_truth"]:
        errors.append(_error("PACKAGE.EVIDENCE.LAYERS", "manifest.json", "Public projection and protected truth must remain separate."))
    if any("truth" in value.lower() for value in manifest["assets"].values()):
        errors.append(_error("PACKAGE.ASSET.TRUTH", "manifest.json", "Asset references must not point at protected truth material."))
    if manifest["compatibility"]["canonical_model"] != (canonical or {}).get("model_version", manifest["compatibility"]["canonical_model"]):
        errors.append(_error("PACKAGE.COMPATIBILITY.MODEL", "manifest.json", "The declared canonical model must agree with the canonical reference."))
    return errors


def validate_all_case_packages(root: Path | None = None) -> dict[str, list[dict[str, str]]]:
    package_root = (root or project_root() / "case-packages").resolve()
    return {
        directory.name: validate_case_package(directory)
        for directory in sorted(package_root.iterdir())
        if directory.is_dir()
    }
