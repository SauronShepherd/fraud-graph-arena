from __future__ import annotations
import hashlib, json, math
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from fraud_graph_arena.case_data.registry import TABLE_PATHS
from .models import PackageIdentity

def content_digest(root: Path) -> str:
    parts = []
    for rel in sorted(TABLE_PATHS):
        p = root / rel
        data = p.read_bytes()
        parts.append({"relative_path": rel, "byte_length": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return hashlib.sha256(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def publication_id(identity: PackageIdentity) -> str:
    value = json.dumps(identity.__dict__, sort_keys=True, separators=(",", ":"))
    return "pub_" + hashlib.sha256(value.encode()).hexdigest()

def _typed_node(value):
    """Encode Python values with explicit, collision-free type tags."""
    if value is None: return ["null"]
    if isinstance(value, bool): return ["bool", value]
    if isinstance(value, int): return ["int", str(value)]
    if isinstance(value, Decimal):
        if not value.is_finite(): raise ValueError("non-finite Decimal cannot be fingerprinted")
        normalized = format(value, "f")
        if value == 0: normalized = "0"
        elif "." in normalized: normalized = normalized.rstrip("0").rstrip(".")
        return ["decimal", normalized]
    if isinstance(value, float):
        if not math.isfinite(value): raise ValueError("non-finite float cannot be fingerprinted")
        return ["float", value.hex()]
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("naive datetime cannot be fingerprinted")
        normalized = value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return ["datetime", normalized]
    if isinstance(value, date): return ["date", value.isoformat()]
    if isinstance(value, str): return ["string", value]
    if isinstance(value, list): return ["list", [_typed_node(item) for item in value]]
    if isinstance(value, tuple): return ["tuple", [_typed_node(item) for item in value]]
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("canonical JSON object keys must be strings")
        items = sorted(value.items(), key=lambda item: item[0])
        return ["object", [[key, _typed_node(item)] for key, item in items]]
    raise TypeError(f"unsupported canonical value type: {type(value).__name__}")

def canonical_json(value) -> str:
    """Serialize typed values deterministically without conflating SQL types."""
    return json.dumps(_typed_node(value), separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def semantic_hash(rows: dict[str, list[dict]]) -> str:
    value = canonical_json(rows)
    return hashlib.sha256(value.encode()).hexdigest()

def topology_hash(names: set[str] | tuple[str, ...]) -> str:
    return hashlib.sha256(json.dumps(sorted(names), separators=(",", ":")).encode()).hexdigest()
