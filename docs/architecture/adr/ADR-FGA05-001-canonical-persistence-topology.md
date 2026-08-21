# ADR-FGA05-001 — Canonical persistence topology

FGA 05 uses one closed physical target per Canonical Model v1 path and five operational tables. Cases and snapshots are row identity, not table names. The reference implementation is adapter-driven and its in-memory adapter is the qualification baseline; a Databricks adapter is required for live Unity Catalog qualification.
