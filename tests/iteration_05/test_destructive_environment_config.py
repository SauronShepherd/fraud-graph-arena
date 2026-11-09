import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_destructive_tuple_is_explicitly_allowlisted():
    data = json.loads((ROOT / "config/lakehouse/destructive-environments.v1.json").read_text())
    assert data["production_is_absent"] is True
    approved = [
        {key: item[key] for key in ("environment", "catalog", "schema", "destructive_unit")}
        for item in data["approved"]
    ]
    assert {"environment": "fga_dev", "catalog": "sda_dev", "schema": "sandbox", "destructive_unit": "owned_objects"} in approved
