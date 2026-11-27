from __future__ import annotations

import copy
import json
import sqlite3
from pathlib import Path

from fraud_graph_arena.case_packages import CasePackageRegistry
from fraud_graph_arena.release_engineering import (
    CompatibilityDecision,
    ReleasePromotion,
    apply_round_migrations,
    build_release_manifest,
    evaluate_saved_round,
    load_runtime_context,
    validate_release_manifest,
)
from fraud_graph_arena.rounds.adapters.sqlite import SqliteRoundRepository


ROOT = Path(__file__).resolve().parents[2]


def test_release_manifest_names_every_deployable_unit_and_validates_digests() -> None:
    manifest = build_release_manifest(ROOT, release_id="fga19-test.1", source_revision="0" * 40)
    assert not validate_release_manifest(manifest, ROOT)
    assert {unit["id"] for unit in manifest["units"]} == {
        "frontend",
        "python_backend",
        "database_migrations",
        "case_packages",
        "graph_assets",
        "analytics_jobs",
    }
    assert all(unit["immutable"] is True for unit in manifest["units"])


def test_release_manifest_rejects_a_changed_unit_digest() -> None:
    manifest = build_release_manifest(ROOT, release_id="fga19-test.2", source_revision="1" * 40)
    broken = copy.deepcopy(manifest)
    broken["units"][0]["digest"] = "sha256:" + ("0" * 64)
    errors = validate_release_manifest(broken, ROOT)
    assert any("digest mismatch for frontend" in error for error in errors)


def test_ci_contract_keeps_blocking_stages_explicit() -> None:
    contract = json.loads((ROOT / "contracts/release/fga19-ci-pipeline.json").read_text(encoding="utf-8"))
    assert [stage["id"] for stage in contract["stages"]] == [
        "lint",
        "unit",
        "contracts",
        "case-validation",
        "end-to-end",
        "container-build",
        "deployment-smoke",
    ]
    assert contract["stages"][-1]["blocks"] == "promotion"


def test_sqlite_migration_preserves_an_old_round_as_legacy_bound(tmp_path: Path) -> None:
    path = tmp_path / "old.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE rounds (
                id TEXT PRIMARY KEY, player_id TEXT NOT NULL, path_id TEXT NOT NULL,
                case_id TEXT NOT NULL, case_version TEXT NOT NULL, status TEXT NOT NULL,
                created_at TEXT NOT NULL, started_at TEXT NULL, intro_completed_at TEXT NULL,
                credits_remaining INTEGER NOT NULL DEFAULT 0, version INTEGER NOT NULL DEFAULT 1,
                submitted_at TEXT NULL, submission_id TEXT NULL
            )
            """
        )
        connection.execute(
            "INSERT INTO rounds (id, player_id, path_id, case_id, case_version, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("old-round", "hercule", "DETECTIVE_ACADEMY", "ACADEMY_001", "1.0.0", "ACTIVE", "2026-01-01T00:00:00+00:00"),
        )
    with sqlite3.connect(path) as connection:
        report = apply_round_migrations(connection)
        row = connection.execute("SELECT release_id, package_version, package_digest FROM rounds WHERE id = 'old-round'").fetchone()
        migration = connection.execute("SELECT version FROM schema_migrations").fetchone()
    assert report["reversible"] is False
    assert row == ("fga18-legacy", "legacy-package", "legacy-package-digest")
    assert migration == ("rounds-v2-release-binding",)


def test_repository_migration_runs_before_a_new_round_is_written(tmp_path: Path) -> None:
    repository = SqliteRoundRepository(tmp_path / "rounds.sqlite3")
    assert repository.is_ready()
    with sqlite3.connect(tmp_path / "rounds.sqlite3") as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(rounds)").fetchall()}
    assert {"release_id", "scoring_version", "package_digest"}.issubset(columns)


def test_round_binds_release_and_package_contract(client) -> None:
    response = client.post(
        "/api/v1/rounds",
        json={"player_id": "hercule", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T03"},
    )
    assert response.status_code == 201, response.text
    round_payload = response.json()
    assert round_payload["release_id"] == "fga19-runtime-v1"
    assert round_payload["package_version"] == "1.0.0-fga13"
    assert round_payload["rules_version"] == "fga13-engine-v1"
    assert round_payload["economy_version"] == "fga12-economy-v1"
    assert round_payload["scoring_version"] == "fga12-scoring-v1"
    assert len(round_payload["package_digest"]) == 64


def test_saved_round_stays_bound_after_a_runtime_restart(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient
    from fraud_graph_arena.application import create_app
    from fraud_graph_arena.config import Settings

    path = tmp_path / "restart.sqlite3"
    settings = Settings(environment="test", round_repository="sqlite", sqlite_path=path, frontend_dist=tmp_path / "missing", allowed_origins=[])
    with TestClient(create_app(settings)) as first:
        created = first.post("/api/v1/rounds", json={"player_id": "hercule", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T03"}).json()
        first.post(f"/api/v1/rounds/{created['id']}/start")
        active = first.post(f"/api/v1/rounds/{created['id']}/opening/complete").json()
    with TestClient(create_app(settings)) as restarted:
        workspace = restarted.get(f"/api/v1/rounds/{created['id']}/workspace")
    assert workspace.status_code == 200, workspace.text
    restored = workspace.json()["round"]
    assert restored["release_id"] == active["release_id"]
    assert restored["case_version"] == active["case_version"]
    assert restored["package_digest"] == active["package_digest"]


def test_old_round_is_playable_only_when_its_exact_case_version_remains() -> None:
    package = CasePackageRegistry().require("ACADEMY_T03", "1.0.0-fga12")
    binding = load_runtime_context().bind(package)
    playable = evaluate_saved_round(binding, current_release_id="fga19-runtime-v2", available_packages={("ACADEMY_T03", "1.0.0-fga12")})
    frozen = evaluate_saved_round(binding, current_release_id="fga19-runtime-v2", available_packages={("ACADEMY_T03", "2.0.0")})
    assert playable.decision == CompatibilityDecision.PLAYABLE
    assert frozen.decision == CompatibilityDecision.FROZEN


def test_broken_promotion_is_rejected_and_rollback_moves_only_the_app_pointer() -> None:
    promotion = ReleasePromotion(ROOT)
    stable = build_release_manifest(ROOT, release_id="fga19-stable-test", source_revision="2" * 40)
    assert promotion.promote(stable, gates={"tests": True}).status == "PROMOTED"
    broken = copy.deepcopy(stable)
    broken["release_id"] = "fga19-broken-test"
    broken["units"][0]["digest"] = "sha256:" + ("f" * 64)
    assert promotion.promote(broken, gates={"tests": True}).status == "REJECTED"
    candidate = build_release_manifest(ROOT, release_id="fga19-candidate-test", source_revision="3" * 40)
    assert promotion.promote(candidate, gates={"tests": True}).status == "PROMOTED"
    receipt = promotion.rollback("fga19-stable-test")
    assert receipt.status == "ROLLED_BACK"
    assert "data rollback remains separate" in receipt.reason
    assert promotion.active_release_id == "fga19-stable-test"
