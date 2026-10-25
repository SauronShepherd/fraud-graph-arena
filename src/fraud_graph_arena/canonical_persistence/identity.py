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

def _iter_typed_json(value):
    """Stream deterministic typed JSON without materializing a whole package."""
    if value is None: yield '["null"]'; return
    if isinstance(value, bool): yield json.dumps(["bool", value], separators=(",", ":")); return
    if isinstance(value, int): yield json.dumps(["int", str(value)], separators=(",", ":")); return
    if isinstance(value, Decimal):
        if not value.is_finite(): raise ValueError("non-finite Decimal cannot be fingerprinted")
        normalized = format(value, "f")
        if value == 0: normalized = "0"
        elif "." in normalized: normalized = normalized.rstrip("0").rstrip(".")
        yield json.dumps(["decimal", normalized], separators=(",", ":")); return
    if isinstance(value, float):
        if not math.isfinite(value): raise ValueError("non-finite float cannot be fingerprinted")
        yield json.dumps(["float", value.hex()], separators=(",", ":")); return
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None: raise ValueError("naive datetime cannot be fingerprinted")
        normalized = value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        yield json.dumps(["datetime", normalized], separators=(",", ":")); return
    if isinstance(value, date):
        yield json.dumps(["date", value.isoformat()], separators=(",", ":")); return
    if isinstance(value, str): yield json.dumps(["string", value], separators=(",", ":"), ensure_ascii=False); return
    if isinstance(value, (list, tuple)):
        yield '["list",[' if isinstance(value, list) else '["tuple",['
        for index, item in enumerate(value):
            if index: yield ","
            yield from _iter_typed_json(item)
        yield "]]"; return
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value): raise TypeError("canonical JSON object keys must be strings")
        yield '["object",['
        for index, key in enumerate(sorted(value)):
            if index: yield ","
            yield "[" + json.dumps(key, ensure_ascii=False) + ","
            yield from _iter_typed_json(value[key])
            yield "]"
        yield "]]"; return
    raise TypeError(f"unsupported canonical value type: {type(value).__name__}")

def canonical_json(value) -> str:
    """Serialize typed values deterministically without conflating SQL types."""
    return "".join(_iter_typed_json(value))

def semantic_hash(rows: dict[str, list[dict]]) -> str:
    digest = hashlib.sha256()
    for chunk in _iter_typed_json(rows): digest.update(chunk.encode("utf-8"))
    return digest.hexdigest()

def topology_hash(names: set[str] | tuple[str, ...]) -> str:
    return hashlib.sha256(json.dumps(sorted(names), separators=(",", ":")).encode()).hexdigest()
