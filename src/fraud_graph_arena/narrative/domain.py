from __future__ import annotations

from dataclasses import dataclass, field
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
    caption: str = ""
    transcript: str = ""
    audio_asset_id: str | None = None

    @property
    def accessible_caption(self) -> str:
        return self.caption or self.narration

    @property
    def accessible_transcript(self) -> str:
        return self.transcript or self.narration


@dataclass(frozen=True, slots=True)
class ComicSequence:
    id: str
    case_id: str
    case_version: str
    kind: ComicKind
    skippable: bool
    pages: tuple[ComicPage, ...]
    variants: dict[str, tuple[ComicPage, ...]] = field(default_factory=dict)
    fictionalization_statement: str = ""
    reduced_motion_behavior: str = "Keep the current panel visible and remove transition motion."
    preload_next: bool = True
    audio_asset_ids: tuple[str, ...] = ()

    def pages_for_variant(self, variant: str | None = None) -> tuple[ComicPage, ...]:
        if not variant:
            return self.pages
        return self.variants.get(variant.upper(), self.pages)
