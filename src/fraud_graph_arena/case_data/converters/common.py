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
            reader=csv.reader(f,strict=True)
            try: header=next(reader)
            except StopIteration: raise ValueError(f'{file.name}: missing header')
            if any(not name or name != name.strip() for name in header): raise ValueError(f'{file.name}: blank or padded source header')
            if len(set(header)) != len(header): raise ValueError(f'{file.name}: duplicate source header')
            if not header: raise ValueError(f'{file.name}: missing header')
            for index,values in enumerate(reader,1):
                if len(values) != len(header): raise ValueError(f'{file.name}: row {index+1} has {len(values)} cells; expected {len(header)}')
                row=dict(zip(header,values,strict=True))
                source_key=row.get('id') or row.get('record_id') or str(index)
                rid=stable_id('REC',case_id,file.stem,source_key)
                builder.add('authoring/records.csv',{'record_id':rid,'case_id':case_id,'record_type':file.stem.upper(),'record_subtype':'','display_label':row.get('name') or row.get('label') or source_key,'source_system_id':file.stem,'source_dataset':file.name,'source_record_key':source_key,'occurred_at':'','valid_from':'','valid_to':'','status':'','summary':'','attributes_json':'{}','provenance_ref':f'{file.name}#{index}','content_role':'EVIDENCE','source_payload_hash':'','snapshot_version':'1.0.0'})
    return builder.write(converter=converter)
