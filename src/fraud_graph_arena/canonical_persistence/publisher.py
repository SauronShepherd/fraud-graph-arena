"""Pointer-based publication activation and rollback."""
from __future__ import annotations
from .lifecycle import require_transition
from .models import PublicationStatus

class PublicationError(ValueError): pass

class PointerPublisher:
    def __init__(self, warehouse): self.warehouse = warehouse

    def activate(self, publication_id: str) -> None:
        publication = self.warehouse.publications.get(publication_id)
        if publication is None: raise PublicationError("unknown publication")
        if publication.status == PublicationStatus.CANDIDATE:
            require_transition(publication.status, PublicationStatus.VALIDATED); publication.status = PublicationStatus.VALIDATED
        if publication.status != PublicationStatus.VALIDATED: raise PublicationError("publication is not validated")
        scope = publication.identity.key; previous = self.warehouse.active.get(scope)
        require_transition(publication.status, PublicationStatus.ACTIVE); publication.status = PublicationStatus.ACTIVE
        self.warehouse.active[scope] = publication_id
        if previous and previous != publication_id:
            require_transition(self.warehouse.publications[previous].status, PublicationStatus.SUPERSEDED); self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED

    def rollback(self, scope: tuple[str, str], publication_id: str) -> None:
        publication = self.warehouse.publications.get(publication_id)
        if publication is None or publication.identity.key != scope or publication.status in {PublicationStatus.CANDIDATE, PublicationStatus.REJECTED}:
            raise PublicationError("publication is not rollback-eligible")
        previous = self.warehouse.active.get(scope)
        require_transition(publication.status, PublicationStatus.ACTIVE)
        publication.status = PublicationStatus.ACTIVE; self.warehouse.active[scope] = publication_id
        if previous and previous != publication_id:
            require_transition(self.warehouse.publications[previous].status, PublicationStatus.SUPERSEDED); self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED

    def active_for(self, scope):
        publication_id = self.warehouse.active.get(scope)
        return self.warehouse.publications.get(publication_id) if publication_id else None
