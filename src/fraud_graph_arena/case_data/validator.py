from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from .json_codec import loads
from .registry import TABLE_PATHS, headers
from .types import parse_json, parse_temporal_value

FORBIDDEN = ("canonical_entity", "culpability", "solve_gate", "mastermind", "guilty", "scoring_rule", "ending_rule")


def validate_package(root: Path) -> list[dict]:
    errors: list[dict] = []
    root = Path(root)

    def err(check: str, table: str, message: str) -> None:
        errors.append({"check_id": check, "severity": "ERROR", "table": table, "message": message})

    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        err("PKG.MANIFEST", "manifest.json", "Manifest is required.")
        return errors
    try:
        manifest = loads(manifest_path.read_text(encoding="utf-8"), field="manifest.json")
    except (OSError, UnicodeError, ValueError):
        err("PKG.MANIFEST.JSON", "manifest.json", "Manifest is not valid UTF-8 JSON or contains duplicate keys.")
        return errors
    if not isinstance(manifest, dict):
        err("PKG.MANIFEST.ROOT", "manifest.json", "Manifest root must be an object.")
        return errors
    if manifest.get("canonical_model_version") != "1.0.0":
        err("PKG.MODEL.VERSION", "manifest.json", "Unsupported canonical model version.")

    receipts_value = manifest.get("files")
    if not isinstance(receipts_value, list):
        err("PKG.RECEIPTS", "manifest.json", "Manifest files must be an array.")
        receipts: dict[str, dict] = {}
    else:
        receipts = {}
        for index, receipt in enumerate(receipts_value):
            if not isinstance(receipt, dict) or not isinstance(receipt.get("path"), str):
                err("PKG.RECEIPT.SHAPE", f"manifest.json:files[{index}]", "File receipt must be an object with a path.")
                continue
            rel = receipt["path"]
            if rel in receipts:
                err("PKG.RECEIPT.DUPLICATE", rel, "Duplicate file receipt.")
            receipts[rel] = receipt
    if not set(TABLE_PATHS).issubset(receipts):
        err("PKG.RECEIPT.SET", "manifest.json", "Manifest receipts must cover each canonical table exactly once.")

    for rel in TABLE_PATHS:
        path = root / rel
        receipt = receipts.get(rel)
        if not path.is_file():
            err("PKG.FILE.MISSING", rel, "Canonical table is missing.")
            continue
        raw = path.read_bytes()
        if not raw:
            err("PKG.FILE.EMPTY", rel, "Canonical CSV must contain its header.")
            continue
        try:
            with path.open(newline="", encoding="utf-8") as stream:
                reader = csv.reader(stream, strict=True)
                try:
                    header = next(reader)
                except StopIteration:
                    err("CANONICAL.HEADER", rel, "CSV header is missing.")
                    continue
                if any(not name or name != name.strip() for name in header) or len(set(header)) != len(header):
                    err("CANONICAL.HEADER", rel, "CSV header contains blank, padded, or duplicate names.")
                if header != list(headers(rel)):
                    err("CANONICAL.HEADER", rel, "Ordered header mismatch.")
                    continue
                row_count = 0
                for row_number, values in enumerate(reader, start=2):
                    row_count += 1
                    if len(values) != len(header):
                        err("CANONICAL.ROW.WIDTH", rel, f"Row {row_number} has {len(values)} cells; expected {len(header)}.")
                        continue
                    row = dict(zip(header, values, strict=True))
                    layer = rel.split("/", 1)[0]
                    if layer in {"published", "genie"}:
                        if any(key.lower() in FORBIDDEN for key in row) or "DO_NOT_SHOW_HERCULE_THIS" in str(row):
                            err("SAFE.TRUTH.LEAK", rel, "Protected truth field or sentinel found.")
                            break
                    for key, value in row.items():
                        if key.endswith("_json") and value:
                            try:
                                parse_json(value, key)
                            except ValueError as exc:
                                err("CANONICAL.JSON", rel, str(exc))
                        if key in {"valid_from", "valid_to", "event_time", "occurrence_time"} and value:
                            try:
                                parse_temporal_value(value, key)
                            except ValueError as exc:
                                err("CANONICAL.TIME", rel, str(exc))
            if receipt is None:
                continue
            if receipt.get("sha256") != hashlib.sha256(raw).hexdigest():
                err("PKG.RECEIPT.SHA256", rel, "Manifest digest does not match bytes.")
            if receipt.get("bytes") != len(raw):
                err("PKG.RECEIPT.BYTES", rel, "Manifest byte count does not match file.")
            if receipt.get("rows") != row_count:
                err("PKG.RECEIPT.ROWS", rel, "Manifest row count does not match parsed CSV rows.")
        except (OSError, UnicodeError, csv.Error) as exc:
            err("CANONICAL.CSV", rel, f"Invalid UTF-8 CSV: {exc}")

    for path in root.rglob("*.csv"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel not in TABLE_PATHS:
            err("PKG.FILE.EXTRA", rel, "Unexpected canonical CSV.")
    return errors
