# ADR-FGA05-004 — Destructive namespace policy

Status: accepted

FGA qualification destruction is limited to the exact tuple in
`config/lakehouse/destructive-environments.v1.json`. The approved destructive
unit is the owned-object set inside the schema: unexpected objects are dropped,
owned objects are recreated from source-controlled DDL, and production is not
present in the allowlist. Execution requires both `--apply` and the exact
environment/catalog/schema confirmation token. A tuple mismatch is rejected
before the first warehouse statement.
