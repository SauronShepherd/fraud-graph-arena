from __future__ import annotations
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "apps/web/src/screen-system/schema/screen-set.schema.json"
DEFINITIONS = ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json"

def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    definitions = json.loads(DEFINITIONS.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(definitions)
    ids = [screen["id"] for screen in definitions["screens"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate screen id")
    known = set(ids)
    for screen in definitions["screens"]:
        if screen["route"]["mode"] == "INTERNAL" and screen["route"]["pattern"] is not None:
            raise SystemExit(f"internal screen has route: {screen['id']}")
        for transition in screen["transitions"]:
            if transition["target"] not in known:
                raise SystemExit(f"unknown transition target: {transition['target']}")
    print(f"validated {len(ids)} screen definitions")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
