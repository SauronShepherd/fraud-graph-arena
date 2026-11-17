from __future__ import annotations

import re
import unicodedata
from typing import Any

from .models import NormalizedRecord, NormalizedValue

NORMALIZATION_VERSION = "fga09-norm-v1"
PLACEHOLDER_REGISTRY_VERSION = "fga09-placeholder-v1"

_PLACEHOLDER_TOKENS = {
    "",
    "na",
    "n/a",
    "none",
    "null",
    "unknown",
    "notavailable",
    "notprovided",
    "notapplicable",
    "nil",
    "-",
    "000000",
}
_FIELD_ALIASES = {"verified_email": "email", "verified_phone": "phone"}
_IDENTITY_FIELDS = {
    "given_name",
    "surname",
    "email",
    "phone",
    "identifier",
    "director_id",
    "portal_user_id",
    "account_id",
    "customer_id",
    "address",
    "registered_address",
    "device_id",
    "wallet",
    "domain",
    "ip",
}


def canonical_field_name(field: str) -> str:
    return _FIELD_ALIASES.get(field.strip().lower(), field.strip().lower())


def _fold(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    return " ".join(value.split())


def _compact(value: str) -> str:
    return "".join(character for character in _fold(value) if character.isalnum())


def _is_placeholder(field: str, value: str) -> bool:
    folded = _fold(value)
    compact = _compact(value)
    if folded in _PLACEHOLDER_TOKENS or compact in {"na", "none", "null", "unknown", "notprovided"}:
        return True
    if compact.startswith("test") and ("example" in compact or field in {"device_id", "account_id"}):
        return True
    if field == "phone" and compact and set(compact) == {"0"}:
        return True
    return False


def normalize_value(field: str, value: Any) -> NormalizedValue:
    field = canonical_field_name(field)
    if value is None:
        return NormalizedValue(field, False, None, False, True, "MISSING", None)
    original = str(value)
    if not original.strip():
        return NormalizedValue(field, True, None, False, True, "EMPTY", original)
    if _is_placeholder(field, original):
        return NormalizedValue(field, True, None, False, True, "PLACEHOLDER", original)

    folded = _fold(original)
    if field == "email":
        normalized = folded.replace(" ", "")
        valid = bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized))
    elif field == "phone":
        normalized = "".join(character for character in folded if character.isdigit())
        valid = len(normalized) >= 7
    elif field in {"identifier", "director_id", "portal_user_id", "account_id", "customer_id", "device_id", "wallet", "domain", "ip"}:
        normalized = _compact(original)
        valid = bool(normalized)
    else:
        normalized = _compact(original)
        valid = bool(normalized)
    return NormalizedValue(field, True, normalized if valid else None, valid, False, "VALID" if valid else "INVALID", original)


def normalize_record(raw: dict[str, Any]) -> NormalizedRecord:
    attributes = raw.get("safe_attributes_json", raw.get("safe_attributes", {}))
    if isinstance(attributes, str):
        import json

        try:
            attributes = json.loads(attributes)
        except json.JSONDecodeError:
            attributes = {}
    attributes = attributes if isinstance(attributes, dict) else {}
    fields: dict[str, NormalizedValue] = {}
    for raw_field, raw_value in attributes.items():
        field = canonical_field_name(str(raw_field))
        if field not in _IDENTITY_FIELDS:
            continue
        value = normalize_value(field, raw_value)
        previous = fields.get(field)
        if previous is None or (not previous.valid and value.valid):
            fields[field] = value
    identifier_validation_flag = raw.get("identifier_validated", attributes.get("identifier_validated"))
    identifier_validated = identifier_validation_flag is True or (
        isinstance(identifier_validation_flag, str)
        and identifier_validation_flag.strip().casefold() in {"true", "yes", "1"}
    )
    return NormalizedRecord(
        record_id=str(raw.get("record_id", "")),
        entity_type=str(raw.get("record_type", "")).removesuffix("_RECORD") or "UNKNOWN",
        label=str(raw.get("display_label", "")),
        provenance_ref=str(raw.get("provenance_ref", "")),
        snapshot_version=str(raw.get("snapshot_version", "")),
        fields=fields,
        identifier_validated=identifier_validated,
    )


def value(record: NormalizedRecord, field: str) -> str | None:
    item = record.fields.get(field)
    if item is None or not item.valid or item.placeholder:
        return None
    return item.normalized

