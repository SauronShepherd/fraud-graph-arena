from __future__ import annotations
from .models import ImportStatus

TERMINAL = {ImportStatus.PUBLISHED, ImportStatus.REUSED, ImportStatus.FAILED, ImportStatus.FAILED_CLEANUP}

def reconcile_import_runs(warehouse) -> list[str]:
    """Mark interrupted local runs failed without changing active pointers."""
    reconciled = []
    for run in warehouse.runs.values():
        if run.status not in TERMINAL:
            run.status = ImportStatus.FAILED
            run.error_code = "PROCESS_RESTART_RECONCILED"
            reconciled.append(run.run_id)
    return reconciled

def cleanup_rejected_candidate(warehouse, run_id: str, publication_id: str, *, fail: bool = False) -> None:
    """Remove only one rejected candidate and persist cleanup failure explicitly."""
    run = warehouse.runs[run_id]
    try:
        warehouse.cleanup_candidate(publication_id, fail=fail)
    except Exception as exc:
        run.status = ImportStatus.FAILED_CLEANUP
        run.error_code = "CANDIDATE_CLEANUP_FAILED"
        run.error_summary = str(exc)[:512]
        raise
