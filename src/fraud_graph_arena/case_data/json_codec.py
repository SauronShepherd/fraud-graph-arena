from __future__ import annotations

import json
from typing import Any


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads(value: str, *, field: str = "json") -> Any:
    try:
        return json.loads(value, object_pairs_hook=_reject_duplicates)
    except (TypeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{field}: invalid JSON or duplicate object key") from exc
