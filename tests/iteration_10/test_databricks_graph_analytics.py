from __future__ import annotations

from typing import Any

from scripts.qualify_graph_analytics import build_statements, qualify


def _response(rows: list[list[Any]]) -> dict[str, Any]:
    return {"result": {"data_array": rows}}


def test_graph_qualification_is_read_only_and_requires_known_cycle_fixture() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")
    calls: list[str] = []

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        calls.append(statement)
        lowered = statement.lower()
        assert not any(word in lowered for word in (" create ", " delete ", " drop ", " insert ", " merge ", " update "))
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "3.0.0-canonical.1", "2026.07.19.1", "pub-1"]])
        if statement == statements["records"]:
            return _response([[20, 20, 1]])
        if statement == statements["relationships"]:
            return _response([[21, 21, 1]])
        if statement == statements["dangling_endpoints"]:
            return _response([[0]])
        if statement == statements["known_cycle"]:
            return _response([
                ["T2-REL-016", "PAYS", "T2-O-ALPHA", "T2-O-BETA", "2026-03-01T09:00:00Z", "2026.07.19.1"],
                ["T2-REL-017", "PAYS", "T2-O-BETA", "T2-O-GAMMA", "2026-03-01T10:00:00Z", "2026.07.19.1"],
                ["T2-REL-018", "PAYS", "T2-O-GAMMA", "T2-O-ALPHA", "2026-03-01T11:00:00Z", "2026.07.19.1"],
            ])
        if statement == statements["runtime_probe"]:
            return _response([["warehouse"]])
        return _response([["fga_active_published_relationships_csv", "relationship_id"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert report["graphframes_compatibility"]["actual_engine_run"] is False
    assert len(calls) == 7


def test_graph_qualification_rejects_truth_column() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "v", "s", "p"]])
        if statement == statements["records"]:
            return _response([[20, 20, 1]])
        if statement == statements["relationships"]:
            return _response([[21, 21, 1]])
        if statement == statements["dangling_endpoints"]:
            return _response([[0]])
        if statement == statements["known_cycle"]:
            return _response([["e1", "PAYS", "a", "b", "t", "s"], ["e2", "PAYS", "b", "c", "t", "s"], ["e3", "PAYS", "c", "a", "t", "s"]])
        if statement == statements["runtime_probe"]:
            return _response([["warehouse"]])
        return _response([["fga_active_published_records_csv", "expected_truth"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "fail"
    assert report["forbidden_columns"] == ["expected_truth"]
