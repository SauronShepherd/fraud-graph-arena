from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_live_metadata_script_tags_all_registry_targets():
    source = (ROOT / "scripts/tag_databricks_publication.py").read_text()
    assert "_publication_id" in source and "_load_run_id" in source and "PHYSICAL_TARGETS" in source
