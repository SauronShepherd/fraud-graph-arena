from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_iteration_00.py"
IMPORTER = ROOT / "scripts" / "import_normative_pair.py"
TAGGER = ROOT / "scripts" / "create_iteration_00_tag.py"


def run(*arguments: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments), cwd=cwd, text=True, capture_output=True, check=False
    )


def run_validator(*arguments: str, root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return run(sys.executable, str(root / "scripts/validate_iteration_00.py"), *arguments, cwd=root)


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
    completed = run(sys.executable, "-S", str(VALIDATOR))

    assert completed.returncode == 3, completed.stdout + completed.stderr
    assert "pip install -e" in completed.stderr
    assert ".[test]" in completed.stderr
    assert "pyproject.toml" in completed.stderr


def test_validation_is_side_effect_free_by_default_and_structurally_green() -> None:
    before = run("git", "status", "--porcelain", "--untracked-files=all").stdout
    completed = run_validator()
    after = run("git", "status", "--porcelain", "--untracked-files=all").stdout

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert before == after
    payload = json.loads(completed.stdout)
    assert payload["status"] == "pass"
    assert payload["checks"]["evidence"] == "pass"


def test_formal_closure_blocks_missing_sources_and_pending_approvals_in_fixture(tmp_path: Path) -> None:
    repository = tmp_path / "blocked"
    copy_repository(repository)
    assert run("git", "init", "-b", "Iteration-00", cwd=repository).returncode == 0
    run("git", "config", "user.name", "Test Reviewer", cwd=repository)
    run("git", "config", "user.email", "reviewer@example.invalid", cwd=repository)

    baseline_path = repository / "config/governance/baseline.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    missing_ids = []
    for artifact in baseline["artifacts"]:
        if artifact["artifact_id"] in {
            "FGA-NORMATIVE-FUNCTIONAL-10.0-20260726",
            "FGA-NORMATIVE-TECHNICAL-10.0-20260726",
        }:
            artifact["availability"] = "external_missing"
            artifact["external_reference"] = "Fixture intentionally missing."
            artifact.pop("path", None)
            artifact.pop("sha256", None)
            missing_ids.append(artifact["artifact_id"])
    baseline["status"] = "blocked"
    baseline["closure_requirements"] = {
        "all_required_available": False,
        "all_available_digests_verified": True,
        "unresolved_required_artifact_ids": sorted(missing_ids),
    }
    baseline_path.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")

    approvals_path = repository / "config/governance/approvals.yaml"
    approvals = yaml.safe_load(approvals_path.read_text(encoding="utf-8"))
    approvals["approvals"] = [
        {"role": role, "status": "pending"}
        for role in approvals["required_roles"]
    ]
    approvals_path.write_text(yaml.safe_dump(approvals, sort_keys=False), encoding="utf-8")

    normative = repository / "specifications/normative-pair-v10.0"
    for path in normative.glob("*Specification_v10.0.md"):
        path.unlink()

    assert run("git", "add", ".", cwd=repository).returncode == 0
    assert run("git", "commit", "-m", "Create blocked fixture", cwd=repository).returncode == 0
    completed = run_validator("--require-closure", root=repository)

    assert completed.returncode == 2, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    blockers = payload["closure_blockers"]
    assert any("FGA-NORMATIVE-FUNCTIONAL-10.0" in item for item in blockers)
    assert any("FGA-NORMATIVE-TECHNICAL-10.0" in item for item in blockers)
    assert any(item.startswith("approval:") for item in blockers)


def test_importer_rejects_placeholder_documents(tmp_path: Path) -> None:
    functional = tmp_path / "functional.md"
    technical = tmp_path / "technical.md"
    functional.write_text("# Placeholder\n", encoding="utf-8")
    technical.write_text("# Placeholder\n", encoding="utf-8")

    completed = run(sys.executable, str(IMPORTER), str(functional), str(technical))

    assert completed.returncode != 0
    assert "identity validation failed" in completed.stderr


def test_tag_creation_refuses_unqualified_iteration(tmp_path: Path) -> None:
    repository = tmp_path / "unqualified-tag"
    copy_repository(repository)
    assert run("git", "init", "-b", "Iteration-00", cwd=repository).returncode == 0
    run("git", "config", "user.name", "Test Reviewer", cwd=repository)
    run("git", "config", "user.email", "reviewer@example.invalid", cwd=repository)
    assert run("git", "add", ".", cwd=repository).returncode == 0
    assert run("git", "commit", "-m", "Create unqualified fixture", cwd=repository).returncode == 0

    evidence_path = repository / "reports/iteration-00/evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["status"] = "blocked"
    evidence["closure_eligible"] = False
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    run("git", "add", "reports/iteration-00/evidence.json", cwd=repository)
    run("git", "commit", "-m", "Record unqualified evidence", cwd=repository)

    completed = run(
        sys.executable,
        str(repository / "scripts/create_iteration_00_tag.py"),
        "--tag",
        "fga-test-unqualified",
        cwd=repository,
    )

    assert completed.returncode != 0, completed.stdout + completed.stderr
    assert run("git", "rev-parse", "-q", "--verify", "refs/tags/fga-test-unqualified", cwd=repository).returncode != 0


def copy_repository(destination: Path) -> None:
    ignored = shutil.ignore_patterns(
        ".git", ".pytest_cache", "__pycache__", "*.pyc", "*.egg-info", ".venv"
    )
    shutil.copytree(ROOT, destination, ignore=ignored)


def create_normative_document(title: str) -> str:
    header = (
        "# Fraud Graph Arena\n\n"
        f"{title}\n\n"
        "**Document version:** 10.0  \n"
        "**Normative pair ID:** `FGA-NORMATIVE-PAIR-10.0-20260726`  \n\n"
    )
    return header + "\n".join(f"## Qualification section {index}\n\nApproved content {index}." for index in range(1, 80)) + "\n"


def make_qualified_closure(repository: Path) -> tuple[str, str]:
    copy_repository(repository)
    assert run("git", "init", "-b", "Iteration-00", cwd=repository).returncode == 0
    run("git", "config", "user.name", "Test Reviewer", cwd=repository)
    run("git", "config", "user.email", "reviewer@example.invalid", cwd=repository)

    sources = repository / "test-inputs"
    sources.mkdir()
    functional = sources / "Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md"
    technical = sources / "Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md"
    functional.write_text(create_normative_document("## Complete Functional Specification"), encoding="utf-8")
    technical.write_text(create_normative_document("## Complete Technical Architecture and Design Specification"), encoding="utf-8")

    imported = run(
        sys.executable,
        str(repository / "scripts/import_normative_pair.py"),
        str(functional),
        str(technical),
        cwd=repository,
    )
    assert imported.returncode == 0, imported.stdout + imported.stderr
    shutil.rmtree(sources)

    approval_path = repository / "config/governance/approvals.yaml"
    approvals = yaml.safe_load(approval_path.read_text(encoding="utf-8"))
    for record in approvals["approvals"]:
        record.update(
            {
                "status": "approved",
                "name": f"{record['role']} reviewer",
                "date": "2026-07-26",
                "evidence": f"Independent review completed for {record['role']}.",
            }
        )
    approval_path.write_text(yaml.safe_dump(approvals, sort_keys=False), encoding="utf-8")

    assert run("git", "add", ".", cwd=repository).returncode == 0
    assert run("git", "commit", "-m", "Create qualified Iteration-00 candidate", cwd=repository).returncode == 0
    candidate = run("git", "rev-parse", "HEAD", cwd=repository).stdout.strip()

    generated = run_validator("--generate-evidence", root=repository)
    assert generated.returncode == 0, generated.stdout + generated.stderr
    assert run("git", "add", "reports/iteration-00", cwd=repository).returncode == 0
    assert run("git", "commit", "-m", "Record Iteration-00 qualification evidence", cwd=repository).returncode == 0
    closure = run("git", "rev-parse", "HEAD", cwd=repository).stdout.strip()
    return candidate, closure


def test_qualified_candidate_and_evidence_only_closure_pass(tmp_path: Path) -> None:
    repository = tmp_path / "qualified"
    candidate, closure = make_qualified_closure(repository)

    completed = run_validator("--require-closure", root=repository)

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["closure_blockers"] == []
    evidence = json.loads((repository / "reports/iteration-00/evidence.json").read_text())
    assert evidence["status"] == "passing"
    assert evidence["closure_eligible"] is True
    assert evidence["source_commit"] == candidate
    assert candidate != closure


def test_closure_detects_post_qualification_source_change(tmp_path: Path) -> None:
    repository = tmp_path / "tampered"
    make_qualified_closure(repository)
    with (repository / "README.md").open("a", encoding="utf-8") as handle:
        handle.write("\nUnqualified change.\n")
    run("git", "add", "README.md", cwd=repository)
    run("git", "commit", "-m", "Unqualified source change", cwd=repository)

    completed = run_validator("--require-closure", root=repository)

    assert completed.returncode == 2, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert any(
        item.startswith("non-evidence-files-changed-after-qualification:")
        for item in payload["closure_blockers"]
    )
