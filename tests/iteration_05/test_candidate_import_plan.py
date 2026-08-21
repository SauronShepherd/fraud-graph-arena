from pathlib import Path
from scripts.import_databricks_candidate import plan

ROOT = Path(__file__).resolve().parents[2]

def test_candidate_plan_tags_rows_at_write_time():
    statements = plan(ROOT / "case-data/canonical/v1/T1_THE_MISSING_120_canonical_case_data_v3", "run_test", "sda_dev", "sandbox")
    assert len(statements) == 64
    assert all("INSERT INTO" in statement or "CREATE OR REPLACE TEMPORARY VIEW" in statement for statement in statements)
    assert all("_publication_id" in statement for statement in statements if statement.startswith("INSERT INTO"))
    assert not any("UPDATE" in statement for statement in statements)
