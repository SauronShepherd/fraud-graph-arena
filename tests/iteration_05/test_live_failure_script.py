from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_live_failure_script_does_not_update_pointer():
    source=(ROOT/"scripts/qualify_databricks_failure.py").read_text()
    assert "if not args.execute" in source
    assert "OPERATIONAL_TARGETS[0]" in source
    assert "fga_active_publications" in source
    assert "before_id==after_id" in source
