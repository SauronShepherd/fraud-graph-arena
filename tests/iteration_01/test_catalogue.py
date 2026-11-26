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
        "PUPPY": "OPEN",
        "ADULT_DOG": "OPEN",
        "SENIOR_DOG": "OPEN",
    }


def test_academy_catalogue_contains_the_three_canonical_training_cases_and_empty_shell(client: TestClient) -> None:
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
            "id": "ACADEMY_T01",
            "version": "3.0.0-canonical.1-fga13",
            "path_id": "DETECTIVE_ACADEMY",
            "name": "The Missing 120",
            "description": "A guided Academy file for learning a bounded evidence trail without treating a first lead as a verdict.",
            "status": "OPEN",
        },
        {
            "id": "ACADEMY_T02",
            "version": "1.0.0-fga06",
            "path_id": "DETECTIVE_ACADEMY",
            "name": "The Circular Collar",
            "description": "A spoiler-free graph lesson about records, organizations, and directed source relationships.",
            "status": "OPEN",
        },
        {
            "id": "ACADEMY_T03",
            "version": "1.0.0-fga12",
            "path_id": "DETECTIVE_ACADEMY",
            "name": "The Ghost Invoice",
            "description": "An advanced Academy file where chronology, unavailable evidence and uncertainty matter more than a loud accusation.",
            "status": "OPEN",
        },
    ]


def test_ranked_catalogue_publishes_the_ten_case_catalogue(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/PUPPY")

    assert response.status_code == 200
    payload = response.json()
    assert payload["path"]["status"] == "OPEN"
    assert [case["id"] for case in payload["cases"]] == ["BISCUIT_RELIEF", "CEO_BARKED_TWICE", "MADDOG"]
    assert all(case["status"] == "OPEN" for case in payload["cases"])


def test_invalid_path_is_a_deliberate_problem_contract(client: TestClient) -> None:
    response = client.get("/api/v1/catalogue/senior-dog")

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["code"] == "INVALID_PATH_ID"
    assert payload["correlation_id"]
    assert payload["recovery"]
