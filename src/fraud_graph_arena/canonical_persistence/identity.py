from __future__ import annotations
import hashlib, json
from datetime import date, datetime
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

def semantic_hash(rows: dict[str, list[dict]]) -> str:
    def encode(value):
        if isinstance(value, (datetime, date)): return value.isoformat().replace("+00:00", "Z")
        if isinstance(value, Decimal): return format(value, "f")
        raise TypeError(f"unsupported semantic-hash value: {type(value).__name__}")
    value = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=encode)
    return hashlib.sha256(value.encode()).hexdigest()

def topology_hash(names: set[str] | tuple[str, ...]) -> str:
    return hashlib.sha256(json.dumps(sorted(names), separators=(",", ":")).encode()).hexdigest()
