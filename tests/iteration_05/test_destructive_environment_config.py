import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_destructive_tuple_is_explicitly_allowlisted():
    data = json.loads((ROOT / "config/lakehouse/destructive-environments.v1.json").read_text())
    approved = next(item for item in data["approved"] if item["environment"] == "fga_dev")
    assert approved["catalog"] == "sda_dev" and approved["schema"] == "sandbox"
    assert data["production_is_absent"] is True
