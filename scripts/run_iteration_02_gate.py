from __future__ import annotations

import json
import platform
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).parents[1]
REPORT = ROOT / "reports" / "iteration-02"
NPM = "npm.cmd" if os.name == "nt" else "npm"

def run(label: str, command: list[str], cwd: Path = ROOT) -> dict[str, object]:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=300)
        return {"label": label, "command": command, "returncode": result.returncode, "duration_seconds": round(time.monotonic() - started, 3), "stdout": (result.stdout or "")[-12000:], "stderr": (result.stderr or "")[-12000:]}
    except subprocess.TimeoutExpired as exc:
        return {"label": label, "command": command, "returncode": 124, "duration_seconds": round(time.monotonic() - started, 3), "stdout": str(exc.stdout or "")[-12000:], "stderr": "timed out after 300 seconds"}

def main() -> int:
    REPORT.mkdir(parents=True, exist_ok=True)
    checks = [
        run("python-tests", [sys.executable, "-m", "pytest", "-q"]),
        run("release-lineage", [sys.executable, "scripts/verify_release_lineage.py"]),
        run("board-manifest", [sys.executable, "scripts/validate_board_manifest.py"]),
        run("frontend-typecheck", [NPM, "run", "typecheck"], ROOT / "apps/web"),
        run("frontend-build", [NPM, "run", "build"], ROOT / "apps/web"),
        run("frontend-vitest", [NPM, "test"], ROOT / "apps/web"),
        run("frontend-e2e-accessibility", [NPM, "run", "test:e2e"], ROOT / "apps/web"),
    ]
    payload = {"iteration": "02", "scope": "FGA 00-02 backlog", "timestamp_utc": datetime.now(UTC).isoformat(), "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "platform": platform.platform(), "checks": checks, "fully_qualified": all(check["returncode"] == 0 for check in checks)}
    (REPORT / "gate.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"fully_qualified": payload["fully_qualified"], "report": str(REPORT / "gate.json")}))
    return 0 if payload["fully_qualified"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
