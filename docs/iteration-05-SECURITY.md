# FGA 05 security qualification

The local security checks verify closed-registry identifiers, rejection of unexpected datasets, redacted operational errors, and truth-safe separation inherited from the Canonical v1 validator. SQL values must be parameterized by the concrete warehouse adapter; package strings are never accepted as identifiers. The non-admin Databricks qualification is now verified in `reports/iteration-05/security/truth-access-negative.json`.

## Non-admin qualification handoff

The provisioned test identity is `angel.alvarez.pascua@gmail.com` (Databricks user ID `78190839190880`). It is active, has no groups, and has only workspace/SQL entitlements. The user must accept the workspace invitation and authenticate a local CLI profile, for example:

```text
databricks auth login --host https://dbc-66c0ff61-f366.cloud.databricks.com --profile fga-web
databricks current-user me --profile fga-web
```

Then run:

```text
python scripts/qualify_databricks_security.py --profile fga-web
```

Expected result: safe published/Genie `SELECT` succeeds and truth-table `SELECT` fails with permission denied. Tokens and secrets must remain local and must not be placed in reports or source control.
