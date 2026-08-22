"""Small deterministic report helpers; reports never contain secrets or row payloads."""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

def qualified_source_sha(root: Path | None = None) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

def safe_report(payload: dict) -> dict:
    forbidden = ("token", "secret", "password", "access_token", "stack_trace")
    encoded=json.dumps(payload, ensure_ascii=False).lower()
    if any(key in encoded for key in forbidden): raise ValueError("report contains a forbidden secret-bearing key")
    return payload

def write_safe_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(safe_report(payload), indent=2) + "\n", encoding="utf-8")

def digest_report(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
