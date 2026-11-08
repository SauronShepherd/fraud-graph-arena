# FGA06 prior-iteration gap ledger

This ledger records the predecessor status visible in the current checkout. It does not rewrite historical reports. Current `FGA-06` evidence is kept separate from the historical predecessor closure records.

| Iteration | Classification | Evidence observed | FGA06 disposition |
|---|---|---|---|
| FGA00 | COMPLETE_AND_CLOSED / VERIFY_IN_REAL_GIT | `reports/iteration-00/README.md`; tag ancestry still requires real-git verification | Regression only |
| FGA01 | IMPLEMENTED_EVIDENCE_STALE | `reports/iteration-01/gate.json` conflicts with README qualification prose | Reconcile with current evidence; preserve ACADEMY_001 |
| FGA02 | IMPLEMENTED_EVIDENCE_STALE + PARTIAL_RUNTIME | board evidence and runtime geometry claims require current reconciliation | Reconcile before formal closure |
| FGA03 | VERIFY_IN_REAL_GIT | source and gate artifacts exist; ZIP-style evidence cannot prove tag lineage | Verify lineage; do not reopen scope casually |
| FGA04 | COMPLETE_SCOPED | canonical contract and truth-firewall source/tests are present | Preserve as renderer input boundary |
| FGA05 | CLOSURE_BLOCKER | historical formal predecessor release closure is still not reconstructed from one frozen release candidate | FGA06 now has current live `fga` sandbox evidence: 13 packages, 44 objects, 32 active tables and an idempotent rerun; this does not rewrite the predecessor's historical formal closure requirement |

Deferred by design (not FGA06 defects): analytics execution, identity-candidate reveal, exact-match reveal, credits, accusation, bounded expansion, filtering, focus mode, and advanced graph accessibility.

## Current evidence policy

Local compilation, schema/JSON parsing, browser comparison and live Databricks evidence are kept separate. `reports/iteration-06/databricks-qualification-current.json` is historical/stale evidence for the old `sda_dev` workspace; the current `fga` evidence is named explicitly in `reports/iteration-06/qualification-status.json`. A raw renderer timing report is not a qualification decision, and a live sandbox pass does not rewrite a predecessor's immutable closure record.
