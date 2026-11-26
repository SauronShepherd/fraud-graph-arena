# FGA-13 implementation and qualification log

## Scope

- Article: `FGA 13 — Puppy Love, Adult Problems`.
- Editorial sources: `FGA_Development_Series_Outline_07-19.md`, Iteration I13, and the FGA-13 entry in `Fraud Graph Arena — Master Series Outline Updated.md`.
- Code branch: `FGA-13`.
- Code worktree: `C:\Users\angel.alvarez\PycharmProjects\_worktrees\fraud-graph-arena-fga13-20261126`.
- Article branch: `FGA-13`.
- Article worktree: `C:\Users\angel.alvarez\PycharmProjects\_worktrees\articles-fga13-20261126`.
- Asset branch: `FGA-13`.
- Asset worktree: `C:\Users\angel.alvarez\PycharmProjects\_worktrees\angelic-assets-fga13-20261126`.
- Databricks profile: `fga`.
- Databricks qualification mode: read-only SQL Warehouse queries.

The acceptance target was four meaningfully different difficulty paths on one reusable engine. Difficulty had to be a validated vector of ambiguity, noise, graph depth, evidence quality, resource pressure, mixed roles and legitimate comparators. It could not be a disguised node count, a cumulative player level or a case-specific branch in the application.

## What changed

1. Added `DifficultyProfile`, `validate_profile()` and `validate_catalogue()` under `src/fraud_graph_arena/difficulty/`. Profiles are versioned, path-bound, non-cumulative and checked for path-specific ranges, evidence quality and legitimate comparators.
2. Added `contracts/case-packages/fga13-case-package.schema.json`, requiring a closed `difficulty_profile` object with explicit fields and enums.
3. Added deterministic manifest generation for thirteen canonical packages: three Academy, three Puppy, four Adult and three Senior. The existing empty Academy shell remains a compatibility manifest, so fourteen manifests are discovered in total.
4. Kept legacy package/economy/scoring versions for the existing Academy cases while assigning the FGA-13 difficulty contract and preserving their historical behavior.
5. Made all four memory-catalogue paths open and package-backed. The shared round, opening, workspace, graph, identity and resolution flow consumes package data rather than a new path-specific engine.
6. Applied each package's `graph_node_limit` to the initial graph view while preserving the API hard ceiling of 300 nodes and 700 relationships. Partial views expose omitted node and relationship counts and preserve the graph snapshot version.
7. Added FGA-13 tests for profile/schema/catalogue rules and for one shared playable round in Academy, Puppy, Adult and Senior. Updated historical catalogue and package-count tests to describe the new published catalogue rather than the old Academy-only baseline.
8. Added `scripts/qualify_fga13_difficulty.py`, a read-only Databricks qualifier for every canonical package. It records the requested profile, warehouse, active publication, exact public counts, forbidden-column scan, source commit and the fact that GraphFrames was not executed in a SQL-Warehouse-only run.
9. Added the numbered newspaper and infographic assets under the FGA-13 asset branch and pinned their CDN commit in the article.

## Iteration history and failures

| Pass | Observation | Correction | Result |
|---|---|---|---|
| Outline review | The two outlines required four paths, multiple difficulty dimensions, legitimate comparators, one profile per packaged dataset and cross-path regression. | Converted those requirements into a typed profile, a closed manifest schema, catalogue validation and shared-engine tests. | The article, code and tests use the same vocabulary; no scalar difficulty field was introduced. |
| Manifest generation 1 | The first generator changed the existing Academy case versions and economy/scoring versions while adding the new profile. | Added explicit legacy compatibility maps for ACADEMY_T02 and ACADEMY_T03. | Existing package identity and FGA-12 economy/scoring contracts remain stable. |
| Catalogue regression 1 | Historical tests still expected Puppy and Adult to be locked and expected only the original Academy package count. | Updated those tests to assert the four open paths, thirteen canonical packages and the compatibility shell. | The old tests now protect the new catalogue contract rather than stale assumptions. |
| Cross-path gate 1 | Adult and Senior initial projections exceeded the graph API's 300-node / 700-relationship limits. | Made `graph_node_limit` select the learning-sized package view, applied the global ceiling in the provider and emitted explicit omission counts. | The graph remains bounded without hiding that it was bounded. |
| Cross-path gate 2 | The workspace mapper received dictionaries from the bounded provider but accessed them as dataclass attributes. | Added a small dict/dataclass boundary adapter in `web/mappers.py`. | The same workspace contract works for the bounded package graph and the older service projections. |
| Cross-path gate 3 | The bounded subset dropped `snapshot_version`, causing the fallback round snapshot to appear in API tests. | Preserved the authorized graph snapshot through initial, expand and filter projections and declared it compatibly in `GraphResponse`. | Snapshot identity survives every graph view. |
| Python regression 1 | The full suite reached 270 passing tests and one OpenAPI-contract failure after the new graph field was added. | Regenerated `contracts/openapi-v1.json` with `scripts/export_openapi.py`. | The committed schema matches the application contract. A full rerun is required after this repair. |
| Databricks invocation 1 | Running the new qualifier as a file could not import the sibling qualifier module with package-only imports. | Added a direct-file import fallback. | The exact command used for the external check runs without changing the repository import layout. |
| Databricks qualification | Profile `fga` authenticated to the configured SQL Warehouse; all thirteen active public boundaries passed. | Kept the run read-only and recorded `truth_source_queried=false`, `actual_engine_run=false` and `UNRESOLVED_SQL_WAREHOUSE_ONLY`. | The report proves the published safe boundary, not an unperformed GraphFrames execution. |
| Visual pass 1 | The first generated artwork was brighter than the established FGA-11/FGA-12 desk images. | Regenerated both pieces with a darker sepia/umber treatment and restrained lamp glow. | The cover and infographic use the same low-key noir palette and Spanish Water Dog detective. |

## Tests and checks

### Python

Commands run during implementation:

```text
PYTHONPATH=src python scripts/validate_case_packages.py
PYTHONPATH=src pytest -q tests/iteration_13/test_cross_path_playability.py tests/iteration_12/test_case_packages.py --tb=short
PYTHONPATH=src pytest -q tests/iteration_06/test_graph_api.py tests/iteration_13/test_cross_path_playability.py tests/iteration_12/test_case_packages.py --tb=short
PYTHONPATH=src python scripts/export_openapi.py
PYTHONPATH=src pytest -q tests/iteration_01/test_openapi_contract.py --tb=short
PYTHONPATH=src pytest -q --tb=short
```

The focused graph/package/cross-path gate passed 24 tests after the snapshot compatibility fix. The first full-suite run after that fix passed 270 tests and exposed one committed-OpenAPI mismatch; the OpenAPI export corrected it. The final full-suite command is rerun after the correction and its exact result is recorded in the release receipt below.

The package validator discovered fourteen manifests and returned zero validation errors. The FGA-13 tests cover profile variance, required comparators, rejection of cumulative profiles, package schema validity and one shared playable round for each path. The historical graph tests cover seeds, expansion, filtering, hard ceilings and safe response fields.

### Databricks qualification

The requested profile was checked before the run:

```text
databricks auth profiles
```

The `fga` entry resolved to the configured Databricks workspace. The read-only qualification command was:

```text
$env:PYTHONPATH='src'; python scripts/qualify_fga13_difficulty.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --report reports/iteration-13/databricks-fga13-difficulty-current.json
```

The live report passed for all thirteen canonical packages. It used catalog `sda_dev`, schema `sandbox` and warehouse `eded42c9d0a69b84`. The allowlisted statements were `SELECT` checks against the active publication and player-safe records/relationships. The run did not query protected truth, write a table or mutate a publication. `actual_engine_run` is false and `graphframes_compatibility` is `UNRESOLVED_SQL_WAREHOUSE_ONLY` because this profile reaches a SQL Warehouse rather than a Spark runtime.

The first report was generated before the FGA-13 code commit and therefore carried the FGA-12 parent SHA. It is intentionally superseded by the final report after the implementation commit; the final source commit is recorded in the JSON receipt and the release receipt below.

## Article ↔ implementation invariants

- Every article dimension exists in `DifficultyProfile` and in the closed manifest schema.
- The four paths and their package counts come from `PATH_COUNTS` and the generated canonical package set.
- The article's one-profile rule is `progression_mode=PACKAGE_SINGLE_PROFILE` and is rejected when changed to a cumulative mode.
- The article's legitimate-comparator rule is validated as a positive manifest requirement and is also checked in the live public-boundary report without querying truth.
- The article's bounded-view claim is implemented in `build_web_container()`, `initial_subset()` and `GraphResponse`; omitted counts and snapshot identity are tested.
- The article's shared-engine claim is implemented by `test_one_shared_round_engine_serves_each_path`, which starts one round in each path through the same API flow.
- The article says the cross-path test is executable playability evidence, not a human usability study. No human playtest or player telemetry is claimed in the article.
- The article says GraphFrames/Zingg did not execute; the external report carries `actual_engine_run=false`.

## Known limits carried honestly into the article

- The local playability gate is deterministic API regression, not a study with human players. It cannot tell us where a person stalls, misunderstands a clue or experiences a path as unfair.
- The difficulty vector is a contract and a boundary, not a calibrated predictor of session completion time.
- The Databricks run qualifies the active safe publication boundary through profile `fga`; it does not claim a Spark GraphFrames or Zingg execution.
- The generated artwork is an editorial asset. Its exact bytes and CDN identity are pinned to the separate asset-branch commit.

## Release receipt

The final values are filled after the implementation branch is committed, the article branch is built and the post-commit Databricks qualification is rerun. No earlier green result is treated as the final receipt when a later correction changed the source commit.

| Surface | Final result |
|---|---|
| Code branch / commit | `FGA-13` / pending final commit |
| Article branch / commit | `FGA-13` / pending final commit |
| Asset branch / commit | `FGA-13` / `31620dfdbc18f59a30390415bd4d3ff3bb899aeb` |
| Python suite | pending final post-correction rerun |
| Package validation | 14 manifests; zero validation errors |
| Databricks profile | `fga`; read-only; 13 canonical package boundaries passed |
| GraphFrames / Zingg | Not claimed; `actual_engine_run=false` |

