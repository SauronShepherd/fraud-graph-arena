from __future__ import annotations

import json

import pytest

from fraud_graph_arena.case_data.academy_graph import t02_expandable_graph
from fraud_graph_arena.graph_analytics.engine import GraphAnalyticsEngine


def _run(algorithm: str, **parameters):
    return GraphAnalyticsEngine().analyze(
        t02_expandable_graph(),
        {"algorithm": algorithm, "result_limit": 20, **parameters},
    )


def test_neighbourhood_is_bounded_and_direction_aware() -> None:
    result = _run("NEIGHBOURHOOD", seed_record_id="T2-O-ALPHA", max_hops=1, directed=True)
    assert result["result_type"] == "NEIGHBOURHOOD_FOUND"
    assert [item["record_id"] for item in result["nodes"]] == ["T2-O-ALPHA", "T2-O-BETA"]
    assert result["supporting_relationship_ids"] == ("T2-REL-016",)


def test_shortest_path_returns_supporting_edges_and_respects_relationship_type() -> None:
    result = _run(
        "SHORTEST_PATH",
        source_record_id="T2-O-ALPHA",
        target_record_id="T2-O-GAMMA",
        max_path_length=3,
        relationship_types=["PAYS"],
    )
    assert result["result_type"] == "PATH_FOUND"
    assert result["paths"] == ({
        "record_ids": ["T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA"],
        "relationship_ids": ["T2-REL-016", "T2-REL-017"],
        "length": 2,
    },)
    assert result["supporting_relationship_ids"] == ("T2-REL-016", "T2-REL-017")


def test_components_are_structural_not_identity_claims() -> None:
    result = _run("CONNECTED_COMPONENTS", directed=False)
    assert result["result_type"] == "COMPONENT"
    assert result["components"][0]["node_count"] == 17
    assert len(result["components"]) >= 2
    serialized = json.dumps(result).lower()
    assert "expected_truth" not in serialized
    assert "mastermind" not in serialized
    assert any("not" in limitation.lower() and "culpability" in limitation.lower() for limitation in result["limitations"])


def test_centrality_is_deterministic_and_explicitly_structural() -> None:
    first = _run("CENTRALITY", centrality_metric="pagerank", directed=True)
    second = _run("CENTRALITY", centrality_metric="pagerank", directed=True)
    assert first["ranked_leads"] == second["ranked_leads"]
    assert first["result_type"] == "RANKED_LEAD"
    assert "not a conviction" in first["interpretation"]
    assert all(item["supporting_relationship_ids"] for item in first["ranked_leads"])


def test_motif_and_circular_flow_preserve_direction_and_time() -> None:
    motif = _run("MOTIF", relationship_types=["PAYS"], max_path_length=3, directed=True)
    cycle = _run("CIRCULAR_FLOW", relationship_types=["PAYS"], max_path_length=3, directed=True)
    assert motif["result_type"] == "MOTIF_CANDIDATE"
    assert cycle["result_type"] == "CIRCULAR_FLOW"
    assert cycle["motifs"][0]["length"] == 3
    assert cycle["motifs"][0]["chronology_observed"] is True
    assert cycle["supporting_relationship_ids"] == ("T2-REL-016", "T2-REL-017", "T2-REL-018")


def test_time_window_can_remove_a_cycle_without_rewriting_the_graph() -> None:
    result = _run(
        "CIRCULAR_FLOW",
        relationship_types=["PAYS"],
        max_path_length=3,
        time_from="2026-03-01T09:30:00Z",
        directed=True,
    )
    assert result["result_type"] == "NO_QUALIFYING_STRUCTURE"
    assert result["motifs"] == ()


def test_engine_rejects_dangling_endpoints_and_duplicate_ids() -> None:
    with pytest.raises(ValueError, match="endpoint"):
        GraphAnalyticsEngine().analyze(
            {"nodes": [{"record_id": "A"}], "edges": [{"relationship_id": "E", "source_record_id": "A", "target_record_id": "MISSING"}]},
            {"algorithm": "CENTRALITY"},
        )
    with pytest.raises(ValueError, match="duplicate relationship"):
        GraphAnalyticsEngine().analyze(
            {
                "nodes": [{"record_id": "A"}, {"record_id": "B"}],
                "edges": [
                    {"relationship_id": "E", "source_record_id": "A", "target_record_id": "B"},
                    {"relationship_id": "E", "source_record_id": "A", "target_record_id": "B"},
                ],
            },
            {"algorithm": "CENTRALITY"},
        )
