from pathlib import Path
import yaml

ROOT = Path(__file__).parents[2]

def test_module_map_has_exactly_m01_to_m20_and_existing_paths():
    data = yaml.safe_load((ROOT / "config/governance/module-implementation-map.yaml").read_text())
    modules = data["modules"]
    assert [m["id"] for m in modules] == [f"M{i:02d}" for i in range(1, 21)]
    for module in modules:
        if module["status"] == "planned":
            continue
        for location in module["locations"]:
            assert (ROOT / location).exists(), (module["id"], location)


def test_module_map_uses_truthful_statuses_roles_and_test_paths():
    data = yaml.safe_load((ROOT / "config/governance/module-implementation-map.yaml").read_text())
    allowed_statuses = {"planned", "boundary_only", "partial", "implemented"}
    allowed_roles = {"WEB", "MAINTENANCE", "EVALUATOR", "MIGRATE"}
    for module in data["modules"]:
        assert module["status"] in allowed_statuses
        assert set(module["roles"]) <= allowed_roles
        for test_path in module.get("tests", []):
            assert (ROOT / test_path).exists(), (module["id"], test_path)
        if module["status"] != "planned":
            assert module["locations"], module["id"]
