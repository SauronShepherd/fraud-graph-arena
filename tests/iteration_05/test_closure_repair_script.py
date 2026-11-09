from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_closure_repair_is_revision_pinned_and_keeps_admin_gap_explicit():
    source = (ROOT / "scripts/run_iteration_05_closure_repair.py").read_text(encoding="utf-8")
    assert "working_tree_before_artifact" in source
    assert "closure_tag_allowed" in source
    assert "non_admin_truth_denial" in source
    assert "5eebf83666c84e3e90722431688de8926a24476b" in source
