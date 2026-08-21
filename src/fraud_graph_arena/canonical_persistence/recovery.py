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
