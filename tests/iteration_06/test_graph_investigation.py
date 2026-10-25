import pytest

from fraud_graph_arena.case_data.academy_graph import t02_expandable_graph, t02_graph
from fraud_graph_arena.case_data.graph_investigation import MAX_GRAPH_EDGES, MAX_GRAPH_NODES, expand, filter_relationships, initial_subset


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
    graph = t02_expandable_graph()
    visible = initial_subset(graph, seeds=["T2-O-BAKERY"])
    expanded = expand(graph, visible, "T2-O-BAKERY")
    expanded_ids = {node["record_id"] for node in expanded["nodes"]}
    assert {"T2-O-BAKERY", "T2-ADDR-HUB", "T2-FILE-BAKERY", "T2-P-CYPHER"} <= expanded_ids
    assert "T2-LOGIN-A" not in expanded_ids
    repeated = expand(graph, expanded, "T2-O-BAKERY")
    assert [node["record_id"] for node in repeated["nodes"]] == [node["record_id"] for node in expanded["nodes"]]
    assert [edge["relationship_id"] for edge in repeated["edges"]] == [edge["relationship_id"] for edge in expanded["edges"]]
    with pytest.raises(ValueError):
        expand(graph, visible, "T2-O-BAKERY", depth=2)


def test_expansion_cannot_start_from_hidden_node() -> None:
    graph = t02_expandable_graph()
    visible = initial_subset(graph, seeds=["T2-O-BAKERY"])
    with pytest.raises(PermissionError):
        expand(graph, visible, "T2-O-ALPHA")


def test_filter_changes_view_not_nodes_or_truth() -> None:
    graph = t02_graph()
    filtered = filter_relationships(graph, ["DIRECT_SOURCE"])
    assert filtered["node_count"] == graph["node_count"]
    assert all(edge["relationship_family"] == "DIRECT_SOURCE" for edge in filtered["edges"])
    assert filtered["relationship_filters"] == ["DIRECT_SOURCE"]


def test_initial_projection_enforces_node_ceiling():
    graph = {"nodes": [{"record_id": f"N{i:03}", "record_type": "PERSON_RECORD"} for i in range(MAX_GRAPH_NODES + 5)], "edges": []}
    result = initial_subset(graph, limit=MAX_GRAPH_NODES)
    assert result["node_count"] == MAX_GRAPH_NODES
    assert result["omitted_node_count"] == 5
    assert result["partial"] is True


def test_initial_projection_enforces_edge_ceiling_and_reports_omissions():
    graph = {
        "nodes": [{"record_id": "N0", "record_type": "PERSON_RECORD"}, {"record_id": "N1", "record_type": "PERSON_RECORD"}],
        "edges": [{"relationship_id": f"E{i:04}", "source_record_id": "N0", "target_record_id": "N1", "relationship_family": "DIRECT_SOURCE"} for i in range(MAX_GRAPH_EDGES + 5)],
    }
    result = initial_subset(graph, edge_limit=MAX_GRAPH_EDGES)
    assert result["edge_count"] == MAX_GRAPH_EDGES
    assert result["omitted_edge_count"] == 5
    assert result["partial"] is True


def test_expansion_rejects_client_claims_outside_the_safe_projection():
    graph = t02_graph()
    visible = initial_subset(graph, seeds=["T2-O-BAKERY"])
    visible["nodes"].append({"record_id": "SYNTHETIC-HIDDEN", "record_type": "PERSON_RECORD"})
    with pytest.raises(PermissionError, match="outside the authorized projection"):
        expand(graph, visible, "T2-O-BAKERY")


def test_expansion_respects_both_hard_ceilings():
    nodes = [{"record_id": "N000", "record_type": "PERSON_RECORD"}, {"record_id": "N001", "record_type": "PERSON_RECORD"}]
    edges = [{"relationship_id": f"E{i:04}", "source_record_id": "N000", "target_record_id": "N001", "relationship_family": "DIRECT_SOURCE"} for i in range(MAX_GRAPH_EDGES + 5)]
    graph = {"nodes": nodes, "edges": edges}
    visible = initial_subset(graph, seeds=["N000"])
    result = expand(graph, visible, "N000")
    assert result["node_count"] <= MAX_GRAPH_NODES
    assert result["edge_count"] <= MAX_GRAPH_EDGES
    assert result["omitted_edge_count"] == 5
    assert result["partial"] is True
