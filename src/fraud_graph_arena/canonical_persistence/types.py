from __future__ import annotations
import json
from datetime import date, datetime

def validate_row_types(row: dict[str, str], path: str) -> None:
    """Apply the closed v1 lexical rules that CSV cannot express itself."""
    for field, value in row.items():
        if value == "": continue
        if field.endswith("_json") or field == "json_value":
            try: json.loads(value)
            except json.JSONDecodeError as exc: raise ValueError(f"{path}.{field}: invalid JSON") from exc
        elif field.endswith("_decimal"):
            try: float(value)
            except ValueError as exc: raise ValueError(f"{path}.{field}: invalid decimal") from exc
        elif field in {"sequence", "case_order", "initial_item_count", "genie_row_limit", "expected_min_rows", "expected_max_rows", "false_accusations", "expected_score"}:
            try: int(value)
            except ValueError as exc: raise ValueError(f"{path}.{field}: invalid integer") from exc
        elif field in {"cumulative", "ranked", "quote_required", "no_result_charged", "directed", "required", "is_sensitive", "is_masked"}:
            if value not in {"true", "false", "TRUE", "FALSE"}: raise ValueError(f"{path}.{field}: invalid boolean")
        elif field.endswith("_at") or field in {"valid_from", "valid_to", "event_time"}:
            try: datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc: raise ValueError(f"{path}.{field}: invalid timestamp") from exc
