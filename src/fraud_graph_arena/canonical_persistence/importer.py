from __future__ import annotations
import csv, uuid, hashlib
from pathlib import Path
from .identity import content_digest, publication_id, semantic_hash
from .models import ImportResult, ImportRun, ImportStatus, PackageIdentity, Publication, PublicationStatus
from .registry import PHYSICAL_TARGETS, validate_registry
from .types import validate_row_types

class CanonicalImportError(ValueError): pass

class CanonicalImporter:
    def __init__(self, warehouse): self.warehouse = warehouse; validate_registry(); self.warehouse.topology.update(PHYSICAL_TARGETS.values())
    def _identity(self, root: Path) -> PackageIdentity:
        import json
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        listed = {item["path"]: item for item in manifest.get("files", [])}
        if not set(PHYSICAL_TARGETS).issubset(listed): raise CanonicalImportError("manifest canonical file inventory mismatch")
        import hashlib
        for rel in PHYSICAL_TARGETS:
            item = listed[rel]
            data = (root / rel).read_bytes()
            if len(data) != item.get("bytes") or hashlib.sha256(data).hexdigest() != item.get("sha256"):
                raise CanonicalImportError(f"manifest digest mismatch: {rel}")
        return PackageIdentity(manifest["case_id"], manifest.get("case_version", "1.0.0"), manifest["snapshot_version"], manifest["canonical_model_version"], content_digest(root))
    def import_package(self, root: str | Path, *, retry_of: str | None = None, fail_after: int | None = None) -> ImportResult:
        root = Path(root); identity = self._identity(root); run_id = "run_" + uuid.uuid4().hex
        run = ImportRun(run_id, identity, retry_of); self.warehouse.runs[run_id] = run
        pub_id = publication_id(identity); active = self.warehouse.active.get(identity.key)
        if active == pub_id:
            run.status = ImportStatus.REUSED; return ImportResult(run_id, run.status, pub_id, self.warehouse.publications[pub_id].semantic_hash)
        # Immutable identity excludes the content digest for conflict detection:
        # the same case/version/snapshot/model may never acquire different bytes.
        if any((p.identity.case_id, p.identity.case_version, p.identity.snapshot_version, p.identity.canonical_model_version) ==
               (identity.case_id, identity.case_version, identity.snapshot_version, identity.canonical_model_version)
               and p.identity.content_digest != identity.content_digest for p in self.warehouse.publications.values()):
            run.status = ImportStatus.FAILED; run.error_code = "IMMUTABLE_SNAPSHOT_CONFLICT"; return ImportResult(run_id, run.status, None, None)
        try:
            run.status = ImportStatus.PREFLIGHTED; rows = {}; run.status = ImportStatus.STAGING
            for index, rel in enumerate(PHYSICAL_TARGETS):
                path = root / rel
                if not path.is_file() or path.stat().st_size == 0: raise CanonicalImportError(f"missing or zero-byte canonical file: {rel}")
                data = path.read_bytes(); digest = hashlib.sha256(data).hexdigest(); run.files[rel] = {"bytes": len(data), "sha256": digest}; self.warehouse.record_file(run_id, rel, len(data), digest)
                with path.open(newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh); expected = __import__("fraud_graph_arena.case_data.registry", fromlist=["headers"]).headers(rel)
                    if tuple(reader.fieldnames or ()) != expected: raise CanonicalImportError(f"header mismatch: {rel}")
                    rows[rel] = [dict(row) for row in reader]
                    for row in rows[rel]: validate_row_types(row, rel)
                run.datasets[rel] = len(rows[rel])
                run.dataset_phases[rel] = "STAGED"; self.warehouse.record_dataset(run_id, rel, len(rows[rel]), len(rows[rel]), None, "STAGED")
                if fail_after is not None and index + 1 == fail_after: raise RuntimeError("injected failure")
            run.status = ImportStatus.STAGED; run.status = ImportStatus.VALIDATING
            fingerprint = semantic_hash(rows)
            persisted_rows = {path: [dict(row, _publication_id=pub_id, _load_run_id=run_id) for row in values] for path, values in rows.items()}
            candidate = Publication(pub_id, identity, PublicationStatus.CANDIDATE, persisted_rows, fingerprint); self.warehouse.candidates[pub_id] = candidate
            candidate.status = PublicationStatus.VALIDATED; self.warehouse.publications[pub_id] = candidate; self.warehouse.candidates.pop(pub_id, None)
            for rel, count in run.datasets.items(): run.dataset_phases[rel] = "VALIDATED"; self.warehouse.record_dataset(run_id, rel, count, count, count, "VALIDATED")
            previous = self.warehouse.active.get(identity.key)
            if previous: self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED
            candidate.status = PublicationStatus.ACTIVE; self.warehouse.active[identity.key] = pub_id; run.status = ImportStatus.PUBLISHED
            return ImportResult(run_id, run.status, pub_id, candidate.semantic_hash)
        except Exception as exc:
            run.status = ImportStatus.FAILED; run.error_code = type(exc).__name__; run.error_summary = str(exc)[:512]; return ImportResult(run_id, run.status, None, None)
