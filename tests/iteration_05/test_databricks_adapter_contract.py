import pytest
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def test_adapter_rejects_unregistered_identifiers():
    warehouse = DatabricksWarehouse()
    with pytest.raises(ValueError): warehouse.qualify_table("fga_arbitrary")
    with pytest.raises(ValueError): warehouse.select(["COUNT(*)"], "fga_import_runs")

def test_candidate_operations_are_registry_resolved(monkeypatch):
    warehouse = DatabricksWarehouse()
    statements = []
    monkeypatch.setattr(DatabricksWarehouse, "execute", lambda self, statement: statements.append(statement) or {"status": {"state": "SUCCEEDED"}})
    warehouse.insert_candidate("config/cases.csv", [{"case_id": "case'1"}], "pub_1", "run_1")
    warehouse.cleanup_candidate("pub_1")
    warehouse.activate_publication("case_1", "1.0.0", "snap_1", "1.0.0", "pub_1", "run_1")
    assert any("fga_config_cases_csv" in statement and "case''1" in statement for statement in statements)
    assert all("fga_" in statement for statement in statements)
