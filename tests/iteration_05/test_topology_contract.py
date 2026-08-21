from pathlib import Path
import json
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, OPERATIONAL_TARGETS

ROOT = Path(__file__).resolve().parents[2]

def test_checked_in_topology_contract_matches_registry():
    config = json.loads((ROOT / "config/lakehouse/expected-topology.v1.json").read_text())
    assert config["operational_tables"] == list(OPERATIONAL_TARGETS)
    assert config["canonical_table_prefix"] == "fga_"
    assert len(PHYSICAL_TARGETS) == 32

def test_ledger_ddl_declares_all_operational_tables():
    ddl = (ROOT / "sql/lakehouse/fga_import_ledger_v1.sql").read_text()
    for table in OPERATIONAL_TARGETS: assert f"CREATE TABLE IF NOT EXISTS {table}" in ddl
