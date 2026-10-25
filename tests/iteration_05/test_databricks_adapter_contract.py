import pytest
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def test_adapter_rejects_unregistered_identifiers():
    warehouse = DatabricksWarehouse()
    with pytest.raises(ValueError): warehouse.qualify_table("fga_arbitrary")
    with pytest.raises(ValueError): warehouse.select(["COUNT(*)"], "fga_import_runs")

def test_candidate_operations_are_registry_resolved(monkeypatch):
    import csv
    from pathlib import Path
    warehouse = DatabricksWarehouse()
    statements = []
    monkeypatch.setattr(DatabricksWarehouse, "execute", lambda self, statement: statements.append(statement) or {"status": {"state": "SUCCEEDED"}})
    package = Path("case-data/canonical/v1/T1_THE_MISSING_120_canonical_case_data_v3")
    with (package / "config/cases.csv").open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    row["case_id"] = "case'1"
    warehouse.insert_candidate("config/cases.csv", [row], "pub_1", "run_1")
    warehouse.cleanup_candidate("pub_1")
    warehouse.activate_publication("case_1", "1.0.0", "snap_1", "1.0.0", "pub_1", "run_1")
    assert any("fga_config_cases_csv" in statement and "case''1" in statement for statement in statements)
    assert all("fga_" in statement for statement in statements)

def test_import_records_use_typed_operational_values():
    from pathlib import Path
    from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
    from fraud_graph_arena.canonical_persistence.models import ImportRunDataset, ImportRunFile
    from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse
    package = Path("case-data/canonical/v1/T1_THE_MISSING_120_canonical_case_data_v3")
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(package)
    run = warehouse.runs[result.run_id]
    assert isinstance(next(iter(run.files.values())), ImportRunFile)
    assert isinstance(next(iter(run.datasets.values())), ImportRunDataset)
    assert warehouse.active_records[run.identity.key].activating_run_id == result.run_id
