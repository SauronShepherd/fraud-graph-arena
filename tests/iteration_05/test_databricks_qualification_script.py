from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_databricks_qualification_is_explicit_and_scoped():
    source = (ROOT / "scripts/qualify_databricks.py").read_text()
    assert "sda_dev" in source and "sandbox" in source
    assert "SHOW TABLES" in source and "expected_topology" in source
