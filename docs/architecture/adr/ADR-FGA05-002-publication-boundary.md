# ADR-FGA05-002 — Publication boundary

Imports write an invisible candidate tagged with a deterministic publication identity. The candidate is validated before the case-scoped active pointer changes. Exact retries reuse the active publication; changed bytes for the same immutable identity fail.
