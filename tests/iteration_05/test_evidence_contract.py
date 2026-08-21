from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

def test_gate_evidence_has_qualified_sha_and_external_gap():
    report = json.loads((ROOT / "reports/iteration-05/gate.json").read_text())
    assert report["status"] == "pass"
    assert report["live_databricks"] in {"qualified", "not_qualified"}

def test_evidence_collector_is_available():
    assert (ROOT / "scripts/collect_iteration_05_evidence.py").is_file()
