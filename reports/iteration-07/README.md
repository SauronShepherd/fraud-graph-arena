# FGA-07 local implementation evidence

This report records the verified local implementation slice. It is not a closure report: live import qualification, non-admin authorization evidence, complete cumulative release closure, and the remaining production-scale performance/accessibility envelope remain outstanding.

## Verified commands

- `python -m pytest tests/iteration_06 tests/iteration_01/test_openapi_contract.py -q` — 28 passed.
- `npm test -- --run` from `apps/web` — 53 passed across 22 files (fork-pool execution).
- `python -m pytest -q` — 173 passed in 12:07 after corpus repair and cumulative integration fixes.
- `python scripts/run_iteration_04_gate.py --report reports/iteration-07/iteration-04-current.json` — 13/13 packages strict-valid, zero blockers.
- `python scripts/qualify_databricks_security.py --profile fga-web` — fail-closed `not_qualified` because the profile is not configured.
- `python scripts/audit_iteration_05_requirements.py --root reports/iteration-05 --output reports/iteration-07/iteration-05-current-audit.json` — `external_gap`; live receipts, repeat qualification, non-admin denial, and revision consistency remain unproven.
- `databricks auth describe --profile fga` — profile reauthenticated successfully; a dedicated `FGA-07-qualification` warehouse was created as `eded42c9d0a69b84` and stopped after testing.
- `python scripts/qualify_databricks.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --create` — PASS, 44/44 expected objects and zero column mismatches.
- `python scripts/qualify_databricks_all_packages.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84` — blocked during the first package transfer after creating the required staging volume; the retry produced no result and was stopped.
- `python scripts/qualify_databricks_security.py --profile fga` — `not_qualified` because the authenticated principal is an administrator.
- `python scripts/verify_databricks_package_counts.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84` — FAIL, 32 active/publication count mismatches because package loading did not complete.
- `python scripts/qualify_databricks_failure.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84 --execute` — FAIL, script raised `KeyError: data_array` while handling the incomplete lifecycle state.
- `npm run typecheck` from `apps/web` — passed.
- `npm run build` from `apps/web` — passed.
- `npm run test:e2e` from `apps/web` — 15 passed with one Playwright worker and the repository virtual environment, including the populated `ACADEMY_T02` graph flow.
- targeted graph viewport tests after focus/minimap controls — 8 passed, including selected-node context fitting, controlled filters and the 100-node/99-edge bounded renderer envelope (<1s in jsdom).
- `npx playwright test -c playwright.qualification.config.ts` — 11 passed with one worker, including renderer exhibit, manual capture and the 12-repetition-per-candidate performance qualification.
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
