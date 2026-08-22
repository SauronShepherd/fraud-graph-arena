from fraud_graph_arena.canonical_persistence.registry import expected_topology
from fraud_graph_arena.canonical_persistence.topology import classify_objects

def test_topology_flags_case_specific_and_unexpected_objects():
    report = classify_objects([*expected_topology(), "fga_BONE_LEDGER_debug", "fga_stage_abandoned"], case_ids=["BONE_LEDGER"])
    assert report["status"] == "fail"
    assert report["case_specific"] == ["fga_BONE_LEDGER_debug"]
    assert report["temporary"] == ["fga_stage_abandoned"]
    assert report["unexpected"] == ["fga_BONE_LEDGER_debug"]
