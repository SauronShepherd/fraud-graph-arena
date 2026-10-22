from __future__ import annotations
SAFE_LAYERS={'published','genie'}
TRUTH_LAYERS={'truth'}
from .registry import headers

def safe_row(row: dict, *, layer: str, table: str) -> dict:
    if layer not in SAFE_LAYERS: raise ValueError('projection layer must be published or genie')
    if not table.startswith(f'{layer}/'):
        raise ValueError('projection table must belong to the selected safe layer')
    allowed=headers(table)
    return {key:row[key] for key in allowed if key in row}
