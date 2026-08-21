from __future__ import annotations
import json
from datetime import datetime, timezone
def parse_json(value: str, field: str='json'):
    try: return json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc: raise ValueError(f'{field}: invalid JSON') from exc
def parse_timestamp(value: str, field: str='timestamp') -> datetime:
    if len(value)==10 and value[4]=='-' and value[7]=='-':
        try: return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        except ValueError as exc: raise ValueError(f'{field}: invalid date') from exc
    if not value or not value.endswith('Z'): raise ValueError(f'{field}: timestamp must be UTC RFC3339 with Z')
    try: result=datetime.fromisoformat(value[:-1]+'+00:00')
    except ValueError as exc: raise ValueError(f'{field}: invalid timestamp') from exc
    if result.tzinfo != timezone.utc: raise ValueError(f'{field}: timestamp must be UTC')
    return result
