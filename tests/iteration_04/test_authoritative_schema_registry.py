import json
from pathlib import Path
from fraud_graph_arena.case_data.registry import TABLE_PATHS, load_typed_registry

ROOT = Path(__file__).resolve().parents[2]

def test_contract_registry_is_the_complete_typed_32_table_authority():
    data = json.loads((ROOT / "contracts/canonical/v1/schema-registry.json").read_text())
    assert data["physical_table_count"] == 32
    assert set(data["tables"]) == set(TABLE_PATHS)
    assert data["tables"] == load_typed_registry()
    assert all(column["sql_type"] and "nullable" in column for table in data["tables"].values() for column in table["columns"])

def test_all_package_registry_copies_match_the_authority():
    authority = json.loads((ROOT / "contracts/canonical/v1/schema-registry.json").read_text())["tables"]
    copies = sorted((ROOT / "case-data/canonical/v1").glob("*/fga_canonical_schema_registry_v1.json"))
    assert len(copies) == 13
    assert all(json.loads(path.read_text())["tables"] == authority for path in copies)
