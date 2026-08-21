from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class ImportStatus(StrEnum):
    STARTED = "STARTED"; PREFLIGHTED = "PREFLIGHTED"; STAGING = "STAGING"; STAGED = "STAGED"
    VALIDATING = "VALIDATING"; VALIDATED = "VALIDATED"; PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"; REUSED = "REUSED"; FAILED = "FAILED"; FAILED_CLEANUP = "FAILED_CLEANUP"

class PublicationStatus(StrEnum):
    CANDIDATE = "CANDIDATE"; VALIDATED = "VALIDATED"; ACTIVE = "ACTIVE"; SUPERSEDED = "SUPERSEDED"; REJECTED = "REJECTED"

@dataclass(frozen=True)
class PackageIdentity:
    case_id: str; case_version: str; snapshot_version: str; canonical_model_version: str; content_digest: str
    @property
    # Active publication is case-version scoped. Snapshot identity remains part
    # of the publication ID, but must not create a second visible pointer.
    def key(self) -> tuple[str, str]: return (self.case_id, self.case_version)

@dataclass
class ImportRun:
    run_id: str; identity: PackageIdentity; retry_of: str | None = None
    status: ImportStatus = ImportStatus.STARTED; error_code: str | None = None
    error_summary: str | None = None
    files: dict[str, dict[str, Any]] = field(default_factory=dict)
    datasets: dict[str, int] = field(default_factory=dict)
    dataset_phases: dict[str, str] = field(default_factory=dict)

@dataclass
class Publication:
    publication_id: str; identity: PackageIdentity; status: PublicationStatus
    rows: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    semantic_hash: str = ""

@dataclass(frozen=True)
class ImportResult:
    run_id: str; status: ImportStatus; publication_id: str | None; semantic_hash: str | None
