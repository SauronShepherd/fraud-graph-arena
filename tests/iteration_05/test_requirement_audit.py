import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def test_requirement_audit_is_honest_about_external_gap(tmp_path):
    output=tmp_path/"audit.json"; subprocess.run([sys.executable,"scripts/audit_iteration_05_requirements.py","--root","reports/iteration-05","--output",str(output)],cwd=ROOT,check=True)
    report=json.loads(output.read_text()); assert report["status"]=="external_gap"; assert report["closure_tag_allowed"] is False
    assert report["requirements"]["live_candidate_pipeline"]=="external_gap"
