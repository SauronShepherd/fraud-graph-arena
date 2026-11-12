from pathlib import Path

import pytest

from fraud_graph_arena.case_data.converters.common import convert_flat_csv
from fraud_graph_arena.case_data.validator import validate_package


def test_converter_rejects_duplicate_source_headers_before_mapping(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "people.csv").write_text("id,name,name\n1,Alice,Attacker\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate source header"):
        convert_flat_csv(source, tmp_path / "output", case_id="CASE_1", family="ACADEMY")


def test_converter_emits_a_valid_canonical_records_table(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "people.csv").write_text("id,name\n1,Alice\n", encoding="utf-8")
    convert_flat_csv(source, tmp_path / "output", case_id="CASE_1", family="ACADEMY")
    assert validate_package(tmp_path / "output") == []


def test_converter_rejects_ragged_source_rows(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "people.csv").write_text("id,name\n1,Alice,extra\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 2"):
        convert_flat_csv(source, tmp_path / "output", case_id="CASE_1", family="ACADEMY")
