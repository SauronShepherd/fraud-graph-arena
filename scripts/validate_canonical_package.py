from pathlib import Path
import argparse, json, sys
from fraud_graph_arena.case_data.validator import validate_package
p=argparse.ArgumentParser(); p.add_argument('package'); p.add_argument('--report'); a=p.parse_args()
e=validate_package(Path(a.package)); out={'valid':not e,'errors':e}
if a.report: Path(a.report).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,sort_keys=True)); sys.exit(bool(e))
