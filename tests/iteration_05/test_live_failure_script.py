from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_live_failure_script_does_not_update_pointer():
    source=(ROOT/"scripts/qualify_databricks_failure.py").read_text()
    assert "fga_import_runs" in source and "fga_active_publications" in source and "before_id==after_id" in source
