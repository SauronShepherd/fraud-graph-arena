from fastapi.testclient import TestClient


def create_academy_round(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/api/v1/rounds",
        json={
            "player_id": "hercule",
            "path_id": "DETECTIVE_ACADEMY",
            "case_id": "ACADEMY_001",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_selected_academy_case_reaches_opening_then_empty_board(client: TestClient) -> None:
    created = create_academy_round(client)

    started = client.post(f"/api/v1/rounds/{created['id']}/start")
    assert started.status_code == 200
    assert started.json()["status"] == "INTRO_PENDING"

    opening = client.get(f"/api/v1/rounds/{created['id']}/opening")
    assert opening.status_code == 200
    opening_payload = opening.json()
    assert opening_payload["case"]["id"] == "ACADEMY_001"
    assert opening_payload["sequence"]["kind"] == "OPENING"
    assert len(opening_payload["sequence"]["pages"]) == 2
    assert all(page["alt_text"] for page in opening_payload["sequence"]["pages"])

    blocked_board = client.get(f"/api/v1/rounds/{created['id']}/workspace")
    assert blocked_board.status_code == 409
    assert blocked_board.json()["code"] == "INTRO_REQUIRED"

    completed = client.post(f"/api/v1/rounds/{created['id']}/opening/complete")
    assert completed.status_code == 200
    assert completed.json()["status"] == "ACTIVE"

    board = client.get(f"/api/v1/rounds/{created['id']}/workspace")
    assert board.status_code == 200
    payload = board.json()

    assert payload["round"]["path_id"] == "DETECTIVE_ACADEMY"
    assert payload["round"]["case_id"] == "ACADEMY_001"
    assert payload["case"]["id"] == "ACADEMY_001"
    assert payload["case"]["name"] == "The Case of the Empty Evidence Board"
    assert payload["evidence_count"] == 0
    assert payload["suspect_count"] == 0


def test_start_and_opening_completion_are_idempotent(client: TestClient) -> None:
    created = create_academy_round(client)

    first_start = client.post(f"/api/v1/rounds/{created['id']}/start")
    second_start = client.post(f"/api/v1/rounds/{created['id']}/start")
    assert first_start.json() == second_start.json()

    first_complete = client.post(f"/api/v1/rounds/{created['id']}/opening/complete")
    second_complete = client.post(f"/api/v1/rounds/{created['id']}/opening/complete")
    assert first_complete.json() == second_complete.json()


def test_academy_case_cannot_be_guessed_from_a_ranked_path(client: TestClient) -> None:
    response = client.post(
        "/api/v1/rounds",
        json={
            "player_id": "hercule",
            "path_id": "PUPPY",
            "case_id": "ACADEMY_001",
        },
    )

    assert response.status_code == 409
    assert response.json()["code"] == "PATH_NOT_OPEN"


def test_unpublished_ranked_case_identifiers_are_not_available_as_defaults(client: TestClient) -> None:
    response = client.post(
        "/api/v1/rounds",
        json={
            "player_id": "hercule",
            "path_id": "PUPPY",
            "case_id": "RANKED_CASE_001",
        },
    )

    assert response.status_code == 409
    assert response.json()["code"] == "PATH_NOT_OPEN"


def test_unknown_round_does_not_render_a_fixture_board(client: TestClient) -> None:
    response = client.get("/api/v1/rounds/not-a-round/workspace")

    assert response.status_code == 404
    assert response.json()["code"] == "ROUND_NOT_FOUND"
