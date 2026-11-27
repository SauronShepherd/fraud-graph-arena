from __future__ import annotations

import json

from fraud_graph_arena.academy import ScenarioRegistry


def test_academy_curriculum_has_nine_stable_scenarios_and_golden_transitions() -> None:
    registry = ScenarioRegistry()
    assert registry.curriculum_version == "1.0.0"
    scenarios = registry.scenarios()
    assert len(scenarios) == 9
    assert len({scenario.scenario_id for scenario in scenarios}) == 9
    assert registry.validate_contract() == []
    assert {scenario.mechanic for scenario in scenarios} == {
        "NODE_SELECTION",
        "EDGE_INSPECTION",
        "ENTITY_RESOLUTION",
        "GRAPH_TRAVERSAL",
        "RESOURCE_SPENDING",
        "CONTRADICTORY_EVIDENCE",
        "CORRECT_ACCUSATION",
        "INCORRECT_ACCUSATION",
        "COMPLETE_GAME_LOOP",
    }
    assert all(scenario.seed.startswith("fga16-") for scenario in scenarios)
    assert all(len(scenario.actions) == len(scenario.expected_transitions) for scenario in scenarios)


def test_player_curriculum_excludes_protected_results_and_leading_answer_markers(client) -> None:
    response = client.get("/api/v1/academy/curriculum")
    assert response.status_code == 200, response.text
    payload = response.json()
    serialized = json.dumps(payload).lower()
    assert payload["scenario_count"] == 9
    assert all("protected_expected_outcome" not in scenario for scenario in payload["scenarios"])
    assert "golden_result_id" not in serialized
    assert "expected_final_state" not in serialized
    assert "expected_truth" not in serialized


def test_academy_curriculum_is_embedded_in_the_academy_case_door(client) -> None:
    response = client.get("/api/v1/catalogue/DETECTIVE_ACADEMY")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["academy_curriculum"]["scenario_count"] == 9
    assert payload["academy_curriculum"]["path_id"] == "DETECTIVE_ACADEMY"


def test_public_scenario_payload_is_a_copy_not_a_mutable_private_view() -> None:
    registry = ScenarioRegistry()
    public = registry.public_curriculum()
    public["scenarios"][0]["actions"].clear()
    assert registry.require("academy-node-selection").actions
