from pathlib import Path
import argparse, json
from fraud_graph_arena.case_data.converters.common import convert_flat_csv
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--case-id',required=True); p.add_argument('--family',required=True); a=p.parse_args()
print(json.dumps(convert_flat_csv(Path(a.input),Path(a.output),case_id=a.case_id,family=a.family),sort_keys=True))
