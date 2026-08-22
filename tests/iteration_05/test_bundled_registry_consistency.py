import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_bundled_schema_registries_match_authoritative_registry():
    central = json.loads((ROOT / "contracts/canonical/v1/schema-registry.json").read_text(encoding="utf-8"))
    copies = sorted((ROOT / "case-data/canonical/v1").glob("*/fga_canonical_schema_registry_v1.json"))
    assert len(copies) == 13
    for copy in copies:
        bundled = json.loads(copy.read_text(encoding="utf-8"))
        assert bundled["physical_table_count"] == central["physical_table_count"], copy
        assert bundled["tables"] == central["tables"], copy
        assert bundled["canonical_model_version"] == central["model_version"], copy
