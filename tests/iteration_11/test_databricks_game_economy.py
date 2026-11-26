from __future__ import annotations

from typing import Any

from scripts.qualify_game_economy import build_statements, qualify


def response(rows: list[list[Any]]) -> dict[str, Any]:
    return {"result": {"data_array": rows}}


def test_game_economy_qualification_is_read_only_and_does_not_query_truth() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")
    calls: list[str] = []

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        calls.append(statement)
        assert statement.lstrip().upper().startswith("SELECT")
        assert not any(token in statement.lower() for token in ("insert", "update", "delete", "merge", "drop", "create"))
        if statement == statements["publication"]:
            return response([["ACADEMY_T02", "1.0.0-fga06", "2026.07.19.1", "pub-1"]])
        if statement == statements["records"]:
            return response([[20, 20, 1]])
        if statement == statements["relationships"]:
            return response([[21, 21, 1]])
        if statement == statements["runtime_probe"]:
            return response([["warehouse"]])
        return response([["fga_active_published_records_csv", "record_id"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert report["scoring_contract"]["truth_source_queried"] is False
    assert len(calls) == 5


def test_game_economy_qualification_rejects_hidden_column() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return response([["ACADEMY_T02", "v", "s", "p"]])
        if statement == statements["records"]:
            return response([[20, 20, 1]])
        if statement == statements["relationships"]:
            return response([[21, 21, 1]])
        return response([["fga_active_published_records_csv", "expected_truth"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "fail"
    assert report["forbidden_columns"] == ["expected_truth"]
