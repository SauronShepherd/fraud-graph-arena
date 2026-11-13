import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_current_evidence_manifest_is_source_coherent():
    path = ROOT / "reports/iteration-05/unified-audit-current.json"
    data = json.loads(path.read_text())
    assert len(data["source_sha"]) == 40
    assert data["live_databricks"]["source_sha"] == data["source_sha"]
    assert data["closure_allowed"] is False


def test_release_manifest_requires_non_admin_security_for_closure():
    source = (ROOT / "scripts/create_release_evidence_manifest.py").read_text(encoding="utf-8")
    assert "--security-status" in source
    assert 'args.live_status == "qualified" and args.security_status == "qualified"' in source


def test_release_manifest_indexes_the_full_fga07_local_qualification_surface():
    source = (ROOT / "scripts/create_release_evidence_manifest.py").read_text(encoding="utf-8")
    for command in (
        '"python_tests": "python -m pytest -q"',
        '"frontend_build": "npm run build"',
        '"frontend_e2e": "npm run test:e2e -- --workers=1"',
        '"qualification_e2e": "npx playwright test -c playwright.qualification.config.ts --workers=1"',
    ):
        assert command in source
