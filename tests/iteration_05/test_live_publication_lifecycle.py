from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_live_publication_recorder_is_dry_run_by_default_and_validation_gated():
    source = (ROOT / "scripts/record_databricks_publication.py").read_text(encoding="utf-8")
    assert "--execute" in source
    assert "validate_results" in source
    assert "'STARTED'" in source and "'CANDIDATE'" in source
    assert "INSERT INTO {runs}" in source
    assert "INSERT INTO {runs} VALUES" not in source
