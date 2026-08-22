from __future__ import annotations
import hashlib, json
from pathlib import Path
from .registry import TABLE_PATHS
def build_manifest(root: Path, *, case_id: str, family: str, case_version='1.0.0', snapshot_version='1.0.0', converter='unknown', source_inputs=None, source_dialect=None, mapping_version='family-mappings.v1') -> dict:
    files=[]
    for rel in TABLE_PATHS:
        p=root/rel; data=p.read_bytes()
        files.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rows':max(0, data.count(b'\n')-1)})
    manifest = {'package_name': root.name, 'package_version': '1.0.0', 'case_id':case_id,'case_version':case_version,'family':family,'snapshot_version':snapshot_version,'canonical_model_version':'1.0.0','converter':converter,'converter_version':converter.rsplit('.', 1)[-1] if '.' in converter else converter,'mapping_version':mapping_version,'files':files}
    if source_dialect is not None:
        manifest['source_dialect'] = source_dialect
    if source_inputs is not None:
        manifest['source_inputs'] = source_inputs
    return manifest
def write_manifest(root: Path, **kwargs):
    m=build_manifest(root,**kwargs); (root/'manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8'); return m
