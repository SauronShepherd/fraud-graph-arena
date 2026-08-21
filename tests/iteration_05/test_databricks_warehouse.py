import pytest
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def test_live_adapter_only_qualifies_closed_registry_tables():
    warehouse = DatabricksWarehouse()
    assert warehouse.qualify_table("fga_active_publications") == "sda_dev.sandbox.fga_active_publications"
    with pytest.raises(ValueError): warehouse.qualify_table("fga_case_injected")
