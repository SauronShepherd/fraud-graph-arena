import copy
import json
from pathlib import Path
import jsonschema
import pytest

ROOT = Path(__file__).parents[2]
SCHEMA = json.loads((ROOT / "apps/web/src/screen-system/schema/screen-set.schema.json").read_text())
DEFINITIONS = json.loads((ROOT / "apps/web/src/screen-system/definitions/fga-screen-set.v1.json").read_text())

def test_production_screen_set_is_valid():
    jsonschema.Draft202012Validator(SCHEMA).validate(DEFINITIONS)

@pytest.mark.parametrize("mutation", [
    lambda d: d["screens"][0].update({"expression": "round.status"}),
    lambda d: d["screens"][0].update({"schema_version": "9.0"}),
    lambda d: d["screens"][0]["transitions"][0].update({"history": "SIDEWAYS"}),
])
def test_invalid_screen_set_is_rejected(mutation):
    candidate = copy.deepcopy(DEFINITIONS)
    mutation(candidate)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(SCHEMA).validate(candidate)
