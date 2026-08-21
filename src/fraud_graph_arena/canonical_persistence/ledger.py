"""In-memory ledger contract used by the deterministic adapter and tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from .models import ImportStatus

@dataclass
class LedgerRun:
    run_id: str; status: ImportStatus; retry_of: str | None = None
    files: dict[str, dict] = field(default_factory=dict)
    datasets: dict[str, dict] = field(default_factory=dict)
    error_code: str | None = None; error_summary: str | None = None
    started_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ImportLedger:
    def __init__(self): self.runs: dict[str, LedgerRun] = {}
    def start(self, run_id: str, retry_of: str | None = None) -> LedgerRun:
        if run_id in self.runs: raise ValueError("duplicate import run id")
        run = LedgerRun(run_id, ImportStatus.STARTED, retry_of); self.runs[run_id] = run; return run
    def observe_file(self, run_id: str, path: str, byte_length: int, sha256: str) -> None:
        self.runs[run_id].files[path] = {"bytes": byte_length, "sha256": sha256}
    def observe_dataset(self, run_id: str, path: str, source_rows: int, staged_rows: int | None = None, status: str = "OBSERVED") -> None:
        self.runs[run_id].datasets[path] = {"source_rows": source_rows, "staged_rows": staged_rows, "status": status}
    def fail(self, run_id: str, code: str, summary: str) -> None:
        if len(summary) > 512: summary = summary[:512]
        run = self.runs[run_id]; run.status = ImportStatus.FAILED; run.error_code = code; run.error_summary = summary

