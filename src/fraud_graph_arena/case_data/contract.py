from __future__ import annotations
from dataclasses import dataclass
from .registry import TABLE_PATHS, headers
@dataclass(frozen=True)
class TableSpec:
    path: str
    columns: tuple[str,...]
    @property
    def layer(self): return self.path.split('/',1)[0]
TABLE_SPECS=tuple(TableSpec(p,headers(p)) for p in TABLE_PATHS)
MODEL_VERSION='1.0.0'
