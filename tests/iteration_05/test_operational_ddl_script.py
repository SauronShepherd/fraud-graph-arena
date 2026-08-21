from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_operational_repair_script_declares_all_ledger_tables():
    source=(ROOT/"scripts/repair_databricks_operational_ddl.py").read_text()
    for name in ("fga_import_runs","fga_import_run_files","fga_import_run_datasets","fga_import_publications","fga_active_publications"):
        assert name in source
