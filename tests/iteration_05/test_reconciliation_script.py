import json, subprocess, sys

def test_reconcile_marks_only_incomplete_runs_failed(tmp_path):
    state=tmp_path/"state.json"; output=tmp_path/"out.json"
    state.write_text(json.dumps({"runs":[{"run_id":"done","status":"PUBLISHED"},{"run_id":"open","status":"STAGING"}],"active_publication_id":"pub_old"}))
    subprocess.run([sys.executable,"scripts/reconcile_import_runs.py","--state",str(state),"--output",str(output)],check=True)
    result=json.loads(output.read_text()); statuses={r["run_id"]:r["status"] for r in result["runs"]}
    assert statuses == {"done":"PUBLISHED","open":"FAILED"}; assert result["reconciled_run_ids"] == ["open"]; assert result["active_publication_id"] == "pub_old"
