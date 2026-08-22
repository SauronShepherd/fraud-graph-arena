# ADR-0001: graph renderer qualification

Status: `BLOCKED_PENDING_LOCAL_QUALIFICATION`

The plan names Cytoscape.js as the normative incumbent but requires an honest comparison. No winner is declared until the frozen requirements, fixture, versions, license evidence, lifecycle evidence, and benchmark results exist. Databricks qualification is outside this local-only task and remains a predecessor closure blocker.

The production boundary is renderer-neutral: FGA graph IDs, typed records, directed relationship semantics, safe summaries, and explicit counts cross the workspace API; renderer-native objects do not.

Reopen triggers: a hard requirement failure, performance-envelope failure, incompatible license, unsupported version maturity, or a future FGA change requiring capabilities not available behind the adapter.
