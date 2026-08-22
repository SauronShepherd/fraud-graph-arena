from __future__ import annotations
import csv, json
import hashlib
from pathlib import Path
from ..identity import stable_id
from ..package import PackageBuilder
def convert_flat_csv(source: Path, output: Path, *, case_id: str, family: str, converter='common.csv.v1'):
    builder=PackageBuilder(output,case_id,family)
    builder.add('config/cases.csv', {'case_id': case_id, 'short_id': case_id, 'title': case_id, 'path_code': family, 'case_version': '1.0.0', 'snapshot_version': '1.0.0', 'generation_seed': 0, 'generation_mode': 'DIRECT_SOURCE', 'ranked': 'false', 'career_unlock': 'false', 'canonical_model_version': '1.0.0'})
    files=sorted(Path(source).glob('*.csv'))
    if not files:
        raise ValueError(f'NO_SOURCE_CSV:{source}')
    source_inputs=[]
    for file in files:
        source_inputs.append({'path': file.name, 'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    for file in files:
        with file.open(newline='',encoding='utf-8') as f:
            for index,row in enumerate(csv.DictReader(f),1):
                source_key=row.get('id') or row.get('record_id') or str(index)
                rid=stable_id('REC',case_id,file.stem,source_key)
                display = row.get('name') or row.get('label') or source_key
                builder.add('authoring/records.csv', {'record_id': rid, 'case_id': case_id, 'record_type': file.stem.upper(), 'record_subtype': 'SOURCE', 'display_label': display, 'source_system_id': 'DIRECT_SOURCE', 'source_dataset': file.name, 'source_record_key': source_key, 'status': 'ACTIVE', 'summary': display, 'attributes_json': json.dumps(row, sort_keys=True), 'provenance_ref': file.name, 'content_role': 'PUBLIC', 'source_payload_hash': hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest(), 'snapshot_version': '1.0.0'})
    return builder.write(converter=converter, source_inputs=source_inputs)
