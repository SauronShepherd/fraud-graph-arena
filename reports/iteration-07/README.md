# FGA-07 local implementation evidence

This report records the verified local implementation slice. It is not a closure report: live import qualification, non-admin authorization evidence, complete cumulative release closure, and the remaining production-scale performance/accessibility envelope remain outstanding.

## Verified commands

- `python -m pytest tests/iteration_06 tests/iteration_01/test_openapi_contract.py -q` — 13 passed.
- `npm test -- --run` from `apps/web` — 51 passed across 22 files.
- `python -m pytest -q` — 173 passed in 25:31 after corpus repair and cumulative integration fixes.
- `python scripts/run_iteration_04_gate.py --report reports/iteration-07/iteration-04-current.json` — 13/13 packages strict-valid, zero blockers.
- `python scripts/qualify_databricks_security.py --profile fga-web` — fail-closed `not_qualified` because the profile is not configured.
- `python scripts/audit_iteration_05_requirements.py --root reports/iteration-05 --output reports/iteration-07/iteration-05-current-audit.json` — `external_gap`; live receipts, repeat qualification, non-admin denial, and revision consistency remain unproven.
- `databricks auth describe --profile fga` and `databricks warehouses get e444f39962128242 --profile fga` — profile valid and warehouse healthy/running.
- `python scripts/qualify_databricks_all_packages.py --profile fga --catalog sda_dev --schema sandbox --warehouse e444f39962128242` — attempted but failed on the first package at SQL transport (`wsarecv` connection abort); a retry was stopped after hanging without a result.
- `python scripts/qualify_databricks_security.py --profile fga` — `not_qualified` because the authenticated principal is an administrator.
- `npm run typecheck` from `apps/web` — passed.
- `npm run build` from `apps/web` — passed.
- targeted graph viewport tests — 2 passed.
- `npm run test:e2e` from `apps/web` — 11 passed with one Playwright worker and the repository virtual environment, including the populated `ACADEMY_T02` graph flow.
- targeted graph viewport tests after focus/minimap controls — 6 passed, including the 100-node/99-edge bounded renderer envelope (<1s in jsdom).
- qualification Playwright — 11 passed, including renderer exhibit, manual capture and performance qualification.
- renderer comparison — four engines exercised with the common contract; Cytoscape recorded as the conditional incumbent in `docs/iteration-06/ADR-0001-renderer-qualification.md`.

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

- live FGA-05/Databricks qualification, evidence revision reconciliation, and non-admin authorization evidence;
- progressive loading and request-level performance envelope;
- full cumulative closure gate and immutable release evidence;
- final cumulative closure gate.
