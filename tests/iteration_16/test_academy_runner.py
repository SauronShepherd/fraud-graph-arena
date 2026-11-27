from __future__ import annotations

from fraud_graph_arena.academy import AcademyValidationRunner


def test_shared_runner_qualifies_components_api_complete_loop_regression_and_restart() -> None:
    report = AcademyValidationRunner().run()
    assert report.status == "PASS", report.as_dict()
    assert report.scenario_count == 9
    assert all(run.status == "PASS" for run in report.runs)
    assert report.regression["status"] == "PASS"
    assert report.regression["package_count"] == 14
    assert report.persistence["status"] == "PASS"
    complete = next(run for run in report.runs if run.scenario_id == "academy-complete-game-loop")
    assert complete.action_history == ("SELECT_NODE", "RUN_ENTITY_RESOLUTION", "TRAVERSE_GRAPH", "SPEND_CREDIT", "SUBMIT_CORRECT")
    assert len(complete.correlation_ids) >= 6


def test_failed_component_run_keeps_diagnostics_explicit(monkeypatch) -> None:
    runner = AcademyValidationRunner()
    scenario = runner.registry.require("academy-node-selection")
    broken = scenario.__class__(
        scenario_id=scenario.scenario_id,
        scenario_version=scenario.scenario_version,
        title=scenario.title,
        mechanic=scenario.mechanic,
        learning_objective=scenario.learning_objective,
        path_id=scenario.path_id,
        case_id=scenario.case_id,
        seed=scenario.seed,
        visible_evidence=scenario.visible_evidence,
        actions=scenario.actions,
        expected_transitions=({"from": "WRONG_STATE", "action_id": "SELECT_NODE", "to": "NODE_SELECTED"},),
        tutorial_guidance=scenario.tutorial_guidance,
        resource_profile=scenario.resource_profile,
        execution_mode=scenario.execution_mode,
        protected_expected_outcome=scenario.protected_expected_outcome,
    )
    result = runner._simulate(broken)
    assert result.status == "FAIL"
    assert result.evidence_diff
    assert result.expected_state == "NODE_SELECTED"
