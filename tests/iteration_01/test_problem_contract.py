from fastapi.testclient import TestClient


def test_validation_failures_are_rfc_9457_style_problem_details(client: TestClient) -> None:
    response = client.post(
        "/api/v1/rounds",
        json={"player_id": "", "path_id": "", "case_id": ""},
        headers={"X-Correlation-ID": "case-file-42"},
    )

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["type"].endswith("request-validation-failed")
    assert payload["code"] == "REQUEST_VALIDATION_FAILED"
    assert payload["correlation_id"] == "case-file-42"
    assert payload["instance"] == "/api/v1/rounds"
    assert len(payload["errors"]) == 3
    assert "traceback" not in response.text.lower()


def test_unknown_api_route_uses_problem_contract(client: TestClient) -> None:
    response = client.get("/api/v1/no-such-route")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "ROUTE_NOT_FOUND"
