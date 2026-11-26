from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from jsonschema import Draft202012Validator

from fraud_graph_arena.paths import project_root


NARRATIVE_SCHEMA_VERSION = "fga15-narrative-v1"
CLOSURE_VARIANTS = ("EXCELLENT", "PARTIAL", "FAILED")
NARRATIVE_SCHEMA_PATH = "contracts/narrative/fga15-narrative.schema.json"


def _schema() -> dict[str, Any]:
    path = project_root() / NARRATIVE_SCHEMA_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def _location(error: Any) -> str:
    return ".".join(str(part) for part in error.absolute_path) or "narrative"


def validate_narrative_manifest(
    value: Mapping[str, Any],
    *,
    package_assets: Mapping[str, str] | None = None,
) -> list[str]:
    """Validate the player-facing narrative layer without opening protected truth."""

    errors = [f"{_location(error)}: {error.message}" for error in Draft202012Validator(_schema()).iter_errors(value)]
    if errors:
        return sorted(errors)

    if value.get("schema_version") != NARRATIVE_SCHEMA_VERSION:
        errors.append(f"schema_version: expected {NARRATIVE_SCHEMA_VERSION}")
    if package_assets is not None:
        allowed = set(package_assets)
        scopes = [value["opening"], value["closing"]]
        scopes.extend(value["closing"]["variants"].values())
        for scope in scopes:
            for panel in scope["panels"]:
                reference = panel["asset_ref"]
                if reference not in allowed:
                    errors.append(f"asset_ref: {reference!r} is not declared by the case package")
        for asset in value["audio"]["assets"]:
            if asset["enabled"] and not asset["file"]:
                errors.append(f"audio.assets.{asset['id']}: enabled audio requires a shipped file")
            if asset["enabled"] and asset["license"].upper() in {"NOT_SHIPPED", "UNKNOWN", "PENDING"}:
                errors.append(f"audio.assets.{asset['id']}: enabled audio requires an approved license")
    return sorted(set(errors))
