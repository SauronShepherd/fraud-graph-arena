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
        if publication.status == PublicationStatus.CANDIDATE: publication.status = PublicationStatus.VALIDATED
        if publication.status != PublicationStatus.VALIDATED: raise PublicationError("publication is not validated")
        scope = publication.identity.key; previous = self.warehouse.active.get(scope)
        if previous and previous != publication_id: self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED
        require_transition(publication.status, PublicationStatus.ACTIVE); publication.status = PublicationStatus.ACTIVE
        self.warehouse.active[scope] = publication_id

    def rollback(self, scope, publication_id: str) -> None:
        publication = self.warehouse.publications.get(publication_id)
        if publication is None or publication.identity.key != scope or publication.status in {PublicationStatus.CANDIDATE, PublicationStatus.REJECTED}:
            raise PublicationError("publication is not rollback-eligible")
        previous = self.warehouse.active.get(scope)
        if previous and previous != publication_id: self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED
        publication.status = PublicationStatus.ACTIVE; self.warehouse.active[scope] = publication_id

    def active_for(self, scope):
        publication_id = self.warehouse.active.get(scope)
        return self.warehouse.publications.get(publication_id) if publication_id else None

