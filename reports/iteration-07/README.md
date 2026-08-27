# FGA-07 local implementation evidence

This report records the verified local implementation slice. It is not a closure report: renderer qualification, full cumulative gates, live import qualification, and complete browser accessibility/performance evidence remain outstanding.

## Verified commands

- `python -m pytest tests/iteration_06 tests/iteration_01/test_openapi_contract.py -q` — 13 passed.
- `npm test -- --run` from `apps/web` — 34 passed across 18 files.
- `python -m pytest -q` — 148 passed in 8:18 after corpus repair.
- `python scripts/run_iteration_04_gate.py --report reports/iteration-07/iteration-04-current.json` — 13/13 packages strict-valid, zero blockers.
- `python scripts/qualify_databricks_security.py --profile fga-web` — fail-closed `not_qualified` because the profile is not configured.
- `python scripts/audit_iteration_05_requirements.py --root reports/iteration-05 --output reports/iteration-07/iteration-05-current-audit.json` — `external_gap`; live receipts, repeat qualification, non-admin denial, and revision consistency remain unproven.
- `npm run typecheck` from `apps/web` — passed.
- `npm run build` from `apps/web` — passed.
- targeted graph viewport tests — 2 passed.
- `npm run test:e2e` from `apps/web` — 11 passed with one Playwright worker and the repository virtual environment, including the populated `ACADEMY_T02` graph flow.
- targeted graph viewport tests after focus/minimap controls — 4 passed, including the 100-node/99-edge bounded renderer envelope (<1s in jsdom).

## Implemented slice

- bounded deterministic graph projections;
- one-hop expansion constrained to the authorized graph;
- reversible view-only node collapse;
- relationship-family filtering;
- graph API contracts and structured authorization errors;
- frontend zoom, layout, filtering, semantic selection, expansion, and collapse controls;
- presentation-only focus mode and an accessible minimap;
- evaluator-field and forbidden-sentinel rejection before graph projection.
- directed relationships rendered with explicit arrowheads.

## Outstanding closure work

- live FGA-05 Databricks qualification, evidence revision reconciliation, and immutable cumulative release closure;
- production renderer candidate qualification and real-browser performance evidence;
- live Databricks qualification (local strict corpus qualification is now complete);
- progressive loading and performance envelope;
- populated-graph performance envelope and full cumulative closure gate;
- final cumulative closure gate.
