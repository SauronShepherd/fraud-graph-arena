from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.models import ImportStatus

TERMINAL={status.value for status in (ImportStatus.PUBLISHED,ImportStatus.REUSED,ImportStatus.FAILED,ImportStatus.FAILED_CLEANUP)}

def reconcile(state: dict) -> dict:
    runs=state.get("runs", [])
    if isinstance(runs, dict): runs=list(runs.values())
    reconciled=[]
    for run in runs:
        if run.get("status") not in TERMINAL:
            run["status"]="FAILED"; run["error_code"]="PROCESS_RESTART_RECONCILED"; run["error_summary"]="run was incomplete at reconciliation"; reconciled.append(run.get("run_id"))
    state["runs"]=runs; state["reconciled_run_ids"]=[item for item in reconciled if item is not None]; state["reconciled"]=True
    return state

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--state",required=True,type=Path); p.add_argument("--output",type=Path); args=p.parse_args()
    state=json.loads(args.state.read_text(encoding="utf-8")); result=reconcile(state); rendered=json.dumps(result,indent=2)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(rendered,encoding="utf-8")
    else: print(rendered,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
