from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_live_publication_script_uses_pointer_tables():
    source=(ROOT/"scripts/record_databricks_publication.py").read_text()
    assert "fga_import_publications" in source and "fga_active_publications" in source and "PUBLISHED" in source
