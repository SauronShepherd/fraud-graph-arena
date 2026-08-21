from pathlib import Path
import argparse,json,sys
from fraud_graph_arena.case_data.validator import validate_package
p=argparse.ArgumentParser(); p.add_argument('root'); p.add_argument('--report',required=True); a=p.parse_args()
packages=sorted(x for x in Path(a.root).iterdir() if x.is_dir()); results=[{'package':x.name,'errors':validate_package(x)} for x in packages]
out={'valid':all(not x['errors'] for x in results),'package_count':len(results),'results':results}; Path(a.report).parent.mkdir(parents=True,exist_ok=True); Path(a.report).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,sort_keys=True)); sys.exit(0 if out['valid'] else 1)
