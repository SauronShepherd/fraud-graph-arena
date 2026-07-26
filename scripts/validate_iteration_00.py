#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import jsonschema
    import yaml
except ModuleNotFoundError as exc:
    dependency = exc.name or "unknown"
    project_file = Path(__file__).resolve().parents[1] / "pyproject.toml"
    print(
        "Iteration-00 validator dependency is missing: " + dependency + "\n"
        "From the repository root, install the declared project and test dependencies with:\n"
        f'  "{sys.executable}" -m pip install -e ".[test]"\n'
        f"Dependency configuration: {project_file}",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / 'reports/iteration-00/validation-results.json'
EVIDENCE_PATH = ROOT / 'reports/iteration-00/evidence.json'


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical_evidence_digest(obj: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(obj))
    clone.pop('bundle_digest', None)
    payload = json.dumps(clone, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def current_commit() -> str:
    try:
        return subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return 'WORKTREE-NO-COMMIT'


def clean_checkout() -> bool:
    try:
        out = subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        return out.strip() == ''
    except Exception:
        return False


def validate_schema_instance(schema_path: Path, instance_path: Path) -> None:
    schema = read_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(read_json(instance_path))


def graph_semantic_errors(graph: dict[str, Any]) -> list[str]:
    errors=[]
    ids=[n['id'] for n in graph['nodes']]
    if len(ids) != len(set(ids)):
        errors.append('duplicate traceability node IDs')
    node_ids=set(ids)
    degree={i:0 for i in ids}
    for edge in graph['edges']:
        if edge['from'] not in node_ids: errors.append(f"missing edge source {edge['from']}")
        if edge['to'] not in node_ids: errors.append(f"missing edge target {edge['to']}")
        if edge['from'] in degree: degree[edge['from']]+=1
        if edge['to'] in degree: degree[edge['to']]+=1
    orphans=[nid for nid,d in degree.items() if d==0]
    if orphans: errors.append('orphan nodes: '+', '.join(sorted(orphans)))
    present_modules={n['id'] for n in graph['nodes'] if n['kind']=='module'}
    present_interactions={n['id'] for n in graph['nodes'] if n['kind']=='interaction'}
    expected_modules={f'M{i:02d}' for i in range(1,21)}
    expected_interactions={f'I{i:02d}' for i in range(1,20)}
    if present_modules != expected_modules: errors.append('module coverage differs from M01-M20')
    if present_interactions != expected_interactions: errors.append('interaction coverage differs from I01-I19')
    # Each task must have exactly one path and a test edge.
    task_ids={n['id'] for n in graph['nodes'] if n['kind']=='task'}
    for n in graph['nodes']:
        if n['kind']=='task' and not n.get('path'): errors.append(f"task {n['id']} has no path")
    for tid in task_ids:
        if not any(e['from']==tid and e['relationship']=='verified_by' for e in graph['edges']): errors.append(f'task {tid} has no verifying test')
    return errors


def markdown_errors() -> list[str]:
    errors=[]
    authored_roots=[ROOT/'README.md',ROOT/'docs',ROOT/'reports/iteration-00/README.md']
    files=[]
    for p in authored_roots:
        if p.is_file(): files.append(p)
        elif p.exists(): files.extend(p.rglob('*.md'))
    for path in sorted(set(files)):
        text=path.read_text(encoding='utf-8')
        rel=path.relative_to(ROOT)
        if not text.endswith('\n'): errors.append(f'{rel}: missing final newline')
        for idx,line in enumerate(text.splitlines(),1):
            if line.rstrip()!=line: errors.append(f'{rel}:{idx}: trailing whitespace')
        if not text.startswith('# '): errors.append(f'{rel}: first line is not H1')
        if text.count('```') % 2: errors.append(f'{rel}: unbalanced code fence')
        for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
            target=match.group(1).split('#',1)[0]
            if not target or re.match(r'^[a-z]+://',target) or target.startswith('mailto:'):
                continue
            resolved=(path.parent/target).resolve()
            try: resolved.relative_to(ROOT.resolve())
            except ValueError: errors.append(f'{rel}: link escapes repository: {target}'); continue
            if not resolved.exists(): errors.append(f'{rel}: broken link: {target}')
    return errors


def owner_errors() -> list[str]:
    data=yaml.safe_load((ROOT/'config/governance/owners.yaml').read_text())
    teams=set(data['teams'])
    assignments=data['assignments']
    errors=[]
    for a in assignments:
        if a['owner'] not in teams or a['reviewer'] not in teams: errors.append(f"unknown team in {a['path']}")
        if a['owner']==a['reviewer']: errors.append(f"owner equals reviewer in {a['path']}")
    governed=[]
    for base in ['README.md','.gitignore','pyproject.toml','docs','config','schemas','reports','scripts','tests','specifications']:
        p=ROOT/base
        if p.is_file(): governed.append(p)
        elif p.exists(): governed.extend(x for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts)
    def matches(pattern:str, rel:str)->bool:
        if pattern.endswith('/**'):
            return rel.startswith(pattern[:-3].rstrip('/')+'/')
        return fnmatch.fnmatch(rel,pattern)
    for path in governed:
        rel=path.relative_to(ROOT).as_posix()
        matched=[a for a in assignments if matches(a['path'],rel)]
        if not matched: errors.append(f'unowned path: {rel}')
    return errors


def id_errors() -> list[str]:
    errors=[]
    baseline=read_json(ROOT/'config/governance/baseline.json')
    artifact_ids=[a['artifact_id'] for a in baseline['artifacts']]
    if len(artifact_ids)!=len(set(artifact_ids)): errors.append('duplicate artifact IDs')
    graph=read_json(ROOT/'config/governance/traceability.json')
    patterns={
      'module':r'^M(?:0[1-9]|1[0-9]|20)$','interaction':r'^I(?:0[1-9]|1[0-9])$',
      'requirement':r'^REQ-[A-Z0-9]+-[A-Z0-9-]+-[0-9]{3}$','stage':r'^I[0-9]{2}-S[0-9]{2}$',
      'task':r'^I[0-9]{2}-S[0-9]{2}-T[0-9]{2}$','test':r'^TEST-[A-Z0-9-]+$',
      'evidence':r'^EVID-I[0-9]{2}-[A-Z0-9-]+$'
    }
    for n in graph['nodes']:
        pat=patterns.get(n['kind'])
        if pat and not re.match(pat,n['id']): errors.append(f"malformed {n['kind']} ID {n['id']}")
    policy=yaml.safe_load((ROOT/'config/governance/iteration-policy.yaml').read_text())
    gate_ids=[g['id'] for g in policy['gates']]
    if gate_ids != [f'G{i:02d}' for i in range(1,16)]: errors.append('gate IDs are not exactly G01-G15 in order')
    if policy.get('principle')!='no-pass-no-progress': errors.append('no-pass-no-progress principle missing')
    for ref_name, ref_path in policy.get('references', {}).items():
        if not (ROOT/ref_path).is_file(): errors.append(f'missing iteration-policy reference {ref_name}: {ref_path}')
    if not policy['skips_and_quarantine']['critical_skip_forbidden'] or not policy['skips_and_quarantine']['critical_quarantine_forbidden']:
        errors.append('critical skip/quarantine prohibition missing')
    return errors


def scan_errors() -> tuple[list[str],list[str]]:
    secret_errors=[]; truth_errors=[]
    excluded_prefixes=('specifications/', '.git/')
    secret_patterns=[
      re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
      re.compile(r'(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*["\'][A-Za-z0-9_\-]{16,}["\']'),
      re.compile(r'AKIA[0-9A-Z]{16}')
    ]
    truth_names={'truth.json','answer-key.json','answer_key.json','protected-truth.json'}
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts: continue
        rel=path.relative_to(ROOT).as_posix()
        if rel.startswith(excluded_prefixes): continue
        if path.name.lower() in truth_names: truth_errors.append(f'protected truth artifact outside specifications: {rel}')
        if path.suffix.lower() not in {'.md','.json','.yaml','.yml','.py','.txt','.toml'}: continue
        text=path.read_text(encoding='utf-8',errors='ignore')
        for pat in secret_patterns:
            if pat.search(text): secret_errors.append(f'possible secret in {rel}: {pat.pattern}')
    return secret_errors,truth_errors


def baseline_errors() -> tuple[list[str], list[str]]:
    errors=[]; blockers=[]
    baseline=read_json(ROOT/'config/governance/baseline.json')
    validate_schema_instance(ROOT/'schemas/governance/baseline.schema.json',ROOT/'config/governance/baseline.json')
    for a in baseline['artifacts']:
        if a['availability']=='available':
            path=ROOT/a['path']
            if not path.is_file(): errors.append(f"artifact path missing: {a['artifact_id']} -> {a['path']}")
            elif sha256(path)!=a['sha256']: errors.append(f"digest mismatch: {a['artifact_id']}")
        elif a['availability']=='external_missing' and a['required_for_closure']:
            blockers.append(a['artifact_id'])
    if baseline['closure_requirements']['unresolved_required_artifact_ids'] != blockers:
        errors.append('closure unresolved artifact list does not match registry')
    if baseline['closure_requirements']['all_required_available'] != (not blockers):
        errors.append('all_required_available is inconsistent')
    return errors,blockers


def schema_fixture_errors() -> list[str]:
    errors=[]
    schemas={
      'baseline':ROOT/'schemas/governance/baseline.schema.json',
      'traceability':ROOT/'schemas/governance/traceability.schema.json',
      'evidence':ROOT/'schemas/testing/iteration-evidence.schema.json'
    }
    positives={'baseline':ROOT/'tests/fixtures/governance/baseline.valid.json','traceability':ROOT/'tests/fixtures/governance/traceability.valid.json','evidence':ROOT/'tests/fixtures/governance/evidence.valid.json'}
    negatives={'baseline':ROOT/'tests/fixtures/governance/baseline.invalid.json','evidence':ROOT/'tests/fixtures/governance/evidence.invalid.json'}
    for name,schema_path in schemas.items():
        schema=read_json(schema_path)
        try: jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as e: errors.append(f'{name} schema invalid: {e}')
        try: jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(read_json(positives[name]))
        except Exception as e: errors.append(f'{name} positive fixture failed: {e}')
    for name,path in negatives.items():
        schema=read_json(schemas[name])
        try:
            jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(read_json(path))
            errors.append(f'{name} negative fixture unexpectedly passed')
        except jsonschema.ValidationError:
            pass
    orphan=read_json(ROOT/'tests/fixtures/governance/traceability.orphan.json')
    try:
        jsonschema.Draft202012Validator(read_json(schemas['traceability'])).validate(orphan)
    except Exception as e:
        errors.append(f'traceability orphan fixture should be structurally valid: {e}')
    if not graph_semantic_errors(orphan): errors.append('traceability orphan fixture unexpectedly passed semantic validation')
    return errors


def dependency_manifest_errors() -> list[str]:
    errors=[]
    path=ROOT/'pyproject.toml'
    if not path.is_file():
        return ['pyproject.toml is missing']
    try:
        data=tomllib.loads(path.read_text(encoding='utf-8'))
    except tomllib.TOMLDecodeError as exc:
        return [f'pyproject.toml is invalid: {exc}']

    project=data.get('project', {})
    runtime_entries=project.get('dependencies', [])
    test_entries=project.get('optional-dependencies', {}).get('test', [])

    def normalized_exact(entries: list[str], group: str) -> dict[str,str]:
        declared={}
        for entry in entries:
            if not isinstance(entry, str):
                errors.append(f'{group} dependency entry is not a string: {entry!r}')
                continue
            name, separator, version=entry.partition('==')
            normalized=re.sub(r'[-_.]+','-',name.strip()).lower()
            if not separator or not normalized or not version.strip() or any(op in version for op in '<>!=~'):
                errors.append(f'{group} dependency must be exactly pinned: {entry}')
                continue
            declared[normalized]=entry
        return declared

    runtime=normalized_exact(runtime_entries, 'runtime')
    tests=normalized_exact(test_entries, 'test')
    for dependency in sorted({'jsonschema','pyyaml'}-set(runtime)):
        errors.append(f'undeclared runtime dependency: {dependency}')
    if 'pytest' not in tests:
        errors.append('undeclared test dependency: pytest')

    pytest_config=data.get('tool', {}).get('pytest', {}).get('ini_options', {})
    if pytest_config.get('testpaths') != ['tests']:
        errors.append('pytest testpaths must be exactly ["tests"]')
    if pytest_config.get('python_files') != ['test_*.py']:
        errors.append('pytest python_files must be exactly ["test_*.py"]')
    addopts=pytest_config.get('addopts', [])
    if '--strict-config' not in addopts or '--strict-markers' not in addopts:
        errors.append('pytest strict configuration and marker validation must be enabled')
    return errors


def evidence_errors() -> list[str]:
    errors=[]
    try: validate_schema_instance(ROOT/'schemas/testing/iteration-evidence.schema.json',EVIDENCE_PATH)
    except Exception as e: errors.append(f'evidence schema validation: {e}')
    obj=read_json(EVIDENCE_PATH)
    if obj.get('bundle_digest') != canonical_evidence_digest(obj): errors.append('evidence bundle digest mismatch')
    gate_ids=[g['gate_id'] for g in obj.get('gates',[])]
    if gate_ids != [f'G{i:02d}' for i in range(1,16)]: errors.append('evidence gates are not exactly G01-G15')
    if any(t['status']=='fail' for t in obj.get('tests',[])) and obj.get('status')=='passing': errors.append('passing evidence contains failed test')
    if any(e.get('critical') for e in obj.get('exceptions',[])): errors.append('critical exception is forbidden')
    return errors


def update_evidence(report: dict[str,Any], blockers:list[str]) -> None:
    obj=read_json(EVIDENCE_PATH)
    obj['generated_at']=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    obj['source_commit']=current_commit()
    obj['environment']['os']=platform.platform()
    obj['environment']['python']=platform.python_version()
    obj['environment']['clean_checkout']=bool(report['clean_checkout_observed'])
    durations={r['id']:r['duration_ms'] for r in report['checks']}
    test_map={
      'TEST-I00-DEPENDENCIES':'dependencies','TEST-I00-SCHEMAS':'schemas','TEST-I00-DIGESTS':'baseline','TEST-I00-MARKDOWN':'markdown','TEST-I00-IDS':'ids','TEST-I00-OWNERS':'owners','TEST-I00-TRACEABILITY':'traceability','TEST-I00-SECRET-SCAN':'secret_scan','TEST-I00-TRUTH-SCAN':'truth_scan'
    }
    for t in obj['tests']:
        if t['test_id'] in test_map:
            check=next(r for r in report['checks'] if r['id']==test_map[t['test_id']])
            t['duration_ms']=check['duration_ms']
            t['status']='pass' if check['status']=='pass' else 'fail'
        elif t['test_id']=='TEST-I00-CLOSURE':
            t['status']='blocked' if blockers else 'pass'
            t['result']=('Expected governance block: '+', '.join(blockers)+' unavailable.') if blockers else 'All closure prerequisites are available.'
    has_fail=any(c['status']=='fail' for c in report['checks'])
    if has_fail:
        obj['status']='failing'; obj['closure_eligible']=False
    elif blockers:
        obj['status']='blocked'; obj['closure_eligible']=False
    else:
        obj['status']='passing'; obj['closure_eligible']=True
        for g in obj['gates']:
            if g['gate_id'] in {'G01','G15'}: g['status']='pass'; g['rationale']='All I00 governance prerequisites and validation checks pass.'
        obj['known_gaps']=[g for g in obj['known_gaps'] if not g.get('blocks_closure')]
    obj['bundle_digest']=canonical_evidence_digest(obj)
    EVIDENCE_PATH.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def run_check(check_id, fn):
    start=time.perf_counter()
    try:
        result=fn()
        if isinstance(result,tuple): errors=result[0]
        else: errors=result
        status='pass' if not errors else 'fail'
    except Exception as e:
        errors=[f'{type(e).__name__}: {e}']; status='fail'
    return {'id':check_id,'status':status,'duration_ms':round((time.perf_counter()-start)*1000),'errors':errors}


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-closure',action='store_true')
    parser.add_argument('--no-update-evidence',action='store_true')
    parser.add_argument('--no-write-report',action='store_true')
    args=parser.parse_args()

    checks=[]
    checks.append(run_check('dependencies',dependency_manifest_errors))
    checks.append(run_check('schemas',schema_fixture_errors))
    baseline_blockers=[]
    def baseline_check():
        nonlocal baseline_blockers
        errors,baseline_blockers=baseline_errors(); return errors
    checks.append(run_check('baseline',baseline_check))
    checks.append(run_check('markdown',markdown_errors))
    checks.append(run_check('ids',id_errors))
    checks.append(run_check('owners',owner_errors))
    checks.append(run_check('traceability',lambda: graph_semantic_errors(read_json(ROOT/'config/governance/traceability.json'))))
    scan_result={'secret':[],'truth':[]}
    def secrets():
        s,t=scan_errors(); scan_result['secret']=s; scan_result['truth']=t; return s
    checks.append(run_check('secret_scan',secrets))
    checks.append(run_check('truth_scan',lambda: scan_result['truth'] if scan_result['truth'] else scan_errors()[1]))
    checks.append(run_check('evidence',evidence_errors))

    report={
      'report_id':'FGA-I00-VALIDATION-RESULTS-1.0-20260726',
      'generated_at':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      'repository':str(ROOT),
      'source_commit':current_commit(),
      'clean_checkout_observed':clean_checkout(),
      'checks':checks,
      'blocking_prerequisites':baseline_blockers,
      'status':'fail' if any(c['status']=='fail' for c in checks) else ('blocked' if baseline_blockers else 'pass')
    }
    if not args.no_write_report:
        RESULT_PATH.parent.mkdir(parents=True,exist_ok=True)
        RESULT_PATH.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if not args.no_update_evidence:
        update_evidence(report,baseline_blockers)
        # Validate updated evidence and refresh report if necessary.
        post=evidence_errors()
        if post:
            checks[-1]={'id':'evidence','status':'fail','duration_ms':checks[-1]['duration_ms'],'errors':post}
            report['status']='fail'
            if not args.no_write_report:
                RESULT_PATH.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checks':{c['id']:c['status'] for c in checks},'blocking_prerequisites':baseline_blockers,'report':str(RESULT_PATH.relative_to(ROOT))},indent=2))
    if report['status']=='fail': return 1
    if args.require_closure and baseline_blockers: return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())
