"""Closed lifecycle rules for FGA-05 runs and publications."""
from __future__ import annotations

from .models import ImportStatus, PublicationStatus

RUN_TRANSITIONS: dict[ImportStatus, frozenset[ImportStatus]] = {
    ImportStatus.STARTED: frozenset({ImportStatus.PREFLIGHTED, ImportStatus.FAILED}),
    ImportStatus.PREFLIGHTED: frozenset({ImportStatus.STAGING, ImportStatus.REUSED, ImportStatus.FAILED}),
    ImportStatus.STAGING: frozenset({ImportStatus.STAGED, ImportStatus.FAILED, ImportStatus.FAILED_CLEANUP}),
    ImportStatus.STAGED: frozenset({ImportStatus.VALIDATING, ImportStatus.FAILED}),
    ImportStatus.VALIDATING: frozenset({ImportStatus.VALIDATED, ImportStatus.FAILED, ImportStatus.FAILED_CLEANUP}),
    ImportStatus.VALIDATED: frozenset({ImportStatus.PUBLISHING, ImportStatus.FAILED}),
    ImportStatus.PUBLISHING: frozenset({ImportStatus.PUBLISHED, ImportStatus.REUSED, ImportStatus.FAILED}),
    ImportStatus.PUBLISHED: frozenset(), ImportStatus.REUSED: frozenset(),
    ImportStatus.FAILED: frozenset(), ImportStatus.FAILED_CLEANUP: frozenset(),
}

PUBLICATION_TRANSITIONS: dict[PublicationStatus, frozenset[PublicationStatus]] = {
    PublicationStatus.CANDIDATE: frozenset({PublicationStatus.VALIDATED, PublicationStatus.REJECTED}),
    PublicationStatus.VALIDATED: frozenset({PublicationStatus.ACTIVE, PublicationStatus.REJECTED}),
    PublicationStatus.ACTIVE: frozenset({PublicationStatus.SUPERSEDED}),
    PublicationStatus.SUPERSEDED: frozenset({PublicationStatus.ACTIVE}), PublicationStatus.REJECTED: frozenset(),
}

def can_transition(current, target) -> bool:
    table = RUN_TRANSITIONS if isinstance(current, ImportStatus) else PUBLICATION_TRANSITIONS
    return target in table[current]

def require_transition(current, target) -> None:
    if not can_transition(current, target):
        raise ValueError(f"invalid lifecycle transition: {current} -> {target}")
