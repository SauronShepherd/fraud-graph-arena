from __future__ import annotations
from copy import deepcopy
from .models import ImportRun, Publication
from .identity import topology_hash

class MemoryWarehouse:
    """Reference adapter used by tests and dry-run qualification; no SQL or app-state authority."""
    def __init__(self) -> None:
        self.runs: dict[str, ImportRun] = {}; self.publications: dict[str, Publication] = {}
        self.active: dict[tuple[str, str, str], str] = {}; self.topology: set[str] = set(); self.candidates: dict[str, Publication] = {}
    def snapshot(self) -> dict: return deepcopy({"runs": self.runs, "publications": self.publications, "active": self.active, "topology": self.topology, "candidates": self.candidates})
    def topology_digest(self) -> str: return topology_hash(self.topology)
    def rollback(self, scope: tuple[str, str, str], publication_id: str) -> None:
        publication = self.publications.get(publication_id)
        if publication is None or publication.status in ("REJECTED", "CANDIDATE"):
            raise ValueError("publication is not rollback-eligible")
        if publication.identity.key != scope: raise ValueError("publication scope mismatch")
        previous = self.active.get(scope)
        if previous and previous != publication_id: self.publications[previous].status = "SUPERSEDED"
        publication.status = "ACTIVE"; self.active[scope] = publication_id
    def cleanup_candidate(self, publication_id: str, *, fail: bool = False) -> None:
        if fail: raise RuntimeError("candidate cleanup failed")
        self.candidates.pop(publication_id, None)
