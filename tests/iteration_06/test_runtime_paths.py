from pathlib import Path

from fraud_graph_arena.paths import project_root


def test_runtime_asset_root_is_resolved_from_checkout() -> None:
    root = project_root()
    assert (root / "contracts/canonical/v1/canonical-model.json").is_file()
    assert (root / "config/canonical-reference-rules.v1.json").is_file()
