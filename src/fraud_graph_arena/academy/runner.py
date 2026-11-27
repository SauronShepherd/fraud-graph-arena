"""Shared Academy validation runner.

The runner intentionally labels component simulation separately from API execution.
The same scenario contract feeds both, while the protected expected outcome stays
inside this module and the qualification report.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
import gc
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

from fraud_graph_arena.academy.models import AcademyScenario, ScenarioRegistry
from fraud_graph_arena.config import Settings
from fraud_graph_arena.case_packages import CasePackageRegistry, validate_all_case_packages
from fraud_graph_arena.paths import project_root


@dataclass(frozen=True, slots=True)
class ScenarioRun:
    scenario_id: str
    scenario_version: str
    seed: str
    execution_mode: str
    status: str
    final_state: str | None
    action_history: tuple[str, ...]
    expected_state: str
    actual_state: str | None
    correlation_ids: tuple[str, ...] = ()
    evidence_diff: tuple[str, ...] = ()
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_version": self.scenario_version,
            "seed": self.seed,
            "execution_mode": self.execution_mode,
            "status": self.status,
            "final_state": self.final_state,
            "action_history": list(self.action_history),
            "expected_state": self.expected_state,
            "actual_state": self.actual_state,
            "correlation_ids": list(self.correlation_ids),
            "evidence_diff": list(self.evidence_diff),
            "diagnostics": self.diagnostics,
        }


@dataclass(frozen=True, slots=True)
class AcademyValidationReport:
    status: str
    curriculum_version: str
    scenario_count: int
    runs: tuple[ScenarioRun, ...]
    regression: dict[str, Any]
    persistence: dict[str, Any]
    generated_at_utc: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "curriculum_version": self.curriculum_version,
            "scenario_count": self.scenario_count,
            "runs": [run.as_dict() for run in self.runs],
            "regression": self.regression,
            "persistence": self.persistence,
            "generated_at_utc": self.generated_at_utc,
        }


class AcademyValidationRunner:
    """Run the deterministic component catalogue and the real public API path."""

    def __init__(self, registry: ScenarioRegistry | None = None) -> None:
        self.registry = registry or ScenarioRegistry()

    def run(self) -> AcademyValidationReport:
        runs = tuple(self._run_scenario(scenario) for scenario in self.registry.scenarios())
        regression = self._run_regression()
        persistence = self._run_persistence_probe()
        status = "PASS" if all(run.status == "PASS" for run in runs) and regression["status"] == "PASS" and persistence["status"] == "PASS" else "FAIL"
        return AcademyValidationReport(
            status=status,
            curriculum_version=self.registry.curriculum_version,
            scenario_count=len(runs),
            runs=runs,
            regression=regression,
            persistence=persistence,
            generated_at_utc=datetime.now(UTC).isoformat(),
        )

    def _run_scenario(self, scenario: AcademyScenario) -> ScenarioRun:
        if scenario.mechanic == "MIXED_ROLE_ETHICS":
            return self._run_mixed_role(scenario)
        if scenario.execution_mode == "COMPONENT_MOCK":
            return self._simulate(scenario)
        if scenario.execution_mode == "COMPLETE_LOOP":
            return self._run_complete_loop(scenario)
        return self._run_api_contract(scenario)

    def _run_mixed_role(self, scenario: AcademyScenario) -> ScenarioRun:
        fixture_path = project_root() / "contracts/academy/fga16-mixed-role-cases.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        case = next((item for item in fixture.get("cases", []) if item.get("case_id") == scenario.case_id), None)
        result = self._simulate(scenario)
        errors = list(result.evidence_diff)
        if case is None:
            errors.append(f"mixed-role fixture missing {scenario.case_id}")
        elif case.get("expected_disposition") != "DO_NOT_ACCUSE_WITHOUT_ROLE_EVIDENCE":
            errors.append(f"mixed-role fixture {scenario.case_id} has an unsafe disposition")
        return replace(
            result,
            status="PASS" if not errors else "FAIL",
            final_state=result.expected_state if not errors else None,
            actual_state=result.expected_state if not errors else None,
            evidence_diff=tuple(errors),
            diagnostics={
                **result.diagnostics,
                "runner": "mixed-role-ethics-component-runner",
                "role_pattern": case.get("role_pattern") if case else None,
                "fixture": str(fixture_path.relative_to(project_root())),
            },
        )

    def _simulate(self, scenario: AcademyScenario) -> ScenarioRun:
        state = "READY"
        actions: list[str] = []
        errors: list[str] = []
        for action, transition in zip(scenario.actions, scenario.expected_transitions, strict=False):
            actions.append(action.action_id)
            if transition["from"] != state:
                errors.append(f"{action.action_id}: expected source {transition['from']}, actual {state}")
            state = transition["to"]
        status = "PASS" if not errors and state == scenario.expected_final_state else "FAIL"
        if state != scenario.expected_final_state:
            errors.append(f"final state expected {scenario.expected_final_state}, actual {state}")
        golden = self.registry.golden(scenario.scenario_id)
        if int(golden["expected_transition_count"]) != len(actions):
            errors.append("golden transition count mismatch")
        return ScenarioRun(
            scenario_id=scenario.scenario_id,
            scenario_version=scenario.scenario_version,
            seed=scenario.seed,
            execution_mode=scenario.execution_mode,
            status=status,
            final_state=state,
            action_history=tuple(actions),
            expected_state=scenario.expected_final_state,
            actual_state=state,
            correlation_ids=(f"academy:{scenario.scenario_id}:{scenario.seed}",),
            evidence_diff=tuple(errors),
            diagnostics={"runner": "shared-scenario-component-runner", "golden_result_id": scenario.golden_result_id},
        )

    def _run_api_contract(self, scenario: AcademyScenario) -> ScenarioRun:
        with self._client() as client:
            round_id, correlations = self._open_round(client, scenario)
            action_history: list[str] = []
            errors: list[str] = []
            if scenario.mechanic == "ENTITY_RESOLUTION":
                response = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:analysis"}, json={"idempotency_key": f"{scenario.scenario_id}-analysis"})
                action_history.append("RUN_ENTITY_RESOLUTION")
                correlations.append(response.headers.get("x-correlation-id", "missing"))
                if response.status_code != 200:
                    errors.append(f"entity resolution returned {response.status_code}")
                else:
                    body = response.json()
                    if body.get("actual_engine_run") is not False or not body.get("candidates"):
                        errors.append("entity resolution did not return a deterministic candidate result")
            elif scenario.mechanic == "RESOURCE_SPENDING":
                response = client.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:analysis"}, json={"idempotency_key": f"{scenario.scenario_id}-analysis", "algorithm": "CENTRALITY", "result_limit": 5})
                replay = client.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:replay"}, json={"idempotency_key": f"{scenario.scenario_id}-analysis", "algorithm": "CENTRALITY", "result_limit": 5})
                action_history.append("SPEND_CREDIT")
                correlations.extend([response.headers.get("x-correlation-id", "missing"), replay.headers.get("x-correlation-id", "missing")])
                if response.status_code != 200 or replay.status_code != 200 or not replay.json().get("cached"):
                    errors.append("paid action was not successful and replayable")
            elif scenario.mechanic == "CORRECT_ACCUSATION":
                response = client.post(f"/api/v1/rounds/{round_id}/submission", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:submission"}, json=self._correct_submission(f"{scenario.scenario_id}-submission"))
                action_history.append("SUBMIT_CORRECT")
                correlations.append(response.headers.get("x-correlation-id", "missing"))
                if response.status_code != 200 or response.json().get("ending_code") != "CLEAN_COLLAR":
                    errors.append("supported submission did not produce the golden public receipt")
            elif scenario.mechanic == "INCORRECT_ACCUSATION":
                response = client.post(f"/api/v1/rounds/{round_id}/submission", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:submission"}, json={"idempotency_key": f"{scenario.scenario_id}-submission", "suspect_record_ids": ["T2-P-CYPHER"]})
                action_history.append("SUBMIT_INCORRECT")
                correlations.append(response.headers.get("x-correlation-id", "missing"))
                if response.status_code != 200 or response.json().get("ending_code") != "BARKING_UP_THE_WRONG_TREE":
                    errors.append("unsupported submission did not preserve its public consequence")
            else:
                errors.append(f"no API contract handler for {scenario.mechanic}")
            final_state = scenario.expected_final_state if not errors else None
            return ScenarioRun(
                scenario_id=scenario.scenario_id,
                scenario_version=scenario.scenario_version,
                seed=scenario.seed,
                execution_mode=scenario.execution_mode,
                status="PASS" if not errors else "FAIL",
                final_state=final_state,
                action_history=tuple(action_history),
                expected_state=scenario.expected_final_state,
                actual_state=final_state,
                correlation_ids=tuple(correlations),
                evidence_diff=tuple(errors),
                diagnostics={"round_id_observed": round_id, "runner": "public-api-contract-runner", "golden_result_id": scenario.golden_result_id},
            )

    def _run_complete_loop(self, scenario: AcademyScenario) -> ScenarioRun:
        with self._client() as client:
            round_id, correlations = self._open_round(client, scenario)
            errors: list[str] = []
            actions = ["SELECT_NODE"]
            identity = client.post(f"/api/v1/rounds/{round_id}/investigations/entity-resolution", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:identity"}, json={"idempotency_key": f"{scenario.scenario_id}-identity"})
            correlations.append(identity.headers.get("x-correlation-id", "missing"))
            actions.append("RUN_ENTITY_RESOLUTION")
            analysis = client.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:graph"}, json={"idempotency_key": f"{scenario.scenario_id}-graph", "algorithm": "CENTRALITY", "result_limit": 5})
            correlations.append(analysis.headers.get("x-correlation-id", "missing"))
            actions.extend(["TRAVERSE_GRAPH", "SPEND_CREDIT"])
            submission = client.post(f"/api/v1/rounds/{round_id}/submission", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:submission"}, json=self._correct_submission(f"{scenario.scenario_id}-submission"))
            correlations.append(submission.headers.get("x-correlation-id", "missing"))
            actions.append("SUBMIT_CORRECT")
            workspace = client.get(f"/api/v1/rounds/{round_id}/workspace", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:workspace"})
            ledger = client.get(f"/api/v1/rounds/{round_id}/economy/ledger", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:ledger"})
            closing = client.get(f"/api/v1/rounds/{round_id}/closing", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:closing"})
            correlations.extend([workspace.headers.get("x-correlation-id", "missing"), ledger.headers.get("x-correlation-id", "missing"), closing.headers.get("x-correlation-id", "missing")])
            if identity.status_code != 200 or identity.json().get("actual_engine_run") is not False:
                errors.append("identity boundary failed")
            if analysis.status_code != 200 or analysis.json().get("actual_engine_run") is not False:
                errors.append("graph analytics boundary failed")
            if submission.status_code != 200 or submission.json().get("ending_code") != "CLEAN_COLLAR":
                errors.append("resolution receipt failed")
            if workspace.status_code != 200 or workspace.json()["round"]["credits_remaining"] != 3:
                errors.append("workspace did not reflect two paid actions")
            if ledger.status_code != 200 or len(ledger.json()["entries"]) != 2:
                errors.append("ledger did not preserve two charges")
            if closing.status_code != 200:
                errors.append("closing narrative was not reachable")
            final_state = scenario.expected_final_state if not errors else None
            return ScenarioRun(
                scenario_id=scenario.scenario_id,
                scenario_version=scenario.scenario_version,
                seed=scenario.seed,
                execution_mode=scenario.execution_mode,
                status="PASS" if not errors else "FAIL",
                final_state=final_state,
                action_history=tuple(actions),
                expected_state=scenario.expected_final_state,
                actual_state=final_state,
                correlation_ids=tuple(correlations),
                evidence_diff=tuple(errors),
                diagnostics={"round_id_observed": round_id, "runner": "complete-game-loop-api-runner", "golden_result_id": scenario.golden_result_id, "public_receipt": submission.json() if submission.status_code == 200 else None},
            )

    def _run_regression(self) -> dict[str, Any]:
        registry = CasePackageRegistry()
        manifests = validate_all_case_packages()
        packages = registry.published()
        errors: list[str] = [f"{package_id}: {items}" for package_id, items in manifests.items() if items]
        smoke: list[dict[str, Any]] = []
        with self._client() as client:
            for package in packages:
                created = client.post("/api/v1/rounds", json={"path_id": package.path_id.value, "case_id": package.case_id})
                if created.status_code != 201:
                    errors.append(f"{package.case_id}: create returned {created.status_code}")
                    continue
                round_id = created.json()["id"]
                started = client.post(f"/api/v1/rounds/{round_id}/start")
                completed = client.post(f"/api/v1/rounds/{round_id}/opening/complete")
                workspace = client.get(f"/api/v1/rounds/{round_id}/workspace")
                passed = started.status_code == 200 and completed.status_code == 200 and workspace.status_code == 200
                if not passed:
                    errors.append(f"{package.case_id}: smoke journey failed")
                smoke.append({"case_id": package.case_id, "package_id": package.package_id, "status": "PASS" if passed else "FAIL", "round_status": workspace.json().get("round", {}).get("status") if workspace.status_code == 200 else None})
        return {"status": "PASS" if not errors else "FAIL", "package_count": len(packages), "manifest_count": len(manifests), "smoke": smoke, "errors": errors, "runner": "published-case-regression"}

    def _run_persistence_probe(self) -> dict[str, Any]:
        from fraud_graph_arena.application import create_app

        with TemporaryDirectory(prefix="fga16-academy-") as directory:
            settings = Settings(environment="test", round_repository="sqlite", sqlite_path=Path(directory) / "academy.sqlite3", frontend_dist=Path(directory) / "missing")
            with __import__("fastapi.testclient", fromlist=["TestClient"]).TestClient(create_app(settings)) as first:
                round_id, _ = self._open_round(first, self.registry.require("academy-complete-game-loop"))
                response = first.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", json={"idempotency_key": "fga16-persistence-analysis", "algorithm": "CENTRALITY", "result_limit": 5})
                before = first.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"]
            del first
            gc.collect()
            with __import__("fastapi.testclient", fromlist=["TestClient"]).TestClient(create_app(settings)) as second:
                after = second.get(f"/api/v1/rounds/{round_id}/workspace").json()["round"]["credits_remaining"]
                replay = second.post(f"/api/v1/rounds/{round_id}/investigations/graph-analytics", json={"idempotency_key": "fga16-persistence-analysis", "algorithm": "CENTRALITY", "result_limit": 5})
            del second
            gc.collect()
            idempotent_replay = replay.status_code == 200 and replay.json().get("cached") is True
            passed = response.status_code == 200 and before == 6 and after == before and idempotent_replay
            return {"status": "PASS" if passed else "FAIL", "round_recovered": after == before, "idempotent_replay": idempotent_replay, "errors": [] if passed else ["SQLite restart did not preserve the Academy ledger and replay contract"]}

    @staticmethod
    def _correct_submission(key: str) -> dict[str, Any]:
        return {"idempotency_key": key, "suspect_record_ids": ["T2-P-CIPHER-A", "T2-P-CIPHER-B"], "evidence_claim_ids": ["IDENTITY_MERGE", "FALSE_MERGE_REJECTION", "DIRECTED_PAYMENT_CYCLE", "COORDINATED_ADMINISTRATION", "BENIGN_SHARED_INFRASTRUCTURE"]}

    @staticmethod
    def _client():
        from fastapi.testclient import TestClient
        from fraud_graph_arena.application import create_app

        return TestClient(create_app(Settings(environment="test", round_repository="memory", frontend_dist=Path(".fga16-missing"))))

    @staticmethod
    def _open_round(client: Any, scenario: AcademyScenario) -> tuple[str, list[str]]:
        correlations = [f"academy:{scenario.scenario_id}:round"]
        created = client.post("/api/v1/rounds", headers={"X-Correlation-ID": correlations[0]}, json={"path_id": scenario.path_id, "case_id": scenario.case_id})
        if created.status_code != 201:
            raise RuntimeError(f"Academy scenario could not create its round: {created.status_code} {created.text}")
        round_id = created.json()["id"]
        started = client.post(f"/api/v1/rounds/{round_id}/start", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:start"})
        completed = client.post(f"/api/v1/rounds/{round_id}/opening/complete", headers={"X-Correlation-ID": f"academy:{scenario.scenario_id}:opening"})
        correlations.extend([started.headers.get("x-correlation-id", "missing"), completed.headers.get("x-correlation-id", "missing")])
        if started.status_code != 200 or completed.status_code != 200:
            raise RuntimeError(f"Academy scenario could not enter the board: {started.status_code}/{completed.status_code}")
        return round_id, correlations
