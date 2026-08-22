from __future__ import annotations
import csv, uuid, hashlib
from datetime import datetime, timezone
from pathlib import Path
from .identity import content_digest, publication_id, semantic_hash
from .models import ImportResult, ImportRun, ImportStatus, PackageIdentity, Publication, PublicationStatus, LoadPolicy
from .registry import PHYSICAL_TARGETS, validate_registry
from .types import validate_row_types
from .validator import validate_candidate
from .lifecycle import require_transition
from .security import redact_error

class CanonicalImportError(ValueError): pass
class ResponseLostAfterActivation(RuntimeError): pass

def serialized_import(method):
    def wrapped(self, root, **kwargs):
        identity = self._identity(Path(root))
        with self.warehouse.scope_lock(identity.key):
            return method(self, root, **kwargs)
    return wrapped

class CanonicalImporter:
    def __init__(self, warehouse): self.warehouse = warehouse; validate_registry(); self.warehouse.topology.update(PHYSICAL_TARGETS.values())
    @staticmethod
    def _transition(run: ImportRun, target: ImportStatus) -> None:
        require_transition(run.status, target); run.status = target
    def _identity(self, root: Path) -> PackageIdentity:
        import csv, json
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        if not manifest.get("case_version"):
            raise CanonicalImportError("manifest case_version is required")
        with (root / "config/cases.csv").open(newline="", encoding="utf-8") as handle:
            case_row = next(csv.DictReader(handle), None)
        if not case_row or case_row.get("case_id") != manifest.get("case_id"):
            raise CanonicalImportError("manifest case_id disagrees with config/cases.csv")
        if case_row.get("case_version") != manifest.get("case_version"):
            raise CanonicalImportError("manifest case_version disagrees with config/cases.csv")
        if case_row.get("snapshot_version") != manifest.get("snapshot_version"):
            raise CanonicalImportError("manifest snapshot_version disagrees with config/cases.csv")
        listed = {item["path"]: item for item in manifest.get("files", [])}
        if not set(PHYSICAL_TARGETS).issubset(listed): raise CanonicalImportError("manifest canonical file inventory mismatch")
        import hashlib
        for rel in PHYSICAL_TARGETS:
            item = listed[rel]
            data = (root / rel).read_bytes()
            if len(data) != item.get("bytes") or hashlib.sha256(data).hexdigest() != item.get("sha256"):
                raise CanonicalImportError(f"manifest digest mismatch: {rel}")
        return PackageIdentity(manifest["case_id"], manifest["case_version"], manifest["snapshot_version"], manifest["canonical_model_version"], content_digest(root))
    @serialized_import
    def import_package(self, root: str | Path, *, retry_of: str | None = None, fail_after: int | None = None, lose_response_after_activation: bool = False, load_policy: LoadPolicy = LoadPolicy.SAFE_ONLY) -> ImportResult:
        root = Path(root); identity = self._identity(root); run_id = "run_" + uuid.uuid4().hex
        run = ImportRun(run_id, identity, retry_of, load_policy=load_policy); self.warehouse.runs[run_id] = run
        if retry_of is not None:
            previous_run = self.warehouse.runs.get(retry_of)
            if previous_run is None or previous_run.identity != identity:
                self._transition(run, ImportStatus.FAILED); run.error_code = "INVALID_RETRY_REFERENCE"; run.finished_at_utc = datetime.now(timezone.utc).isoformat()
                return ImportResult(run_id, run.status, None, None)
        pub_id = publication_id(identity); active = self.warehouse.active.get(identity.key)
        if active == pub_id:
            self._transition(run, ImportStatus.PREFLIGHTED)
            self._transition(run, ImportStatus.REUSED); run.finished_at_utc = datetime.now(timezone.utc).isoformat(); return ImportResult(run_id, run.status, pub_id, self.warehouse.publications[pub_id].semantic_hash)
        # Immutable identity excludes the content digest for conflict detection:
        # the same case/version/snapshot/model may never acquire different bytes.
        if any((p.identity.case_id, p.identity.case_version, p.identity.snapshot_version, p.identity.canonical_model_version) ==
               (identity.case_id, identity.case_version, identity.snapshot_version, identity.canonical_model_version)
               and p.identity.content_digest != identity.content_digest for p in self.warehouse.publications.values()):
            self._transition(run, ImportStatus.FAILED); run.error_code = "IMMUTABLE_SNAPSHOT_CONFLICT"; run.finished_at_utc = datetime.now(timezone.utc).isoformat(); return ImportResult(run_id, run.status, None, None)
        try:
            self._transition(run, ImportStatus.PREFLIGHTED); rows = {}; self._transition(run, ImportStatus.STAGING)
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
            self._transition(run, ImportStatus.STAGED); self._transition(run, ImportStatus.VALIDATING)
            fingerprint = validate_candidate(rows, case_id=identity.case_id, snapshot_version=identity.snapshot_version)
            persisted_rows = {path: [dict(row, _publication_id=pub_id, _load_run_id=run_id) for row in values]
                              for path, values in rows.items()
                              if load_policy != LoadPolicy.SAFE_ONLY or not path.startswith("truth/")}
            candidate = Publication(pub_id, identity, PublicationStatus.CANDIDATE, persisted_rows, fingerprint); self.warehouse.candidates[pub_id] = candidate
            require_transition(candidate.status, PublicationStatus.VALIDATED); candidate.status = PublicationStatus.VALIDATED; self.warehouse.publications[pub_id] = candidate; self.warehouse.candidates.pop(pub_id, None)
            self._transition(run, ImportStatus.VALIDATED); self._transition(run, ImportStatus.PUBLISHING)
            for rel, count in run.datasets.items(): run.dataset_phases[rel] = "VALIDATED"; self.warehouse.record_dataset(run_id, rel, count, count, count, "VALIDATED")
            previous = self.warehouse.active.get(identity.key)
            self.warehouse.active[identity.key] = pub_id
            require_transition(candidate.status, PublicationStatus.ACTIVE); candidate.status = PublicationStatus.ACTIVE
            if previous and previous != pub_id: require_transition(self.warehouse.publications[previous].status, PublicationStatus.SUPERSEDED); self.warehouse.publications[previous].status = PublicationStatus.SUPERSEDED
            self._transition(run, ImportStatus.PUBLISHED); run.finished_at_utc = datetime.now(timezone.utc).isoformat()
            if lose_response_after_activation:
                raise ResponseLostAfterActivation("injected response loss after activation")
            return ImportResult(run_id, run.status, pub_id, candidate.semantic_hash)
        except Exception as exc:
            if isinstance(exc, ResponseLostAfterActivation) and self.warehouse.active.get(identity.key) == pub_id:
                # The commit succeeded; only the client response was lost.
                raise
            if run.status not in (ImportStatus.FAILED, ImportStatus.FAILED_CLEANUP): self._transition(run, ImportStatus.FAILED)
            run.error_code = type(exc).__name__; run.error_summary = redact_error(str(exc)); run.finished_at_utc = datetime.now(timezone.utc).isoformat(); return ImportResult(run_id, run.status, None, None)
