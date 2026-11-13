from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_bulk_path_uses_write_time_tagged_candidate_plan():
    source = (ROOT / "scripts/import_databricks_candidate.py").read_text()
    assert "_publication_id" in source and "_load_run_id" in source and "/Volumes/" in source

def test_bulk_transfer_is_bounded_and_retryable():
    source = (ROOT / "scripts/databricks_bulk_lifecycle.py").read_text()
    assert "TRANSFER_TIMEOUT_SECONDS" in source
    assert "TRANSFER_RETRIES" in source
    assert "timeout=TRANSFER_TIMEOUT_SECONDS" in source
    assert "for attempt in range(1, TRANSFER_RETRIES + 1)" in source
    assert "PHYSICAL_TARGETS" in source
    assert '"databricks", "fs", "mkdirs"' in source
    assert "ThreadPoolExecutor(max_workers=8)" in source
    assert "existing_status" in source
