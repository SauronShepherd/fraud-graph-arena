from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings
from fraud_graph_arena.investigation_commands.adapters.sqlite import SqliteInvestigationCommandRepository
from fraud_graph_arena.investigation_commands.service import InvestigationCommand
from fraud_graph_arena.shared.errors import ConflictError


def _active_round(client: TestClient, case_id: str = "ACADEMY_T02") -> str:
    created = client.post(
        "/api/v1/rounds",
        json={"path_id": "DETECTIVE_ACADEMY", "case_id": case_id},
    )
    assert created.status_code == 201
    round_id = created.json()["id"]
    assert client.post(f"/api/v1/rounds/{round_id}/start").status_code == 200
    assert client.post(f"/api/v1/rounds/{round_id}/opening/complete").status_code == 200
    return round_id


def _payload(key: str = "case-note-001") -> dict[str, str]:
    return {
        "idempotency_key": key,
        "source_record_id": "T2-O-BAKERY",
        "target_record_id": "T2-P-CYPHER",
        "relationship_type": "POSSIBLE_CONTROL",
    }


@pytest.fixture
def client(tmp_path: Path):
    settings = Settings(
        environment="test",
        round_repository="memory",
        sqlite_path=tmp_path / "rounds.sqlite3",
        frontend_dist=tmp_path / "missing",
    )
    with TestClient(create_app(settings)) as value:
        yield value


def test_hypothesis_is_recorded_without_charging_or_revealing(client: TestClient) -> None:
    round_id = _active_round(client)
    before = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"]

    response = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload())

    assert response.status_code == 200
    command = response.json()
    assert command["action"] == "MANUAL_HYPOTHESIS"
    assert command["status"] == "RECORDED"
    assert command["charged_credits"] == 0
    assert command["revealed_record_ids"] == []
    assert command["replayed"] is False
    assert client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"] == before
    assert len(client.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]) == 1


def test_exact_retry_replays_and_same_key_with_new_payload_conflicts(client: TestClient) -> None:
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/hypotheses"

    first = client.post(path, json=_payload()).json()
    replay = client.post(path, json=_payload()).json()
    changed = client.post(path, json={**_payload(), "target_record_id": "T2-O-ALPHA"})

    assert replay["replayed"] is True
    assert replay["command_id"] == first["command_id"]
    assert changed.status_code == 409
    assert changed.json()["code"] == "IDEMPOTENCY_KEY_REUSED"
    assert len(client.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]) == 1


def test_concurrent_same_key_has_one_effect(client: TestClient) -> None:
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/hypotheses"

    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(lambda _: client.post(path, json=_payload()), range(8)))

    assert all(response.status_code == 200 for response in responses)
    bodies = [response.json() for response in responses]
    assert len({body["command_id"] for body in bodies}) == 1
    assert sum(not body["replayed"] for body in bodies) == 1
    assert len(client.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]) == 1


def test_hypothesis_rejects_unknown_same_and_unsupported_subjects(client: TestClient) -> None:
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/hypotheses"

    unknown = client.post(path, json={**_payload("unknown"), "source_record_id": "NO-SUCH-RECORD"})
    same = client.post(path, json={**_payload("same"), "target_record_id": "T2-O-BAKERY"})
    unsupported = client.post(path, json={**_payload("unsupported"), "relationship_type": "OWNS"})

    assert unknown.status_code == 404
    assert unknown.json()["code"] == "SUBJECT_NOT_AVAILABLE"
    assert same.status_code == 400
    assert same.json()["code"] == "INVALID_HYPOTHESIS_SUBJECTS"
    assert unsupported.status_code == 400
    assert unsupported.json()["code"] == "INVALID_HYPOTHESIS_TYPE"


def test_hypothesis_requires_safe_idempotency_key_shape(client: TestClient) -> None:
    round_id = _active_round(client)
    response = client.post(
        f"/api/v1/rounds/{round_id}/investigations/hypotheses",
        json=_payload("contains spaces"),
    )
    assert response.status_code == 422


def test_history_requires_a_real_round_and_command_requires_active_enabled_case(client: TestClient) -> None:
    missing = client.get("/api/v1/rounds/missing/investigations/history")
    assert missing.status_code == 404

    created = client.post(
        "/api/v1/rounds",
        json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"},
    ).json()
    not_active = client.post(
        f"/api/v1/rounds/{created['id']}/investigations/hypotheses",
        json=_payload(),
    )
    assert not_active.status_code == 409
    assert not_active.json()["code"] == "ROUND_NOT_ACTIVE"

    other_round = _active_round(client, "ACADEMY_001")
    unavailable = client.post(
        f"/api/v1/rounds/{other_round}/investigations/hypotheses",
        json=_payload("other-case"),
    )
    assert unavailable.status_code == 409
    assert unavailable.json()["code"] == "ACTION_NOT_AVAILABLE"


def test_workspace_exposes_only_the_t02_manual_hypothesis_action(client: TestClient) -> None:
    t02 = _active_round(client)
    t02_actions = client.get(f"/api/v1/rounds/{t02}/workspace").json()["actions"]
    assert {action["id"] for action in t02_actions if action["state"] == "AVAILABLE"} == {"CREATE_HYPOTHESIS"}

    academy = _active_round(client, "ACADEMY_001")
    academy_actions = client.get(f"/api/v1/rounds/{academy}/workspace").json()["actions"]
    assert all(action["id"] != "CREATE_HYPOTHESIS" for action in academy_actions)


def _command(command_id: str, key: str, request_hash: str = "hash-1") -> InvestigationCommand:
    return InvestigationCommand(
        command_id,
        "round-1",
        key,
        request_hash,
        "MANUAL_HYPOTHESIS",
        "A",
        "B",
        "POSSIBLE_FLOW",
        "RECORDED",
        0,
        (),
        "2026-11-14T00:00:00+00:00",
    )


def test_sqlite_command_survives_reopen_and_conflicting_reuse(tmp_path: Path) -> None:
    path = tmp_path / "commands.sqlite3"
    repository = SqliteInvestigationCommandRepository(path)
    item = _command("cmd-1", "key-1")

    assert repository.accept(item) == (item, True)
    reopened = SqliteInvestigationCommandRepository(path)
    assert reopened.list_for_round("round-1") == (item,)
    assert reopened.accept(item) == (item, False)
    with pytest.raises(ConflictError):
        reopened.accept(_command("cmd-2", "key-1", "different-hash"))


def test_sqlite_concurrent_retries_settle_once(tmp_path: Path) -> None:
    repository = SqliteInvestigationCommandRepository(tmp_path / "concurrent.sqlite3")
    item = _command("cmd-race", "key-race", "hash-race")

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: repository.accept(item), range(8)))

    assert sum(created for _, created in results) == 1
    assert {command.command_id for command, _ in results} == {"cmd-race"}
    assert repository.list_for_round("round-1") == (item,)


def test_durable_app_restart_preserves_round_and_hypothesis_history(tmp_path: Path) -> None:
    settings = Settings(
        environment="test",
        round_repository="sqlite",
        sqlite_path=tmp_path / "durable.sqlite3",
        frontend_dist=tmp_path / "missing",
    )
    with TestClient(create_app(settings)) as first:
        round_id = _active_round(first)
        created = first.post(
            f"/api/v1/rounds/{round_id}/investigations/hypotheses",
            json=_payload(),
        ).json()
    with TestClient(create_app(settings)) as restarted:
        replay = restarted.post(
            f"/api/v1/rounds/{round_id}/investigations/hypotheses",
            json=_payload(),
        ).json()
        history = restarted.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]

    assert replay["command_id"] == created["command_id"]
    assert replay["replayed"] is True
    assert len(history) == 1
