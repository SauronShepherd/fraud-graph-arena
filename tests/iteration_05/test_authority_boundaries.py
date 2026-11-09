from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_permissions_revoke_truth_and_grant_safe_layers_only():
    sql = (ROOT / "sql/lakehouse/fga_permissions_dev_v1.sql").read_text()
    assert "REVOKE ALL PRIVILEGES ON TABLE fga_truth_entities_csv FROM `fga_web`" in sql
    assert "GRANT SELECT ON VIEW fga_active_published_records_csv TO `fga_web`" in sql
    assert "fga_analytics_entity_resolution_candidates_csv" in sql

def test_importer_has_no_mutable_application_state_imports():
    source = (ROOT / "src/fraud_graph_arena/canonical_persistence/importer.py").read_text()
    for forbidden in ("rounds", "credits", "sessions", "submissions"):
        assert f"fraud_graph_arena.{forbidden}" not in source
