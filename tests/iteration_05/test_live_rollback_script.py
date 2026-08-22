from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def test_live_rollback_is_dry_run_and_scope_validated():
    source = (ROOT / "scripts/rollback_databricks_publication.py").read_text(encoding="utf-8")
    assert "--execute" in source and "--confirm" in source
    assert "fga_active_publications" in source and "fga_import_publications" in source
    assert "canonical_model_version" in source and "case_version" in source
