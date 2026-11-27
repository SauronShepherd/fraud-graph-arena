# FGA-19 implementation log — The Board Must Go On

## Scope and authority

- Implementation branch: `FGA-19`, based on the final FGA-18 implementation branch. Functional commit: `9d2469ad08f977a3be5bd699906b9b97a983c9fd`.
- Article branch: `FGA-19` in the `angelic-articles` checkout. Article commit: `32b6271`.
- Assets branch: `FGA-19` in the `angelic-assets` checkout. Artwork commit: `1511c92151fb2660e28d6e90dd0a773b79548572`.
- The Master Series Outline is authoritative and names this article FGA-19. The older Development outline labels the same release-engineering block FGA-18; the discrepancy is recorded rather than silently renumbering the series.
- The article claims only behaviour represented in this branch or in a stored test/qualification receipt. The release manifest points to the functional implementation commit; this log commit changes documentation only.

## What was implemented

1. Added `fraud_graph_arena.release_engineering` with release manifests, deterministic tree/package digests, runtime context, saved-round compatibility decisions and an immutable local promotion pointer.
2. Added strict release contracts for the FGA-19 manifest, runtime versions and the seven CI stages: lint, unit, contracts, case validation, end-to-end, container build and deployment smoke.
3. Defined six release-unit boundaries: frontend, Python backend, database migrations, case packages, graph assets and analytics jobs. Each unit is represented by a SHA-256 tree digest and an immutable declaration in the manifest.
4. Bound every new round to its release, case package, rules, scoring, economy, screen, API, analytics and package-digest versions. The binding is persisted through SQLite and survives a restart.
5. Added an idempotent forward-only migration that creates the current round table when needed, adds the nine binding columns to an old database and records `rounds-v2-release-binding` in `schema_migrations`.
6. Added `PLAYABLE`, `MIGRATE` and `FROZEN` compatibility decisions. The current proof keeps an exact old package playable and freezes a round whose package is no longer available; future migration remains explicit rather than invented.
7. Added candidate feature-flag metadata, digest-gated promotion, application-pointer rollback and a local player-path smoke covering create, start, opening, complete and workspace access.
8. Added release-manifest generation/validation, the local release smoke, the Databricks profile qualification script and the stored receipts under `reports/iteration-19/`.

## Iteration and failure ledger

### Branch and baseline

- Created and pushed `FGA-19` in all three repositories before implementation: `fraud-graph-arena`, `articles` and `angelic-assets`. No FGA-18 branch was reused or overwritten.
- Confirmed the FGA-18 implementation suite before extending it (`7 passed`). The article comparison established the series invariant: three short italic opening paragraphs; Parts I–VIII; `The Arrest`; `Case Closed?`; `Next in the Series`; one separator; `Source Code`; release receipt; one separator; final infographic and caption.

### Implementation corrections

- The first SQLite insert after adding release binding supplied one more placeholder than the 22 persisted columns. The focused migration/round tests exposed it; the adapter was corrected and the restart test now proves all nine binding values survive persistence.
- The first complete backend regression recorded `312 passed, 1 failed`. The only failure was the committed OpenAPI comparison: the new `RoundResponse` fields existed in Pydantic but not in `contracts/openapi-v1.json`. The contract was updated, the focused OpenAPI test passed, and the final complete regression recorded `313 passed in 1091.53s`.
- The first manifest qualification after code edits intentionally rejected stale tree digests for the backend and migration units. That was the desired integrity signal, not a release defect: the manifest was regenerated after the functional commit and revalidated before the final Databricks run.
- The first local frontend check found no `node_modules`, so `tsc` was unavailable. `npm ci` installed the lockfile dependencies. npm reported one deprecated transitive package and five dependency vulnerabilities (`2 moderate`, `3 high`); no `audit fix` was applied because changing the dependency graph is outside FGA-19. Typechecking, tests and the production build then passed.
- The first article worktree also needed its locked dependencies. Content validation and the static build passed after installation. Pagefind emitted its informational notice about the supported Default UI; it is not an article or build failure.
- Port `4322` was already occupied during preview, so Astro selected `4323`. The direct route check passed at the selected port; the existing process was not touched.

## Test receipts

Commands run from the implementation worktree:

```text
python -m pytest -q tests/iteration_19 tests/iteration_18 tests/iteration_01/test_openapi_contract.py
python scripts/fga19_release_smoke.py
python scripts/generate_fga19_release_manifest.py --output reports/iteration-19/fga19-release-manifest-current.json
python scripts/validate_fga19_release.py --manifest reports/iteration-19/fga19-release-manifest-current.json
python -m pytest -q
python scripts/fga17_compose_contract.py
docker compose --profile local-build config --quiet
docker compose --profile local-build build web
python scripts/fga17_startup_smoke.py --base-url http://127.0.0.1:8019
```

Final receipts:

- Focused FGA-19/FGA-18/OpenAPI suite: `17 passed`.
- Full Python regression: `313 passed in 1091.53s (0:18:11)`.
- Release smoke: pass. It migrated an old SQLite database, rejected a corrupted frontend digest, promoted a valid candidate and rolled the application pointer back without data rollback.
- Manifest: pass; 6 release units, 7 ordered CI stages and one disabled candidate flag.
- Compose contract and `docker compose ... config --quiet`: pass.
- Docker image build: pass; `fraud-graph-arena:local` built from the branch.
- Container startup smoke: pass for liveness, readiness, frontend distribution, academy catalogue and board access on port `8019`.

Commands run from the frontend directory:

```text
npm ci
npm run typecheck
npm run validate:screens
npm test -- --run
npm run build
npm run test:e2e
```

Final frontend receipts:

- TypeScript typecheck: pass.
- Screen definitions: pass.
- Vitest: `27` files and `71` tests passed.
- Production build: pass.
- Playwright: `18 passed (2.7m)`.

Commands run from the article checkout:

```text
npm run content:validate
npm run build
npm run check:links
```

Final article receipts:

- Content validation: `117` canonical articles valid.
- Astro/Pagefind build: `107` pages generated, including `/fga/19-the-board-must-go-on/`; `102` pages indexed and `16969` words indexed.
- Internal links: `116` same-origin URLs checked, no failing internal URLs.
- Direct static preview: `200` for `/fga/19-the-board-must-go-on/`, title present, and `404` for the invalid legacy route `/articles/fga--19-the-board-must-go-on/`.
- The article contains no fenced code blocks, uses inline code/backticks consistently with the current FGA articles, and the matching separator count/section structure was checked against FGA-16, FGA-17 and FGA-18.

## Databricks receipt

Command:

```text
python scripts/qualify_fga19_release.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --manifest reports/iteration-19/fga19-release-manifest-current.json --report reports/iteration-19/databricks-fga19-release-current.json
```

The final live run completed with:

- status `pass`;
- source commit `9d2469ad08f977a3be5bd699906b9b97a983c9fd`;
- profile `fga`, authenticated;
- warehouse `eded42c9d0a69b84` and catalog/schema `sda_dev.sandbox`;
- 13 canonical package boundaries passed;
- read-only `SELECT` checks only;
- `truth_source_queried: false`;
- `actual_engine_run: false`;
- `docker_execution_on_databricks: false`;
- no forbidden player-facing columns and matching record/relationship counts for every package.

The report intentionally qualifies Databricks' public publication boundary. It does not claim that the local release pointer, SQLite migration or Docker image ran inside the SQL Warehouse.

## Editorial and visual reconciliation

- The article follows the established FGA-16/FGA-17/FGA-18 structure: three short italic opening paragraphs; Parts I–VIII; `The Arrest`; `Case Closed?`; `Next in the Series`; one separator; `Source Code`; release receipt; one separator; final infographic and caption.
- The narrative keeps the short detective-noir opening, dry canine humour and the technical deep dive. It uses the previous articles only when the versioning case benefits from continuity; it does not rely on unexplained cross-references.
- The exact reading-time estimator counted `2878` words and produced `15 minutes`, below the series' 20-minute target. Frontmatter is set to `readingTime: 15`.
- The newspaper cover and final infographic were generated as matching FGA artwork in the dark sepia palette and stored as `1.png` and `2.png` in the assets branch. Both commit-pinned jsDelivr URLs returned HTTP `200` as `image/png` before publication.

## Limits kept visible

- The frontend release unit is a deterministic `apps/web/src` source boundary; the Docker build is tested separately. The manifest is not presented as a signed registry image digest.
- `MIGRATE` is an explicit compatibility state reserved for a future data migration; this iteration proves exact-package replay and safe freezing, not an invented migration transform.
- The promotion/rollback pointer is local and immutable. No Databricks publication or external production deployment was changed.
- The Databricks qualification does not execute GraphFrames, Docker or hidden truth in the SQL Warehouse.
- Dependency audit notices from the existing lockfiles remain visible and are not silently presented as application failures or fixed by an unrelated dependency upgrade.
