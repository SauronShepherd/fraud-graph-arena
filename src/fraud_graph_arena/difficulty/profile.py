from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


PROFILE_VERSION = "fga13-difficulty-profile-v1"
SINGLE_PACKAGE_MODE = "PACKAGE_SINGLE_PROFILE"
PATH_COUNTS = {
    "DETECTIVE_ACADEMY": 3,
    "PUPPY": 3,
    "ADULT_DOG": 4,
    "SENIOR_DOG": 3,
}
EVIDENCE_QUALITIES = frozenset({"GUIDED", "CLEAR", "MIXED", "CONFLICTED", "FRAGMENTED"})


@dataclass(frozen=True, slots=True)
class DifficultyProfile:
    """A difficulty vector attached to one packaged dataset.

    The vector deliberately has no aggregate score.  Higher numeric values mean
    more pressure for the four pressure dimensions, while evidence quality is a
    labelled observation and not an ordered grade.  Progression is owned by the
    path catalogue; this object describes one case only.
    """

    profile_version: str
    path_id: str
    ambiguity: int
    noise: int
    graph_depth: int
    evidence_quality: str
    resource_pressure: int
    mixed_roles: bool
    legitimate_comparators: int
    session_minutes: int
    action_budget: int
    graph_node_limit: int
    hypothesis_target: int
    evidence_threshold: int
    progression_mode: str

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DifficultyProfile":
        return cls(
            profile_version=str(raw["profile_version"]),
            path_id=str(raw["path_id"]),
            ambiguity=int(raw["ambiguity"]),
            noise=int(raw["noise"]),
            graph_depth=int(raw["graph_depth"]),
            evidence_quality=str(raw["evidence_quality"]),
            resource_pressure=int(raw["resource_pressure"]),
            mixed_roles=bool(raw["mixed_roles"]),
            legitimate_comparators=int(raw["legitimate_comparators"]),
            session_minutes=int(raw["session_minutes"]),
            action_budget=int(raw["action_budget"]),
            graph_node_limit=int(raw["graph_node_limit"]),
            hypothesis_target=int(raw["hypothesis_target"]),
            evidence_threshold=int(raw["evidence_threshold"]),
            progression_mode=str(raw["progression_mode"]),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "profile_version": self.profile_version,
            "path_id": self.path_id,
            "ambiguity": self.ambiguity,
            "noise": self.noise,
            "graph_depth": self.graph_depth,
            "evidence_quality": self.evidence_quality,
            "resource_pressure": self.resource_pressure,
            "mixed_roles": self.mixed_roles,
            "legitimate_comparators": self.legitimate_comparators,
            "session_minutes": self.session_minutes,
            "action_budget": self.action_budget,
            "graph_node_limit": self.graph_node_limit,
            "hypothesis_target": self.hypothesis_target,
            "evidence_threshold": self.evidence_threshold,
            "progression_mode": self.progression_mode,
        }


def validate_profile(profile: DifficultyProfile, *, package_path_id: str | None = None) -> list[str]:
    errors: list[str] = []
    if profile.profile_version != PROFILE_VERSION:
        errors.append(f"unsupported profile_version: {profile.profile_version}")
    if profile.path_id not in PATH_COUNTS:
        errors.append(f"unknown path_id: {profile.path_id}")
    if package_path_id is not None and profile.path_id != package_path_id:
        errors.append(f"profile path_id {profile.path_id} disagrees with package path_id {package_path_id}")
    for field in ("ambiguity", "noise", "graph_depth", "resource_pressure"):
        value = getattr(profile, field)
        if not 0 <= value <= 5:
            errors.append(f"{field} must be between 0 and 5")
    if profile.evidence_quality not in EVIDENCE_QUALITIES:
        errors.append(f"unknown evidence_quality: {profile.evidence_quality}")
    if profile.mixed_roles not in (True, False):
        errors.append("mixed_roles must be boolean")
    if profile.legitimate_comparators < 1:
        errors.append("every case needs at least one legitimate comparator")
    if not 5 <= profile.session_minutes <= 60:
        errors.append("session_minutes must be between 5 and 60")
    if profile.action_budget < 1:
        errors.append("action_budget must be positive")
    if profile.graph_node_limit < 1:
        errors.append("graph_node_limit must be positive")
    if not 0 <= profile.hypothesis_target <= 5:
        errors.append("hypothesis_target must be between 0 and 5")
    if not 1 <= profile.evidence_threshold <= 10:
        errors.append("evidence_threshold must be between 1 and 10")
    if profile.progression_mode != SINGLE_PACKAGE_MODE:
        errors.append("difficulty must be attached to one package, never accumulated across levels")
    ranges = {
        "DETECTIVE_ACADEMY": {
            "ambiguity": (0, 2), "noise": (0, 2), "graph_depth": (1, 3),
            "resource_pressure": (0, 2), "session_minutes": (5, 20),
        },
        "PUPPY": {
            "ambiguity": (1, 3), "noise": (0, 3), "graph_depth": (1, 3),
            "resource_pressure": (1, 3), "session_minutes": (15, 30),
        },
        "ADULT_DOG": {
            "ambiguity": (2, 4), "noise": (2, 4), "graph_depth": (2, 4),
            "resource_pressure": (2, 4), "session_minutes": (20, 40),
        },
        "SENIOR_DOG": {
            "ambiguity": (3, 5), "noise": (3, 5), "graph_depth": (3, 5),
            "resource_pressure": (2, 5), "session_minutes": (25, 60),
        },
    }
    expected = ranges.get(profile.path_id)
    if expected:
        for field, (lower, upper) in expected.items():
            value = getattr(profile, field)
            if not lower <= value <= upper:
                errors.append(f"{profile.path_id} {field} must be between {lower} and {upper}")
        if profile.path_id == "DETECTIVE_ACADEMY" and profile.mixed_roles:
            errors.append("Academy teaches mechanics before mixed-role ambiguity")
        if profile.path_id in {"ADULT_DOG", "SENIOR_DOG"} and not profile.mixed_roles:
            errors.append(f"{profile.path_id} must include mixed roles")
        if profile.path_id == "PUPPY" and profile.evidence_quality not in {"CLEAR", "MIXED"}:
            errors.append("Puppy evidence must remain clear or mixed, not fragmented")
        if profile.path_id == "ADULT_DOG" and profile.evidence_quality not in {"MIXED", "CONFLICTED"}:
            errors.append("Adult evidence must expose mixed or conflicting sources")
        if profile.path_id == "SENIOR_DOG" and profile.evidence_quality not in {"CONFLICTED", "FRAGMENTED"}:
            errors.append("Senior evidence must include conflict or fragmentation")
    return errors


def validate_catalogue(packages: Iterable[Any]) -> list[dict[str, str]]:
    """Validate the cross-path balance contract without inventing a scalar score."""

    packages = tuple(package for package in packages if getattr(package, "kind", "canonical") == "canonical")
    errors: list[dict[str, str]] = []
    counts: dict[str, int] = {path: 0 for path in PATH_COUNTS}
    keys: set[tuple[str, str]] = set()
    vectors: list[DifficultyProfile] = []
    for package in packages:
        path_id = str(package.path_id)
        counts[path_id] = counts.get(path_id, 0) + 1
        key = (package.case_id, package.case_version)
        if key in keys:
            errors.append({"check_id": "DIFFICULTY.CASE.DUPLICATE", "message": f"duplicate package identity: {key[0]} {key[1]}"})
        keys.add(key)
        profile = package.difficulty_profile
        vectors.append(profile)
        for message in validate_profile(profile, package_path_id=path_id):
            errors.append({"check_id": "DIFFICULTY.PROFILE", "message": f"{package.case_id}: {message}"})
    for path_id, expected in PATH_COUNTS.items():
        if counts.get(path_id, 0) != expected:
            errors.append({"check_id": "DIFFICULTY.PATH.COUNT", "message": f"{path_id} has {counts.get(path_id, 0)} packages; expected {expected}"})
    if len({(p.ambiguity, p.noise, p.graph_depth, p.resource_pressure) for p in vectors}) < 4:
        errors.append({"check_id": "DIFFICULTY.VECTOR.VARIANCE", "message": "difficulty must vary by dimensions, not collapse to one repeated level"})
    if any(p.progression_mode != SINGLE_PACKAGE_MODE for p in vectors):
        errors.append({"check_id": "DIFFICULTY.PROGRESSION.CUMULATIVE", "message": "path progression and package difficulty must remain separate"})
    return errors
