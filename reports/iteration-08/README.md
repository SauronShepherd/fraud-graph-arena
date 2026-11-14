# FGA-08 qualification evidence

This report records the FGA-08 implementation slice that is actually shipped on the branch. It is intentionally narrower than the full investigation protocol described as the target architecture in the article and the master outline.

## Scope

- Branch: `FGA-08`, created from the FGA-07 line.
- Delivered action: `CREATE_HYPOTHESIS` for an active `ACADEMY_T02` round.
- Persistence: in-memory adapter for ephemeral mode; SQLite adapter for the durable application mode.
- Guarantees: typed relationship allowlist, distinct subjects, active-round/case eligibility, request hashing, exact replay, same-key conflict, concurrent one-effect history and zero evidence/credit mutation.
- Frontend: labeled manual-hypothesis form, authoritative success/error feedback and semantic command history.
- Databricks: read-only qualification of the active player-safe T02 publication. Hypothesis commands are not written into the analytical snapshot.

## Executed checks

| Area | Command | Result |
|---|---|---|
| Python full regression | `$env:PYTHONPATH="src"; python -m pytest -q` | `200 passed in 10:59` |
| FGA-08 + graph regression | `$env:PYTHONPATH="src"; python -m pytest tests/iteration_08 tests/iteration_06 -q` | `44 passed in 4.99s` |
| Frontend tests | `npm test -- --run` from `apps/web` | `58 passed across 23 files` |
| Frontend typecheck | `npm run typecheck` from `apps/web` | passed |
| Frontend build | `npm run build` from `apps/web` | passed; 61 modules transformed |
| Content validation | `npm run content:validate` from the articles repository | `104` canonical articles validated |
| Databricks boundary | `python scripts/qualify_investigation_boundary.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --case-id ACADEMY_T02 --report reports/iteration-08/databricks-fga08-investigation-boundary.json` | pass |
| Syntax/whitespace | `python -m compileall -q src tests scripts`; `git diff --check` | pass |

## Databricks result

The read-only qualification used profile `fga` and warehouse `eded42c9d0a69b84` in `sda_dev.sandbox`. It found one active `ACADEMY_T02` publication, 20 distinct records, 21 distinct relationships, one snapshot for each view, zero dangling relationship endpoints and no forbidden player-facing column names. The warehouse was stopped after the check.

The detailed machine-readable receipt is [databricks-fga08-investigation-boundary.json](databricks-fga08-investigation-boundary.json).

## Explicit limits

- No player authentication or cross-player authorization was added.
- No per-player reveal ledger was added.
- No paid quotes, credit ledger, provider dispatch, Zingg, exact-match analysis, Genie retrieval, reveal settlement, evaluator or submission flow was claimed.
- The live Databricks check proves the source publication boundary only; it is not evidence that manual hypotheses are persisted in Databricks.
