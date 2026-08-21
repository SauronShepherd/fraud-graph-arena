import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_destructive_tuple_is_explicitly_allowlisted():
    data = json.loads((ROOT / "config/lakehouse/destructive-environments.v1.json").read_text())
    assert data["environments"]["fga_dev"] == {"catalog": "sda_dev", "schema": "sandbox", "allow_destructive_recreation": True}
