"""Versioned, spoiler-safe Academy curriculum contracts for FGA-16."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from fraud_graph_arena.paths import project_root


SCENARIO_SCHEMA_VERSION = "fga16-academy-scenario-v1"
GOLDEN_SCHEMA_VERSION = "fga16-academy-golden-v1"
ACADEMY_CURRICULUM_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class ScenarioAction:
    action_id: str
    label: str
    kind: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ScenarioAction":
        return cls(action_id=str(value["action_id"]), label=str(value["label"]), kind=str(value["kind"]))

    def public_payload(self) -> dict[str, str]:
        return {"action_id": self.action_id, "label": self.label, "kind": self.kind}


@dataclass(frozen=True, slots=True)
class AcademyScenario:
    scenario_id: str
    scenario_version: str
    title: str
    mechanic: str
    learning_objective: str
    path_id: str
    case_id: str
    seed: str
    visible_evidence: tuple[str, ...]
    actions: tuple[ScenarioAction, ...]
    expected_transitions: tuple[dict[str, str], ...]
    tutorial_guidance: tuple[str, ...]
    resource_profile: dict[str, int]
    execution_mode: str
    protected_expected_outcome: dict[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AcademyScenario":
        return cls(
            scenario_id=str(value["scenario_id"]),
            scenario_version=str(value["scenario_version"]),
            title=str(value["title"]),
            mechanic=str(value["mechanic"]),
            learning_objective=str(value["learning_objective"]),
            path_id=str(value["path_id"]),
            case_id=str(value["case_id"]),
            seed=str(value["seed"]),
            visible_evidence=tuple(str(item) for item in value["visible_evidence"]),
            actions=tuple(ScenarioAction.from_mapping(item) for item in value["actions"]),
            expected_transitions=tuple(
                {"from": str(item["from"]), "action_id": str(item["action_id"]), "to": str(item["to"])}
                for item in value["expected_transitions"]
            ),
            tutorial_guidance=tuple(str(item) for item in value["tutorial_guidance"]),
            resource_profile={str(key): int(item) for key, item in value["resource_profile"].items()},
            execution_mode=str(value["execution_mode"]),
            protected_expected_outcome=dict(value["protected_expected_outcome"]),
        )

    @property
    def golden_result_id(self) -> str:
        return str(self.protected_expected_outcome["golden_result_id"])

    @property
    def expected_final_state(self) -> str:
        return str(self.protected_expected_outcome["final_state"])

    def public_payload(self) -> dict[str, Any]:
        """Return the player-facing contract without golden outcomes or internals."""
        return {
            "scenario_id": self.scenario_id,
            "scenario_version": self.scenario_version,
            "title": self.title,
            "mechanic": self.mechanic,
            "learning_objective": self.learning_objective,
            "path_id": self.path_id,
            "case_id": self.case_id,
            "seed": self.seed,
            "visible_evidence": list(self.visible_evidence),
            "actions": [action.public_payload() for action in self.actions],
            "tutorial_guidance": list(self.tutorial_guidance),
            "resource_profile": dict(self.resource_profile),
        }


class ScenarioRegistry:
    """Loads one immutable curriculum and keeps its public/private views separate."""

    def __init__(self, scenarios_path: Path | None = None, golden_path: Path | None = None) -> None:
        root = project_root()
        self.scenarios_path = scenarios_path or root / "contracts/academy/fga16-scenarios.json"
        self.golden_path = golden_path or root / "contracts/academy/fga16-golden-results.json"
        raw = json.loads(self.scenarios_path.read_text(encoding="utf-8"))
        self._validate_schema(raw)
        self.curriculum_version = str(raw["curriculum_version"])
        self._scenarios = tuple(AcademyScenario.from_mapping(item) for item in raw["scenarios"])
        golden_raw = json.loads(self.golden_path.read_text(encoding="utf-8"))
        if golden_raw.get("schema_version") != GOLDEN_SCHEMA_VERSION:
            raise ValueError("unsupported Academy golden-results schema version")
        self._golden = {str(item["scenario_id"]): dict(item) for item in golden_raw.get("results", [])}
        errors = self.validate_contract()
        if errors:
            raise ValueError("invalid Academy curriculum: " + "; ".join(errors))

    @classmethod
    def from_paths(cls, scenarios_path: Path, golden_path: Path) -> "ScenarioRegistry":
        return cls(scenarios_path=scenarios_path, golden_path=golden_path)

    @staticmethod
    def _validate_schema(raw: Mapping[str, Any]) -> None:
        schema_path = project_root() / "contracts/academy/fga16-academy-scenario.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(raw), key=lambda item: list(item.path))
        if errors:
            location = ".".join(str(part) for part in errors[0].path) or "root"
            raise ValueError(f"{location}: {errors[0].message}")

    def validate_contract(self) -> list[str]:
        errors: list[str] = []
        ids: set[str] = set()
        golden_ids: set[str] = set()
        for scenario in self._scenarios:
            if scenario.scenario_id in ids:
                errors.append(f"duplicate scenario_id: {scenario.scenario_id}")
            ids.add(scenario.scenario_id)
            if scenario.path_id != "DETECTIVE_ACADEMY":
                errors.append(f"{scenario.scenario_id}: Academy scenarios must use DETECTIVE_ACADEMY")
            action_ids = [item.action_id for item in scenario.actions]
            if len(action_ids) != len(set(action_ids)):
                errors.append(f"{scenario.scenario_id}: action ids must be unique")
            if len(scenario.expected_transitions) != len(scenario.actions):
                errors.append(f"{scenario.scenario_id}: every action needs one expected transition")
            state = "READY"
            for action, transition in zip(scenario.actions, scenario.expected_transitions, strict=False):
                if transition["from"] != state:
                    errors.append(f"{scenario.scenario_id}: transition starts at {transition['from']}, expected {state}")
                if transition["action_id"] != action.action_id:
                    errors.append(f"{scenario.scenario_id}: transition action does not match {action.action_id}")
                state = transition["to"]
            if state != scenario.expected_final_state:
                errors.append(f"{scenario.scenario_id}: golden final state disagrees with transition chain")
            golden = self._golden.get(scenario.scenario_id)
            if golden is None:
                errors.append(f"{scenario.scenario_id}: missing golden result")
            else:
                golden_ids.add(str(golden["golden_result_id"]))
                if golden.get("golden_result_id") != scenario.golden_result_id:
                    errors.append(f"{scenario.scenario_id}: golden result id disagrees")
                if golden.get("expected_final_state") != scenario.expected_final_state:
                    errors.append(f"{scenario.scenario_id}: golden final state disagrees")
                if int(golden.get("expected_transition_count", -1)) != len(scenario.actions):
                    errors.append(f"{scenario.scenario_id}: golden transition count disagrees")
        if len(golden_ids) != len(self._golden):
            errors.append("golden results contain an unknown or duplicate scenario")
        return errors

    def scenarios(self) -> tuple[AcademyScenario, ...]:
        return self._scenarios

    def require(self, scenario_id: str) -> AcademyScenario:
        for scenario in self._scenarios:
            if scenario.scenario_id == scenario_id:
                return scenario
        raise KeyError(f"unknown Academy scenario: {scenario_id}")

    def golden(self, scenario_id: str) -> dict[str, Any]:
        try:
            return dict(self._golden[scenario_id])
        except KeyError as exc:
            raise KeyError(f"missing golden result for Academy scenario: {scenario_id}") from exc

    def public_curriculum(self) -> dict[str, Any]:
        return {
            "curriculum_version": self.curriculum_version,
            "path_id": "DETECTIVE_ACADEMY",
            "scenario_count": len(self._scenarios),
            "scenarios": [scenario.public_payload() for scenario in self._scenarios],
        }
