from __future__ import annotations
import csv
from pathlib import Path
from ..identity import stable_id
from ..package import PackageBuilder
def convert_flat_csv(source: Path, output: Path, *, case_id: str, family: str, converter='common.csv.v1'):
    builder=PackageBuilder(output,case_id,family)
    files=sorted(Path(source).glob('*.csv'))
    for file in files:
        with file.open(newline='',encoding='utf-8') as f:
            for index,row in enumerate(csv.DictReader(f),1):
                source_key=row.get('id') or row.get('record_id') or str(index)
                rid=stable_id('REC',case_id,file.stem,source_key)
                builder.add('authoring/records.csv',{'record_id':rid,'case_id':case_id,'record_type':file.stem.upper(),'source_record_id':source_key,'label':row.get('name') or row.get('label') or source_key,'snapshot_version':'1.0.0','source_dataset':file.name,'provenance_json':'{"mode":"DIRECT_SOURCE"}'})
    return builder.write(converter=converter)
