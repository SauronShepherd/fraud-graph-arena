# FGA-16 implementation and test log

## Scope

FGA-16 implements the updated master-outline item “Test Me Baby One More Time”: make the hidden validation level a player-facing Detective Academy and a machine-facing qualification suite. The work covers the implementation repo, the article repo and the separate assets repo. The article is kept under 20 minutes and follows the FGA newspaper/noir structure: three short italic opening paragraphs, Parts I–VIII, an arrest, a case-status section, next-case handoff, source code, release receipt and final infographic.

## Branches and worktrees

| Repository | Branch | Worktree |
| --- | --- | --- |
| `fraud-graph-arena` | `FGA-16` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\fraud-graph-arena-fga16-20261126` |
| `articles` | `FGA-16` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\articles-fga16-20261126` |
| `angelic-assets` | `FGA-16` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\angelic-assets-fga16-20261126` |

All three branches were created from the preceding FGA-15 branch and pushed to their respective origins. The implementation and article branches remain independent so a direct article route can be reviewed without featuring it in the publication catalogue.

## Chronological record

### 1. Editorial and outline reconnaissance

- Read `Fraud Graph Arena — Master Series Outline Updated.md` and `FGA_Development_Series_Outline_07-19.md`.
- Read the FGA-14 and FGA-15 articles and checked the repeated opening, section notation, noir narration, tables, separator placement, source-code receipt and final-image treatment.
- Applied the editorial-review skill to the draft: checked intent, reader path, certainty, observable claims, paragraph pulse, repeated recap, scope boundaries, accessibility and traceability.
- Kept FGA-16 at `readingTime: 18`, with no fenced code blocks and no invented provider claim.

### 2. Contract and implementation pass

Added:

- `contracts/academy/fga16-academy-scenario.schema.json`
- `contracts/academy/fga16-scenarios.json`
- `contracts/academy/fga16-golden-results.json`
- `src/fraud_graph_arena/academy/` scenario registry, models and three runner layers
- `src/fraud_graph_arena/web/routes/academy.py`
- public Academy response models, catalogue mapping and frontend contract/types
- Academy curriculum rendering, responsive styles and semantic navigation assertions
- `tests/iteration_16/` contract, redaction, runner, persistence and regression tests
- `scripts/qualify_fga16_academy.py`
- regenerated `contracts/openapi-v1.json`

The public response removes protected expected outcomes and golden identifiers. The local runner retains them for assertions. The remote qualification only checks the public projection boundary.

### 3. First red test pass and corrections

The first focused FGA-16 run was `5 passed, 2 failed`.

1. The catalogue route read `.value` from a `PathDefinition`; the contract exposes the path through its `PathId`. The route now compares the path identifier explicitly.
2. The persistence probe expected a `replayed` field on Graph Analytics, but the actual contract reports cached replay. The probe now checks `cached` and releases TestClient resources before the SQLite file is reopened on Windows.

After those corrections, `tests/iteration_16` passed `7 tests`. The isolated shared-runner test passed, and the relevant earlier suites were rerun after regenerating the OpenAPI snapshot. The initial stale snapshot failure was not left masked.

### 4. Frontend pass and environment corrections

- The first frontend install had no dependency tree in the FGA-16 worktree. `npm ci` restored the lockfile state. npm reported the existing `whatwg-encoding@3.1.1` deprecation and five audit findings (two moderate, three high); no automatic upgrade was applied.
- TypeScript passed.
- Vitest passed 70 tests in 26 files.
- Vite production build passed with no Vite build warnings.
- The first E2E attempt used a hard-coded `.venv` Python path that did not exist in this worktree. Playwright now accepts `FGA_PYTHON` and supplies `PYTHONPATH=src` to its backend server.
- A subsequent E2E run exposed a Windows Proactor `ConnectionResetError` during server teardown. The web entrypoint now uses the Windows selector event-loop policy for the local test server; the exception disappeared on rerun.
- The host also exported conflicting Node colour flags. The Playwright launcher now sets `FORCE_COLOR=0` before Node starts the test process; the final E2E receipt has no colour warning.
- Final E2E result: `16 passed`, no warnings and no exceptions.

### 5. Article-repo pass

- The first content validation failed because the new article worktree had no `node_modules`; `yaml` could not be imported. This was an environment failure, not a content failure.
- `npm ci` restored the article dependencies. npm reported five audit findings (four moderate, one high) and install-script notices for `esbuild` and `workerd`; these notices remain recorded rather than hidden.
- Content validation passed for `114 canonical articles`.
- The static build passed and generated `/fga/16-test-me-baby-one-more-time/index.html`.
- Pagefind indexed 99 pages. Its existing informational note about the default UI was recorded; it was not a build failure.
- The new slug was added to `unlistedArticleSlugs`, preserving direct access without changing the public homepage count.

### 6. Visual assets

Generated and visually inspected two FGA-16 assets using the image-generation skill:

- `1.png`: dark muted sepia newspaper cover with the Detective Academy, nine scenarios, seeds, golden results and regression.
- `2.png`: dark sepia top-down case-file infographic with eight numbered panels, three runner layers, diagnostics, regression and complete loop.

Both keep Hercule Perrot as a recognisable Spanish Water Dog rather than a wolf or generic hound. Assets were committed and pushed to `angelic-assets` as `f0ae64e9f03e7aadaa4e0122475903fee9b65c62`. The article pins both CDN URLs to that immutable commit.

### 7. Databricks qualification

- Verified the requested profile with `databricks current-user me --profile fga`.
- Ran `scripts/qualify_fga16_academy.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84`.
- Result: `status=pass`, local Academy `PASS`, 9 scenarios, 14 local packages, SQLite persistence `PASS`, 13 remote canonical public boundaries `pass`.
- Remote mode is read-only. It queried no protected truth source and did not claim an actual GraphFrames or Zingg run. The receipt records `actual_engine_run=false` and `graphframes_compatibility=UNRESOLVED_SQL_WAREHOUSE_ONLY`.
- Full JSON receipt: `reports/iteration-16/databricks-fga16-academy-current.json`.

### 8. Final verification receipts

| Check | Result |
| --- | --- |
| Backend full suite | `293 passed in 1445.83s` |
| FGA-16 focused backend suite | `7 passed` |
| Frontend typecheck | PASS |
| Frontend Vitest | `26 files, 70 passed` |
| Frontend Vite build | PASS; no Vite warnings |
| Browser E2E | `16 passed`; no warnings/exceptions in final run |
| Article content validation | `114 canonical articles` |
| Article static build | PASS; FGA-16 route generated |
| Databricks profile | `fga`, authenticated |
| Databricks public-boundary qualification | PASS; 13 canonical cases; SELECT-only |
| Article/implementation matrix | All rows PASS |

## Residual notices kept visible

The code and test receipts are clean. npm still reports dependency audit/deprecation notices during fresh installs, and Pagefind prints an informational integration note. They are intentionally documented here and in the article rather than silently treated as application failures. No dependency upgrade was introduced without a separate security/dependency scope.

## Closure

FGA-16 does not claim a graph engine ran inside SQL Warehouse. It claims that the player-facing Academy, deterministic local qualification suite, published-case regression, persistence probe, browser path and read-only Databricks public boundary all passed under their declared contracts.
