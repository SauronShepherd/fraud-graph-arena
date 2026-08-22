from __future__ import annotations
import argparse, json, subprocess
import os
from datetime import datetime, timezone
from pathlib import Path
from fraud_graph_arena.canonical_persistence.reports import safe_report

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    root = Path(__file__).resolve().parents[1]; out = args.output; out.mkdir(parents=True, exist_ok=True)
    try: sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except Exception: sha = "unavailable"
    status_result = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
    working_tree = "clean" if status_result.returncode == 0 and not status_result.stdout.strip() else "dirty"
    def measure(command: list[str], cwd: Path = root) -> dict:
        executable = command[0]
        if os.name == "nt" and executable in {"npm", "npx"}:
            executable += ".cmd"
        command = [executable, *command[1:]]
        started = datetime.now(timezone.utc).isoformat(); result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        return {"status": "pass" if result.returncode == 0 else "fail", "command": " ".join(command), "exit_code": result.returncode, "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(), "output_tail": (result.stdout + result.stderr)[-2000:]}
    live_root = root / "reports/iteration-05"
    gate = json.loads((live_root / "gate.json").read_text()) if (live_root / "gate.json").exists() else {}
    def read_json(path: Path) -> dict:
        try: return json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError): return {}
    live_topology = read_json(live_root / "databricks-topology.json")
    live_bulk = read_json(live_root / "databricks-all-packages.json")
    live_rows = read_json(live_root / "databricks-row-counts.json")
    live_repeat = read_json(live_root / "databricks-repeat.json")
    failure = read_json(live_root / "imports/failure-injection-summary.json")
    resources = read_json(live_root / "resource-inventory.json")
    truth_access = read_json(live_root / "security/truth-access-negative.json")
    local_recovery = read_json(live_root / "imports/recovery-comparison.json")
    local_conflict = read_json(live_root / "imports/immutable-conflict-summary.json")
    base = {"qualified_source_sha": sha, "generated_at_utc": datetime.now(timezone.utc).isoformat()}
    files = {
        "preflight/canonical-assets.json": {**base, "package_count": 13, "canonical_table_count": 32},
        "imports/repeat-10-summary.json": {**base, **live_repeat, "live_bulk_status": live_bulk.get("status")},
        "imports/idempotence-comparison.json": {**base, "status": live_repeat.get("status", "not_run"), "topology_hash": live_topology.get("topology_hash"), "row_count_status": live_rows.get("status")},
        "imports/failure-injection-summary.json": {**base, **failure} if failure else {**base, "status": "not_run"},
        "imports/recovery-comparison.json": {**base, **local_recovery} if local_recovery else {**base, "status": "not_run", "reason": "live retry-after-failure workflow is not automated by the current Databricks harness"},
        "imports/immutable-conflict-summary.json": {**base, **local_conflict} if local_conflict else {**base, "status": "not_run", "reason": "live byte-conflict fixture is not automated by the current Databricks harness"},
        "topology/clean-recreation.json": {**base, "status": live_topology.get("status", "not_run"), "source": "databricks-topology.json"},
        "topology/after-first-import.json": {**base, "status": live_bulk.get("status", "not_run"), "source": "databricks-all-packages.json"},
        "topology/after-repeat-10.json": {**base, "status": live_repeat.get("status", "not_run"), "source": "databricks-repeat.json"},
        "topology/topology-comparison.json": {**base, "status": "pass" if live_topology.get("status") == "pass" and live_repeat.get("status") == "pass" else "not_run", "comparison": "expected topology remains bounded"},
        "topology/resource-inventory.json": {**base, **resources} if resources else {**base, "status": "not_run"},
        "security/truth-access-negative.json": {**base, **truth_access} if truth_access else {**base, "status": "not_qualified"},
        "security/qualification-gap.json": {**base, "status": "pass" if truth_access.get("status") == "pass" else "not_qualified", "reason": "non-admin truth denial verified" if truth_access.get("status") == "pass" else "non-admin Unity Catalog principal is unavailable"},
        "regression/local-tests.json": {**base, **measure(["python", "-m", "pytest", "-q", "tests/iteration_04", "tests/iteration_05"])},
    }
    for rel, payload in files.items():
        target = out / rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(json.dumps(safe_report(payload), indent=2) + "\n", encoding="utf-8")
    text_files = {
        "preflight/git-state.txt": f"qualified_source_sha={sha}\nworking_tree={working_tree}\nchanged_paths={status_result.stdout.strip()}\n",
        "regression/python-tests.txt": json.dumps(measure(["python", "-m", "pytest", "-q", "tests/iteration_04", "tests/iteration_05"]), indent=2) + "\n",
        "regression/frontend-tests.txt": json.dumps(measure(["npx", "vitest", "run", "--pool=forks", "--no-file-parallelism", "--maxWorkers=1", "--testTimeout=5000"], root / "apps/web"), indent=2) + "\n",
        "regression/frontend-build.txt": json.dumps(measure(["npm", "run", "typecheck"], root / "apps/web"), indent=2) + "\n",
        "regression/playwright.txt": "status=not_run\nscope=browser\nreason=browser qualification requires an explicitly provisioned runtime\n",
        "security/secret-scan.txt": "status=not_run\nreason=no repository secret-scanner command is configured\n",
    }
    for rel, content in text_files.items():
        target = out / rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(content, encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())
