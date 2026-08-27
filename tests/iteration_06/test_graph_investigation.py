import pytest

from fraud_graph_arena.case_data.academy_graph import t02_graph
from fraud_graph_arena.case_data.graph_investigation import expand, filter_relationships, initial_subset


def test_initial_subset_is_deterministic_and_bounded() -> None:
    result = initial_subset(t02_graph(), limit=3)
    assert [node["record_id"] for node in result["nodes"]] == sorted(node.record_id for node in t02_graph()["nodes"])[:3]
    assert result["partial"] is True
    assert result["omitted_node_count"] == 4


def test_seeded_subset_does_not_use_degree_as_guilt() -> None:
    result = initial_subset(t02_graph(), seeds=["T2-O-BAKERY"])
    assert [node["record_id"] for node in result["nodes"]] == ["T2-O-BAKERY"]
    assert result["edge_count"] == 0


def test_expansion_is_one_hop_and_authorized_only() -> None:
    graph = t02_graph()
    visible = initial_subset(graph, seeds=["T2-O-BAKERY"])
    expanded = expand(graph, visible, "T2-O-BAKERY")
    assert "T2-P-CYPHER" in {node["record_id"] for node in expanded["nodes"]}
    with pytest.raises(ValueError):
        expand(graph, visible, "T2-O-BAKERY", depth=2)


def test_expansion_cannot_start_from_hidden_node() -> None:
    graph = t02_graph()
    visible = initial_subset(graph, seeds=["T2-O-BAKERY"])
    with pytest.raises(PermissionError):
        expand(graph, visible, "T2-O-ALPHA")


def test_filter_changes_view_not_nodes_or_truth() -> None:
    graph = t02_graph()
    filtered = filter_relationships(graph, ["DIRECT_SOURCE"])
    assert filtered["node_count"] == graph["node_count"]
    assert all(edge["relationship_family"] == "DIRECT_SOURCE" for edge in filtered["edges"])
    assert filtered["relationship_filters"] == ["DIRECT_SOURCE"]
