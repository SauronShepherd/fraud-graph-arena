# FGA-12 implementation and qualification log

## Scope

- Article: `FGA 12 — Case Me If You Can`.
- Editorial source: `FGA_Development_Series_Outline_07-19.md`, Iteration I12, and the corresponding FGA-12 entry in `Fraud Graph Arena — Master Series Outline Updated.md`.
- Code branch: `FGA-12`.
- Code worktree: `C:\Users\angel.alvarez\PycharmProjects\_worktrees\fraud-graph-arena-fga12-20261126`.
- Article branch: `FGA-12`, commit `7fe1e084f63e3abd1feebdb9241b25b7490683a1`.
- Asset branch: `FGA-12`, commit `103b4b6f29fcdb82c9f1646239d23c31c09e201a`.
- Suggested series tag: `fga-i12-case-packages`.

The acceptance target was a second canonical case that can be discovered, validated, opened, investigated and resolved through shared services. A case-specific `if case_id == ...` branch in shared application screens or services was not accepted as the implementation.

## What changed

1. Added `contracts/case-packages/fga12-case-package.schema.json`, a closed JSON Schema contract. It distinguishes package, canonical data, engine, scoring/economy and publication versions, and does not permit arbitrary executable configuration.
2. Added declarative manifests for the existing empty Academy file, the migrated Circular Collar case and the new Ghost Invoice case under `case-packages/`.
3. Added `CasePackage`, `CasePackageRegistry` and the package validator. The validator checks schema, directory identity, canonical references, snapshot identity, action/economy compatibility, asset references, public/protected separation and publication rules.
4. Added `scripts/validate_case_packages.py` and `scripts/qualify_case_packages.py`.
5. Replaced T02-only application wiring with package discovery. Catalogue, narrative opening/closing, round credits, graph projection, identity records, action authorization, economy costs and case-resolution scoring now resolve through the active package. T02's manual-hypothesis capability is declared by its manifest; T03 does not declare it.
6. Kept the evaluator’s protected truth on the server. The player receives published records, safe graph metadata and a versioned receipt; `truth/` is never serialized into the workspace or analysis response.
7. Added T03 package contract tests, including a clean six-claim resolution, undeclared-action rejection, safe projection checks and an executable-configuration rejection.
8. Updated the committed OpenAPI contract because a package may declare more than five evidence claims; the public submission limit is now thirty-two.

## Iteration history and failures

| Pass | Observation | Correction | Result |
|---|---|---|---|
| Discovery | T02, the graph provider, identity records, evaluator, economy and narrative repository each contained case-specific knowledge. | Mapped those seams before drafting the package contract. | The shared flow has a package provider; case IDs remain in package data and canonical fixtures, not shared service branches. |
| Package validation 1 | `ImportError: cannot import name 'CasePackage' from partially initialized module 'fraud_graph_arena.case_packages'`. | Moved the catalogue service’s package type import behind `TYPE_CHECKING`; the runtime delegation does not need the type import. | `python scripts/validate_case_packages.py` passed for all three packages. |
| T03 smoke 1 | The first manual graph request used `/graph/analysis` and returned the expected `404 ROUTE_NOT_FOUND`. | Replayed the request against the actual route `/investigations/graph-analytics`. | The correct route returned a completed bounded analysis. The typo was recorded rather than hidden. |
| T03 smoke 2 | `NameError: name 'self' is not defined` in graph authorization. The method was still marked `@staticmethod` after gaining package access. | Converted `_require_active_round` to an instance method and used the injected package provider. | T02 regression and T03 analysis tests passed. |
| Contract gate | The OpenAPI equality test failed after increasing evidence claims from five to thirty-two. | Regenerated `contracts/openapi-v1.json` with `scripts/export_openapi.py`. | The committed contract and application schema match. |
| Adversarial package review | A shared investigation-command service still checked `ACADEMY_T02` directly and loaded the T02 graph. | Injected the active package provider, required the declared `CREATE_HYPOTHESIS` capability and loaded the package graph. | No T02 case branch remains in that service; T02 behavior is preserved by its manifest. |
| Adversarial workspace review | The workspace exposed `CREATE_HYPOTHESIS` for every canonical package, although T03 did not declare it. | Added the action to the schema and T02 manifest, and gated the workspace action by `package.supports(...)`; updated the T03 contract test. | T03 exposes only its declared graph action; FGA-08/T02 keeps the manual-hypothesis action. |
| Web gate 1 | `tsc` was not found because the clean worktree had no `node_modules`. | Installed the locked dependencies with `npm ci`; no source or lockfile change was made. | Typecheck, screen validation, Vitest and build passed. |
| Dependency installation | npm reported one deprecated transitive package and five audit findings (2 moderate, 3 high). | Did not run `npm audit fix --force`; that would change dependency scope outside I12 and could rewrite the lockfile. | Logged as an environment/dependency limitation, not as a product-test failure. |
| Databricks | First live package qualification ran before the final code commit and therefore reported the parent SHA. | Re-run the same read-only qualification after the final code commit and keep that receipt as the authoritative one. | Both ACADEMY_T02 and ACADEMY_T03 must pass against profile `fga`. |

## Tests and checks completed before the final receipt

### Python

- `python -m compileall -q src scripts`: passed.
- `python scripts/validate_case_packages.py`: passed; `academy-001`, `academy-t02` and `academy-t03` returned no errors.
- `pytest -q tests/iteration_12`: passed.
- `pytest -q tests/iteration_01 tests/iteration_09 tests/iteration_10 tests/iteration_11 tests/iteration_12`: 97 passed, no pytest warning summary.
- Full repository run: `pytest -q`: 263 passed in 14:22 on the corrected implementation. No warning summary was emitted.
- Final implementation SHA for the refreshed live receipt: `08d2a90af24bb25f9b1e4312adcc081df6a49f6a`.

### Web

- Initial attempt failed before execution because `tsc` was unavailable in the clean worktree.
- After `npm ci`: 65 tests passed in 24 files.
- Typecheck passed.
- Screen definitions parsed successfully.
- Vite production build passed.
- After the package-capability correction, the web gate was rerun: typecheck passed, screen definitions parsed, 65 Vitest tests across 24 files passed, and the production build passed.

### Article site

- `npm ci` in the article worktree restored 355 packages. npm reported two install scripts requiring approval (`esbuild` and `workerd`) and five audit findings (4 moderate, 1 high); no dependency files were changed.
- `npm run content:validate` passed with 110 canonical articles in the series-folder structure.
- `npm run check:links` passed with 116 same-origin URLs checked and no failing internal URL.
- `npm run build` passed: Astro generated 100 pages, including `/fga/12-case-me-if-you-can/`; Pagefind indexed 95 pages.
- The final article build after the package-capability correction again generated 100 pages and indexed 95 pages. Pagefind printed its informational note about the supported default UI reference; it is not a build failure.
- The first editorial run used the default remote site and failed on an unrelated deployed-catalogue expectation for `greased-reyden`. The first local run used port `4321`, which was already serving another worktree; it therefore failed against the wrong generated href. The FGA-12 Astro server auto-bound to `4323`, where the static server correctly exposed the article but not the Worker-only admin routes (404 instead of the expected 401).
- The final local runtime used `npx wrangler dev --local --ip 127.0.0.1 --port 4332 --persist-to .wrangler/fga12`. `npm run test:editorial` passed 1/1 against that Worker runtime. The FGA-12 route returned HTTP 200 and contained both image references; both pinned CDN image URLs returned HTTP 200.
- Wrangler displayed its expected local-development warning that scheduled Workers are not triggered automatically. No cron path is part of this article gate.
- Git reported the expected LF-to-CRLF normalization warning when committing the article Markdown file; `git diff --check` was clean and the pushed commit contains no whitespace error.
- Git also reported the expected CRLF-to-LF normalization warning when refreshing the generated JSON receipt; `git diff --check` remained clean.

### Live Databricks qualification

The command was executed with the requested profile:

```text
databricks current-user me --profile fga
$env:PYTHONPATH='src'; python scripts/qualify_case_packages.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --report reports/iteration-12/databricks-fga12-packages-current.json
```

The final live receipt, after pushing the code commit, passed for both cases. It was run as the authenticated Databricks user `angel.alvarez.pascua@gmail.com` with profile `fga`, catalog `sda_dev`, schema `sandbox` and warehouse `eded42c9d0a69b84`.

- ACADEMY_T02: 20 public records, 21 public relationships, one active snapshot.
- ACADEMY_T03: 23 public records, 27 public relationships, one active snapshot.
- Both cases: no forbidden player columns, no truth source queried, all statements read-only.
- Final source commit reported by the refreshed qualifier: `08d2a90af24bb25f9b1e4312adcc081df6a49f6a`.
- `actual_engine_run: false`: the `fga` profile reaches a SQL Warehouse, so this qualification proves the safe published boundary and does not pretend to have run GraphFrames.

The report is intentionally read-only. All generated statements begin with `SELECT`, query only the active publication/public-record/public-relationship views and information schema, and never query protected `truth` files.

## Known limits carried honestly into the article

- FGA-12 makes case addition package-driven, but it does not claim that SQL Warehouse executed GraphFrames or Zingg. The application’s deterministic graph adapter remains explicit.
- The package validator is a validation CLI, not a CMS or an arbitrary rules interpreter. Authors add declarative manifests and referenced canonical data; reusable engine capabilities remain code-owned.
- npm’s locked dependency tree reports five audit findings. They are not silently presented as zero-risk; changing them belongs to dependency maintenance, not this article’s case-package slice.
- The image files are generated editorial assets; their provenance is recorded by the asset repository commit and the article’s release receipt.

