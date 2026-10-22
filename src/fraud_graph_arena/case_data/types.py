from __future__ import annotations
from datetime import datetime, timezone
import re
from .json_codec import loads

_UTC_RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

def parse_json(value: str, field: str='json'):
    return loads(value, field=field)
def parse_timestamp(value: str, field: str='timestamp') -> datetime:
    if not isinstance(value, str):
        raise ValueError(f'{field}: timestamp must be a string')
    if len(value)==10 and value[4]=='-' and value[7]=='-':
        raise ValueError(f'{field}: date-only values are not timestamps; provide an explicit instant')
    if not _UTC_RFC3339.fullmatch(value): raise ValueError(f'{field}: timestamp must be UTC RFC3339 with Z')
    try: result=datetime.fromisoformat(value[:-1]+'+00:00')
    except ValueError as exc: raise ValueError(f'{field}: invalid timestamp') from exc
    if result.tzinfo != timezone.utc: raise ValueError(f'{field}: timestamp must be UTC')
    return result

def parse_temporal_value(value: str, field: str='temporal') -> datetime | str:
    """Keep calendar dates as dates; never reinterpret them as midnight instants."""
    if len(value) == 10 and value[4] == '-' and value[7] == '-':
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError as exc:
            raise ValueError(f'{field}: invalid date') from exc
    return parse_timestamp(value, field)
