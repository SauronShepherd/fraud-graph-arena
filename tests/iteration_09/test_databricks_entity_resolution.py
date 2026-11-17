from __future__ import annotations

from typing import Any

from scripts.qualify_entity_resolution import build_statements, qualify


def _response(rows: list[list[Any]]) -> dict[str, Any]:
    return {"result": {"data_array": rows}}


def test_qualification_is_read_only_and_requires_golden_and_hard_negative_pairs() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")
    calls: list[str] = []

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        calls.append(statement)
        lowered = statement.lower()
        assert not any(word in lowered for word in (" create ", " delete ", " drop ", " insert ", " merge ", " update "))
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "3.0.0-canonical.1", "2026.07.19.1", "pub-1"]])
        if statement == statements["candidate_pairs"]:
            return _response([["T2-Z-001", "T2-P-CIPHER-A", "T2-P-CIPHER-B", "PERSON", "HIGH", "false", "CURATED_APPROXIMATION", "ZINGG_LIKE", "2026.07.19.1"], ["T2-Z-002", "T2-P-CIPHER-A", "T2-P-CYPHER", "PERSON", "MEDIUM", "false", "CURATED_APPROXIMATION", "ZINGG_LIKE", "2026.07.19.1"]])
        if statement == statements["candidate_count"]:
            return _response([[2, 2, 1]])
        if statement == statements["exact_count"]:
            return _response([[5, 5, 1]])
        if statement == statements["exact_pair_types"]:
            return _response([["T2-GF-001", "SAME_DEVICE", "T2-LOGIN-A", "T2-LOGIN-B", "device", "false", "2026.07.19.1"]])
        if statement == statements["runtime_probe"]:
            return _response([["warehouse"]])
        return _response([["fga_active_published_entity_resolution_candidates_csv", "case_id"], ["fga_active_published_entity_resolution_candidates_csv", "candidate_id"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert report["zingg_compatibility"]["actual_zingg_run"] is False
    assert len(calls) == 7


def test_qualification_rejects_truth_column() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "v", "s", "p"]])
        if statement == statements["candidate_pairs"]:
            return _response([])
        if statement == statements["candidate_count"]:
            return _response([[2, 2, 1]])
        if statement == statements["exact_count"]:
            return _response([[5, 5, 1]])
        if statement == statements["exact_pair_types"]:
            return _response([])
        if statement == statements["runtime_probe"]:
            return _response([["warehouse"]])
        return _response([["fga_active_published_entity_resolution_candidates_csv", "expected_truth"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "fail"
    assert report["forbidden_columns"] == ["expected_truth"]


def test_qualification_rejects_unsupported_candidate_band() -> None:
    statements = build_statements("sda_dev", "sandbox", "ACADEMY_T02")

    def execute(profile: str, warehouse: str, catalog: str, schema: str, statement: str) -> dict[str, Any]:
        if statement == statements["publication"]:
            return _response([["ACADEMY_T02", "v", "s", "p"]])
        if statement == statements["candidate_pairs"]:
            return _response([
                ["c1", "T2-P-CIPHER-A", "T2-P-CIPHER-B", "PERSON", "UNKNOWN", "false", "CURATED_APPROXIMATION", "ZINGG_LIKE", "s"],
                ["c2", "T2-P-CIPHER-A", "T2-P-CYPHER", "PERSON", "MEDIUM", "false", "CURATED_APPROXIMATION", "ZINGG_LIKE", "s"],
            ])
        if statement == statements["candidate_count"]:
            return _response([[2, 2, 1]])
        if statement == statements["exact_count"]:
            return _response([[5, 5, 1]])
        if statement == statements["exact_pair_types"]:
            return _response([["m1", "SAME_DEVICE", "a", "b", "device", "false", "s"]])
        if statement == statements["runtime_probe"]:
            return _response([["warehouse"]])
        return _response([["candidates", "case_id"]])

    report = qualify("fga", "warehouse", "sda_dev", "sandbox", "ACADEMY_T02", execute)
    assert report["status"] == "fail"
    assert report["checks"]["candidate_bands_supported"] is False
