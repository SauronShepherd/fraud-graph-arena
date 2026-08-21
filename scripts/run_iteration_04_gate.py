from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from fraud_graph_arena.case_data.registry import TABLE_PATHS
from fraud_graph_arena.case_data.validator import validate_package

ROOT=Path(__file__).resolve().parents[1]
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--report',required=True); p.add_argument('--packages-root',default='case-data/canonical/v1'); a=p.parse_args()
    root=ROOT/ a.packages_root; packages=sorted(x for x in root.iterdir() if x.is_dir()) if root.is_dir() else []
    families={}
    for x in packages:
        try:
            m=json.loads((x/'manifest.json').read_text(encoding='utf-8'))
            family=m.get('family') or m.get('profile_code') or {'T':'ACADEMY','P':'PUPPY','A':'ADULT','S':'SENIOR'}.get(x.name[:1])
            families[family]=families.get(family,0)+1
        except Exception: pass
    contract=subprocess.run([sys.executable,str(ROOT/'scripts/validate_canonical_contract.py')],cwd=ROOT,text=True,capture_output=True)
    corpus_ok=len(packages)==13 and families=={'ACADEMY':3,'PUPPY':3,'ADULT':4,'SENIOR':3}
    validation=[{'package':x.name,'errors':validate_package(x)} for x in packages]
    packages_valid=all(not item['errors'] for item in validation)
    out={'iteration':'FGA04','canonical_model_version':'1.0.0','table_count':len(TABLE_PATHS),'package_count':len(packages),'family_counts':families,'contract_valid':contract.returncode==0,'corpus_complete':corpus_ok,'packages_valid':packages_valid,'validation':validation,'fully_qualified':contract.returncode==0 and corpus_ok and packages_valid,'blockers':([] if corpus_ok and packages_valid else (['approved 13-package corpus is not present'] if not corpus_ok else ['one or more packages failed strict validation']))}
    path=ROOT/a.report; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,sort_keys=True)); return 0 if out['fully_qualified'] else 1
if __name__=='__main__': raise SystemExit(main())
