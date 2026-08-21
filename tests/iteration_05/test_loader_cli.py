import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = next((ROOT / "case-data/canonical/v1").iterdir())

def test_plan_cli_is_closed_and_machine_readable():
    result = subprocess.run([sys.executable, "scripts/load_case_datasets.py", str(PACKAGE), "--plan"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    plan = json.loads(result.stdout); assert len(plan["datasets"]) == 32
    assert all(name.startswith("fga_") for name in plan["targets"])
