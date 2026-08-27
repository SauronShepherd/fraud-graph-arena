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
    assert body["omitted_node_count"] == 5


def test_graph_api_rejects_expansion_of_hidden_node(client):
    round_id = _active_t02(client)
    visible = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]}).json()
    response = client.post(f"/api/v1/rounds/{round_id}/graph/expand", json={"visible": visible, "node_id": "T2-O-ALPHA"})
    assert response.status_code == 403
