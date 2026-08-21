from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
class Converter(ABC):
    family: str
    converter_id: str
    @abstractmethod
    def convert(self, source: Path, output: Path, mapping: dict[str, Any]) -> None: ...
class ConverterRegistry:
    def __init__(self): self._items: dict[str, type[Converter]] = {}
    def register(self, cls: type[Converter]):
        if cls.converter_id in self._items: raise ValueError(f'duplicate converter: {cls.converter_id}')
        self._items[cls.converter_id]=cls; return cls
    def resolve(self, converter_id: str) -> Converter:
        try: return self._items[converter_id]()
        except KeyError: raise ValueError(f'unregistered converter: {converter_id}') from None
    def ids(self): return tuple(sorted(self._items))
