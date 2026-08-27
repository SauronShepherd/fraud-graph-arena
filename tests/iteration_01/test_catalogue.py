from fastapi.testclient import TestClient


EXPECTED_PATH_IDS = {
    "DETECTIVE_ACADEMY",
    "PUPPY",
    "ADULT_DOG",
    "SENIOR_DOG",
}


def test_catalogue_exposes_canonical_path_identifiers_and_server_owned_access(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/sections")

    assert response.status_code == 200
    sections = response.json()["sections"]
    assert {item["id"] for item in sections} == EXPECTED_PATH_IDS
    statuses = {item["id"]: item["status"] for item in sections}
    assert statuses == {
        "DETECTIVE_ACADEMY": "OPEN",
        "PUPPY": "COMING_SOON",
        "ADULT_DOG": "LOCKED",
        "SENIOR_DOG": "LOCKED",
    }


def test_academy_catalogue_contains_only_spoiler_free_training_case(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/DETECTIVE_ACADEMY")

    assert response.status_code == 200
    payload = response.json()
    assert payload["path"]["id"] == "DETECTIVE_ACADEMY"
    assert payload["path"]["ranked"] is False
    assert payload["cases"] == [
        {
            "id": "ACADEMY_001",
            "version": "1.0.0-i01",
            "path_id": "DETECTIVE_ACADEMY",
            "name": "The Case of the Empty Evidence Board",
            "description": (
                "A spoiler-free training file whose only mystery is whether the application "
                "can carry it safely from catalogue to board."
            ),
            "status": "OPEN",
        },
        {
            "id": "ACADEMY_T02",
            "version": "1.0.0-fga06",
            "path_id": "DETECTIVE_ACADEMY",
            "name": "The Circular Collar",
            "description": "A spoiler-free graph lesson about records, organizations, and directed source relationships.",
            "status": "OPEN",
        }
    ]


def test_ranked_catalogue_does_not_publish_real_case_details(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/PUPPY")

    assert response.status_code == 200
    payload = response.json()
    assert payload["path"]["status"] == "COMING_SOON"
    assert payload["cases"] == []


def test_invalid_path_is_a_deliberate_problem_contract(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/senior-dog")

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["code"] == "INVALID_PATH_ID"
    assert payload["correlation_id"]
    assert payload["recovery"]
