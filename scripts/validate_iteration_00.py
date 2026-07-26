#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import platform
import re
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from governance_digest import canonical_sha256

try:
    import jsonschema
    import yaml
except ModuleNotFoundError as exc:
    dependency = exc.name or "unknown"
    project_file = Path(__file__).resolve().parents[1] / "pyproject.toml"
    print(
        "Iteration-00 validator dependency is missing: " + dependency + "\n"
        "From the repository root, install the declared project and test dependencies with:\n"
        f'  "{sys.executable}" -m pip install -e ".[test]"\n'
        f"Dependency configuration: {project_file}",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = DEFAULT_ROOT
RESULT_PATH = ROOT / "reports/iteration-00/validation-results.json"
EVIDENCE_PATH = ROOT / "reports/iteration-00/evidence.json"
APPROVALS_PATH = ROOT / "config/governance/approvals.yaml"
EXPECTED_TAG = "fga-iteration-00-r1"
PAIR_ID = "FGA-NORMATIVE-PAIR-10.0-20260726"
NORMATIVE_MEMBERS = {
    "FGA-NORMATIVE-FUNCTIONAL-10.0-20260726": {
        "title": "## Complete Functional Specification",
        "filename": "Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md",
    },
    "FGA-NORMATIVE-TECHNICAL-10.0-20260726": {
        "title": "## Complete Technical Architecture and Design Specification",
        "filename": "Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md",
    },
}


def configure_root(root: Path) -> None:
    global ROOT, RESULT_PATH, EVIDENCE_PATH, APPROVALS_PATH
    ROOT = root.resolve()
    RESULT_PATH = ROOT / "reports/iteration-00/validation-results.json"
    EVIDENCE_PATH = ROOT / "reports/iteration-00/evidence.json"
    APPROVALS_PATH = ROOT / "config/governance/approvals.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_evidence_digest(value: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(value))
    clone.pop("bundle_digest", None)
    payload = json.dumps(
        clone, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, text=True, capture_output=True, check=False
    )


def current_commit() -> str:
    completed = git("rev-parse", "HEAD")
    return completed.stdout.strip() if completed.returncode == 0 else "WORKTREE-NO-COMMIT"


def clean_checkout() -> bool:
    completed = git("status", "--porcelain", "--untracked-files=all")
    return completed.returncode == 0 and not completed.stdout.strip()


def commit_exists(commit: str) -> bool:
    if not commit or commit == "WORKTREE-NO-COMMIT":
        return False
    return git("cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return git("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def changed_paths(old: str, new: str) -> list[str]:
    completed = git("diff", "--name-only", f"{old}..{new}")
    if completed.returncode != 0:
        return ["<unable-to-calculate-diff>"]
    return [line for line in completed.stdout.splitlines() if line]


def tag_target(tag: str) -> str | None:
    completed = git("rev-list", "-n", "1", tag)
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def validate_instance(schema_path: Path, value: Any) -> None:
    schema = read_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(value)


def validate_schema_file(schema_path: Path, instance_path: Path) -> None:
    validate_instance(schema_path, read_json(instance_path))


def graph_semantic_errors(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    ids = [node["id"] for node in graph["nodes"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate traceability node IDs")
    node_ids = set(ids)
    degree = {identifier: 0 for identifier in ids}
    for edge in graph["edges"]:
        if edge["from"] not in node_ids:
            errors.append(f"missing edge source {edge['from']}")
        if edge["to"] not in node_ids:
            errors.append(f"missing edge target {edge['to']}")
        if edge["from"] in degree:
            degree[edge["from"]] += 1
        if edge["to"] in degree:
            degree[edge["to"]] += 1
    orphans = sorted(identifier for identifier, count in degree.items() if count == 0)
    if orphans:
        errors.append("orphan nodes: " + ", ".join(orphans))

    present_modules = {n["id"] for n in graph["nodes"] if n["kind"] == "module"}
    present_interactions = {
        n["id"] for n in graph["nodes"] if n["kind"] == "interaction"
    }
    if present_modules != {f"M{i:02d}" for i in range(1, 21)}:
        errors.append("module coverage differs from M01-M20")
    if present_interactions != {f"I{i:02d}" for i in range(1, 20)}:
        errors.append("interaction coverage differs from I01-I19")

    tasks = [n for n in graph["nodes"] if n["kind"] == "task"]
    for task in tasks:
        task_id = task["id"]
        path = task.get("path")
        if not path:
            errors.append(f"task {task_id} has no path")
        elif not (ROOT / path).is_file():
            errors.append(f"task {task_id} path does not exist: {path}")
        if not any(
            edge["from"] == task_id and edge["relationship"] == "verified_by"
            for edge in graph["edges"]
        ):
            errors.append(f"task {task_id} has no verifying test")
    return errors


def markdown_errors() -> list[str]:
    errors: list[str] = []
    authored_roots = [
        ROOT / "README.md",
        ROOT / "docs",
        ROOT / "reports/iteration-00/README.md",
        ROOT / "specifications/normative-pair-v10.0/README.md",
    ]
    files: list[Path] = []
    for item in authored_roots:
        if item.is_file():
            files.append(item)
        elif item.exists():
            files.extend(item.rglob("*.md"))
    for path in sorted(set(files)):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if not text.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{line_number}: trailing whitespace")
        if not text.startswith("# "):
            errors.append(f"{relative}: first line is not H1")
        if text.count("```") % 2:
            errors.append(f"{relative}: unbalanced code fence")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).split("#", 1)[0]
            if (
                not target
                or re.match(r"^[a-z]+://", target)
                or target.startswith("mailto:")
            ):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{relative}: broken link: {target}")
    return errors


def owner_errors() -> list[str]:
    data = read_yaml(ROOT / "config/governance/owners.yaml")
    teams = set(data["teams"])
    assignments = data["assignments"]
    errors: list[str] = []
    for assignment in assignments:
        if assignment["owner"] not in teams or assignment["reviewer"] not in teams:
            errors.append(f"unknown team in {assignment['path']}")
        if assignment["owner"] == assignment["reviewer"]:
            errors.append(f"owner equals reviewer in {assignment['path']}")

    governed: list[Path] = []
    for base in [
        "README.md",
        ".gitignore",
        ".gitattributes",
        "pyproject.toml",
        "docs",
        "config",
        "schemas",
        "reports",
        "scripts",
        "tests",
        "specifications",
    ]:
        path = ROOT / base
        if path.is_file():
            governed.append(path)
        elif path.exists():
            governed.extend(
                child
                for child in path.rglob("*")
                if child.is_file() and "__pycache__" not in child.parts
            )

    def matches(pattern: str, relative: str) -> bool:
        if pattern.endswith("/**"):
            return relative.startswith(pattern[:-3].rstrip("/") + "/")
        return fnmatch.fnmatch(relative, pattern)

    for path in governed:
        relative = path.relative_to(ROOT).as_posix()
        if not any(matches(a["path"], relative) for a in assignments):
            errors.append(f"unowned path: {relative}")
    return errors


def id_errors() -> list[str]:
    errors: list[str] = []
    baseline = read_json(ROOT / "config/governance/baseline.json")
    artifact_ids = [artifact["artifact_id"] for artifact in baseline["artifacts"]]
    if len(artifact_ids) != len(set(artifact_ids)):
        errors.append("duplicate artifact IDs")

    graph = read_json(ROOT / "config/governance/traceability.json")
    patterns = {
        "module": r"^M(?:0[1-9]|1[0-9]|20)$",
        "interaction": r"^I(?:0[1-9]|1[0-9])$",
        "requirement": r"^REQ-[A-Z0-9]+-[A-Z0-9-]+-[0-9]{3}$",
        "stage": r"^I[0-9]{2}-S[0-9]{2}$",
        "task": r"^I[0-9]{2}-S[0-9]{2}-T[0-9]{2}$",
        "test": r"^TEST-[A-Z0-9-]+$",
        "evidence": r"^EVID-I[0-9]{2}-[A-Z0-9-]+$",
    }
    for node in graph["nodes"]:
        pattern = patterns.get(node["kind"])
        if pattern and not re.match(pattern, node["id"]):
            errors.append(f"malformed {node['kind']} ID {node['id']}")

    policy = read_yaml(ROOT / "config/governance/iteration-policy.yaml")
    gate_ids = [gate["id"] for gate in policy["gates"]]
    if gate_ids != [f"G{i:02d}" for i in range(1, 16)]:
        errors.append("gate IDs are not exactly G01-G15 in order")
    if policy.get("principle") != "no-pass-no-progress":
        errors.append("no-pass-no-progress principle missing")
    for name, path in policy.get("references", {}).items():
        if not (ROOT / path).is_file():
            errors.append(f"missing iteration-policy reference {name}: {path}")
    quarantine = policy["skips_and_quarantine"]
    if not quarantine["critical_skip_forbidden"] or not quarantine[
        "critical_quarantine_forbidden"
    ]:
        errors.append("critical skip/quarantine prohibition missing")
    return errors


def scan_errors() -> tuple[list[str], list[str]]:
    secret_errors: list[str] = []
    truth_errors: list[str] = []
    excluded_prefixes = ("specifications/", ".git/")
    secret_patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(
            r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']"
        ),
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ]
    truth_names = {
        "truth.json",
        "answer-key.json",
        "answer_key.json",
        "protected-truth.json",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith(excluded_prefixes):
            continue
        if path.name.lower() in truth_names:
            truth_errors.append(
                f"protected truth artifact outside specifications: {relative}"
            )
        if path.suffix.lower() not in {
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".py",
            ".txt",
            ".toml",
        }:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            if pattern.search(text):
                secret_errors.append(f"possible secret in {relative}: {pattern.pattern}")
    return secret_errors, truth_errors


def validate_normative_member(artifact: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    expected = NORMATIVE_MEMBERS.get(artifact["artifact_id"])
    if expected is None:
        return [f"unexpected normative member {artifact['artifact_id']}"]
    if path.name != expected["filename"]:
        errors.append(
            f"normative filename mismatch for {artifact['artifact_id']}: {path.name}"
        )
    text = path.read_text(encoding="utf-8")
    required = [
        "# Fraud Graph Arena",
        expected["title"],
        "**Document version:** 10.0",
        f"**Normative pair ID:** `{PAIR_ID}`",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(
                f"normative identity fragment missing in {artifact['artifact_id']}: {fragment}"
            )
    if len(text.splitlines()) < 100:
        errors.append(
            f"normative source is implausibly short for {artifact['artifact_id']}"
        )
    return errors


def baseline_errors() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    blockers: list[str] = []
    baseline_path = ROOT / "config/governance/baseline.json"
    try:
        validate_schema_file(
            ROOT / "schemas/governance/baseline.schema.json", baseline_path
        )
    except Exception as exc:
        return [f"baseline schema validation: {exc}"], []

    baseline = read_json(baseline_path)
    artifact_ids = {artifact["artifact_id"] for artifact in baseline["artifacts"]}
    if set(NORMATIVE_MEMBERS) - artifact_ids:
        errors.append("both v10.0 normative member artifacts must be registered separately")

    for artifact in baseline["artifacts"]:
        if artifact["availability"] == "available":
            path = ROOT / artifact["path"]
            if not path.is_file():
                errors.append(
                    f"artifact path missing: {artifact['artifact_id']} -> {artifact['path']}"
                )
                continue
            if canonical_sha256(path) != artifact["sha256"]:
                errors.append(f"digest mismatch: {artifact['artifact_id']}")
            if artifact["artifact_id"] in NORMATIVE_MEMBERS:
                errors.extend(validate_normative_member(artifact, path))
        elif artifact.get("required_for_closure"):
            blockers.append(artifact["artifact_id"])

    blockers = sorted(blockers)
    closure = baseline["closure_requirements"]
    if sorted(closure["unresolved_required_artifact_ids"]) != blockers:
        errors.append("closure unresolved artifact list does not match registry")
    if closure["all_required_available"] != (not blockers):
        errors.append("all_required_available is inconsistent")
    expected_status = "active" if not blockers else "blocked"
    if baseline["status"] != expected_status:
        errors.append(
            f"baseline status must be {expected_status} for current availability"
        )
    if not any(
        item["authority"] == PAIR_ID and item["rank"] == 1
        for item in baseline["precedence"]
    ):
        errors.append("rank-one normative pair authority is missing")
    return errors, blockers


def approvals_errors() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    blockers: list[str] = []
    if not APPROVALS_PATH.is_file():
        return ["approval file is missing"], ["approvals"]
    approvals = read_yaml(APPROVALS_PATH)
    try:
        validate_instance(
            ROOT / "schemas/governance/approvals.schema.json", approvals
        )
    except Exception as exc:
        return [f"approval schema validation: {exc}"], ["approvals"]

    required = approvals["required_roles"]
    records = approvals["approvals"]
    roles = [record["role"] for record in records]
    if len(roles) != len(set(roles)):
        errors.append("duplicate approval roles")
    if set(roles) != set(required):
        errors.append("approval records do not exactly cover required roles")
    for record in records:
        if record["status"] != "approved":
            blockers.append(f"approval:{record['role']}:{record['status']}")
    return errors, sorted(blockers)


def schema_fixture_errors() -> list[str]:
    errors: list[str] = []
    json_schemas = {
        "baseline": ROOT / "schemas/governance/baseline.schema.json",
        "traceability": ROOT / "schemas/governance/traceability.schema.json",
        "evidence": ROOT / "schemas/testing/iteration-evidence.schema.json",
    }
    positives = {
        "baseline": ROOT / "tests/fixtures/governance/baseline.valid.json",
        "traceability": ROOT / "tests/fixtures/governance/traceability.valid.json",
        "evidence": ROOT / "tests/fixtures/governance/evidence.valid.json",
    }
    negatives = {
        "baseline": ROOT / "tests/fixtures/governance/baseline.invalid.json",
        "evidence": ROOT / "tests/fixtures/governance/evidence.invalid.json",
    }
    for name, schema_path in json_schemas.items():
        schema = read_json(schema_path)
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"{name} schema invalid: {exc}")
            continue
        try:
            validate_instance(schema_path, read_json(positives[name]))
        except Exception as exc:
            errors.append(f"{name} positive fixture failed: {exc}")
    for name, fixture_path in negatives.items():
        try:
            validate_instance(json_schemas[name], read_json(fixture_path))
            errors.append(f"{name} negative fixture unexpectedly passed")
        except jsonschema.ValidationError:
            pass

    orphan = read_json(ROOT / "tests/fixtures/governance/traceability.orphan.json")
    try:
        validate_instance(json_schemas["traceability"], orphan)
    except Exception as exc:
        errors.append(f"traceability orphan fixture should be structurally valid: {exc}")
    if not graph_semantic_errors(orphan):
        errors.append("traceability orphan fixture unexpectedly passed semantics")

    approval_schema = ROOT / "schemas/governance/approvals.schema.json"
    try:
        jsonschema.Draft202012Validator.check_schema(read_json(approval_schema))
        validate_instance(
            approval_schema,
            read_yaml(ROOT / "tests/fixtures/governance/approvals.valid.yaml"),
        )
    except Exception as exc:
        errors.append(f"approvals positive fixture failed: {exc}")
    try:
        validate_instance(
            approval_schema,
            read_yaml(ROOT / "tests/fixtures/governance/approvals.invalid.yaml"),
        )
        errors.append("approvals negative fixture unexpectedly passed")
    except jsonschema.ValidationError:
        pass
    return errors


def dependency_manifest_errors() -> list[str]:
    errors: list[str] = []
    path = ROOT / "pyproject.toml"
    if not path.is_file():
        return ["pyproject.toml is missing"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"pyproject.toml is invalid: {exc}"]

    project = data.get("project", {})

    def normalized_exact(entries: list[str], group: str) -> dict[str, str]:
        declared: dict[str, str] = {}
        for entry in entries:
            if not isinstance(entry, str):
                errors.append(f"{group} dependency entry is not a string: {entry!r}")
                continue
            name, separator, version = entry.partition("==")
            normalized = re.sub(r"[-_.]+", "-", name.strip()).lower()
            if (
                not separator
                or not normalized
                or not version.strip()
                or any(operator in version for operator in "<>!=~")
            ):
                errors.append(f"{group} dependency must be exactly pinned: {entry}")
                continue
            declared[normalized] = entry
        return declared

    runtime = normalized_exact(project.get("dependencies", []), "runtime")
    tests = normalized_exact(
        project.get("optional-dependencies", {}).get("test", []), "test"
    )
    for dependency in sorted({"jsonschema", "pyyaml"} - set(runtime)):
        errors.append(f"undeclared runtime dependency: {dependency}")
    if "pytest" not in tests:
        errors.append("undeclared test dependency: pytest")

    pytest_config = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    if pytest_config.get("testpaths") != ["tests"]:
        errors.append('pytest testpaths must be exactly ["tests"]')
    if pytest_config.get("python_files") != ["test_*.py"]:
        errors.append('pytest python_files must be exactly ["test_*.py"]')
    addopts = pytest_config.get("addopts", [])
    if "--strict-config" not in addopts or "--strict-markers" not in addopts:
        errors.append("pytest strict configuration and marker validation must be enabled")
    return errors


def baseline_artifact_projection() -> list[dict[str, Any]]:
    baseline = read_json(ROOT / "config/governance/baseline.json")
    projection: list[dict[str, Any]] = []
    for artifact in baseline["artifacts"]:
        if not artifact.get("required_for_closure"):
            continue
        item: dict[str, Any] = {
            "artifact_id": artifact["artifact_id"],
            "status": "verified"
            if artifact["availability"] == "available"
            else "missing",
        }
        if artifact["availability"] == "available":
            item["path"] = artifact["path"]
            item["sha256"] = artifact["sha256"]
        projection.append(item)
    return projection


def evidence_errors() -> list[str]:
    errors: list[str] = []
    if not EVIDENCE_PATH.is_file():
        return ["evidence file is missing"]
    try:
        validate_schema_file(
            ROOT / "schemas/testing/iteration-evidence.schema.json", EVIDENCE_PATH
        )
    except Exception as exc:
        errors.append(f"evidence schema validation: {exc}")
        return errors

    evidence = read_json(EVIDENCE_PATH)
    if evidence.get("bundle_digest") != canonical_evidence_digest(evidence):
        errors.append("evidence bundle digest mismatch")
    gate_ids = [gate["gate_id"] for gate in evidence.get("gates", [])]
    if gate_ids != [f"G{i:02d}" for i in range(1, 16)]:
        errors.append("evidence gates are not exactly G01-G15")
    if evidence.get("closure_eligible") != (evidence.get("status") == "passing"):
        errors.append("closure_eligible is inconsistent with evidence status")
    if any(test["status"] == "fail" for test in evidence.get("tests", [])) and evidence.get(
        "status"
    ) == "passing":
        errors.append("passing evidence contains failed test")
    if any(exception.get("critical") for exception in evidence.get("exceptions", [])):
        errors.append("critical exception is forbidden")

    required_pass_gates = {"G01", "G02", "G04", "G11", "G14", "G15"}
    gates = {gate["gate_id"]: gate for gate in evidence["gates"]}
    if evidence["status"] == "passing":
        for gate_id in required_pass_gates:
            if gates[gate_id]["status"] != "pass":
                errors.append(f"passing I00 evidence requires {gate_id} to pass")
        if any(gate["status"] in {"fail", "blocked"} for gate in evidence["gates"]):
            errors.append("passing evidence contains failed or blocked gate")
        if any(test["status"] in {"fail", "blocked"} for test in evidence["tests"]):
            errors.append("passing evidence contains failed or blocked test")
        if any(gap.get("blocks_closure") for gap in evidence["known_gaps"]):
            errors.append("passing evidence contains a closure-blocking gap")
        if evidence["exceptions"]:
            errors.append("passing I00 evidence may not contain temporary exceptions")
        if not evidence["environment"].get("clean_checkout"):
            errors.append("passing evidence was not generated from a clean checkout")

    expected_artifacts = baseline_artifact_projection()
    if evidence["source_artifacts"] != expected_artifacts:
        errors.append("evidence source-artifact projection is stale or incomplete")

    approval_config = read_yaml(APPROVALS_PATH)
    if evidence["approvals"] != approval_config["approvals"]:
        errors.append("evidence approvals do not match governed approval records")

    source_commit = evidence["source_commit"]
    if not commit_exists(source_commit):
        errors.append(f"evidence source commit does not exist: {source_commit}")
    return errors


def run_check(identifier: str, function: Callable[[], list[str]]) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        errors = function()
        status = "pass" if not errors else "fail"
    except Exception as exc:  # pragma: no cover - defensive boundary
        errors = [f"{type(exc).__name__}: {exc}"]
        status = "fail"
    return {
        "id": identifier,
        "status": status,
        "duration_ms": round((time.perf_counter() - started) * 1000),
        "errors": errors,
    }


def test_statuses(checks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {check["id"]: check for check in checks}


def closure_blockers(
    checks: list[dict[str, Any]],
    baseline_blockers: list[str],
    approval_blockers: list[str],
    evidence: dict[str, Any] | None = None,
) -> list[str]:
    blockers: list[str] = []
    blockers.extend(f"failed-check:{c['id']}" for c in checks if c["status"] == "fail")
    blockers.extend(f"missing-artifact:{item}" for item in baseline_blockers)
    blockers.extend(approval_blockers)
    if not clean_checkout():
        blockers.append("working-tree-not-clean")

    if evidence is None:
        if EVIDENCE_PATH.is_file():
            evidence = read_json(EVIDENCE_PATH)
        else:
            blockers.append("evidence-file-missing")
            return sorted(set(blockers))

    if evidence.get("status") != "passing" or not evidence.get("closure_eligible"):
        blockers.append("evidence-not-passing")
    if not evidence.get("environment", {}).get("clean_checkout"):
        blockers.append("evidence-not-generated-from-clean-checkout")
    if any(gap.get("blocks_closure") for gap in evidence.get("known_gaps", [])):
        blockers.append("evidence-has-blocking-gaps")
    if evidence.get("exceptions"):
        blockers.append("release-exceptions-present")
    if any(record.get("status") != "approved" for record in evidence.get("approvals", [])):
        blockers.append("required-approvals-incomplete")

    source_commit = evidence.get("source_commit", "")
    head = current_commit()
    if not commit_exists(source_commit):
        blockers.append("qualified-source-commit-missing")
    elif not is_ancestor(source_commit, head):
        blockers.append("qualified-source-is-not-an-ancestor-of-closure")
    elif source_commit != head:
        allowed_prefix = "reports/iteration-00/"
        disallowed = [
            path for path in changed_paths(source_commit, head) if not path.startswith(allowed_prefix)
        ]
        if disallowed:
            blockers.append(
                "non-evidence-files-changed-after-qualification:" + ",".join(disallowed)
            )

    tagged = tag_target(EXPECTED_TAG)
    if tagged is not None and tagged != head:
        blockers.append(f"immutable-tag-points-to-wrong-commit:{tagged}")
    return sorted(set(blockers))


def update_evidence(
    report: dict[str, Any],
    baseline_blockers: list[str],
    approval_blockers: list[str],
) -> None:
    evidence = read_json(EVIDENCE_PATH)
    checks = test_statuses(report["checks"])
    structural_failures = [c["id"] for c in report["checks"] if c["status"] == "fail"]
    generation_blockers = [
        *[f"missing-artifact:{item}" for item in baseline_blockers],
        *approval_blockers,
    ]
    if not report["clean_checkout_observed"]:
        generation_blockers.append("candidate-checkout-not-clean")
    if structural_failures:
        generation_blockers.extend(f"failed-check:{item}" for item in structural_failures)

    evidence["generated_at"] = utc_now()
    evidence["source_commit"] = report["source_commit"]
    evidence["environment"] = {
        "os": platform.platform(),
        "python": platform.python_version(),
        "clean_checkout": bool(report["clean_checkout_observed"]),
    }
    evidence["source_artifacts"] = baseline_artifact_projection()
    evidence["approvals"] = read_yaml(APPROVALS_PATH)["approvals"]

    check_for_test = {
        "TEST-I00-DEPENDENCIES": "dependencies",
        "TEST-I00-SCHEMAS": "schemas",
        "TEST-I00-DIGESTS": "baseline",
        "TEST-I00-MARKDOWN": "markdown",
        "TEST-I00-IDS": "ids",
        "TEST-I00-OWNERS": "owners",
        "TEST-I00-TRACEABILITY": "traceability",
        "TEST-I00-SECRET-SCAN": "secret_scan",
        "TEST-I00-TRUTH-SCAN": "truth_scan",
        "TEST-I00-APPROVALS": "approvals",
    }
    for test in evidence["tests"]:
        check_id = check_for_test.get(test["test_id"])
        if check_id:
            check = checks[check_id]
            test["duration_ms"] = check["duration_ms"]
            test["status"] = "pass" if check["status"] == "pass" else "fail"
            test["result"] = (
                "Validation passed."
                if check["status"] == "pass"
                else "; ".join(check["errors"])
            )
        elif test["test_id"] == "TEST-I00-CLOSURE":
            test["status"] = "blocked" if generation_blockers else "pass"
            test["result"] = (
                "Closure blocked: " + ", ".join(generation_blockers)
                if generation_blockers
                else "All formal Iteration-00 closure conditions are satisfied."
            )

    evidence["known_gaps"] = []
    for artifact in baseline_blockers:
        evidence["known_gaps"].append(
            {
                "id": "RISK-MISSING-" + re.sub(r"[^A-Z0-9]+", "-", artifact.upper()),
                "severity": "high",
                "description": f"Required normative source artifact is unavailable: {artifact}.",
                "owner": "architecture-governance",
                "blocks_closure": True,
                "remediation": "Import the exact approved source with scripts/import_normative_pair.py and commit the updated baseline.",
            }
        )
    if approval_blockers:
        evidence["known_gaps"].append(
            {
                "id": "RISK-I00-APPROVALS-INCOMPLETE",
                "severity": "high",
                "description": "One or more required independent approval records are not approved.",
                "owner": "release-management",
                "blocks_closure": True,
                "remediation": "Record named, dated, evidence-backed approvals in config/governance/approvals.yaml.",
            }
        )
    if not report["clean_checkout_observed"]:
        evidence["known_gaps"].append(
            {
                "id": "RISK-I00-DIRTY-CANDIDATE",
                "severity": "high",
                "description": "Qualification was not generated from a clean candidate checkout.",
                "owner": "quality-engineering",
                "blocks_closure": True,
                "remediation": "Commit all candidate changes and regenerate evidence from a clean checkout.",
            }
        )

    evidence["status"] = "passing" if not generation_blockers else (
        "failing" if structural_failures else "blocked"
    )
    evidence["closure_eligible"] = evidence["status"] == "passing"

    gates = {gate["gate_id"]: gate for gate in evidence["gates"]}
    for gate_id in ["G01", "G02", "G04", "G11", "G14", "G15"]:
        gates[gate_id]["status"] = "pass"
    gates["G01"]["rationale"] = "Normative baseline, IDs, ownership, traceability, schemas, and registered digests pass."
    gates["G02"]["rationale"] = "Governance files, dependency declarations, schemas, Markdown, JSON, YAML, TOML, and validation tooling pass."
    gates["G04"]["rationale"] = "I00 governance schemas have positive and incompatible negative fixtures; product contract compatibility is not yet applicable."
    gates["G11"]["rationale"] = "Secret and protected-truth scans pass for all implemented public governance artifacts."
    gates["G14"]["rationale"] = "Available source artifacts are content-addressed and dependency declarations are exactly pinned for I00."
    gates["G15"]["rationale"] = "Evidence schema, source commit, clean candidate state, approvals, and closure conditions pass."

    if structural_failures:
        for gate_id in ["G01", "G02", "G04", "G11", "G14", "G15"]:
            gates[gate_id]["status"] = "fail"
            gates[gate_id]["rationale"] = "One or more implemented I00 validation checks failed."
    elif baseline_blockers:
        gates["G01"]["status"] = "blocked"
        gates["G01"]["rationale"] = "The registered governance structure passes, but required normative source artifacts are missing."
        gates["G15"]["status"] = "blocked"
        gates["G15"]["rationale"] = "Formal closure is blocked by missing required source artifacts."
    elif approval_blockers or not report["clean_checkout_observed"]:
        gates["G15"]["status"] = "blocked"
        gates["G15"]["rationale"] = "Formal closure is blocked by incomplete approvals or a non-clean candidate checkout."

    evidence["bundle_digest"] = canonical_evidence_digest(evidence)
    write_json(EVIDENCE_PATH, evidence)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--require-closure", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--update-evidence", action="store_true")
    parser.add_argument("--generate-evidence", action="store_true")
    parser.add_argument("--candidate-commit")
    # Backward-compatible side-effect suppression flags. Validation is now side-effect-free by default.
    parser.add_argument("--no-update-evidence", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args()
    configure_root(args.root)

    write_report = (args.write_report or args.generate_evidence) and not args.no_write_report
    update_bundle = (args.update_evidence or args.generate_evidence) and not args.no_update_evidence
    if args.require_closure and (write_report or update_bundle):
        parser.error("--require-closure is side-effect-free; generate and commit evidence first")

    candidate_commit = args.candidate_commit or current_commit()
    if not commit_exists(candidate_commit):
        print(f"Candidate commit does not exist: {candidate_commit}", file=sys.stderr)
        return 1
    if candidate_commit != current_commit():
        print("Candidate commit must equal the checked-out HEAD during validation.", file=sys.stderr)
        return 1
    clean_before = clean_checkout()

    checks: list[dict[str, Any]] = []
    checks.append(run_check("dependencies", dependency_manifest_errors))
    checks.append(run_check("schemas", schema_fixture_errors))

    baseline_blockers: list[str] = []

    def baseline_check() -> list[str]:
        nonlocal baseline_blockers
        errors, baseline_blockers = baseline_errors()
        return errors

    checks.append(run_check("baseline", baseline_check))
    checks.append(run_check("markdown", markdown_errors))
    checks.append(run_check("ids", id_errors))
    checks.append(run_check("owners", owner_errors))
    checks.append(
        run_check(
            "traceability",
            lambda: graph_semantic_errors(
                read_json(ROOT / "config/governance/traceability.json")
            ),
        )
    )
    scan_cache: dict[str, list[str]] = {"secret": [], "truth": []}

    def secret_check() -> list[str]:
        secret, truth = scan_errors()
        scan_cache["secret"] = secret
        scan_cache["truth"] = truth
        return secret

    checks.append(run_check("secret_scan", secret_check))
    checks.append(run_check("truth_scan", lambda: scan_cache["truth"] or scan_errors()[1]))

    approval_blockers: list[str] = []

    def approval_check() -> list[str]:
        nonlocal approval_blockers
        errors, approval_blockers = approvals_errors()
        return errors

    checks.append(run_check("approvals", approval_check))

    report: dict[str, Any] = {
        "report_id": "FGA-I00-VALIDATION-RESULTS-1.1-20260726",
        "generated_at": utc_now(),
        "repository": str(ROOT),
        "source_commit": candidate_commit,
        "clean_checkout_observed": clean_before,
        "checks": checks,
        "blocking_prerequisites": sorted(
            [
                *[f"missing-artifact:{item}" for item in baseline_blockers],
                *approval_blockers,
                *([] if clean_before else ["candidate-checkout-not-clean"]),
            ]
        ),
    }
    report["status"] = (
        "fail"
        if any(check["status"] == "fail" for check in checks)
        else ("blocked" if report["blocking_prerequisites"] else "pass")
    )

    if write_report:
        write_json(RESULT_PATH, report)
    if update_bundle:
        update_evidence(report, baseline_blockers, approval_blockers)

    # Validate the final evidence state. During generation this occurs after writing it.
    evidence_check = run_check("evidence", evidence_errors)
    checks.append(evidence_check)
    report["checks"] = checks
    if evidence_check["status"] == "fail":
        report["status"] = "fail"
    if write_report:
        write_json(RESULT_PATH, report)

    closure = closure_blockers(
        checks,
        baseline_blockers,
        approval_blockers,
        read_json(EVIDENCE_PATH) if EVIDENCE_PATH.is_file() else None,
    )
    output = {
        "status": report["status"],
        "checks": {check["id"]: check["status"] for check in checks},
        "blocking_prerequisites": report["blocking_prerequisites"],
        "closure_blockers": closure,
        "report": str(RESULT_PATH.relative_to(ROOT)),
    }
    print(json.dumps(output, indent=2))

    if report["status"] == "fail":
        return 1
    if args.require_closure and closure:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
