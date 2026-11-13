import pytest
from fraud_graph_arena.canonical_persistence.databricks_warehouse import DatabricksWarehouse

def test_adapter_rejects_unregistered_identifiers():
    warehouse = DatabricksWarehouse()
    with pytest.raises(ValueError): warehouse.qualify_table("fga_arbitrary")
    with pytest.raises(ValueError): warehouse.select(["COUNT(*)"], "fga_import_runs")

def test_candidate_operations_are_registry_resolved(monkeypatch):
    warehouse = DatabricksWarehouse()
    statements = []
    def fake_execute(self, statement):
        statements.append(statement)
        if "SELECT status,case_id,case_version,snapshot_version,canonical_model_version" in statement:
            return {"result": {"data_array": [["VALIDATED", "case_1", "1.0.0", "snap_1", "1.0.0"]]}}
        if "SELECT COUNT(*) AS pointer_count" in statement:
            return {"result": {"data_array": [[0]]}}
        return {"status": {"state": "SUCCEEDED"}}
    monkeypatch.setattr(DatabricksWarehouse, "execute", fake_execute)
    warehouse.insert_candidate("config/cases.csv", [{"case_id": "case'1"}], "pub_1", "run_1")
    warehouse.cleanup_candidate("pub_1")
    warehouse.activate_publication("case_1", "1.0.0", "snap_1", "1.0.0", "pub_1", "run_1")
    assert any("fga_config_cases_csv" in statement and "case''1" in statement for statement in statements)
    assert all("fga_" in statement for statement in statements)


def test_activation_statement_aliases_all_pointer_columns(monkeypatch):
    warehouse = DatabricksWarehouse()
    statements = []

    def fake_execute(self, statement):
        statements.append(statement)
        if "SELECT status,case_id,case_version,snapshot_version,canonical_model_version" in statement:
            return {"result": {"data_array": [["VALIDATED", "case_1", "1.0.0", "snap_1", "1.0.0"]]}}
        if "SELECT COUNT(*) AS pointer_count" in statement:
            return {"result": {"data_array": [[0]]}}
        return {"status": {"state": "SUCCEEDED"}}

    monkeypatch.setattr(DatabricksWarehouse, "execute", fake_execute)
    warehouse.activate_publication("case_1", "1.0.0", "snap_1", "1.0.0", "pub_1", "run_1")
    merge = statements[-1]
    assert "AS canonical_model_version" in merge
    assert "AS activating_run_id" in merge
    assert "source.case_id" in merge
    assert "WHEN NOT MATCHED THEN INSERT" in merge


def test_candidate_validation_scopes_row_count_to_publication():
    from scripts.validate_databricks_candidate import validation_queries

    first = validation_queries("pub_test", "run_test", "sda_dev", "sandbox")[0]
    assert "FROM sda_dev.sandbox.fga_config_cases_csv WHERE _publication_id = 'pub_test'" in first

def test_import_records_use_typed_operational_values():
    from pathlib import Path
    from fraud_graph_arena.canonical_persistence.importer import CanonicalImporter
    from fraud_graph_arena.canonical_persistence.models import ImportRunDataset, ImportRunFile
    from fraud_graph_arena.canonical_persistence.warehouse import MemoryWarehouse
    package = sorted((Path("case-data/canonical/v1")).iterdir())[0]
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(package)
    run = warehouse.runs[result.run_id]
    assert isinstance(next(iter(run.files.values())), ImportRunFile)
    assert isinstance(next(iter(run.datasets.values())), ImportRunDataset)
    assert warehouse.active_records[run.identity.key].activating_run_id == result.run_id


def test_execute_polls_pending_sql_until_success(monkeypatch):
    import json

    calls = []

    class Completed:
        def __init__(self, stdout, returncode=0, stderr=""):
            self.stdout = stdout
            self.returncode = returncode
            self.stderr = stderr

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[1:3] == ["api", "post"]:
            return Completed(json.dumps({"statement_id": "s-1", "status": {"state": "PENDING"}}))
        return Completed(json.dumps({"statement_id": "s-1", "status": {"state": "SUCCEEDED"}, "result": {"data_array": []}}))

    monkeypatch.setattr("fraud_graph_arena.canonical_persistence.databricks_warehouse.subprocess.run", fake_run)
    monkeypatch.setattr("fraud_graph_arena.canonical_persistence.databricks_warehouse.time.sleep", lambda _: None)
    result = DatabricksWarehouse(profile="fga").execute("SELECT 1")
    assert result["status"]["state"] == "SUCCEEDED"
    assert any(command[1:3] == ["api", "get"] for command in calls)


def test_execute_bounds_cli_submission_timeout(monkeypatch):
    import subprocess

    def fake_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

    monkeypatch.setattr("fraud_graph_arena.canonical_persistence.databricks_warehouse.subprocess.run", fake_run)
    with pytest.raises(RuntimeError, match="submission timed out"):
        DatabricksWarehouse(profile="fga").execute("SELECT 1")
