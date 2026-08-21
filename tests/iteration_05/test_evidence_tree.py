from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_required_evidence_tree_is_present():
    required = [
        "gate.json", "preflight/git-state.txt", "preflight/canonical-assets.json",
        "imports/repeat-10-summary.json", "imports/idempotence-comparison.json",
        "topology/topology-comparison.json", "security/secret-scan.txt",
        "regression/python-tests.txt", "regression/frontend-tests.txt",
        "regression/frontend-build.txt", "regression/playwright.txt",
    ]
    root = ROOT / "reports/iteration-05"
    assert all((root / path).is_file() for path in required)
