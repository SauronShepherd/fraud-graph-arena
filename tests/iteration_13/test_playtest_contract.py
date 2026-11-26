from __future__ import annotations

import pytest

from fraud_graph_arena.difficulty.playtest import DifficultyPlaytestEvent, aggregate_playtest


def _session(path_id: str, case_id: str, token: str) -> list[DifficultyPlaytestEvent]:
    return [
        DifficultyPlaytestEvent.from_mapping(
            {
                "session_token": token,
                "path_id": path_id,
                "case_id": case_id,
                "event_name": "SESSION_STARTED",
                "elapsed_seconds": 0,
                "actions_used": 0,
            }
        ),
        DifficultyPlaytestEvent.from_mapping(
            {
                "session_token": token,
                "path_id": path_id,
                "case_id": case_id,
                "event_name": "LEAD_RECORDED",
                "elapsed_seconds": 90,
                "actions_used": 2,
                "first_lead_seconds": 90,
                "clue_family": "CONTACT_PAIR",
                "clue_disposition": "INSPECTED",
                "action_family": "COMPARE_IDENTITIES",
            }
        ),
        DifficultyPlaytestEvent.from_mapping(
            {
                "session_token": token,
                "path_id": path_id,
                "case_id": case_id,
                "event_name": "CASE_FINISHED",
                "elapsed_seconds": 240,
                "actions_used": 5,
                "action_family": "SUBMIT",
                "unsupported_accusation_count": 0,
                "outcome": "COMPLETE",
            }
        ),
    ]


def test_playtest_export_is_allowlisted_and_aggregates_without_identity() -> None:
    events = sum(
        (
            _session("DETECTIVE_ACADEMY", "ACADEMY_T02", "ephemeral-academy-01"),
            _session("PUPPY", "MADDOG", "ephemeral-puppy-01"),
            _session("ADULT_DOG", "BONE_LEDGER", "ephemeral-adult-01"),
            _session("SENIOR_DOG", "LOVE_LEASHES_OFFSHORE", "ephemeral-senior-01"),
        ),
        [],
    )
    assert all("session_token" not in event.public_payload() for event in events)
    report = aggregate_playtest(events)
    assert report["event_version"] == "fga13-playtest-event-v1"
    assert all(report["paths"][path]["sessions"] == 1 for path in ("DETECTIVE_ACADEMY", "PUPPY", "ADULT_DOG", "SENIOR_DOG"))
    assert all(report["paths"][path]["completion_rate"] == 1.0 for path in report["paths"])
    assert report["paths"]["SENIOR_DOG"]["median_first_lead_seconds"] == 90
    assert report["paths"]["SENIOR_DOG"]["action_usage"]["SUBMIT"] == 1


def test_playtest_contract_rejects_identity_and_unknown_fields() -> None:
    base = {
        "session_token": "ephemeral-academy-02",
        "path_id": "DETECTIVE_ACADEMY",
        "case_id": "ACADEMY_T02",
        "event_name": "SESSION_STARTED",
    }
    with pytest.raises(ValueError, match="privacy-sensitive"):
        DifficultyPlaytestEvent.from_mapping({**base, "email": "player@example.invalid"})
    with pytest.raises(ValueError, match="unknown playtest fields"):
        DifficultyPlaytestEvent.from_mapping({**base, "raw_metric": 1})

