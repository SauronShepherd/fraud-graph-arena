from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
from .registry import TABLE_PATHS
def build_manifest(root: Path, *, case_id: str, family: str, case_version='1.0.0', snapshot_version='1.0.0', converter='unknown') -> dict:
    files=[]
    for rel in TABLE_PATHS:
        p=root/rel; data=p.read_bytes()
        with p.open(newline='',encoding='utf-8') as stream:
            reader=csv.reader(stream,strict=True)
            next(reader,None)
            row_count=sum(1 for _ in reader)
        files.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rows':row_count})
    return {'case_id':case_id,'case_version':case_version,'family':family,'snapshot_version':snapshot_version,'canonical_model_version':'1.0.0','converter':converter,'files':files}
def write_manifest(root: Path, **kwargs):
    m=build_manifest(root,**kwargs); (root/'manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8'); return m
