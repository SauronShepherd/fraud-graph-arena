# FGA-09 compatibility decision

## Decision

For the bounded FGA-09 branch and article slice, use the named deterministic
runtime fallback while the Databricks `fga` profile remains
`UNRESOLVED_SQL_WAREHOUSE_ONLY` for Zingg compatibility.

## Authority and boundary

This is the implementation decision authorized by the current FGA-09 task:
deliver the player-safe identity-resolution slice, run the available read-only
qualification, and document the missing Zingg runtime instead of fabricating a
successful job. It is not approval to call the fallback a Zingg execution, not
approval for production model quality, and not approval to close the future
Spark/Zingg compatibility gate.

## Consequences

- `RUNTIME_DETERMINISTIC_FALLBACK` is a visible generation mode.
- `actual_engine_run=false` remains a hard claim in code, UI and receipts.
- The live publication is qualified read-only; no package, cluster or table is
  mutated by this decision.
- A future Zingg delivery still requires a qualified Spark runtime, artifact and
  library path, plus a new compatibility receipt and regression evidence.
