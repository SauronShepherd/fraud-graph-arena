from pathlib import Path
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse, build_plan
from fraud_graph_arena.canonical_persistence.lifecycle import require_transition
from fraud_graph_arena.canonical_persistence.models import ImportStatus
import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = next((ROOT / "case-data/canonical/v1").iterdir())

def test_closed_lifecycle_rejects_invalid_transitions():
    require_transition(ImportStatus.STARTED, ImportStatus.PREFLIGHTED)
    with pytest.raises(ValueError): require_transition(ImportStatus.FAILED, ImportStatus.PUBLISHED)

def test_plan_is_registry_closed():
    plan = build_plan()
    assert len(plan) == 32 and len({item.physical_target for item in plan}) == 32
    with pytest.raises(ValueError): build_plan(["unexpected.csv"])

def test_import_records_every_file_and_dataset_receipt():
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(PACKAGE)
    assert len(warehouse.run_files) == 32
    assert len(warehouse.run_datasets) == 32
    assert all(item["phase"] == "VALIDATED" for item in warehouse.run_datasets.values())
    assert warehouse.runs[result.run_id].error_summary is None

