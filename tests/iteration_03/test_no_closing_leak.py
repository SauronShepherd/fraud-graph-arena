import json
from pathlib import Path

ROOT = Path(__file__).parents[2]

def test_fga11_screen_set_publishes_resolution_after_submission():
    data = json.loads((ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json").read_text())
    resolution = next(screen for screen in data["screens"] if screen["id"] == "CASE_RESOLUTION")
    assert resolution["route"]["mode"] == "PUBLIC"
    assert resolution["route"]["pattern"] == "/rounds/:roundId/resolution"
    assert any(transition["target"] == "CASE_RESOLUTION" for screen in data["screens"] for transition in screen["transitions"])
    serialized = json.dumps(data).lower()
    assert "evaluator" not in serialized

def test_screen_system_keeps_closing_api_explicit_and_forbids_dynamic_code():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "apps/web/src/screen-system").rglob("*.ts*"))
    assert "/closing" not in source  # The page uses the typed data source, not a raw URL.
    assert "eval(" not in source
    assert "new Function" not in source
