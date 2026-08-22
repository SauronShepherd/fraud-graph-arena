from __future__ import annotations
import re
from .registry import PHYSICAL_TARGETS

def canonical_target(path: str) -> str:
    """Resolve identifiers only through the closed registry; never interpolate package input."""
    try: return PHYSICAL_TARGETS[path]
    except KeyError as exc: raise ValueError("unexpected canonical dataset") from exc

def redact_error(message: str, secrets: tuple[str, ...] = ()) -> str:
    # Redact explicit values and token-shaped values even when a caller only
    # has an exception string available.
    for secret in secrets:
        if secret: message = message.replace(secret, "[REDACTED]")
    return re.sub(r"(?i)(token|access_token|password|secret|authorization)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", message)[:1024]
