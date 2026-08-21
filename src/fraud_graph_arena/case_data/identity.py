from __future__ import annotations
import hashlib, json
def stable_id(prefix: str, namespace: str, *parts: object) -> str:
    payload = json.dumps([namespace, *parts], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"{prefix}_{hashlib.sha256(payload.encode()).hexdigest()[:24].upper()}"
