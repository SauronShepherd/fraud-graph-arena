"""Exercise the FGA-19 migration, playable binding and rollback boundaries."""

from __future__ import annotations

import copy
from dataclasses import asdict
import gc
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.application import create_app  # noqa: E402
from fraud_graph_arena.config import Settings  # noqa: E402
from fraud_graph_arena.release_engineering import (  # noqa: E402
    ReleasePromotion,
    apply_round_migrations,
    build_release_manifest,
    validate_release_manifest,
)


def _expect(response, status: int) -> dict:
    assert response.status_code == status, response.text
    return response.json() if response.content else {}


def _old_round_database(path: Path) -> None:
    connection = sqlite3.connect(path)
    try:
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
        connection.commit()
    finally:
        connection.close()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="fga19-release-") as directory:
        temp_root = Path(directory)
        database = temp_root / "old-rounds.sqlite3"
        _old_round_database(database)
        connection = sqlite3.connect(database)
        try:
            migration = apply_round_migrations(connection)
            columns = {row[1] for row in connection.execute("PRAGMA table_info(rounds)").fetchall()}
            legacy = connection.execute("SELECT release_id, package_version FROM rounds WHERE id = 'old-round'").fetchone()
            connection.commit()
        finally:
            connection.close()
        assert {"release_id", "package_version", "package_digest"}.issubset(columns)
        assert legacy == ("fga18-legacy", "legacy-package")

        stable = build_release_manifest(ROOT, release_id="fga19-stable")
        assert not validate_release_manifest(stable, ROOT)
        promotion = ReleasePromotion(ROOT)
        stable_receipt = promotion.promote(stable, gates={"tests": True, "smoke": True})

        broken = copy.deepcopy(stable)
        broken["release_id"] = "fga19-broken"
        broken["units"][0]["digest"] = "sha256:" + ("0" * 64)
        broken_receipt = promotion.promote(broken, gates={"tests": True, "smoke": True})
        assert broken_receipt.status == "REJECTED"
        assert promotion.active_release_id == "fga19-stable"

        candidate = build_release_manifest(ROOT, release_id="fga19-candidate")
        candidate_receipt = promotion.promote(candidate, gates={"tests": True, "smoke": True})
        rollback_receipt = promotion.rollback("fga19-stable")
        assert candidate_receipt.status == "PROMOTED"
        assert rollback_receipt.status == "ROLLED_BACK"
        assert promotion.active_release_id == "fga19-stable"

        sqlite_path = temp_root / "playable-round.sqlite3"
        settings = Settings(environment="test", round_repository="sqlite", sqlite_path=sqlite_path, frontend_dist=temp_root / "missing", allowed_origins=[])
        with TestClient(create_app(settings)) as client:
            created = _expect(client.post("/api/v1/rounds", json={"player_id": "hercule", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T03"}), 201)
            assert created["release_id"] == "fga19-runtime-v1"
            assert created["case_version"] == "1.0.0-fga12"
            _expect(client.post(f"/api/v1/rounds/{created['id']}/start"), 200)
            _expect(client.post(f"/api/v1/rounds/{created['id']}/opening/complete"), 200)
            workspace = _expect(client.get(f"/api/v1/rounds/{created['id']}/workspace"), 200)
            assert workspace["round"]["package_version"] == created["package_version"]
        gc.collect()

        output = {
            "status": "pass",
            "migration": migration,
            "promotion": {
                "stable": asdict(stable_receipt),
                "broken": asdict(broken_receipt),
                "candidate": asdict(candidate_receipt),
                "rollback": asdict(rollback_receipt),
                "active_release_id": promotion.active_release_id,
            },
            "player_journey": "create -> start -> opening/complete -> workspace",
            "boundary": "local SQLite and in-memory release pointer; no Databricks mutation",
        }
        print(json.dumps(output, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
