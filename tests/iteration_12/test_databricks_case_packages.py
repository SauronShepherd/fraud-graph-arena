from __future__ import annotations

from typing import Any

from scripts.qualify_case_packages import build_statements, qualify


def _response(rows: list[list[Any]]) -> dict[str, Any]:
    return {"result": {"data_array": rows}}


def test_case_package_qualification_is_read_only_and_checks_t03_boundary() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T03")
    calls: list[str] = []

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        assert profile == "fga"
        assert warehouse == "warehouse"
        calls.append(statement)
        lowered = statement.lower()
        assert not any(f" {word} " in lowered for word in ("insert", "update", "delete", "merge", "drop", "create", "alter", "truncate"))
        if statement == statements["publication"]:
            return _response([["ACADEMY_T03", "3.0.0-canonical.1", "2026.07.19.1", "pub-t03"]])
        if statement == statements["records"]:
            return _response([[23, 23, 1]])
        if statement == statements["relationships"]:
            return _response([[27, 27, 1]])
        if statement == statements["columns"]:
            return _response([["fga_active_published_records_csv", "case_id"], ["fga_active_published_records_csv", "record_id"], ["fga_active_published_relationships_csv", "relationship_id"]])
        return _response([["warehouse"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T03", execute)
    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert report["package_boundary"]["actual_engine_run"] is False
    assert len(calls) == 5


def test_case_package_qualification_rejects_truth_column() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T03")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return _response([["ACADEMY_T03", "v", "s", "p"]])
        if statement == statements["records"]:
            return _response([[23, 23, 1]])
        if statement == statements["relationships"]:
            return _response([[27, 27, 1]])
        if statement == statements["columns"]:
            return _response([["fga_active_published_records_csv", "expected_truth"]])
        return _response([["warehouse"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T03", execute)
    assert report["status"] == "fail"
    assert report["forbidden_columns"] == ["expected_truth"]

