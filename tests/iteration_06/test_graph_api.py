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


def test_graph_api_does_not_expose_future_investigation_operations(client):
    round_id = _active_t02(client)
    initial = client.post(f"/api/v1/rounds/{round_id}/graph/initial", json={"seeds": ["T2-O-BAKERY"]})
    assert initial.status_code == 200
    for operation in ("expand", "filter"):
        response = client.post(f"/api/v1/rounds/{round_id}/graph/{operation}", json={})
        assert response.status_code == 404
