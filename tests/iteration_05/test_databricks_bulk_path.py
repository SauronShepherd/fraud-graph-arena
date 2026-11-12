from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_bulk_path_uses_write_time_tagged_candidate_plan():
    source = (ROOT / "scripts/import_databricks_candidate.py").read_text()
    assert "_publication_id" in source and "_load_run_id" in source and "/Volumes/" in source
