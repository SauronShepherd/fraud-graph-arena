from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fraud_graph_arena.paths import project_root

from .manifest import ReleaseBinding


@dataclass(frozen=True, slots=True)
class ReleaseContext:
    release_id: str
    api_contract_version: str
    screen_set_version: str
    analytics_version: str
    rules_version: str
    contracts: dict[str, str]

    def bind(self, package: Any) -> ReleaseBinding:
        return ReleaseBinding.from_package(
            package,
            release_id=self.release_id,
            contracts=self.contracts,
            analytics_version=self.analytics_version,
        )


def load_runtime_context(path: Path | None = None) -> ReleaseContext:
    root = project_root()
    source = path or root / "contracts/release/fga19-runtime.json"
    raw: dict[str, Any] = json.loads(source.read_text(encoding="utf-8"))
    contracts = dict(raw["contracts"])
    return ReleaseContext(
        release_id=str(raw["release_id"]),
        api_contract_version=str(contracts["api"]),
        screen_set_version=str(contracts["screen_set"]),
        analytics_version=str(contracts["analytics"]),
        rules_version=str(contracts["rules"]),
        contracts=contracts,
    )
