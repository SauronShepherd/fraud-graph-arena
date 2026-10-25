def _active_t02(client):
    created = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"}).json()
    client.post(f"/api/v1/rounds/{created['id']}/start")
    client.post(f"/api/v1/rounds/{created['id']}/opening/complete")
    return created["id"]


def test_graph_api_returns_bounded_initial_projection(client):
    round_id = _active_t02(client)
    response = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"limit": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["node_count"] == 2
    assert body["partial"] is True
    assert body["omitted_node_count"] == 18


def test_graph_api_rejects_expansion_of_hidden_node(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    response = client.post(f"/api/v1/rounds/{round_id}/graph/expand", json={"visible": visible, "node_id": "T2-O-ALPHA"})
    assert response.status_code == 403


def test_graph_api_expansion_adds_one_safe_neighbourhood_only(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    response = client.post(f"/api/v1/rounds/{round_id}/graph/expand", json={"visible": visible, "node_id": "T2-O-BAKERY"})
    assert response.status_code == 200
    ids = {node["record_id"] for node in response.json()["nodes"]}
    assert ids == {"T2-O-BAKERY", "T2-ADDR-HUB", "T2-FILE-BAKERY", "T2-P-CYPHER"}


def test_graph_service_rejects_evaluator_fields_before_projection():
    from fraud_graph_arena.workspace.graph_service import GraphInvestigationService

    service = GraphInvestigationService(lambda _: {"nodes": [], "edges": [], "mastermind": "DO_NOT_SHOW_HERCULE_THIS"})
    try:
        service.initial("round-1")
    except PermissionError as error:
        assert "protected" in str(error)
    else:
        raise AssertionError("evaluator field crossed graph boundary")


def test_graph_service_rejects_forbidden_truth_sentinel_in_value():
    from fraud_graph_arena.workspace.graph_service import GraphInvestigationService

    service = GraphInvestigationService(lambda _: {"nodes": [{"record_id": "N1", "safe_summary": "DO_NOT_SHOW_HERCULE_THIS"}], "edges": []})
    try:
        service.initial("round-1")
    except PermissionError:
        pass
    else:
        raise AssertionError("forbidden evaluator sentinel crossed graph boundary")


def test_graph_api_filter_preserves_nodes_and_changes_only_visible_edges(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial").json()
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": visible, "families": ["NOT_A_REAL_FAMILY"]})
    assert response.status_code == 200
    body = response.json()
    assert body["node_count"] == visible["node_count"]
    assert body["edge_count"] == 0
    assert body["relationship_filters"] == ["NOT_A_REAL_FAMILY"]


def test_graph_api_enforces_hard_node_and_edge_ceilings(client):
    round_id = _active_t02(client)
    for payload in ({"limit": 301}, {"edge_limit": 701}):
        response = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json=payload)
        assert response.status_code == 422
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial").json()
    response = client.post(f"/api/v1/rounds/{round_id}/graph/expand", json={"visible": visible, "node_id": visible["nodes"][0]["record_id"], "limit": 301})
    assert response.status_code == 422
    oversized = dict(visible)
    oversized["nodes"] = visible["nodes"] * 50
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": oversized, "families": []})
    assert response.status_code == 422


def test_graph_filter_rebuilds_records_from_authoritative_projection(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    original = visible["nodes"][0]["safe_summary"]
    visible["nodes"][0]["safe_summary"] = "client supplied summary"
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": visible, "families": []})
    assert response.status_code == 200
    assert response.json()["nodes"][0]["safe_summary"] == original


def test_graph_filter_rejects_ids_outside_authoritative_projection(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    visible["nodes"][0]["record_id"] = "SYNTHETIC-HIDDEN"
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": visible, "families": []})
    assert response.status_code == 403


def test_graph_api_enforces_hard_node_and_edge_limits(client):
    round_id = _active_t02(client)
    for payload in ({"limit": 301}, {"edge_limit": 701}):
        response = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json=payload)
        assert response.status_code == 422


def test_graph_filter_rebuilds_visible_records_from_authoritative_projection(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    original = visible["nodes"][0]["safe_summary"]
    visible["nodes"][0]["safe_summary"] = "client supplied summary"
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": visible, "families": []})
    assert response.status_code == 200
    assert response.json()["nodes"][0]["safe_summary"] == original


def test_graph_filter_rejects_ids_outside_authoritative_projection(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    visible["nodes"][0]["record_id"] = "SYNTHETIC-HIDDEN"
    response = client.post(f"/api/v1/rounds/{round_id}/graph/filter", json={"visible": visible, "families": []})
    assert response.status_code == 403
