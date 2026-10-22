from pathlib import Path
from fraud_graph_arena.case_data.package import PackageBuilder
from fraud_graph_arena.case_data.validator import validate_package
import json
def test_builder_writes_header_only_empty_tables(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write()
    assert all(p.stat().st_size>0 for p in root.rglob('*.csv')); assert not validate_package(root)
def test_zero_byte_table_fails(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write(); (root/'config/cases.csv').write_bytes(b'')
    assert any(x['check_id']=='PKG.FILE.EMPTY' for x in validate_package(root))


def test_manifest_receipts_must_cover_files_and_match_row_counts(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    manifest['files'][0]['rows']=3
    (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
    assert any(error['check_id']=='PKG.RECEIPT.ROWS' for error in validate_package(root))


def test_duplicate_manifest_receipts_are_rejected(tmp_path):
    root=tmp_path/'pkg'; PackageBuilder(root,'CASE_1','ACADEMY').write()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    manifest['files'].append(manifest['files'][0])
    (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
    assert any(error['check_id']=='PKG.RECEIPT.DUPLICATE' for error in validate_package(root))
