from pathlib import Path
from fraud_graph_arena.case_data.package import PackageBuilder
from fraud_graph_arena.case_data.validator import validate_package
from fraud_graph_arena.case_data.csv_codec import write_table
import pytest
def test_builder_writes_header_only_empty_tables(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write()
    assert all(p.stat().st_size>0 for p in root.rglob('*.csv')); assert not validate_package(root)
def test_zero_byte_table_fails(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write(); (root/'config/cases.csv').write_bytes(b'')
    assert any(x['check_id']=='PKG.FILE.EMPTY' for x in validate_package(root))

def test_csv_writer_rejects_missing_non_nullable_fields(tmp_path):
    with pytest.raises(ValueError, match='missing non-nullable'):
        write_table(tmp_path / 'cases.csv', 'config/cases.csv', [{'case_id': 'CASE'}])
