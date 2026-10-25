# FGA-08 local evidence — 2026-10-25

## Scope and ancestry

- Branch: `FGA-08`, created from the verified FGA-07 HEAD `a2eab31d6f5f14ac4c85a67632b2f9dc4c603bd6`.
- Scope implemented: free manual hypotheses only. This is not the full M13 action/quote/settlement module.
- No external provider, Databricks, deployment, or public-site operation was performed.
- The local article remains unlisted. Its broad target architecture is distinguished from this branch's implemented slice.

## Executed checks

| Directory | Command | Result | Limits |
|---|---|---|---|
| repo root | `$env:PYTHONPATH='src'; python -m pytest tests/iteration_08 tests/iteration_06 -q` | 32 passed, 1 Starlette/httpx deprecation warning, 9.03 s | Focused I08 and I06 suites; not the full repository suite. |
| repo root | `python -m compileall -q src tests` | Exit 0 | Syntax compilation only. |
| repo root | `git diff --check` | Exit 0 | Whitespace/conflict-marker hygiene only. |
| `apps/web` | `& .\node_modules\.bin\tsc.cmd -b --pretty false` | Exit 0 | TypeScript build graph; no lint. |
| `apps/web` | `node .\node_modules\vitest\vitest.mjs run --pool=forks --no-file-parallelism --maxWorkers=1 src/board/InvestigationActions.test.tsx` | 2 passed, 96.48 s | Worker/environment startup was unusually slow; no browser E2E. |
| `apps/web` | `& .\node_modules\.bin\vite.cmd build` | Passed; 60 modules transformed | Production frontend bundle only. |
| site repo | `node tools/validate-content.mjs` | FGA-05–08 metadata/assets passed; command exits 1 on three unrelated existing WTF-draft issues | Other dirty site files were preserved. Full `npm run build` cannot pass until those pre-existing validation errors are corrected. |
| site repo | `npx astro build` | Interrupted after no output/progress in this host session | Static route generation and emitted HTML were not verified. No publication/deployment occurred. |
| workspace | local invariant script for source/body equality, unlisted slugs, hero/back images, catalog predicate and noindex source path | Passed | Static source inspection, not a rendered browser request. |

## Implemented behavior

- The command service accepts only an active Academy T02 round and three allowlisted relationship types.
- Both subject IDs must exist in the fixed player-safe published T02 projection and must differ.
- An accepted command is `MANUAL_HYPOTHESIS` / `RECORDED`, has zero charged credits, and grants no evidence visibility.
- Idempotency keys have a constrained ASCII-safe shape. Exact replay returns the original command; same-key/different-payload conflicts.
- SQLite uses a unique `(round_id, idempotency_key)` constraint and stores command history; memory and SQLite adapters have duplicate/race coverage.
- The board exposes a labeled hypothesis form and history list; an ambiguous transport retry reuses the same key while the request form remains unchanged.

## Open limitations

- No player authentication or cross-player round authorization exists in the inherited local application. A round ID is not an authorization boundary; do not deploy this workflow as a shared/public game.
- The T02 projection is fixed published data, not a per-player persisted reveal ledger. API subject validation does not prove player-specific discovery authorization.
- No quote, credit ledger/debit/refund, paid action, provider dispatch/reconciliation, Zingg, exact shared-field analysis, Genie retrieval, reveal settlement, or full M13 state machine is implemented.
- No full-repository test, browser E2E/accessibility audit, or successful full Astro site build is claimed.
