from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from fraud_graph_arena.case_data.registry import TABLE_PATHS
def digest(root: Path):
    packages={}
    for package in sorted(x for x in root.iterdir() if x.is_dir()):
        h=hashlib.sha256()
        for table in TABLE_PATHS:
            data=(package/table).read_bytes(); h.update(table.encode()); h.update(b'\0'); h.update(hashlib.sha256(data).digest())
        packages[package.name]=h.hexdigest()
    return packages
p=argparse.ArgumentParser(); p.add_argument('root'); p.add_argument('--report',required=True); a=p.parse_args()
first=digest(Path(a.root)); second=digest(Path(a.root)); out={'valid':first==second,'package_count':len(first),'digests':first,'repeat_digests':second}
Path(a.report).parent.mkdir(parents=True,exist_ok=True); Path(a.report).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({'valid':out['valid'],'package_count':out['package_count']})); raise SystemExit(0 if out['valid'] else 1)
