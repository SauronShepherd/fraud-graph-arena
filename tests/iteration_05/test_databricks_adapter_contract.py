import pytest
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def test_adapter_rejects_unregistered_identifiers():
    warehouse = DatabricksWarehouse()
    with pytest.raises(ValueError): warehouse.qualify_table("fga_arbitrary")
    with pytest.raises(ValueError): warehouse.select(["COUNT(*)"], "fga_import_runs")

def test_candidate_operations_are_registry_resolved(monkeypatch):
    warehouse = DatabricksWarehouse()
    statements = []
    def fake_execute(self, statement):
        statements.append(statement)
        if "SELECT status,case_id,case_version,snapshot_version,canonical_model_version" in statement:
            return {"result": {"data_array": [["VALIDATED", "case_1", "1.0.0", "snap_1", "1.0.0"]]}}
        if "SELECT COUNT(*) AS pointer_count" in statement:
            return {"result": {"data_array": [[0]]}}
        return {"status": {"state": "SUCCEEDED"}}
    monkeypatch.setattr(DatabricksWarehouse, "execute", fake_execute)
    warehouse.insert_candidate("config/cases.csv", [{"case_id": "case'1"}], "pub_1", "run_1")
    warehouse.cleanup_candidate("pub_1")
    warehouse.activate_publication("case_1", "1.0.0", "snap_1", "1.0.0", "pub_1", "run_1")
    assert any("fga_config_cases_csv" in statement and "case''1" in statement for statement in statements)
    assert all("fga_" in statement for statement in statements)

def test_import_records_use_typed_operational_values():
    from pathlib import Path
    from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
    from fraud_graph_arena.canonical_persistence.models import ImportRunDataset, ImportRunFile
    from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse
    package = sorted((Path("case-data/canonical/v1")).iterdir())[0]
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(package)
    run = warehouse.runs[result.run_id]
    assert isinstance(next(iter(run.files.values())), ImportRunFile)
    assert isinstance(next(iter(run.datasets.values())), ImportRunDataset)
    assert warehouse.active_records[run.identity.key].activating_run_id == result.run_id
