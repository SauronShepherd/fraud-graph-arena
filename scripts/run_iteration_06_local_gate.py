"""Validate the current FGA06 evidence bundle without mutating external systems."""
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
    assert len(fixture["nodes"]) == 18 and len(fixture["edges"]) == 26
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
    assert status["decision"] == "QUALIFIED_CYTOSCAPE_INCUMBENT"
    assert status["benchmark_executed"] is True and status["tests_executed"] is True
    assert status["databricks_profile"] == "fga"
    assert status["renderer_automatic_status"] == "PASS_ALL_4_CANDIDATES"

    structure = load_json("reports/iteration-06/databricks-structure-fga-2026-11-08.json")
    assert structure["status"] == "pass" and structure["actual_count"] == structure["expected_count"] == 44
    rows = load_json("reports/iteration-06/databricks-row-counts-fga-2026-11-08.json")
    assert rows["status"] == "pass" and rows["mismatch_count"] == 0 and rows["table_count"] == 32
    rerun = load_json("reports/iteration-06/databricks-all-packages-fga-2026-11-08.json")
    assert rerun["status"] == "pass" and rerun["package_count"] == 13
    assert all(result["lifecycle"]["status"] == "REUSED_PRECHECK" and result["statements"] == 0 for result in rerun["results"])
    comparison = load_json("reports/iteration-06/renderer-comparison-fga-2026-11-03.json")
    assert comparison["schema"] == "fga06-renderer-comparison-v3"
    assert comparison["fixture_sha256"] == fixture_sha
    assert comparison["fixture"]["nodes"] == 18 and comparison["fixture"]["edges"] == 26
    assert all(candidate["automatic_status"] == "PASS" for candidate in comparison["candidates"])
    performance = load_json("reports/iteration-06/renderer-performance-fga-2026-11-08.json")
    assert performance["status"] == "PASS" and performance["targets"]["repetitions"] == 12
    assert all(candidate["envelope"]["pass"] for candidate in performance["candidates"])
    qualification = load_json("reports/iteration-06/renderer-cytoscape-qualification-fga-2026-11-08.json")
    assert qualification["decision"] == "QUALIFIED"
    assert all(value == "PASS" for value in qualification["hard_requirements"].values())

    print(json.dumps({"status": "PASS", "fixture_sha256": fixture_sha, "t02_nodes": 7, "t02_edges": 7, "frontend_typecheck": "run separately", "renderer_candidates": 4, "renderer_decision": "QUALIFIED_CYTOSCAPE_INCUMBENT", "renderer_performance_repetitions": 12, "databricks_profile": "fga", "databricks_structure_objects": 44, "databricks_tables_verified": 32, "databricks_idempotency_packages": 13}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
