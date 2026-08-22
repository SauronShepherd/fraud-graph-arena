import subprocess, sys

def test_recreation_rejects_non_disposable_environment():
    result=subprocess.run([sys.executable,"scripts/recreate_lakehouse_namespace.py","--environment","fga_prod","--dry-run"],capture_output=True,text=True)
    assert result.returncode != 0 and "refusing destructive recreation" in result.stderr + result.stdout

def test_recreation_dry_run_is_non_mutating():
    result=subprocess.run([sys.executable,"scripts/recreate_lakehouse_namespace.py","--environment","fga_dev","--dry-run"],capture_output=True,text=True,check=True)
    assert '"status": "dry_run"' in result.stdout and '"expected_count": 44' in result.stdout
