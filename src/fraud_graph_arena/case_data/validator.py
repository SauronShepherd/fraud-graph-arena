from __future__ import annotations
import csv, json, hashlib
from pathlib import Path
from .registry import TABLE_PATHS, headers, sql_types, load_typed_registry
from .types import parse_json, parse_timestamp, validate_sql_value
FORBIDDEN=('canonical_entity','culpability','solve_gate','mastermind','guilty','scoring_rule','ending_rule')
def validate_package(root: Path) -> list[dict]:
    errors=[]; root=Path(root)
    def err(check, table, message): errors.append({'check_id':check,'severity':'ERROR','table':table,'message':message})
    if not (root/'manifest.json').is_file(): err('PKG.MANIFEST','manifest.json','Manifest is required.'); return errors
    try: manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    except Exception: err('PKG.MANIFEST.JSON','manifest.json','Manifest is not valid JSON.'); return errors
    if manifest.get('canonical_model_version')!='1.0.0': err('PKG.MODEL.VERSION','manifest.json','Unsupported canonical model version.')
    loaded={}
    for rel in TABLE_PATHS:
        p=root/rel
        if not p.is_file(): err('PKG.FILE.MISSING',rel,'Canonical table is missing.'); continue
        if p.stat().st_size==0: err('PKG.FILE.EMPTY',rel,'Canonical CSV must contain its header.')
        try:
            with p.open(newline='',encoding='utf-8') as f:
                r=csv.DictReader(f)
                if r.fieldnames != list(headers(rel)): err('CANONICAL.HEADER',rel,'Ordered header mismatch.')
                loaded[rel]=list(r)
                for row in loaded[rel]:
                    layer=rel.split('/',1)[0]
                    if layer in {'published','genie'}:
                        if any(k.lower() in FORBIDDEN for k in row): err('SAFE.TRUTH.LEAK',rel,'Protected truth field found.'); break
                        if 'DO_NOT_SHOW_HERCULE_THIS' in str(row): err('SAFE.TRUTH.LEAK',rel,'Protected truth sentinel found.'); break
                    typed = {column["name"]: column for column in load_typed_registry()[rel]["columns"]}
                    for key,value in row.items():
                        try:
                            if value == "" and not typed[key]["nullable"]: raise ValueError(f"{key}: non-nullable value is empty")
                            validate_sql_value(value, typed[key]["sql_type"], key)
                        except ValueError as exc: err('CANONICAL.TYPE', rel, str(exc))
                        if key.endswith('_json') and value:
                            try: parse_json(value,key)
                            except ValueError as exc: err('CANONICAL.JSON',rel,str(exc))
                        if key in {'valid_from','valid_to','event_time','occurrence_time'} and value:
                            try: parse_timestamp(value,key)
                            except ValueError as exc: err('CANONICAL.TIME',rel,str(exc))
        except (UnicodeError,csv.Error): err('CANONICAL.CSV',rel,'Invalid UTF-8 CSV.')
    for p in root.rglob('*.csv'):
        rel=str(p.relative_to(root)).replace('\\','/')
        if rel not in TABLE_PATHS: err('PKG.FILE.EXTRA',rel,'Unexpected canonical CSV.')
    try:
        manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
        receipts={x.get('path'):x for x in manifest.get('files',[])}
        for rel in TABLE_PATHS:
            p=root/rel
            if p.is_file() and rel in receipts:
                digest=hashlib.sha256(p.read_bytes()).hexdigest()
                if receipts[rel].get('sha256') != digest: err('PKG.RECEIPT.SHA256',rel,'Manifest digest does not match bytes.')
    except Exception: pass
    return errors
