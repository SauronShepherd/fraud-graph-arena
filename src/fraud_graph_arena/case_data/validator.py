from __future__ import annotations
import csv, json, hashlib
from pathlib import Path
from .registry import TABLE_PATHS, headers, sql_types, load_typed_registry, supported_model_versions
from .types import parse_json, parse_timestamp, validate_sql_value
from .semantics import CONFIDENCE_BANDS, FAMILIES, GENERATION_MODES, RELATIONSHIP_FAMILIES, require_controlled
from .projection_contract import truth_leak_paths
from .provenance import provenance_from_row
def validate_package(root: Path) -> list[dict]:
    errors=[]; root=Path(root)
    def err(check, table, message): errors.append({'check_id':check,'severity':'ERROR','table':table,'message':message})
    if not (root/'manifest.json').is_file(): err('PKG.MANIFEST','manifest.json','Manifest is required.'); return errors
    try: manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    except Exception: err('PKG.MANIFEST.JSON','manifest.json','Manifest is not valid JSON.'); return errors
    if manifest.get('canonical_model_version') not in supported_model_versions(): err('PKG.MODEL.VERSION','manifest.json','Unsupported canonical model version.')
    if manifest.get('canonical_csv_table_count') != len(TABLE_PATHS): err('PKG.TABLE.COUNT','manifest.json','Manifest canonical table count must equal the registered inventory.')
    if manifest.get('package_name') != root.name: err('PKG.NAME.IDENTITY','manifest.json','Manifest package_name must match the package directory name.')
    source_inputs = manifest.get('source_inputs', [])
    if not isinstance(source_inputs, list):
        err('PKG.SOURCE.RECEIPTS', 'manifest.json', 'Manifest source_inputs must be an array.')
    else:
        source_paths = []
        for index, receipt in enumerate(source_inputs):
            if not isinstance(receipt, dict) or not receipt.get('path') or not isinstance(receipt.get('bytes'), int) or not isinstance(receipt.get('sha256'), str) or len(receipt.get('sha256', '')) != 64:
                err('PKG.SOURCE.RECEIPTS', 'manifest.json', f'Invalid source input receipt at index {index}.')
            elif receipt['path'] in source_paths:
                err('PKG.SOURCE.DUPLICATE', 'manifest.json', f'Duplicate source input receipt path: {receipt["path"]}.')
            else:
                source_paths.append(receipt['path'])
    for field in ('package_name','package_version','converter','converter_version','mapping_version','source_dialect'):
        if not manifest.get(field): err('PKG.MANIFEST.PROVENANCE','manifest.json',f'Manifest field {field} is required.')
    mapping_file = Path(__file__).resolve().parents[3] / 'config/converters/family-mappings.v1.json'
    approved_mappings = json.loads(mapping_file.read_text(encoding='utf-8')).get('families', {})
    approved_mapping = approved_mappings.get(manifest.get('family'), {})
    for field in ('converter', 'source_dialect'):
        if approved_mapping and manifest.get(field) != approved_mapping.get(field):
            err('PKG.CONVERTER.PROVENANCE', 'manifest.json', f'Manifest {field} disagrees with the approved family mapping.')
    loaded={}
    typed_registry = load_typed_registry(include_references=True)
    package_case_id = None
    package_snapshot = None
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
                        leak_paths=[]
                        for key, value in row.items():
                            candidate=value
                            if key.endswith('_json') and value:
                                try: candidate=json.loads(value)
                                except json.JSONDecodeError: candidate=value
                            leak_paths.extend(truth_leak_paths(candidate, key))
                        if leak_paths: err('SAFE.TRUTH.LEAK',rel,'Protected truth detected at safe field path(s): ' + ','.join(leak_paths[:5])); break
                    typed = {column["name"]: column for column in typed_registry[rel]["columns"]}
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
                primary_key = tuple(typed_registry[rel].get('primary_key', []))
                if primary_key:
                    seen = set()
                    for row_number, row in enumerate(loaded[rel], start=2):
                        key = tuple(row.get(column, '') for column in primary_key)
                        if any(value == '' for value in key):
                            err('CANONICAL.PRIMARY_KEY.NULL', rel, f'Primary key is incomplete at CSV row {row_number}.')
                        elif key in seen:
                            err('CANONICAL.PRIMARY_KEY.DUPLICATE', rel, f'Duplicate primary key at CSV row {row_number}.')
                        seen.add(key)
        except (UnicodeError,csv.Error): err('CANONICAL.CSV',rel,'Invalid UTF-8 CSV.')
    for p in root.rglob('*.csv'):
        rel=str(p.relative_to(root)).replace('\\','/')
        if rel not in TABLE_PATHS: err('PKG.FILE.EXTRA',rel,'Unexpected canonical CSV.')
    for source_path, definition in typed_registry.items():
        for rule in definition.get('references', []):
            source_rows = loaded.get(source_path, [])
            target_values = {(row.get('case_id', ''), row.get(rule['target_column'], '')) for row in loaded.get(rule['to'], [])}
            for row_number, row in enumerate(source_rows, start=2):
                value = row.get(rule['column'], '')
                if value and (row.get('case_id', ''), value) not in target_values:
                    err('CANONICAL.REFERENCE', source_path, f"{rule['column']} at CSV row {row_number} has no matching {rule['to']}.{rule['target_column']}.")
    manifest_files=manifest.get('files', [])
    if not isinstance(manifest_files, list):
        err('PKG.RECEIPT.INVENTORY','manifest.json','Manifest files must be an array of receipts.')
        manifest_files=[]
    if len(manifest_files) != len(TABLE_PATHS):
        err('PKG.RECEIPT.COUNT','manifest.json','Manifest must contain exactly one receipt for each canonical table.')
    if any(not isinstance(item, dict) for item in manifest_files):
        err('PKG.RECEIPT.SHAPE','manifest.json','Every manifest file receipt must be an object.')
    receipts={x.get('path'):x for x in manifest_files if isinstance(x, dict) and isinstance(x.get('path'), str)}
    if len(receipts) != len(manifest_files):
        err('PKG.RECEIPT.DUPLICATE','manifest.json','Manifest file receipt paths must be unique and non-empty.')
    if set(receipts) != set(TABLE_PATHS): err('PKG.RECEIPT.INVENTORY','manifest.json','Manifest receipts must cover exactly the 32 canonical paths.')
    for rel in TABLE_PATHS:
        p=root/rel
        if p.is_file() and rel in receipts:
            data=p.read_bytes()
            digest=hashlib.sha256(data).hexdigest()
            receipt=receipts[rel]
            if not isinstance(receipt.get('bytes'), int) or receipt.get('bytes') < 0:
                err('PKG.RECEIPT.BYTES.TYPE', rel, 'Manifest byte receipt must be a non-negative integer.')
            if not isinstance(receipt.get('rows'), int) or receipt.get('rows') < 0:
                err('PKG.RECEIPT.ROWS.TYPE', rel, 'Manifest row receipt must be a non-negative integer.')
            if not isinstance(receipt.get('sha256'), str) or len(receipt.get('sha256', '')) != 64:
                err('PKG.RECEIPT.SHA256.TYPE', rel, 'Manifest SHA-256 receipt must be a 64-character string.')
            if receipt.get('sha256') != digest: err('PKG.RECEIPT.SHA256',rel,'Manifest digest does not match bytes.')
            if receipt.get('bytes') != len(data): err('PKG.RECEIPT.BYTES',rel,'Manifest byte count does not match bytes.')
            with p.open(newline='', encoding='utf-8') as stream:
                row_count=max(0, sum(1 for _ in csv.DictReader(stream)))
            if receipt.get('rows') != row_count: err('PKG.RECEIPT.ROWS',rel,'Manifest row count does not match parsed CSV rows.')
    try:
        case_rows = loaded.get('config/cases.csv', [])
        profile_rows = loaded.get('config/case_profiles.csv', [])
        if case_rows:
            package_case_id = case_rows[0].get('case_id')
            package_snapshot = case_rows[0].get('snapshot_version')
        for rel, rows in loaded.items():
            for row in rows:
                if package_case_id and row.get('case_id') not in (None, '', package_case_id):
                    err('PKG.CASE_ID.CONSISTENCY', rel, 'Row case_id disagrees with config/cases.csv.')
                if package_snapshot and row.get('snapshot_version') not in (None, '', package_snapshot):
                    err('PKG.SNAPSHOT.CONSISTENCY', rel, 'Row snapshot_version disagrees with config/cases.csv.')
        if case_rows:
            require_controlled(case_rows[0].get('path_code', ''), FAMILIES, 'path_code')
            manifest_family = manifest.get('family')
            if manifest_family and manifest_family != case_rows[0].get('path_code'):
                err('PKG.FAMILY', 'manifest.json', 'Manifest family disagrees with config/cases.csv.')
            for field in ('case_id', 'case_version', 'snapshot_version'):
                if manifest.get(field) != case_rows[0].get(field):
                    err('PKG.IDENTITY', 'manifest.json', f'Manifest {field} disagrees with config/cases.csv.')
        if len(profile_rows) != 1:
            err('PKG.PROFILE.COUNT', 'config/case_profiles.csv', 'Canonical package must contain exactly one profile row.')
        for row in profile_rows:
            require_controlled(row.get('profile_code', ''), FAMILIES, 'profile_code')
            if row.get('cumulative', '').strip().lower() != 'false':
                err('PKG.PROFILE.CUMULATIVE', 'config/case_profiles.csv', 'Canonical package profile must declare cumulative=false.')
        for row in loaded.get('authoring/relationships.csv', []): require_controlled(row.get('relationship_family', ''), RELATIONSHIP_FAMILIES, 'relationship_family')
        for row in loaded.get('authoring/records.csv', []):
            try: provenance_from_row(row)
            except ValueError as exc: err('CANONICAL.PROVENANCE', 'authoring/records.csv', str(exc))
        for row in loaded.get('analytics/entity_resolution_candidates.csv', []): require_controlled(row.get('confidence_band', ''), CONFIDENCE_BANDS, 'confidence_band'); require_controlled(row.get('generation_mode', ''), GENERATION_MODES, 'generation_mode')
    except ValueError as exc: err('CANONICAL.CONTROLLED_VALUE', 'package', str(exc))
    return errors
