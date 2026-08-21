# ADR-FGA05-003 — Qualification boundary

The in-memory warehouse is the deterministic local qualification adapter. It proves lifecycle, identity, isolation, topology, and failure semantics without requiring credentials. Unity Catalog/Databricks tests are separate and must report `not_qualified` when capability or credentials are absent; local pass evidence never substitutes for live authorization or warehouse qualification.
