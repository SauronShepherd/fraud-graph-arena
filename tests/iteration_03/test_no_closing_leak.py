import json
from pathlib import Path

ROOT = Path(__file__).parents[2]

def test_production_screen_set_has_no_public_resolution_or_closing_sequence():
    data = json.loads((ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json").read_text())
    resolution = next(screen for screen in data["screens"] if screen["id"] == "CASE_RESOLUTION")
    assert resolution["route"]["mode"] == "INTERNAL"
    assert resolution["route"]["pattern"] is None
    assert all(transition["target"] != "CASE_RESOLUTION" for screen in data["screens"] for transition in screen["transitions"])
    serialized = json.dumps(data).lower()
    assert "closing" not in serialized
    assert "evaluator" not in serialized

def test_screen_system_does_not_add_closing_api_or_dynamic_code():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "apps/web/src/screen-system").rglob("*.ts*"))
    assert "/closing" not in source
    assert "eval(" not in source
    assert "new Function" not in source
