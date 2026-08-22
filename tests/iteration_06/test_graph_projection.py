from fraud_graph_arena.case_data.academy_graph import t02_graph
from fraud_graph_arena.case_data.graph_data import project_graph


def test_t02_initial_topology_is_exact() -> None:
    graph = t02_graph()
    assert graph["node_count"] == 7
    assert graph["edge_count"] == 7
    assert {node.record_id for node in graph["nodes"]} == {"T2-P-CIPHER-A", "T2-P-CIPHER-B", "T2-P-CYPHER", "T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA", "T2-O-BAKERY"}
    assert {edge.relationship_id for edge in graph["edges"]} == {"T2-REL-001", "T2-REL-002", "T2-REL-003", "T2-REL-004", "T2-REL-016", "T2-REL-017", "T2-REL-018"}


def test_graph_rejects_unresolved_edge_endpoint() -> None:
    try:
        project_graph([{"record_id": "N1"}], [{"relationship_id": "E1", "source_record_id": "N1", "target_record_id": "MISSING"}])
    except ValueError as error:
        assert "endpoint" in str(error)
    else:
        raise AssertionError("unresolved endpoint was accepted")
