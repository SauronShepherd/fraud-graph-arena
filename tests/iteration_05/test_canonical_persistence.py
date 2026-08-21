from pathlib import Path
import json
import pytest
from fraud_graph_arena.canonical_persistence import CanonicalImporter, MemoryWarehouse
from fraud_graph_arena.canonical_persistence.models import ImportStatus
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, expected_topology
from fraud_graph_arena.canonical_persistence.identity import topology_hash
from fraud_graph_arena.canonical_persistence.recovery import reconcile_import_runs
from fraud_graph_arena.canonical_persistence.security import canonical_target, redact_error
from fraud_graph_arena.canonical_persistence.archive import ArchiveSafetyError, safe_extract
from zipfile import ZipFile
from fraud_graph_arena.canonical_persistence.types import validate_row_types

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = sorted((ROOT / "case-data/canonical/v1").iterdir())

def test_registry_is_bounded_and_case_independent():
    assert len(PHYSICAL_TARGETS) == 32
    assert len(expected_topology()) == 37
    assert not any(name.startswith("fga_case_") for name in PHYSICAL_TARGETS.values())

def test_exact_retry_reuses_publication():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    first = importer.import_package(PACKAGES[0]); second = importer.import_package(PACKAGES[0])
    assert first.status == ImportStatus.PUBLISHED
    assert second.status == ImportStatus.REUSED
    assert first.publication_id == second.publication_id
    assert len(warehouse.publications) == 1 and len(warehouse.runs) == 2

def test_failed_candidate_does_not_replace_active():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    first = importer.import_package(PACKAGES[0]); failed = importer.import_package(PACKAGES[1], fail_after=17, retry_of=first.run_id)
    assert failed.status == ImportStatus.FAILED
    assert warehouse.active[(first.publication_id and warehouse.publications[first.publication_id].identity.key)] == first.publication_id

def test_all_packages_share_topology():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    for package in PACKAGES: importer.import_package(package)
    assert warehouse.topology == set(expected_topology()[:32])

def test_manifest_tampering_fails_before_run_staging(tmp_path):
    package = tmp_path / PACKAGES[0].name; import shutil; shutil.copytree(PACKAGES[0], package)
    manifest = json.loads((package / "manifest.json").read_text()); next(item for item in manifest["files"] if item["path"] == "config/cases.csv")["sha256"] = "0" * 64; (package / "manifest.json").write_text(json.dumps(manifest))
    warehouse = MemoryWarehouse()
    with pytest.raises(ValueError): CanonicalImporter(warehouse).import_package(package)
    assert not warehouse.runs

def test_topology_hash_is_order_independent():
    assert topology_hash({"b", "a"}) == topology_hash({"a", "b"})

def test_reconcile_interrupted_run_preserves_active_publication():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    first = importer.import_package(PACKAGES[0]); run = next(iter(warehouse.runs.values())); run.status = "STAGING"
    assert reconcile_import_runs(warehouse) == [run.run_id]
    assert warehouse.active[warehouse.publications[first.publication_id].identity.key] == first.publication_id

def test_rollback_restores_validated_publication_without_rewriting_rows():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    first = importer.import_package(PACKAGES[0]); second = importer.import_package(PACKAGES[1])
    scope = warehouse.publications[second.publication_id].identity.key
    warehouse.rollback(scope, second.publication_id)
    assert warehouse.active[scope] == second.publication_id
    assert warehouse.publications[second.publication_id].semantic_hash == second.semantic_hash

def test_identifiers_are_closed_and_errors_redacted():
    assert canonical_target("config/cases.csv").startswith("fga_")
    with pytest.raises(ValueError): canonical_target("../../secret")
    assert redact_error("token=abc", ("abc",)) == "token=[REDACTED]"

def test_archive_traversal_and_duplicate_paths_are_rejected(tmp_path):
    archive = tmp_path / "bad.zip"
    with ZipFile(archive, "w") as z: z.writestr("../escape.csv", "x")
    with pytest.raises(ArchiveSafetyError): safe_extract(archive, tmp_path / "out")
    duplicate = tmp_path / "duplicate.zip"
    with ZipFile(duplicate, "w") as z: z.writestr("a.csv", "x"); z.writestr("./a.csv", "y")
    with pytest.raises(ArchiveSafetyError): safe_extract(duplicate, tmp_path / "out2")

def test_canonical_type_rules_reject_malformed_values():
    with pytest.raises(ValueError): validate_row_types({"properties_json": "not-json"}, "config/registries.csv")
    with pytest.raises(ValueError): validate_row_types({"sequence": "nope"}, "config/reveal_steps.csv")
    with pytest.raises(ValueError): validate_row_types({"directed": "yes"}, "authoring/relationships.csv")

def test_candidate_cleanup_is_scoped_and_cleanup_failure_is_explicit():
    warehouse = MemoryWarehouse(); importer = CanonicalImporter(warehouse)
    result = importer.import_package(PACKAGES[0]); publication = warehouse.publications[result.publication_id]
    warehouse.candidates[publication.publication_id] = publication
    warehouse.cleanup_candidate(publication.publication_id)
    assert publication.publication_id not in warehouse.candidates
    warehouse.candidates[publication.publication_id] = publication
    with pytest.raises(RuntimeError): warehouse.cleanup_candidate(publication.publication_id, fail=True)
    assert publication.publication_id in warehouse.candidates

def test_persisted_rows_have_correlation_metadata_but_fingerprint_is_semantic():
    warehouse = MemoryWarehouse(); result = CanonicalImporter(warehouse).import_package(PACKAGES[0])
    rows = next(iter(warehouse.publications[result.publication_id].rows.values()))
    if rows:
        assert rows[0]["_publication_id"] == result.publication_id
        assert rows[0]["_load_run_id"] == result.run_id
    assert result.semantic_hash == warehouse.publications[result.publication_id].semantic_hash
