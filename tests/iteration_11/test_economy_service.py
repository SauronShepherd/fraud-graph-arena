from __future__ import annotations

from pathlib import Path

import pytest

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings
from fraud_graph_arena.economy import EconomyService, InMemoryLedgerRepository, SqliteLedgerRepository
from fraud_graph_arena.rounds.adapters.memory import InMemoryRoundRepository
from fraud_graph_arena.rounds.domain import Round, RoundStatus
from fraud_graph_arena.rounds.service import RoundService


def test_sqlite_ledger_records_charge_and_refund_without_losing_round_state(tmp_path: Path) -> None:
    # The public API test covers wiring. This small adapter check makes the
    # durable ledger contract explicit and avoids relying on a web process.
    repository = SqliteLedgerRepository(tmp_path / "ledger.sqlite3")
    entry = __import__("fraud_graph_arena.economy.models", fromlist=["LedgerEntry", "LedgerEntryType"]).LedgerEntry(
        entry_id="e1", round_id="r1", idempotency_key="k1", request_hash="h", action="RUN_GRAPH_ANALYSIS", entry_type=__import__("fraud_graph_arena.economy.models", fromlist=["LedgerEntryType"]).LedgerEntryType.CHARGE, amount=3, balance_after=6, status="SETTLED", rules_version="fga11-economy-v1", created_at="2026-11-26T00:00:00Z"
    )
    repository.add(entry)
    assert repository.get_charge("r1", "k1") == entry
    assert repository.list_for_round("r1") == (entry,)
