import json
from fraud_graph_arena.case_data.registry import TABLE_PATHS, load_registry
def test_fixed_model_has_exactly_32_tables():
    assert len(TABLE_PATHS)==32 and len(set(TABLE_PATHS))==32
    assert set(TABLE_PATHS)==set(json.loads(open('contracts/canonical/v1/canonical-model.json',encoding='utf-8').read())['tables'])
def test_every_table_has_one_ordered_header_registry():
    registry=load_registry(); assert set(registry)==set(TABLE_PATHS); assert all(registry.values())
