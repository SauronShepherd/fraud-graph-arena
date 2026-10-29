from fraud_graph_arena.case_data.academy_graph import t02_graph
from fraud_graph_arena.case_data.graph_investigation import initial_subset


def test_initial_subset_is_deterministic_and_bounded() -> None:
    result = initial_subset(t02_graph(), limit=3)
    assert [node["record_id"] for node in result["nodes"]] == sorted(node.record_id for node in t02_graph()["nodes"])[:3]
    assert result["partial"] is True
    assert result["omitted_node_count"] == 4


def test_seeded_subset_does_not_use_degree_as_guilt() -> None:
    result = initial_subset(t02_graph(), seeds=["T2-O-BAKERY"])
    assert [node["record_id"] for node in result["nodes"]] == ["T2-O-BAKERY"]
    assert result["edge_count"] == 0


def test_initial_projection_keeps_only_relationships_with_visible_endpoints() -> None:
    graph = t02_graph()
    result = initial_subset(graph, seeds=["T2-O-BAKERY"])
    assert result["node_count"] == 1
    assert result["edge_count"] == 0
    assert result["relationship_filters"] == []
