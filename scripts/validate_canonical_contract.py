from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from fraud_graph_arena.case_data.registry import TABLE_PATHS, load_registry
def main():
    model=json.loads((ROOT/'contracts/canonical/v1/canonical-model.json').read_text(encoding='utf-8'))
    assert model['version']=='1.0.0' and len(TABLE_PATHS)==32 and len(set(TABLE_PATHS))==32
    assert all(p.endswith('.csv') and '/' in p and not any(x in p for x in ('<','{','}')) for p in TABLE_PATHS)
    registry=json.loads((ROOT/'contracts/canonical/v1/schema-registry.json').read_text(encoding='utf-8'))
    assert set(x['path'] for x in registry['tables']).issubset(set(TABLE_PATHS))
    assert all(load_registry()[p] for p in TABLE_PATHS)
    print(json.dumps({'valid':True,'model_version':model['version'],'table_count':len(TABLE_PATHS)},sort_keys=True))
if __name__=='__main__':
    try: main()
    except (AssertionError, OSError, ValueError, KeyError) as e: print(f'canonical contract invalid: {e}', file=sys.stderr); raise SystemExit(1)
