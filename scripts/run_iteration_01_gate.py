from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class Check:
    name: str
    command: list[str]
    status: str
    returncode: int | None


def run(name: str, command: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> Check:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=cwd, check=False, env=env)
    return Check(
        name=name,
        command=command,
        status="passed" if result.returncode == 0 else "failed",
        returncode=result.returncode,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Iteration 01 no-pass-no-progress gate")
    parser.add_argument("--allow-missing-frontend-toolchain", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    python_env = os.environ.copy()
    source_path = str(root / "src")
    python_env["PYTHONPATH"] = source_path + os.pathsep + python_env.get("PYTHONPATH", "")
    checks = [
        run(
            "Python tests",
            [sys.executable, "-m", "pytest", "-v"],
            root,
            env=python_env,
        )
    ]

    web = root / "apps" / "web"
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm") or shutil.which("npm")
    has_modules = (web / "node_modules").is_dir()
    if npm and has_modules:
        checks.append(run("Frontend typecheck", [npm, "run", "typecheck"], web))
        checks.append(run("Frontend component tests", [npm, "run", "test"], web))
        checks.append(run("Playwright Academy journey", [npm, "run", "test:e2e"], web))
    else:
        status = "incomplete"
        checks.extend(
            [
                Check("Frontend typecheck", ["npm", "run", "typecheck"], status, None),
                Check("Frontend component tests", ["npm", "run", "test"], status, None),
                Check("Playwright Academy journey", ["npm", "run", "test:e2e"], status, None),
            ]
        )
        print("\nFrontend dependencies are not installed; npm checks were not executed.")

    report = {
        "iteration": "I01",
        "scope": "Detective Academy walking skeleton",
        "checks": [asdict(item) for item in checks],
        "status": "passed" if all(item.status == "passed" for item in checks) else ("incomplete" if any(item.status == "incomplete" for item in checks) else "failed"),
        "executed_checks_passed": all(item.status == "passed" for item in checks if item.status != "incomplete"),
        "mandatory_checks_complete": all(item.status != "incomplete" for item in checks),
        "iteration_gate_passed": all(item.status == "passed" for item in checks),
        "passed": all(item.status == "passed" for item in checks),
        "fully_qualified": all(item.status == "passed" for item in checks),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["iteration_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
