# FGA-07 local implementation evidence

This report records the verified FGA-07 implementation and qualification evidence. It is not a closure report: non-admin authorization evidence, human product-owner acceptance, and the remaining production-scale request performance envelope remain outstanding.

## Verified commands

- `python -m pytest -q` — 188 passed in 11:07 after the cumulative FGA06 closure-validator repair, OpenAPI contract refresh, and complete-manifest indexing.
- `npm test -- --run` from `apps/web` — 55 passed across 22 files.
- `python scripts/run_iteration_04_gate.py --report reports/iteration-07/iteration-04-current.json` — 13/13 packages strict-valid, zero blockers.
- `python scripts/audit_iteration_05_requirements.py --root reports/iteration-05 --output reports/iteration-07/iteration-05-current-audit.json` — remaining gaps are external/non-admin qualification and human acceptance; the FGA-07 live receipts are recorded separately below.
- `databricks auth describe --profile fga` — profile reauthenticated successfully; a dedicated `FGA-07-qualification` warehouse was created as `eded42c9d0a69b84` and stopped after testing.
- `python scripts/qualify_databricks.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --create` — PASS, 44/44 expected objects and zero column mismatches.
- `python scripts/qualify_databricks_all_packages.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84` — PASS, all 13 packages completed the lifecycle through `PUBLISHED`.
- `python scripts/verify_databricks_package_counts.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84` — PASS, 32 tables and zero count mismatches.
- `python scripts/qualify_databricks_repeat.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84 --repeats 10` — PASS, 10 × 13 package attempts, zero failures, idempotent reuse.
- `python scripts/qualify_databricks_failure.py --profile fga --catalog sda_dev --schema sandbox --warehouse eded42c9d0a69b84 --execute` — PASS, rejected candidate remained inactive and active pointer was unchanged.
- `python scripts/qualify_databricks_security.py --profile fga` — `not_qualified` because the authenticated principal is an administrator.
- `npm run typecheck` from `apps/web` — passed.
- `npm run build` from `apps/web` — passed.
- `npm run test:e2e` from `apps/web` — 15 passed with one Playwright worker and the repository virtual environment, including the populated `ACADEMY_T02` graph flow.
- targeted graph viewport tests after focus/minimap controls — 10 passed, including selected-node context fitting, controlled filters, collapse selection clearing and the bounded renderer envelope.
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

- non-admin authorization evidence with a distinct non-administrator Databricks identity;
- production-scale request-byte/wall-clock performance qualification and a product-owner accessibility acceptance;
- final cumulative closure gate; the release manifest is generated and clean but correctly keeps `closure_allowed: false` while security is `not_qualified`.
