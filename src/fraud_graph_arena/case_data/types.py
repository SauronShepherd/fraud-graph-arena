from __future__ import annotations
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

def parse_json(value: str, field: str = "json"):
    try: return json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc: raise ValueError(f"{field}: invalid JSON") from exc

def parse_timestamp(value: str, field: str = "timestamp") -> datetime:
    if not value or not value.endswith("Z"): raise ValueError(f"{field}: timestamp must be UTC RFC3339 with Z")
    try: result = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc: raise ValueError(f"{field}: invalid timestamp") from exc
    if result.tzinfo != timezone.utc: raise ValueError(f"{field}: timestamp must be UTC")
    return result

def coerce_sql_value(value: str, sql_type: str, field: str = "value"):
    """Convert a canonical lexical value using its registry SQL type."""
    if value == "": return None
    normalized = sql_type.upper()
    try:
        if normalized == "STRING": return value
        if normalized in {"INT", "BIGINT"}:
            if not re.fullmatch(r"-?(0|[1-9][0-9]*)", value): raise ValueError
            return int(value)
        if normalized == "BOOLEAN":
            if value not in {"true", "false", "TRUE", "FALSE"}: raise ValueError
            return value.lower() == "true"
        if normalized.startswith("DECIMAL("):
            match = re.fullmatch(r"DECIMAL\((\d+),(\d+)\)", normalized)
            if not match: raise ValueError
            precision, scale = map(int, match.groups()); number = Decimal(value)
            if not re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", value): raise ValueError
            if -number.as_tuple().exponent > scale or len(number.as_tuple().digits) > precision: raise ValueError
            return number
        if normalized == "DATE":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value): raise ValueError
            return date.fromisoformat(value)
        if normalized == "TIMESTAMP": return parse_timestamp(value, field)
        if normalized == "JSON": return parse_json(value, field)
    except (TypeError, ValueError, InvalidOperation) as exc:
        raise ValueError(f"{field}: invalid {sql_type}") from exc
    raise ValueError(f"{field}: unsupported SQL type {sql_type}")

def validate_sql_value(value: str, sql_type: str, field: str = "value") -> None:
    coerce_sql_value(value, sql_type, field)
