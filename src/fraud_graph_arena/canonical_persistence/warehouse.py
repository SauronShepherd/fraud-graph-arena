from __future__ import annotations
from copy import deepcopy
from threading import RLock
from .models import ImportRun, Publication, ActivePublication
from datetime import datetime, timezone
from .identity import topology_hash

class MemoryWarehouse:
    """Reference adapter used by tests and dry-run qualification; no SQL or app-state authority."""
    def __init__(self) -> None:
        self.runs: dict[str, ImportRun] = {}; self.publications: dict[str, Publication] = {}
        self.active: dict[tuple[str, str], str] = {}; self.active_records: dict[tuple[str, str], ActivePublication] = {}; self.topology: set[str] = set(); self.candidates: dict[str, Publication] = {}
        self._scope_locks: dict[tuple[str, str], RLock] = {}; self._scope_locks_guard = RLock()
        self.run_files: dict[tuple[str, str], dict] = {}; self.run_datasets: dict[tuple[str, str], dict] = {}
    def snapshot(self) -> dict: return deepcopy({"runs": self.runs, "run_files": self.run_files, "run_datasets": self.run_datasets, "publications": self.publications, "active": self.active, "active_records": self.active_records, "topology": self.topology, "candidates": self.candidates})
    def topology_digest(self) -> str: return topology_hash(self.topology)
    def scope_lock(self, scope: tuple[str, str]) -> RLock:
        with self._scope_locks_guard:
            return self._scope_locks.setdefault(scope, RLock())
    def rollback(self, scope: tuple[str, str], publication_id: str) -> None:
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
    def record_file(self, run_id: str, relative_path: str, byte_length: int, sha256: str) -> None:
        self.run_files[(run_id, relative_path)] = {"run_id": run_id, "relative_path": relative_path, "byte_length": byte_length, "sha256": sha256}
    def record_dataset(self, run_id: str, dataset_path: str, source_rows: int, staged_rows: int | None = None, validated_rows: int | None = None, phase: str = "OBSERVED", validation_check_codes: tuple[str, ...] = ()) -> None:
        self.run_datasets[(run_id, dataset_path)] = {"run_id": run_id, "dataset_path": dataset_path, "source_row_count": source_rows, "staged_row_count": staged_rows, "validated_row_count": validated_rows, "phase": phase, "validation_check_codes": list(validation_check_codes)}
