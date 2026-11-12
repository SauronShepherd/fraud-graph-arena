"""Dependency-free interaction contract experiment for the proposed FGA engine.

The experiment intentionally models commands rather than browser events. It
checks that pointer and keyboard invocation converge on one command path, that
context-menu actions cannot target a stale graph, that node movement supports
commit/cancel semantics, that selection projects to multiple views by stable
ID, and that stale worker responses are ignored.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any


@dataclass(frozen=True)
class MenuContext:
    target_id: str
    graph_version: str
    selection_version: int
    capabilities: frozenset[str]
    return_focus_id: str


@dataclass
class EngineState:
    graph_version: str = "T02:v1"
    selection_version: int = 0
    selected_ids: tuple[str, ...] = ()
    positions: dict[str, tuple[float, float]] = field(
        default_factory=lambda: {"FGA:N:01": (0.0, 0.0), "FGA:N:02": (20.0, 20.0)}
    )
    menu: MenuContext | None = None
    focused_id: str | None = None
    active_move: tuple[str, tuple[float, float]] | None = None
    accepted_worker_request: str | None = None

    def digest(self) -> str:
        value = {
            "graph_version": self.graph_version,
            "selection_version": self.selection_version,
            "selected_ids": self.selected_ids,
            "positions": sorted(self.positions.items()),
            "focused_id": self.focused_id,
            "accepted_worker_request": self.accepted_worker_request,
        }
        return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def select(state: EngineState, node_id: str) -> None:
    state.selected_ids = (node_id,)
    state.selection_version += 1
    state.focused_id = node_id


def open_context_menu(state: EngineState, target_id: str, capabilities: set[str]) -> MenuContext:
    menu = MenuContext(
        target_id=target_id,
        graph_version=state.graph_version,
        selection_version=state.selection_version,
        capabilities=frozenset(capabilities),
        return_focus_id=target_id,
    )
    state.menu = menu
    state.focused_id = None
    return menu


def invoke_menu(state: EngineState, menu: MenuContext, action: str) -> bool:
    if state.graph_version != menu.graph_version or state.selection_version != menu.selection_version:
        return False
    if action not in menu.capabilities:
        return False
    if action == "focus":
        select(state, menu.target_id)
    state.menu = None
    state.focused_id = menu.return_focus_id
    return True


def begin_move(state: EngineState, node_id: str) -> None:
    state.active_move = (node_id, state.positions[node_id])


def update_move(state: EngineState, position: tuple[float, float]) -> None:
    if state.active_move is None:
        raise RuntimeError("move update without move start")
    node_id, _original = state.active_move
    state.positions[node_id] = position


def finish_move(state: EngineState, commit: bool) -> None:
    if state.active_move is None:
        return
    node_id, original = state.active_move
    if not commit:
        state.positions[node_id] = original
    state.active_move = None


def accept_worker_response(state: EngineState, response: dict[str, Any]) -> bool:
    if response["graphVersion"] != state.graph_version:
        return False
    if response["status"] != "completed":
        return False
    state.accepted_worker_request = response["requestId"]
    return True


def representation_ids(state: EngineState) -> dict[str, set[str]]:
    selected = set(state.selected_ids)
    return {
        "node-link": selected,
        "matrix": selected,
        "path": selected,
        "semantic": selected,
    }


def run() -> None:
    pointer = EngineState()
    keyboard = EngineState()
    pointer_menu = open_context_menu(pointer, "FGA:N:01", {"focus"})
    keyboard_menu = open_context_menu(keyboard, "FGA:N:01", {"focus"})
    assert invoke_menu(pointer, pointer_menu, "focus")
    assert invoke_menu(keyboard, keyboard_menu, "focus")
    assert pointer.digest() == keyboard.digest(), "pointer and keyboard paths diverged"

    stale = EngineState()
    stale_menu = open_context_menu(stale, "FGA:N:01", {"focus"})
    select(stale, "FGA:N:02")
    assert not invoke_menu(stale, stale_menu, "focus"), "stale menu was allowed to act"

    movement = EngineState()
    original = movement.positions["FGA:N:01"]
    begin_move(movement, "FGA:N:01")
    update_move(movement, (50.0, 60.0))
    finish_move(movement, commit=False)
    assert movement.positions["FGA:N:01"] == original
    begin_move(movement, "FGA:N:01")
    update_move(movement, (50.0, 60.0))
    finish_move(movement, commit=True)
    assert movement.positions["FGA:N:01"] == (50.0, 60.0)

    select(movement, "FGA:N:01")
    view_ids = representation_ids(movement)
    assert len({frozenset(ids) for ids in view_ids.values()}) == 1

    worker = EngineState()
    assert not accept_worker_response(
        worker,
        {"requestId": "old", "graphVersion": "T02:v0", "status": "completed"},
    )
    assert accept_worker_response(
        worker,
        {"requestId": "current", "graphVersion": "T02:v1", "status": "completed"},
    )
    assert worker.accepted_worker_request == "current"

    print(
        json.dumps(
            {
                "status": "PASS",
                "pointer_keyboard_equivalent": True,
                "stale_menu_rejected": True,
                "movement_cancel_restored": True,
                "movement_commit_applied": True,
                "cross_representation_selection_equal": True,
                "stale_worker_response_rejected": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    run()
