from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ComicKind(StrEnum):
    OPENING = "OPENING"
    CLOSING = "CLOSING"


@dataclass(frozen=True, slots=True)
class ComicPage:
    id: str
    position: int
    title: str
    narration: str
    image_url: str
    alt_text: str


@dataclass(frozen=True, slots=True)
class ComicSequence:
    id: str
    case_id: str
    case_version: str
    kind: ComicKind
    skippable: bool
    pages: tuple[ComicPage, ...]
