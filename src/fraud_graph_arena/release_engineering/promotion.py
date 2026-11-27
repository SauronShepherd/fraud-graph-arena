from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .manifest import validate_release_manifest


@dataclass(frozen=True, slots=True)
class PromotionReceipt:
    action: str
    release_id: str
    previous_release_id: str | None
    status: str
    reason: str


class ReleasePromotion:
    """A local immutable release pointer used by the FGA-19 rollback drill.

    It deliberately does not deploy containers or mutate Databricks. The same
    guard is useful before a real platform promotion: validate the candidate,
    require all blocking gates, then move one pointer. Data rollback remains a
    separate operation.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self._releases: dict[str, Mapping[str, Any]] = {}
        self._active: str | None = None

    @property
    def active_release_id(self) -> str | None:
        return self._active

    def promote(self, manifest: Mapping[str, Any], *, gates: Mapping[str, bool]) -> PromotionReceipt:
        release_id = str(manifest.get("release_id", ""))
        errors = validate_release_manifest(manifest, self.root)
        failed_gates = sorted(name for name, passed in gates.items() if not passed)
        if errors or failed_gates:
            reasons = list(errors)
            if failed_gates:
                reasons.append(f"blocking gates failed: {', '.join(failed_gates)}")
            reason = "; ".join(reasons)
            return PromotionReceipt("promote", release_id, self._active, "REJECTED", reason)
        previous = self._active
        existing = self._releases.get(release_id)
        if existing is not None and existing.get("source_revision") != manifest.get("source_revision"):
            return PromotionReceipt("promote", release_id, previous, "REJECTED", "release identity is immutable")
        self._releases[release_id] = dict(manifest)
        self._active = release_id
        return PromotionReceipt("promote", release_id, previous, "PROMOTED", "all release gates passed")

    def rollback(self, release_id: str) -> PromotionReceipt:
        if release_id not in self._releases:
            return PromotionReceipt("rollback", release_id, self._active, "REJECTED", "target release is not in the immutable release registry")
        previous = self._active
        self._active = release_id
        return PromotionReceipt("rollback", release_id, previous, "ROLLED_BACK", "application pointer moved; data rollback remains separate")
