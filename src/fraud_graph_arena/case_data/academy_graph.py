from __future__ import annotations

import csv
from pathlib import Path

from .graph_data import project_graph

_ROOT = Path(__file__).resolve().parents[3]
_T02 = _ROOT / "case-data" / "canonical" / "v1" / "T2_THE_CIRCULAR_COLLAR_canonical_case_data_v3" / "published"
_INITIAL = {"T2-P-CIPHER-A", "T2-P-CIPHER-B", "T2-P-CYPHER", "T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA", "T2-O-BAKERY"}

def t02_graph() -> dict:
    with (_T02 / "records.csv").open(newline="", encoding="utf-8") as handle:
        records = [row for row in csv.DictReader(handle) if row["record_id"] in _INITIAL]
    with (_T02 / "relationships.csv").open(newline="", encoding="utf-8") as handle:
        relationships = [row for row in csv.DictReader(handle) if row["source_record_id"] in _INITIAL and row["target_record_id"] in _INITIAL]
    return project_graph(records, relationships)


def t02_expandable_graph() -> dict:
    """Return the complete player-safe published graph available for viewport expansion."""
    with (_T02 / "records.csv").open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    with (_T02 / "relationships.csv").open(newline="", encoding="utf-8") as handle:
        relationships = list(csv.DictReader(handle))
    snapshots = {row.get("snapshot_version") for row in records}
    if len(snapshots) != 1 or None in snapshots or any(row.get("snapshot_version") not in snapshots for row in relationships):
        raise ValueError("T02 published graph must use one complete snapshot")
    return project_graph(records, relationships)
