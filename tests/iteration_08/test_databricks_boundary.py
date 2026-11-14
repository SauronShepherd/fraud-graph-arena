from __future__ import annotations

from typing import Any

from scripts.qualify_investigation_boundary import build_statements, qualify


def _response(rows: list[list[Any]]) -> dict[str, Any]:
    return {"result": {"data_array": rows}}


def test_boundary_qualification_is_read_only_and_checks_player_safe_shape() -> None:
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
        return _response([
            ["fga_active_published_records_csv", "case_id"],
            ["fga_active_published_records_csv", "record_id"],
            ["fga_active_published_relationships_csv", "relationship_id"],
        ])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", 20, 21, execute)

    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert len(calls) == 5


def test_boundary_qualification_fails_on_forbidden_column() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "3.0.0-canonical.1", "snapshot", "pub-1"]])
        if statement == statements["records"]:
            return _response([[20, 20, 1]])
        if statement == statements["relationships"]:
            return _response([[21, 21, 1]])
        if statement == statements["dangling_endpoints"]:
            return _response([[0]])
        return _response([["fga_active_published_records_csv", "evaluator_hint"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", 20, 21, execute)

    assert report["status"] == "fail"
    assert report["forbidden_columns"] == ["evaluator_hint"]
