from pathlib import Path
from fraud_graph_arena.case_data.registry import sql_types

ROOT = Path(__file__).resolve().parents[2]

def test_typed_registry_drives_non_string_ddl():
    assert sql_types("config/cases.csv")[4] == "INT"
    assert sql_types("config/cases.csv")[10] == "BIGINT"
    assert sql_types("config/cases.csv")[12] == "BOOLEAN"

def test_generated_ddl_is_typed():
    text = (ROOT / "sql/lakehouse/fga_canonical_persistence_v1.sql").read_text(encoding="utf-8")
    assert "case_order INT" in text
    assert "generation_seed BIGINT" in text
    assert "ranked BOOLEAN" in text
    assert "case_order STRING" not in text
