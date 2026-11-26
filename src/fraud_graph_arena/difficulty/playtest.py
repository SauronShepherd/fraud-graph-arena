"""Privacy-safe playtest events and aggregate path metrics.

The contract deliberately records investigation behaviour, not player identity,
raw notes or source evidence.  It is an export boundary for a future human
playtest; the deterministic tests exercise the boundary without pretending to
be observations from real players.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Any, Iterable, Mapping

from fraud_graph_arena.difficulty.profile import PATH_COUNTS


PLAYTEST_EVENT_VERSION = "fga13-playtest-event-v1"
EVENT_NAMES = frozenset({"SESSION_STARTED", "CLUE_INSPECTED", "LEAD_RECORDED", "ACTION_USED", "CASE_FINISHED"})
OUTCOMES = frozenset({"COMPLETE", "PARTIAL", "ABANDONED"})
CLUE_DISPOSITIONS = frozenset({"INSPECTED", "IGNORED", "REVISITED"})
ALLOWED_FIELDS = frozenset(
    {
        "event_version",
        "session_token",
        "path_id",
        "case_id",
        "event_name",
        "elapsed_seconds",
        "actions_used",
        "first_lead_seconds",
        "clue_family",
        "clue_disposition",
        "action_family",
        "unsupported_accusation_count",
        "outcome",
    }
)
FORBIDDEN_FIELDS = frozenset({"player_id", "user_id", "email", "phone", "address", "raw_text", "notes", "ip_address"})


@dataclass(frozen=True, slots=True)
class DifficultyPlaytestEvent:
    event_version: str
    session_token: str
    path_id: str
    case_id: str
    event_name: str
    elapsed_seconds: int
    actions_used: int
    first_lead_seconds: int | None = None
    clue_family: str | None = None
    clue_disposition: str | None = None
    action_family: str | None = None
    unsupported_accusation_count: int = 0
    outcome: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DifficultyPlaytestEvent":
        keys = {str(key) for key in raw}
        forbidden = sorted(keys.intersection(FORBIDDEN_FIELDS))
        if forbidden:
            raise ValueError(f"privacy-sensitive playtest fields are not allowed: {', '.join(forbidden)}")
        unknown = sorted(keys - ALLOWED_FIELDS)
        if unknown:
            raise ValueError(f"unknown playtest fields: {', '.join(unknown)}")
        event = cls(
            event_version=str(raw.get("event_version", PLAYTEST_EVENT_VERSION)),
            session_token=str(raw["session_token"]),
            path_id=str(raw["path_id"]),
            case_id=str(raw["case_id"]),
            event_name=str(raw["event_name"]),
            elapsed_seconds=int(raw.get("elapsed_seconds", 0)),
            actions_used=int(raw.get("actions_used", 0)),
            first_lead_seconds=None if raw.get("first_lead_seconds") is None else int(raw["first_lead_seconds"]),
            clue_family=None if raw.get("clue_family") is None else str(raw["clue_family"]),
            clue_disposition=None if raw.get("clue_disposition") is None else str(raw["clue_disposition"]),
            action_family=None if raw.get("action_family") is None else str(raw["action_family"]),
            unsupported_accusation_count=int(raw.get("unsupported_accusation_count", 0)),
            outcome=None if raw.get("outcome") is None else str(raw["outcome"]),
        )
        event.validate()
        return event

    def validate(self) -> None:
        if self.event_version != PLAYTEST_EVENT_VERSION:
            raise ValueError(f"unsupported event_version: {self.event_version}")
        if not self.session_token or len(self.session_token) > 128 or "@" in self.session_token:
            raise ValueError("session_token must be an opaque, non-email token")
        if self.path_id not in PATH_COUNTS:
            raise ValueError(f"unknown path_id: {self.path_id}")
        if not self.case_id or len(self.case_id) > 128:
            raise ValueError("case_id must be a non-empty bounded identifier")
        if self.event_name not in EVENT_NAMES:
            raise ValueError(f"unknown event_name: {self.event_name}")
        if self.elapsed_seconds < 0 or self.actions_used < 0:
            raise ValueError("elapsed_seconds and actions_used must be non-negative")
        if self.first_lead_seconds is not None and self.first_lead_seconds < 0:
            raise ValueError("first_lead_seconds must be non-negative")
        if self.clue_disposition is not None and self.clue_disposition not in CLUE_DISPOSITIONS:
            raise ValueError(f"unknown clue_disposition: {self.clue_disposition}")
        for field_name, value in (("clue_family", self.clue_family), ("action_family", self.action_family)):
            if value is not None and (not value or len(value) > 64):
                raise ValueError(f"{field_name} must be a bounded non-empty value")
        if self.unsupported_accusation_count < 0:
            raise ValueError("unsupported_accusation_count must be non-negative")
        if self.outcome is not None and self.outcome not in OUTCOMES:
            raise ValueError(f"unknown outcome: {self.outcome}")

    def public_payload(self) -> dict[str, Any]:
        """Return the allowlisted event without the opaque session token."""
        return {
            "event_version": self.event_version,
            "path_id": self.path_id,
            "case_id": self.case_id,
            "event_name": self.event_name,
            "elapsed_seconds": self.elapsed_seconds,
            "actions_used": self.actions_used,
            "first_lead_seconds": self.first_lead_seconds,
            "clue_family": self.clue_family,
            "clue_disposition": self.clue_disposition,
            "action_family": self.action_family,
            "unsupported_accusation_count": self.unsupported_accusation_count,
            "outcome": self.outcome,
        }


def aggregate_playtest(events: Iterable[DifficultyPlaytestEvent]) -> dict[str, Any]:
    """Aggregate path metrics without returning session-level identifiers."""
    checked = tuple(events)
    for event in checked:
        event.validate()
    sessions: dict[tuple[str, str, str], list[DifficultyPlaytestEvent]] = {}
    for event in checked:
        sessions.setdefault((event.path_id, event.case_id, event.session_token), []).append(event)

    by_path: dict[str, dict[str, Any]] = {}
    for path_id in PATH_COUNTS:
        path_sessions = [items for (path, _case, _token), items in sessions.items() if path == path_id]
        finished = [items for items in path_sessions if any(item.outcome == "COMPLETE" for item in items)]
        partial = [items for items in path_sessions if any(item.outcome == "PARTIAL" for item in items)]
        lead_times = [item.first_lead_seconds for items in path_sessions for item in items if item.first_lead_seconds is not None]
        action_counts = [max(item.actions_used for item in items) for items in path_sessions]
        action_usage: dict[str, int] = {}
        ignored_clues = 0
        for items in path_sessions:
            for item in items:
                if item.action_family:
                    action_usage[item.action_family] = action_usage.get(item.action_family, 0) + 1
                if item.clue_disposition == "IGNORED":
                    ignored_clues += 1
        by_path[path_id] = {
            "sessions": len(path_sessions),
            "completed": len(finished),
            "partial": len(partial),
            "completion_rate": round(len(finished) / len(path_sessions), 4) if path_sessions else 0.0,
            "partial_success_rate": round(len(partial) / len(path_sessions), 4) if path_sessions else 0.0,
            "median_actions": int(median(action_counts)) if action_counts else 0,
            "median_first_lead_seconds": int(median(lead_times)) if lead_times else None,
            "unsupported_accusations": sum(item.unsupported_accusation_count for items in path_sessions for item in items),
            "ignored_clues": ignored_clues,
            "action_usage": dict(sorted(action_usage.items())),
        }
    return {"event_version": PLAYTEST_EVENT_VERSION, "paths": by_path}

