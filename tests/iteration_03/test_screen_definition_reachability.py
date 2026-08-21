import json
from pathlib import Path

ROOT = Path(__file__).parents[2]

def test_production_graph_reaches_playable_screens_but_not_resolution():
    data = json.loads((ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json").read_text())
    screens = {screen["id"]: screen for screen in data["screens"]}
    reachable = {data["initial_screen"]}
    frontier = list(reachable)
    while frontier:
        current = frontier.pop()
        for transition in screens[current]["transitions"]:
            if transition["target"] not in reachable:
                reachable.add(transition["target"])
                frontier.append(transition["target"])
    assert {"LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD"} <= reachable
    assert "CASE_RESOLUTION" not in reachable
