from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_databricks_smoke_script_uses_registry_targets():
    source = (ROOT / "scripts/qualify_databricks_smoke_import.py").read_text()
    assert "PHYSICAL_TARGETS" in source and "_publication_id" in source and "_load_run_id" in source
