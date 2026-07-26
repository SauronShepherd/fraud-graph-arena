from __future__ import annotations

import hashlib
from pathlib import Path

# These are the text formats currently admitted to the Iteration-00 baseline.
# Their logical content is fingerprinted after newline canonicalization so a
# Git checkout on Windows cannot invalidate an otherwise identical release.
CANONICAL_TEXT_SUFFIXES = {".json", ".md", ".txt"}


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix.lower() not in CANONICAL_TEXT_SUFFIXES:
        return raw
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()
