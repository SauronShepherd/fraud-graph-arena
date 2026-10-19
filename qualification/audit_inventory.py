"""Audit the frozen candidate inventory without installing or running candidates."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "Cytoscape.js": "NORMATIVE_INCUMBENT",
    "Sigma.js": "COMPARISON_CANDIDATE",
    "D3": "COMPARISON_CANDIDATE",
    "React Flow": "COMPARISON_CANDIDATE",
}


def main() -> int:
    inventory = json.loads((ROOT / "qualification" / "candidate-inventory.json").read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in inventory.get("candidates", [])}
    errors: list[str] = []
    for name, role in REQUIRED.items():
        entry = entries.get(name)
        if entry is None:
            errors.append(f"missing required candidate: {name}")
        elif entry.get("role") != role:
            errors.append(f"{name} has role {entry.get('role')!r}, expected {role!r}")
        elif entry.get("status") != "MEASURED":
            errors.append(f"{name} is not measured: {entry.get('status')}")
    if inventory.get("commercial_finalist") and not inventory["commercial_finalist"].get("name"):
        errors.append("commercial_finalist must include a name when selected")
    if inventory.get("production_decision") == "QUALIFIED" and errors:
        errors.append("production_decision cannot be QUALIFIED with incomplete candidate evidence")
    result = {"status": "invalid" if errors else "valid", "required_candidates": len(REQUIRED), "errors": errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
