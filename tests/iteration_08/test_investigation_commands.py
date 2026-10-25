from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings
from fraud_graph_arena.investigation_commands.adapters.sqlite import SqliteInvestigationCommandRepository
from fraud_graph_arena.shared.errors import ConflictError


def _active_round(client: TestClient) -> str:
    created = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"}).json()
    client.post(f"/api/v1/rounds/{created['id']}/start")
    client.post(f"/api/v1/rounds/{created['id']}/opening/complete")
    return created["id"]


@pytest.fixture
def client(tmp_path: Path):
    settings = Settings(environment="test", round_repository="memory", sqlite_path=tmp_path / "rounds.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as value:
        yield value


def _payload(key="case-note-001"):
    return {"idempotency_key": key, "source_record_id": "T2-O-BAKERY", "target_record_id": "T2-P-CYPHER", "relationship_type": "POSSIBLE_CONTROL"}


def test_hypothesis_is_a_durable_command_record_but_does_not_reveal_or_charge(client):
    round_id = _active_round(client)
    before = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"]
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload())
    after = client.get(f"/api/v1/rounds/{round_id}/workspace").json()["graph"]
    assert response.status_code == 200
    command = response.json()
    assert command["status"] == "RECORDED"
    assert command["charged_credits"] == 0
    assert command["revealed_record_ids"] == []
    assert after == before
    assert len(client.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]) == 1


def test_exact_retry_returns_original_command_and_different_payload_conflicts(client):
    round_id = _active_round(client)
    first = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload()).json()
    replay = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload()).json()
    assert replay["replayed"] is True
    assert replay["command_id"] == first["command_id"]
    changed = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json={**_payload(), "target_record_id": "T2-O-ALPHA"})
    assert changed.status_code == 409
    assert changed.json()["code"] == "IDEMPOTENCY_KEY_REUSED"


def test_hypothesis_rejects_unknown_subjects_same_subjects_and_bad_types(client):
    round_id = _active_round(client)
    for invalid in (
        {**_payload("unknown"), "source_record_id": "NO-SUCH-RECORD"},
        {**_payload("same"), "target_record_id": "T2-O-BAKERY"},
        {**_payload("bad-type"), "relationship_type": "OWNS"},
    ):
        assert client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=invalid).status_code in (400, 404)


def test_hypothesis_requires_safe_idempotency_key_shape(client):
    round_id = _active_round(client)
    response = client.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload("contains spaces"))
    assert response.status_code == 422


def test_concurrent_same_key_creates_one_history_item(client):
    round_id = _active_round(client)
    path = f"/api/v1/rounds/{round_id}/investigations/hypotheses"
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: client.post(path, json=_payload()).json(), range(8)))
    assert len({item["command_id"] for item in results}) == 1
    assert sum(not item["replayed"] for item in results) == 1
    assert len(client.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]) == 1


def test_sqlite_command_survives_repository_recreation_and_replays(tmp_path):
    path = tmp_path / "commands.sqlite3"
    repository = SqliteInvestigationCommandRepository(path)
    from fraud_graph_arena.investigation_commands.service import InvestigationCommand
    item = InvestigationCommand("cmd-1", "round-1", "key-1", "hash-1", "MANUAL_HYPOTHESIS", "A", "B", "POSSIBLE_FLOW", "RECORDED", 0, (), "2026-10-25T00:00:00+00:00")
    assert repository.accept(item) == (item, True)
    reopened = SqliteInvestigationCommandRepository(path)
    assert reopened.list_for_round("round-1") == (item,)
    assert reopened.accept(item) == (item, False)
    with pytest.raises(ConflictError):
        reopened.accept(InvestigationCommand("cmd-2", "round-1", "key-1", "other-hash", "MANUAL_HYPOTHESIS", "A", "C", "POSSIBLE_FLOW", "RECORDED", 0, (), "2026-10-25T00:00:01+00:00"))


def test_sqlite_concurrent_retries_settle_once(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from fraud_graph_arena.investigation_commands.service import InvestigationCommand

    repository = SqliteInvestigationCommandRepository(tmp_path / "concurrent.sqlite3")
    item = InvestigationCommand("cmd-race", "round-race", "key-race", "hash-race", "MANUAL_HYPOTHESIS", "A", "B", "POSSIBLE_FLOW", "RECORDED", 0, (), "2026-10-25T00:00:00+00:00")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: repository.accept(item), range(8)))
    assert sum(created for _, created in results) == 1
    assert {command.command_id for command, _ in results} == {"cmd-race"}
    assert repository.list_for_round("round-race") == (item,)


def test_durable_app_restart_preserves_round_hypothesis_history(tmp_path):
    settings = Settings(environment="test", round_repository="sqlite", sqlite_path=tmp_path / "durable.sqlite3", frontend_dist=tmp_path / "missing")
    with TestClient(create_app(settings)) as first:
        round_id = _active_round(first)
        created = first.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload()).json()
    with TestClient(create_app(settings)) as restarted:
        replay = restarted.post(f"/api/v1/rounds/{round_id}/investigations/hypotheses", json=_payload()).json()
        history = restarted.get(f"/api/v1/rounds/{round_id}/investigations/history").json()["commands"]
    assert replay["command_id"] == created["command_id"]
    assert replay["replayed"] is True
    assert len(history) == 1


def test_round_history_does_not_exist_for_unknown_round(client):
    response = client.get("/api/v1/rounds/missing/investigations/history")
    assert response.status_code == 404


def test_hypothesis_requires_active_round_and_enabled_case(client):
    created = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"}).json()
    not_active = client.post(f"/api/v1/rounds/{created['id']}/investigations/hypotheses", json=_payload())
    assert not_active.status_code == 409
    assert not_active.json()["code"] == "ROUND_NOT_ACTIVE"

    other = client.post("/api/v1/rounds", json={"path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_001"}).json()
    client.post(f"/api/v1/rounds/{other['id']}/start")
    client.post(f"/api/v1/rounds/{other['id']}/opening/complete")
    unavailable = client.post(f"/api/v1/rounds/{other['id']}/investigations/hypotheses", json=_payload())
    assert unavailable.status_code == 409
    assert unavailable.json()["code"] == "ACTION_NOT_AVAILABLE"
