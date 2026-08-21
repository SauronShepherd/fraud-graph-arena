from pathlib import Path
import pytest
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse, PointerPublisher, validate_candidate
from fraud_graph_arena.canonical_persistence.models import PublicationStatus
from fraud_graph_arena.canonical_persistence.reports import digest_report, safe_report

ROOT=Path(__file__).resolve().parents[2]
PACKAGE=next((ROOT/"case-data/canonical/v1").iterdir())

def test_candidate_validation_rejects_wrong_snapshot():
    with pytest.raises(ValueError): validate_candidate({"bad": []}, case_id="x", snapshot_version="y")

def test_pointer_publisher_activates_and_rolls_back():
    warehouse=MemoryWarehouse(); importer=CanonicalImporter(warehouse)
    result=importer.import_package(PACKAGE); pub=warehouse.publications[result.publication_id]
    pub.status=PublicationStatus.VALIDATED; warehouse.active.clear()
    publisher=PointerPublisher(warehouse); publisher.activate(pub.publication_id)
    assert publisher.active_for(pub.identity.key).publication_id == pub.publication_id
    publisher.rollback(pub.identity.key, pub.publication_id)

def test_reports_are_deterministic_and_secret_safe():
    payload={"status":"pass","count":3}; assert digest_report(payload)==digest_report(payload)
    with pytest.raises(ValueError): safe_report({"access_token":"redacted"})
