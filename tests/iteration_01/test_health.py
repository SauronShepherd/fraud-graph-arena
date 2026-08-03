from fastapi.testclient import TestClient


def test_liveness_is_deliberately_modest(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
    assert response.headers["x-correlation-id"]


def test_readiness_checks_owned_round_repository(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"round_repository": "ready"},
    }


def test_version_exposes_only_safe_runtime_metadata(client: TestClient) -> None:
    response = client.get("/api/v1/health/version")

    assert response.status_code == 200
    assert response.json() == {
        "build_version": "0.1.0",
        "contract_version": "v1",
        "runtime_role": "WEB",
        "environment": "test",
    }
    body = response.text.lower()
    assert "sqlite_path" not in body
    assert "password" not in body
    assert "secret" not in body
