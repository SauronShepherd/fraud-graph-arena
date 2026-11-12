"""Resolve repository-owned runtime assets in source checkouts and installed images."""
from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    override = os.getenv("FGA_PROJECT_ROOT")
    candidates = [Path(override)] if override else []
    candidates.extend((Path(__file__).resolve().parents[2], Path.cwd()))
    for candidate in candidates:
        if (candidate / "contracts/canonical/v1/canonical-model.json").is_file():
            return candidate
    raise FileNotFoundError("FGA project assets are unavailable; set FGA_PROJECT_ROOT to the runtime asset root")
