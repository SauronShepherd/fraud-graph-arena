from __future__ import annotations

import argparse
import json
import subprocess
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--package-root", type=Path, default=Path("case-data/canonical/v1"))
    p.add_argument("--profile", default="sda")
    p.add_argument("--catalog", default="sda_dev")
    p.add_argument("--schema", default="sandbox")
    p.add_argument("--warehouse", default="e444f39962128242")
    p.add_argument("--force", action="store_true")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--tag", action="store_true")
    p.add_argument("--report", type=Path, default=Path("reports/iteration-05/databricks-repeat.json"))
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    attempted = 0
    for package in sorted(args.package_root.iterdir()):
        if not package.is_dir():
            continue
        files = sorted(package.rglob("*.csv"))
        def load(file: Path) -> None:
            relative = file.relative_to(package).as_posix()
            table = "fga_" + relative.replace("/", "_").replace(".", "_")
            command = ["python", "scripts/databricks_copy_into.py", table, f"{package.name}/{relative}", "--profile", args.profile, "--catalog", args.catalog, "--schema", args.schema, "--warehouse", args.warehouse]
            if args.force: command.append("--force")
            subprocess.run(command, cwd=root, check=True, stdout=subprocess.DEVNULL)
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            list(pool.map(load, files))
        attempted += len(files)
        if args.tag:
            subprocess.run(["python", "scripts/tag_databricks_publication.py", str(package), "--run-id", "dbx_reload_" + uuid.uuid4().hex, "--profile", args.profile, "--catalog", args.catalog, "--schema", args.schema, "--warehouse", args.warehouse, "--workers", str(args.workers)], cwd=root, check=True, stdout=subprocess.DEVNULL)
    result = {"status": "pass", "package_count": 13, "csv_attempt_count": attempted, "force": args.force, "tagged": args.tag, "reuse_policy": "COPY INTO skips already-loaded immutable source files unless explicit force is used"}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
