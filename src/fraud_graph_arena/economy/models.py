from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


ECONOMY_VERSION = "fga11-economy-v1"
ACTION_COSTS: dict[str, int] = {
    "COMPARE_IDENTITIES": 3,
    "RUN_GRAPH_ANALYSIS": 3,
}


class LedgerEntryType(StrEnum):
    CHARGE = "CHARGE"
    REFUND = "REFUND"


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    entry_id: str
    round_id: str
    idempotency_key: str
    request_hash: str
    action: str
    entry_type: LedgerEntryType
    amount: int
    balance_after: int
    status: str
    rules_version: str
    created_at: str
    result_json: str | None = None
