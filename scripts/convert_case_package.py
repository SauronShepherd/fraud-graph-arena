from pathlib import Path
import argparse, json
from fraud_graph_arena.case_data.converters import registry
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--case-id',required=True); p.add_argument('--family',required=True); a=p.parse_args()
converter_id = {"ACADEMY": "academy.csv.v1", "PUPPY": "puppy.csv.v1", "ADULT": "adult.csv.v1", "SENIOR": "senior.csv.v1"}.get(a.family.upper())
if converter_id is None:
    raise SystemExit(f"unsupported family: {a.family}")
registry.resolve(converter_id).convert(Path(a.input), Path(a.output), {"case_id": a.case_id})
print(json.dumps({"converter": converter_id, "case_id": a.case_id, "family": a.family}, sort_keys=True))
