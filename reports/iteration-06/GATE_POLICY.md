# FGA06 local gate policy

`scripts/run_iteration_06_local_gate.py` is intentionally narrower than the formal release gate. It checks only local source-coherent invariants and never imports or invokes Databricks qualification scripts, pytest, Vitest, or Playwright.

The formal release gate remains unavailable until predecessor FGA05 live closure, candidate renderer qualification, benchmark evidence, and the plan's required clean candidate/evidence lineage exist.
