from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("root", type=Path); args = parser.parse_args()
    paths = sorted(args.root.glob("*/fga_canonical_schema_registry_v1.json"))
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        column = next(column for column in data["tables"]["published/records.csv"]["columns"] if column["name"] == "source_system_id")
        column["nullable"] = True
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "registries": len(paths)}, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
