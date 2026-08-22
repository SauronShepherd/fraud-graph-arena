from __future__ import annotations
import csv, uuid, hashlib
from datetime import datetime, timezone
from pathlib import Path
from .identity import content_digest, publication_id, semantic_hash
from .models import ImportResult, ImportRun, ImportStatus, PackageIdentity, Publication, PublicationStatus, LoadPolicy, ImportRunFile, ImportRunDataset
from .registry import PHYSICAL_TARGETS, ACTIVE_VIEW_TARGETS, OPERATIONAL_TARGETS, validate_registry
from .types import coerce_row
from .validator import validate_candidate
from .lifecycle import require_transition
from .security import redact_error
from .publisher import PointerPublisher
from .package import CanonicalPackage

class CanonicalImportError(ValueError): pass
class ResponseLostAfterActivation(RuntimeError): pass
class ImportCancelled(RuntimeError): pass

def serialized_import(method):
    def wrapped(self, root, **kwargs):
        identity = self._identity(Path(root))
        with self.warehouse.scope_lock(identity.key):
            return method(self, root, **kwargs)
    return wrapped

class CanonicalImporter:
    def __init__(self, warehouse): self.warehouse = warehouse; validate_registry(); self.warehouse.topology.update(tuple(PHYSICAL_TARGETS.values()) + tuple(ACTIVE_VIEW_TARGETS.values()) + tuple(OPERATIONAL_TARGETS))
    @staticmethod
    def _transition(run: ImportRun, target: ImportStatus) -> None:
        require_transition(run.status, target); run.status = target
    def _identity(self, root: Path) -> PackageIdentity:
        try:
            package = CanonicalPackage.read(root)
        except (KeyError, OSError, ValueError) as exc:
            raise CanonicalImportError(str(exc)) from exc
        return PackageIdentity(package.case_id, package.case_version, package.snapshot_version, package.canonical_model_version, package.content_digest)
    @serialized_import
    def import_package(self, root: str | Path, *, retry_of: str | None = None, fail_after: int | None = None, lose_response_after_activation: bool = False, load_policy: LoadPolicy = LoadPolicy.SAFE_ONLY, cancel_check=None) -> ImportResult:
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
                if cancel_check is not None and cancel_check(): raise ImportCancelled("import cancellation requested")
                path = root / rel
                if not path.is_file() or path.stat().st_size == 0: raise CanonicalImportError(f"missing or zero-byte canonical file: {rel}")
                data = path.read_bytes(); digest = hashlib.sha256(data).hexdigest(); run.files[rel] = ImportRunFile(run_id, rel, len(data), digest); self.warehouse.record_file(run_id, rel, len(data), digest)
                with path.open(newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh); expected = __import__("fraud_graph_arena.case_data.registry", fromlist=["headers"]).headers(rel)
                    if tuple(reader.fieldnames or ()) != expected: raise CanonicalImportError(f"header mismatch: {rel}")
                    rows[rel] = [dict(row) for row in reader]
                    rows[rel] = [coerce_row(row, rel) for row in rows[rel]]
                run.datasets[rel] = ImportRunDataset(run_id, rel, len(rows[rel]), len(rows[rel]), None, "STAGED")
                run.dataset_phases[rel] = "STAGED"; self.warehouse.record_dataset(run_id, rel, len(rows[rel]), len(rows[rel]), None, "STAGED")
                if fail_after is not None and index + 1 == fail_after: raise RuntimeError("injected failure")
            self._transition(run, ImportStatus.STAGED); self._transition(run, ImportStatus.VALIDATING)
            fingerprint = validate_candidate(rows, case_id=identity.case_id, snapshot_version=identity.snapshot_version)
            if load_policy == LoadPolicy.VALIDATION_ONLY:
                self._transition(run, ImportStatus.VALIDATED); run.finished_at_utc = datetime.now(timezone.utc).isoformat()
                return ImportResult(run_id, run.status, None, fingerprint)
            persisted_rows = {path: [dict(row, _publication_id=pub_id, _load_run_id=run_id) for row in values]
                              for path, values in rows.items()
                              if load_policy != LoadPolicy.SAFE_ONLY or not path.startswith("truth/")}
            candidate = Publication(pub_id, identity, PublicationStatus.CANDIDATE, persisted_rows, fingerprint); self.warehouse.candidates[pub_id] = candidate
            require_transition(candidate.status, PublicationStatus.VALIDATED); candidate.status = PublicationStatus.VALIDATED; self.warehouse.publications[pub_id] = candidate; self.warehouse.candidates.pop(pub_id, None)
            self._transition(run, ImportStatus.VALIDATED); self._transition(run, ImportStatus.PUBLISHING)
            for rel, dataset in run.datasets.items():
                dataset.validated_row_count = dataset.staged_row_count; dataset.phase = "VALIDATED"; dataset.validation_check_codes = ("FGA04-HEADER-001", "FGA04-TYPE-001", "FGA04-IDENTITY-001", "FGA04-KEY-001", "FGA04-REFERENCE-001"); run.dataset_phases[rel] = "VALIDATED"; self.warehouse.record_dataset(run_id, rel, dataset.source_row_count, dataset.staged_row_count, dataset.validated_row_count, "VALIDATED", dataset.validation_check_codes)
            PointerPublisher(self.warehouse).activate(pub_id, activating_run_id=run_id)
            self._transition(run, ImportStatus.PUBLISHED); run.finished_at_utc = datetime.now(timezone.utc).isoformat()
            if lose_response_after_activation:
                raise ResponseLostAfterActivation("injected response loss after activation")
            return ImportResult(run_id, run.status, pub_id, candidate.semantic_hash)
        except Exception as exc:
            if isinstance(exc, ResponseLostAfterActivation) and self.warehouse.active.get(identity.key) == pub_id:
                # The commit succeeded; only the client response was lost.
                raise
            if run.status not in (ImportStatus.FAILED, ImportStatus.FAILED_CLEANUP): self._transition(run, ImportStatus.FAILED)
            secrets = tuple(str(getattr(self.warehouse, name, "")) for name in ("profile", "warehouse_id", "catalog", "schema"))
            run.error_code = "CANCELED" if isinstance(exc, ImportCancelled) else type(exc).__name__; run.error_summary = "import canceled by operator" if isinstance(exc, ImportCancelled) else redact_error(str(exc), secrets); run.finished_at_utc = datetime.now(timezone.utc).isoformat();
            if pub_id in self.warehouse.candidates:
                try: self.warehouse.cleanup_candidate(pub_id)
                except Exception: run.status = ImportStatus.FAILED_CLEANUP
            return ImportResult(run_id, run.status, None, None)
