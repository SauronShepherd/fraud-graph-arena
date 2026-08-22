# FGA06 prior-iteration gap ledger

This ledger records the predecessor status visible in the current checkout. It does not rewrite historical reports and does not claim Databricks qualification.

| Iteration | Classification | Evidence observed | FGA06 disposition |
|---|---|---|---|
| FGA00 | COMPLETE_AND_CLOSED / VERIFY_IN_REAL_GIT | `reports/iteration-00/README.md`; tag ancestry still requires real-git verification | Regression only |
| FGA01 | IMPLEMENTED_EVIDENCE_STALE | `reports/iteration-01/gate.json` conflicts with README qualification prose | Reconcile with current evidence; preserve ACADEMY_001 |
| FGA02 | IMPLEMENTED_EVIDENCE_STALE + PARTIAL_RUNTIME | board evidence and runtime geometry claims require current reconciliation | Reconcile before formal closure |
| FGA03 | VERIFY_IN_REAL_GIT | source and gate artifacts exist; ZIP-style evidence cannot prove tag lineage | Verify lineage; do not reopen scope casually |
| FGA04 | COMPLETE_SCOPED | canonical contract and truth-firewall source/tests are present | Preserve as renderer input boundary |
| FGA05 | CLOSURE_BLOCKER | current reports identify live Databricks qualification/closure work | Not executed per user instruction; formal FGA06 closure remains blocked |

Deferred by design (not FGA06 defects): analytics execution, identity-candidate reveal, exact-match reveal, credits, accusation, bounded expansion, filtering, focus mode, and advanced graph accessibility.

## Local evidence policy

Only static inspection, Python compilation, schema/JSON parsing, and frontend type checking may be used in this task. Tests and Databricks commands are intentionally not run.
