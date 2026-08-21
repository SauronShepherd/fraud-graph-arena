from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_bulk_path_uses_copy_into_and_volume():
    source = (ROOT / "scripts/databricks_copy_into.py").read_text()
    assert "COPY INTO" in source and "/Volumes/" in source
