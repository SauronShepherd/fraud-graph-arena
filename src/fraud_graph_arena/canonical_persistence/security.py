from __future__ import annotations
from .registry import PHYSICAL_TARGETS

def canonical_target(path: str) -> str:
    """Resolve identifiers only through the closed registry; never interpolate package input."""
    try: return PHYSICAL_TARGETS[path]
    except KeyError as exc: raise ValueError("unexpected canonical dataset") from exc

def redact_error(message: str, secrets: tuple[str, ...] = ()) -> str:
    for secret in secrets:
        if secret: message = message.replace(secret, "[REDACTED]")
    return message
