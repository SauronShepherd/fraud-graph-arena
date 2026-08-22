from __future__ import annotations
import argparse, json
from pathlib import Path
from fraud_graph_arena.canonical_persistence.models import ImportStatus

TERMINAL={status.value for status in (ImportStatus.PUBLISHED,ImportStatus.REUSED,ImportStatus.FAILED,ImportStatus.FAILED_CLEANUP)}

def classify(run: dict, state: dict) -> str:
    if run.get("status") in {"PUBLISHED", "REUSED"}:
        return "already-successful"
    if run.get("publication_id") and run.get("publication_id") == state.get("active_publication_id"):
        return "already-successful-response-lost"
    if run.get("status") in {"REJECTED", "FAILED_CLEANUP"} or run.get("candidate_rows"):
        return "cleanup-required-rejected-candidate"
    if run.get("status") in {"STARTED", "PREFLIGHTED", "STAGING", "STAGED", "VALIDATING", "VALIDATED", "PUBLISHING"}:
        return "recoverable-retry"
    return "manual-review-ambiguous"

def actions_for(run: dict, state: dict) -> list[str]:
    classification = classify(run, state)
    if classification == "already-successful-response-lost":
        return ["reconcile_run_to_published", "verify_pointer_and_publication"]
    if classification == "cleanup-required-rejected-candidate":
        return ["cleanup_candidate_by_publication_id", "mark_failed_cleanup_if_cleanup_fails", "block_candidate_reuse_until_clean"]
    if classification == "recoverable-retry":
        return ["mark_abandoned_before_activation_failed", "preserve_active_pointer", "allow_retry_after_cleanup"]
    return ["operator_review"]

def reconcile(state: dict) -> dict:
    runs=state.get("runs", [])
    if isinstance(runs, dict): runs=list(runs.values())
    reconciled=[]
    for run in runs:
        run["reconciliation_classification"] = classify(run, state)
        run["reconciliation_actions"] = actions_for(run, state)
        if run.get("status") not in TERMINAL:
            if run["reconciliation_classification"] == "already-successful-response-lost":
                run["status"] = "PUBLISHED"
            else:
                run["status"]="FAILED"; run["error_code"]="PROCESS_RESTART_RECONCILED"; run["error_summary"]="run was incomplete at reconciliation"; reconciled.append(run.get("run_id"))
    state["runs"]=runs; state["reconciled_run_ids"]=[item for item in reconciled if item is not None]; state["reconciled"]=True
    return state

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--state",required=True,type=Path); p.add_argument("--output",type=Path); p.add_argument("--list",action="store_true"); p.add_argument("--run-id"); p.add_argument("--dry-run",action="store_true"); p.add_argument("--repair",action="store_true"); p.add_argument("--confirm"); args=p.parse_args()
    state=json.loads(args.state.read_text(encoding="utf-8"))
    if args.run_id:
        runs = state.get("runs", []); runs = list(runs.values()) if isinstance(runs, dict) else runs
        state["runs"] = [run for run in runs if run.get("run_id") == args.run_id]
    if args.list or args.dry_run:
        runs = state.get("runs", []); runs = list(runs.values()) if isinstance(runs, dict) else runs
        for run in runs:
            run["reconciliation_classification"] = classify(run, state)
            run["reconciliation_actions"] = actions_for(run, state)
        state["reconciled_run_ids"] = []
    elif args.repair:
        if args.confirm != "REPAIR": raise SystemExit("refusing repair: pass --confirm REPAIR")
        state = reconcile(state)
    else:
        state = reconcile(state)
    rendered=json.dumps(state,indent=2)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(rendered,encoding="utf-8")
    else: print(rendered,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
