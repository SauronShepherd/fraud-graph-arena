from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .manifest import ReleaseBinding


class CompatibilityDecision(StrEnum):
    PLAYABLE = "PLAYABLE"
    MIGRATE = "MIGRATE"
    FROZEN = "FROZEN"


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    decision: CompatibilityDecision
    reasons: tuple[str, ...]


def evaluate_saved_round(
    binding: ReleaseBinding,
    *,
    current_release_id: str,
    available_packages: Iterable[tuple[str, str]],
) -> CompatibilityResult:
    """Evaluate an old round without rewriting its authoritative binding.

    A release change alone is not a migration. A round remains playable when the
    exact case/version package is still available. If that immutable package is
    gone, the safe result is a frozen receipt rather than silently loading newer
    rules. The explicit MIGRATE outcome is reserved for a future, declared
    migration rather than guessed compatibility.
    """

    available = set(available_packages)
    key = (binding.case_id, binding.case_version)
    if key not in available:
        return CompatibilityResult(
            CompatibilityDecision.FROZEN,
            ("the bound immutable case version is not available", "do not substitute the current case package"),
        )
    if binding.release_id == current_release_id:
        return CompatibilityResult(CompatibilityDecision.PLAYABLE, ("round and runtime share a release identity",))
    return CompatibilityResult(
        CompatibilityDecision.PLAYABLE,
        (
            "the round keeps its original release binding",
            "the exact case/version package remains available",
            "new release defaults are not applied to old authoritative state",
        ),
    )
