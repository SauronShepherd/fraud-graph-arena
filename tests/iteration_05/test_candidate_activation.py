from scripts.activate_databricks_publication import activation_statement
from scripts.validate_databricks_candidate import validation_queries

def test_activation_is_case_version_scoped_and_uses_merge():
    statement = activation_statement("sda_dev", "sandbox", "case", "1.0.0", "snap", "pub_test")
    assert statement.startswith("MERGE INTO sda_dev.sandbox.fga_active_publications")
    assert "target.case_id = source.case_id AND target.case_version = source.case_version" in statement
    assert ":case_id" not in statement

def test_candidate_validation_covers_all_physical_targets():
    queries = validation_queries("pub_test", "run_test", "sda_dev", "sandbox")
    assert len(queries) == 64
    assert all("_publication_id = 'pub_test'" in query for query in queries)
