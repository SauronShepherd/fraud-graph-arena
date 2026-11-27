def test_liveness_readiness_and_board_access_are_distinct(client) -> None:
    live = client.get("/api/v1/health/live")
    ready = client.get("/api/v1/health/ready")
    catalogue = client.get("/api/v1/catalogue/DETECTIVE_ACADEMY")

    assert live.status_code == 200
    assert live.json() == {"status": "alive"}
    assert ready.status_code == 200
    assert ready.json() == {
        "status": "ready",
        "checks": {"round_repository": "ready", "frontend_distribution": "ready"},
    }
    assert catalogue.status_code == 200
    assert catalogue.json()["path"]["id"] == "DETECTIVE_ACADEMY"

    created = client.post(
        "/api/v1/rounds",
        json={"player_id": "fga17-smoke", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_001"},
    )
    assert created.status_code == 201, created.text
    round_id = created.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    assert client.get(f"/api/v1/rounds/{round_id}/opening").status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete", json={"completion": "FINISHED"}).status_code == 200
    workspace = client.get(f"/api/v1/rounds/{round_id}/workspace")
    assert workspace.status_code == 200
    assert workspace.json()["round"]["id"] == round_id
