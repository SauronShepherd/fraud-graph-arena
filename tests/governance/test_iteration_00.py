import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_iteration_00.py"


def run_validator(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_pyproject_declares_pinned_runtime_and_test_dependencies() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert "jsonschema==4.26.0" in data["project"]["dependencies"]
    assert "PyYAML==6.0.3" in data["project"]["dependencies"]
    assert "pytest==9.0.2" in data["project"]["optional-dependencies"]["test"]


def test_pytest_discovery_is_configured_in_pyproject() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    configuration = data["tool"]["pytest"]["ini_options"]

    assert configuration["testpaths"] == ["tests"]
    assert configuration["python_files"] == ["test_*.py"]
    assert "--strict-config" in configuration["addopts"]
    assert "--strict-markers" in configuration["addopts"]


def test_missing_dependency_error_is_actionable() -> None:
    completed = subprocess.run(
        [sys.executable, "-S", str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 3, completed.stdout + completed.stderr
    assert "pip install -e" in completed.stderr
    assert ".[test]" in completed.stderr
    assert "pyproject.toml" in completed.stderr


def test_validation_suite_is_structurally_green() -> None:
    completed = run_validator("--no-update-evidence", "--no-write-report")

    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_formal_closure_is_blocked_without_parent_pair() -> None:
    completed = run_validator(
        "--require-closure",
        "--no-update-evidence",
        "--no-write-report",
    )

    assert completed.returncode == 2, completed.stdout + completed.stderr
