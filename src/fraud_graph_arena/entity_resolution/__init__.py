"""Player-safe identity resolution for the FGA-09 investigation slice."""

from .engine import (
    FEATURE_CONFIG_VERSION,
    IDENTIFIER_VALIDATION_VERSION,
    IDENTITY_FEATURE_FIELDS,
    EntityResolutionEngine,
    load_t02_identity_records,
)
from .models import (
    ExactIdentityMatch,
    IdentityCandidate,
    IdentityReview,
    ResolutionRun,
)
from .normalization import NORMALIZATION_VERSION, PLACEHOLDER_REGISTRY_VERSION
from .repository import (
    InMemoryEntityResolutionRepository,
    SqliteEntityResolutionRepository,
)
from .service import EntityResolutionService

__all__ = [
    "EntityResolutionEngine",
    "EntityResolutionService",
    "ExactIdentityMatch",
    "IdentityCandidate",
    "IdentityReview",
    "ResolutionRun",
    "InMemoryEntityResolutionRepository",
    "SqliteEntityResolutionRepository",
    "NORMALIZATION_VERSION",
    "PLACEHOLDER_REGISTRY_VERSION",
    "FEATURE_CONFIG_VERSION",
    "IDENTIFIER_VALIDATION_VERSION",
    "IDENTITY_FEATURE_FIELDS",
    "load_t02_identity_records",
]
