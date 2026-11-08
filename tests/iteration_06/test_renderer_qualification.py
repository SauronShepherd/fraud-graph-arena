import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_formal_renderer_qualification_is_green() -> None:
    report = json.loads((ROOT / "reports/iteration-06/renderer-cytoscape-qualification-fga-2026-11-08.json").read_text(encoding="utf-8"))
    assert report["candidate"] == "Cytoscape.js"
    assert report["decision"] == "QUALIFIED"
    assert all(value == "PASS" for value in report["hard_requirements"].values())


def test_performance_and_manual_review_are_recorded() -> None:
    performance = json.loads((ROOT / "reports/iteration-06/renderer-performance-fga-2026-11-08.json").read_text(encoding="utf-8"))
    manual = json.loads((ROOT / "reports/iteration-06/renderer-manual-review-fga-2026-11-08.json").read_text(encoding="utf-8"))
    assert performance["status"] == "PASS"
    assert performance["targets"]["repetitions"] == 12
    assert all(candidate["envelope"]["pass"] for candidate in performance["candidates"])
    assert manual["status"] == "PASS"
    assert all(candidate["status"].startswith("PASS") for candidate in manual["candidates"])
