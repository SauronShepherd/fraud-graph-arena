from pathlib import Path
import argparse,json
from fraud_graph_arena.case_data.registry import TABLE_PATHS,headers
import csv, hashlib
p=argparse.ArgumentParser(); p.add_argument('root'); p.add_argument('--report'); a=p.parse_args()
packages=[x for x in Path(a.root).iterdir() if x.is_dir()]
digests={}; errors=[]
for table in TABLE_PATHS:
    values=[]
    for package in packages:
        with (package/table).open(newline='',encoding='utf-8-sig') as f: actual=next(csv.reader(f))
        values.append(hashlib.sha256(('\x1f'.join(actual)).encode()).hexdigest())
    digests[table]=values[0] if values else hashlib.sha256(('\x1f'.join(headers(table))).encode()).hexdigest()
    if any(x != values[0] for x in values): errors.append(table)
out={'valid':not errors,'packages':len(packages),'tables':len(TABLE_PATHS),'header_digests':digests,'errors':errors}
if a.report: Path(a.report).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,sort_keys=True))
