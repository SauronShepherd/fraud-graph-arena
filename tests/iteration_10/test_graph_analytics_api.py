from __future__ import annotations

import json

from fastapi.testclient import TestClient

from .conftest import active_t02


def test_graph_analysis_actions_are_available_without_changing_fga09_economy(client: TestClient) -> None:
    round_id = active_t02(client)
    workspace = client.get(f"/api/v1/rounds/{round_id}/workspace").json()
    available = {item["id"] for item in workspace["actions"] if item["state"] == "AVAILABLE"}
    assert "RUN_GRAPH_ANALYSIS" in available
    assert workspace["round"]["credits_remaining"] == 9


def test_centrality_response_is_bounded_player_safe_and_cacheable(client: TestClient) -> None:
    round_id = active_t02(client)
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    payload = {"algorithm": "CENTRALITY", "centrality_metric": "degree", "result_limit": 5}
    first = client.post(path, json=payload)
    second = client.post(path, json=payload)
    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    body = first.json()
    replay = second.json()
    assert body["actual_engine_run"] is False
    assert body["generation_mode"] == "RUNTIME_DETERMINISTIC_FALLBACK"
    assert body["cached"] is False
    assert replay["cached"] is True
    assert replay["analysis_id"] == body["analysis_id"]
    assert len(body["ranked_leads"]) == 5
    assert "culpability" in body["limitations"][0].lower()
    assert "expected_truth" not in json.dumps(body).lower()
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"] == 9


def test_path_and_cycle_results_expose_supporting_relationships(client: TestClient) -> None:
    round_id = active_t02(client)
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    shortest = client.post(path, json={
        "algorithm": "SHORTEST_PATH",
        "source_record_id": "T2-O-ALPHA",
        "target_record_id": "T2-O-GAMMA",
        "relationship_types": ["PAYS"],
        "max_path_length": 3,
    })
    cycle = client.post(path, json={
        "algorithm": "CIRCULAR_FLOW",
        "relationship_types": ["PAYS"],
        "max_path_length": 3,
    })
    assert shortest.status_code == 200, shortest.text
    assert cycle.status_code == 200, cycle.text
    assert shortest.json()["paths"][0]["relationship_ids"] == ["T2-REL-016", "T2-REL-017"]
    assert cycle.json()["motifs"][0]["relationship_ids"] == ["T2-REL-016", "T2-REL-017", "T2-REL-018"]
    assert set(cycle.json()["supporting_relationship_ids"]) == {"T2-REL-016", "T2-REL-017", "T2-REL-018"}


def test_scope_is_authoritative_and_changes_cache_identity(client: TestClient) -> None:
    round_id = active_t02(client)
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    first = client.post(path, json={"algorithm": "NEIGHBOURHOOD", "seed_record_id": "T2-O-ALPHA", "visible_record_ids": ["T2-O-ALPHA", "T2-O-BETA"]})
    changed_scope = client.post(path, json={"algorithm": "NEIGHBOURHOOD", "seed_record_id": "T2-O-ALPHA", "visible_record_ids": ["T2-O-ALPHA"]})
    assert first.status_code == 200, first.text
    assert changed_scope.status_code == 200, changed_scope.text
    assert first.json()["input_node_count"] == 2
    assert changed_scope.json()["input_node_count"] == 1
    assert first.json()["cache_key"] != changed_scope.json()["cache_key"]
    assert changed_scope.json()["result_type"] == "NO_QUALIFYING_STRUCTURE"


def test_subjects_outside_visible_scope_are_rejected_without_a_query(client: TestClient) -> None:
    round_id = active_t02(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
        json={"algorithm": "NEIGHBOURHOOD", "seed_record_id": "T2-O-ALPHA", "visible_record_ids": ["T2-O-BETA"]},
    )
    assert response.status_code == 400
    assert response.json()["code"] == "GRAPH_SUBJECT_NOT_VISIBLE"


def test_history_contains_only_unique_uncached_runs(client: TestClient) -> None:
    round_id = active_t02(client)
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    payload = {"algorithm": "CONNECTED_COMPONENTS", "directed": False, "result_limit": 20}
    client.post(path, json=payload)
    client.post(path, json=payload)
    history = client.get(f"/api/v1/rounds/{round_id}/investigations/graph-analytics/history")
    assert history.status_code == 200
    assert len(history.json()["analyses"]) == 1


def test_pydantic_bounds_reject_overlarge_result_or_scope(client: TestClient) -> None:
    round_id = active_t02(client)
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    assert client.post(path, json={"algorithm": "CENTRALITY", "result_limit": 21}).status_code == 422
    assert client.post(path, json={"algorithm": "CENTRALITY", "visible_record_ids": [f"N-{i}" for i in range(301)]}).status_code == 422


def test_provider_failure_is_explicit_and_is_not_cached(client: TestClient) -> None:
    round_id = active_t02(client)
    service = client.app.state.container.graph_analytics

    class FailingEngine:
        def analyze(self, graph, request):
            raise RuntimeError("provider unavailable")

    service._engine = FailingEngine()
    path = f"/api/v1/rounds/{round_id}/investigations/graph-analytics"
    first = client.post(path, json={"algorithm": "CENTRALITY"})
    second = client.post(path, json={"algorithm": "CENTRALITY"})

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert first.json()["status"] == "FAILED"
    assert first.json()["result_type"] == "EXECUTION_FAILURE"
    assert first.json()["actual_engine_run"] is False
    assert first.json()["nodes"] == []
    assert second.json()["analysis_id"] != first.json()["analysis_id"]
    assert second.json()["cached"] is False
