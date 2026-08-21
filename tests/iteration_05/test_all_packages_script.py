from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_all_package_qualification_is_registry_and_volume_based():
    source=(ROOT/"scripts/qualify_databricks_all_packages.py").read_text()
    assert "databricks\",\"fs\",\"cp" in source and "fga05_stage" in source and "package_count" in source
