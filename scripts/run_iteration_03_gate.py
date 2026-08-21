from __future__ import annotations
import json, os, platform, subprocess, sys, time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).parents[1]
WEB = ROOT / "apps/web"
NPM = "npm.cmd" if os.name == "nt" else "npm"

def run(label: str, command: list[str], cwd: Path = ROOT, timeout: int = 300) -> dict[str, object]:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout)
        return {"label": label, "command": command, "returncode": result.returncode, "duration_seconds": round(time.monotonic() - started, 3), "stdout": (result.stdout or "")[-12000:], "stderr": (result.stderr or "")[-12000:]}
    except subprocess.TimeoutExpired:
        return {"label": label, "command": command, "returncode": 124, "duration_seconds": round(time.monotonic() - started, 3), "stdout": "", "stderr": f"timed out after {timeout} seconds"}

def output(command: list[str], cwd: Path = ROOT) -> str:
    return subprocess.check_output(command, cwd=cwd, text=True, encoding="utf-8", errors="replace").strip()

def main() -> int:
    report_path = Path(sys.argv[sys.argv.index("--report") + 1]) if "--report" in sys.argv else ROOT / "reports/iteration-03/gate.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    status = output(["git", "status", "--porcelain"])
    checks = [
        run("python-tests", [sys.executable, "-m", "pytest", "-q"]),
        run("screen-definition-validator", [sys.executable, "scripts/validate_screen_definitions.py"]),
        run("i03-python-tests", [sys.executable, "-m", "pytest", "-q", "tests/iteration_03"]),
        run("board-manifest", [sys.executable, "scripts/validate_board_manifest.py"]),
        run("approved-artwork", [sys.executable, "scripts/validate_board_manifest.py", "--require-approved-artwork"]),
        run("frontend-typecheck", [NPM, "run", "typecheck"], WEB),
        run("frontend-build", [NPM, "run", "build"], WEB),
        run("frontend-vitest", [NPM, "test"], WEB, 600),
        run("frontend-e2e", [NPM, "run", "test:e2e"], WEB, 900),
    ]
    payload = {"iteration": "03", "scope": "FGA03 declarative screen system", "timestamp_utc": datetime.now(UTC).isoformat(), "commit": output(["git", "rev-parse", "HEAD"]), "clean_before_gate": not bool(status), "status_before_gate": status.splitlines(), "platform": platform.platform(), "python_version": sys.version, "node_version": output(["node", "--version"], WEB), "npm_version": output([NPM, "--version"], WEB), "checks": checks, "fully_qualified": not status and all(check["returncode"] == 0 for check in checks)}
    report_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"fully_qualified": payload["fully_qualified"], "report": str(report_path)}))
    return 0 if payload["fully_qualified"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
