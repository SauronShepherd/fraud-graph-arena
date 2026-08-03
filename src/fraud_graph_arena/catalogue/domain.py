from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PathId(StrEnum):
    DETECTIVE_ACADEMY = "DETECTIVE_ACADEMY"
    PUPPY = "PUPPY"
    ADULT_DOG = "ADULT_DOG"
    SENIOR_DOG = "SENIOR_DOG"


class PathStatus(StrEnum):
    OPEN = "OPEN"
    COMING_SOON = "COMING_SOON"
    LOCKED = "LOCKED"


class CaseStatus(StrEnum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"
    CLOSED = "CLOSED"


@dataclass(frozen=True, slots=True)
class PathDefinition:
    id: PathId
    name: str
    description: str
    ranked: bool
    status: PathStatus
    access_message: str


@dataclass(frozen=True, slots=True)
class CaseSummary:
    id: str
    version: str
    path_id: PathId
    name: str
    description: str
    status: CaseStatus


@dataclass(frozen=True, slots=True)
class CatalogueSection:
    path: PathDefinition
    cases: tuple[CaseSummary, ...]
