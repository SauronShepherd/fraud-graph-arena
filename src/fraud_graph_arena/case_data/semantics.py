from __future__ import annotations

FAMILIES = frozenset({"ACADEMY", "PUPPY", "ADULT", "SENIOR"})
RELATIONSHIP_FAMILIES = frozenset({"DIRECT_SOURCE", "SOURCE_REFERENCE"})
CONFIDENCE_BANDS = frozenset({"LOW", "MEDIUM", "MEDIUM_HIGH", "HIGH"})
GENERATION_MODES = frozenset({"SYNTHETIC", "CURATED", "CURATED_APPROXIMATION", "DIRECT_SOURCE", "ZINGG", "GRAPHFRAMES", "EXACT_SHARED_FIELD"})

def require_controlled(value: str, allowed: frozenset[str], field: str) -> None:
    if value and value not in allowed:
        raise ValueError(f"{field}: unsupported controlled value {value}")
