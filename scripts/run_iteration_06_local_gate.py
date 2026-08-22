"""Run FGA06 checks that are safe in a local-only, no-test, no-Databricks session."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

def main() -> int:
    fixture_path = ROOT / "qualification" / "fixture-v1.json"
    fixture_sha = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    fixture = load_json("qualification/fixture-v1.json")
    assert fixture["fixture_version"] == "1"
    assert len(fixture["nodes"]) == 4 and len(fixture["edges"]) == 3
    ids = {node["id"] for node in fixture["nodes"]}
    assert all(edge["source_id"] in ids and edge["target_id"] in ids for edge in fixture["edges"])

    forbidden = ("/truth/", "entity_resolution_candidates", "exact_matches")
    source = (ROOT / "src" / "fraud_graph_arena" / "case_data" / "academy_graph.py").read_text(encoding="utf-8")
    assert not any(token in source for token in forbidden)

    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from fraud_graph_arena.case_data.academy_graph import t02_graph
    graph = t02_graph()
    assert graph["node_count"] == 7 and graph["edge_count"] == 7
    assert {node.record_id for node in graph["nodes"]} == {"T2-P-CIPHER-A", "T2-P-CIPHER-B", "T2-P-CYPHER", "T2-O-ALPHA", "T2-O-BETA", "T2-O-GAMMA", "T2-O-BAKERY"}
    assert {edge.relationship_id for edge in graph["edges"]} == {"T2-REL-001", "T2-REL-002", "T2-REL-003", "T2-REL-004", "T2-REL-016", "T2-REL-017", "T2-REL-018"}

    status = load_json("reports/iteration-06/qualification-status.json")
    assert status["decision"] == "BLOCKED_PENDING_QUALIFICATION"
    assert status["benchmark_executed"] is False and status["tests_executed"] is False
    print(json.dumps({"status": "PASS", "fixture_sha256": fixture_sha, "t02_nodes": 7, "t02_edges": 7, "frontend_typecheck": "run separately", "tests": "NOT RUN", "databricks": "NOT ACCESSED"}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
