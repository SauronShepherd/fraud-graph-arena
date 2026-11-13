from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_all_package_qualification_is_registry_and_volume_based():
    source=(ROOT/"scripts/qualify_databricks_all_packages.py").read_text()
    helper=(ROOT/"scripts/databricks_bulk_lifecycle.py").read_text()
    assert "run_package" in source and "fga05_stage" in helper and "package_count" in source
    assert "ThreadPoolExecutor" in source and "package-workers" in source


def test_repeat_qualification_is_bounded_and_checks_lifecycle():
    source = (ROOT / "scripts/qualify_databricks_repeat.py").read_text()
    assert "ThreadPoolExecutor" in source
    assert "package-workers" in source
    assert "publication lifecycle did not pass" in source
