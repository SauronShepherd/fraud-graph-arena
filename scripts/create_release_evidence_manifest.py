from __future__ import annotations
import argparse, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--live-status", choices=["qualified", "unavailable", "not_run"], default="not_run"); args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).split(b"\0")
    tree_parts = []
    for raw in tracked:
        if not raw: continue
        path = root / raw.decode()
        if path.is_file(): tree_parts.append({"path": raw.decode(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    tree_digest = hashlib.sha256(json.dumps(tree_parts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    dirty_paths = subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).splitlines()
    manifest = {
        "manifest_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha": source_sha,
        "source_tree_sha256": tree_digest,
        "working_tree": {"clean": not dirty_paths, "changed_paths": dirty_paths},
        "scope": "FGA unified static implementation gap audit",
        "local_evidence": {
            "python_tests": "python -m pytest -q tests/iteration_04 tests/iteration_05",
            "frontend_typecheck": "npm run typecheck",
            "frontend_tests": "npx vitest run --pool=forks --no-file-parallelism --maxWorkers=1 --testTimeout=5000",
            "canonical_packages": "13"
        },
        "live_databricks": {"status": args.live_status, "source_sha": source_sha},
        "closure_allowed": args.live_status == "qualified"
    }
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"); print(json.dumps(manifest, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
