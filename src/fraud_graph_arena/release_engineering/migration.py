from __future__ import annotations

import sqlite3
from pathlib import Path


LEGACY_RELEASE_ID = "fga18-legacy"
ROUND_MIGRATION_VERSION = "rounds-v2-release-binding"

ROUND_BINDING_COLUMNS: tuple[tuple[str, str], ...] = (
    ("release_id", f"TEXT NOT NULL DEFAULT '{LEGACY_RELEASE_ID}'"),
    ("package_version", "TEXT NOT NULL DEFAULT 'legacy-package'"),
    ("rules_version", "TEXT NOT NULL DEFAULT 'legacy-rules'"),
    ("economy_version", "TEXT NOT NULL DEFAULT 'legacy-economy'"),
    ("scoring_version", "TEXT NOT NULL DEFAULT 'legacy-scoring'"),
    ("screen_set_version", "TEXT NOT NULL DEFAULT 'legacy-screen-set'"),
    ("api_contract_version", "TEXT NOT NULL DEFAULT 'v1'"),
    ("analytics_version", "TEXT NOT NULL DEFAULT 'legacy-analytics'"),
    ("package_digest", "TEXT NOT NULL DEFAULT 'legacy-package-digest'"),
)


def apply_round_migrations(connection: sqlite3.Connection) -> dict[str, object]:
    """Apply the forward-only round binding migration and return its receipt."""

    if not connection.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'rounds'").fetchone():
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
        "CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    columns = {row[1] for row in connection.execute("PRAGMA table_info(rounds)").fetchall()}
    added: list[str] = []
    for name, declaration in ROUND_BINDING_COLUMNS:
        if name not in columns:
            connection.execute(f"ALTER TABLE rounds ADD COLUMN {name} {declaration}")
            added.append(name)
    connection.execute(
        "INSERT OR REPLACE INTO schema_migrations(version) VALUES (?)",
        (ROUND_MIGRATION_VERSION,),
    )
    return {"version": ROUND_MIGRATION_VERSION, "added_columns": added, "reversible": False}


def migrate_rounds_database(path: Path) -> dict[str, object]:
    path = Path(path)
    with sqlite3.connect(path) as connection:
        return apply_round_migrations(connection)
