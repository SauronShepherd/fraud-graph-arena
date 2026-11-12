"""Validate the production screen set against its versioned JSON Schema."""

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "apps/web/src/screen-system/schema/screen-set.schema.json"
DEFINITIONS_PATH = ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json"


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    definitions = json.loads(DEFINITIONS_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(definitions)
    print("screen definitions satisfy the JSON Schema")


if __name__ == "__main__":
    main()
