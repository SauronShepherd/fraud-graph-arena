from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
from .registry import TABLE_PATHS
def build_manifest(root: Path, *, case_id: str, family: str, case_version=None, snapshot_version=None, converter=None, source_inputs=None, source_dialect=None, mapping_version='family-mappings.v1') -> dict:
    required = {'case_id': case_id, 'family': family, 'case_version': case_version, 'snapshot_version': snapshot_version, 'converter': converter, 'source_dialect': source_dialect}
    missing = [name for name, value in required.items() if value in (None, '')]
    if missing:
        raise ValueError('manifest identity/provenance fields are required: ' + ','.join(missing))
    files=[]
    for rel in TABLE_PATHS:
        p=root/rel; data=p.read_bytes()
        with p.open(newline='', encoding='utf-8') as stream:
            rows = sum(1 for _ in csv.reader(stream)) - 1
        files.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rows':max(0, rows)})
    manifest = {'package_name': root.name, 'package_version': '1.0.0', 'case_id':case_id,'case_version':case_version,'family':family,'snapshot_version':snapshot_version,'canonical_model_version':'1.0.0','canonical_csv_table_count':len(TABLE_PATHS),'converter':converter,'converter_version':converter.rsplit('.', 1)[-1] if '.' in converter else converter,'mapping_version':mapping_version,'files':files}
    manifest['source_dialect'] = source_dialect
    manifest['source_inputs'] = source_inputs or []
    return manifest
def write_manifest(root: Path, **kwargs):
    m=build_manifest(root,**kwargs); (root/'manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8'); return m
