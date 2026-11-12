import pytest
from pathlib import Path

from fraud_graph_arena.case_data.csv_codec import read_table
from fraud_graph_arena.case_data.json_codec import loads
from fraud_graph_arena.case_data.types import parse_temporal_value, parse_timestamp


def test_duplicate_json_keys_are_rejected_before_projection() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        loads('{"event_id":"a","event_id":"b"}')


def test_date_only_is_not_silently_promoted_to_midnight() -> None:
    with pytest.raises(ValueError, match="date-only"):
        parse_timestamp("2026-10-21", "event_time")


def test_timestamp_requires_rfc3339_utc_seconds_and_preserves_calendar_dates() -> None:
    assert parse_timestamp("2026-10-21T14:30:00.125Z", "event_time").isoformat() == "2026-10-21T14:30:00.125000+00:00"
    assert parse_temporal_value("2026-10-21", "valid_from") == "2026-10-21"
    for invalid in ("2026-10-21 14:30:00Z", "2026-10-21T14:30Z", "2026-10-21T14:30:00+00:00"):
        with pytest.raises(ValueError, match="RFC3339"):
            parse_timestamp(invalid, "event_time")


def test_csv_rows_with_extra_or_missing_cells_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "table.csv"
    path.write_text("case_id,record_id,record_type,record_subtype,display_label,source_system_id,source_dataset,source_record_key,occurred_at,valid_from,valid_to,status,summary,attributes_json,provenance_ref,content_role,source_payload_hash,snapshot_version\na,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s\n", encoding="utf-8")
    with pytest.raises(ValueError, match="row width"):
        read_table(path, "authoring/records.csv")
