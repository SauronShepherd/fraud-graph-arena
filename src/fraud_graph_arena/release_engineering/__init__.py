"""Release identity, compatibility and migration primitives for FGA-19."""

from .compatibility import CompatibilityDecision, CompatibilityResult, evaluate_saved_round
from .manifest import (
    ReleaseBinding,
    ReleaseManifestError,
    build_release_manifest,
    load_release_manifest,
    package_digest,
    validate_release_manifest,
)
from .migration import LEGACY_RELEASE_ID, ROUND_MIGRATION_VERSION, apply_round_migrations
from .promotion import ReleasePromotion
from .runtime import ReleaseContext, load_runtime_context

__all__ = [
    "CompatibilityDecision",
    "CompatibilityResult",
    "LEGACY_RELEASE_ID",
    "ROUND_MIGRATION_VERSION",
    "ReleaseBinding",
    "ReleaseContext",
    "ReleaseManifestError",
    "ReleasePromotion",
    "apply_round_migrations",
    "build_release_manifest",
    "evaluate_saved_round",
    "load_release_manifest",
    "load_runtime_context",
    "package_digest",
    "validate_release_manifest",
]
