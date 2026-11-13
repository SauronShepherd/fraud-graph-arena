# FGA-07 audit log

**Status:** in progress — this is an execution log, not a closure report.  
**Scope:** FGA-07 implementation, cumulative FGA-00…FGA-07 regression, live Databricks qualification with profile `fga`, and reconciliation material for the FGA-07 article.  
**Rule:** an item is recorded as passed only when the command actually completed and its evidence is preserved.

## 2026-11-13 — baseline

- Branch: `FGA-07`.
- Worktree: clean and tracking `origin/FGA-07`.
- Starting source commit: `24e76a2 Reconcile FGA07 qualification report`.
- Existing local evidence was green for the recorded Python/frontend/browser checks, but the release bundle still correctly classified live Databricks qualification, non-admin security, and cumulative closure as pending.
- Existing Databricks facts before this run:
  - profile `fga` authenticated successfully;
  - the authenticated principal is an administrator;
  - warehouse `FGA-07-qualification` (`eded42c9d0a69b84`) exists;
  - topology qualification had already passed `44/44` objects with no column mismatches;
  - package loading had previously stopped during the first package transfer;
  - package counts had `32` mismatches because the load was incomplete;
  - failure qualification had raised `KeyError: data_array`;
  - security qualification was `not_qualified` because an admin cannot prove denial.

## 2026-11-13 — local corrections made during this audit

### Graph contract and view

The frontend `Graph` contract did not declare backend metadata for partial projections. Added optional fields for `partial`, omitted node/edge counts, and relationship filters. The viewport now announces omitted content as a partial view.

The viewport could leave a selected node or connected edge selected after the node was collapsed. Collapse now clears selection through the controlled callbacks. Added component coverage for partial announcements and selection clearing.

Result: `apps/web/src/board/GraphViewport.test.tsx` — `10 passed`.

### Databricks transfer

The original recursive `databricks fs cp` had no timeout, retry, or bounded failure. Replaced it with:

- physical canonical files only;
- explicit staging-directory creation with `fs mkdirs`;
- per-file transfer;
- 120-second transfer timeout;
- three attempts per file;
- explicit error identifying the file that failed.

This also exposed that a package directory is not always created automatically in the Databricks Volume. Explicit `mkdirs` fixed that path failure.

### Databricks SQL execution

The SQL adapter accepted `PENDING` statements as if they had completed and had no timeout on the CLI process. It now:

- bounds SQL submission time;
- polls `PENDING`/`RUNNING` statements;
- bounds polling time;
- raises a structured adapter error for non-success states;
- has unit coverage for pending-to-success and submission timeout.

The topology qualifier received the same bounded submission/polling behavior.

### Failure qualification

The failure script assumed every SQL response contained `result.data_array`. It now polls SQL statements and emits a structured `blocked` report when a statement does not succeed instead of crashing with `KeyError`.

### Publication activation

The first live candidate exposed a real SQL defect in the active-pointer `MERGE`: the source `SELECT` used positional expressions without aliases, while the merge referenced `source.case_id`, etc. The merge now aliases every pointer column and uses explicit update/insert columns.

### Candidate validation

The validator compared `COUNT(*)` for the entire historical table with the candidate publication count. That made every second package fail as soon as the first package was active. The count query is now scoped with `WHERE _publication_id = <candidate>` while retaining separate checks for tags, run correlation, snapshots, references, and keys.

### Lifecycle result propagation and reuse

- `record_databricks_publication.py` previously returned exit code `0` even when its report status was `fail`; it now returns non-zero for failed lifecycle states.
- The all-package qualifier now inspects the lifecycle result instead of treating a subprocess success as publication success.
- Already active/validated publications are reused without re-uploading.
- Rejected publication records can be removed before a controlled retry.
- Independent physical-table inserts use bounded concurrency (`8` workers) after transfer.

## Tests executed after corrections

- Databricks adapter, transfer, activation, publication script, and Graph API focused suite: `25 passed`.
- Additional adapter/publication focused suite before the final validation assertion correction: `9 passed`.
- Graph viewport suite: `10 passed`.
- Frontend typecheck: passed.
- Frontend production build: passed.
- Python compilation of changed Databricks scripts: passed.

### Corpus gate repair

The first cumulative FGA-04 gate run failed on real canonical-data contract errors:

- 10 relationship packages contained date-only `event_time` values in `authoring` and `published` (and the corresponding `genie` relationship projections).
- T3 contained `2026-03-31T23:30:00-04:00` in two attribute tables, while the canonical timestamp contract requires an explicit UTC `Z` instant.

The data was normalized without changing the represented dates or row counts: date-only events now use `T00:00:00Z`, and the T3 value is represented as the equivalent `2026-04-01T03:30:00Z`. Package manifests and `SHA256SUMS.txt` were regenerated. A new governed-corpus regression test now validates all 13 packages through the strict validator.

The rerun passed: FGA-04 contract valid, corpus complete, 13/13 packages valid, 32 tables, `fully_qualified: true`.

The final local split after the corpus and governance-fixture repairs is `169` non-governance Python tests plus `11` governance tests: `180 passed`. Frontend Vitest is `55 passed` across 22 files; standard Playwright is `15 passed`; qualification Playwright is `11 passed`; frontend typecheck and build pass.

The first post-corpus full Python run reached `178 passed, 4 failed` only because governance fixtures copied generated `.vite` and browser artifacts until Windows reported `WinError 112` (disk full). The affected four governance cases passed after cleanup. `copy_repository()` now excludes `.vite`, `test-results`, `playwright-report`, and `coverage`, and the split rerun passed with stable free space.

## Live Databricks observations

### First corrected lifecycle attempt

1. Sandbox topology recreated successfully: `44/44`, no missing objects, no extra objects, no column mismatches.
2. `A1_BONE_LEDGER` loaded and published successfully.
3. `A2_DOWNLINE` was initially rejected. The error was the unscoped historical row count described above; it was not a source-data corruption finding.
4. `A3_PHANTOM_VET` initially failed before loading because the package's `analytics` staging directory did not exist.
5. The run was stopped after the diagnostic was captured; no claim of complete package qualification was made.

### Second corrected lifecycle attempt

1. Sandbox topology recreated again successfully: `44/44`.
2. `A1_BONE_LEDGER`: `ACTIVE`.
3. `A2_DOWNLINE`: `ACTIVE`.
4. The package runner was then resumed with bounded two-package concurrency. It reused the four already-active packages and processed the remaining packages in parallel pairs.
5. Final result: `13/13` package results reported `status: pass`; every lifecycle reached `PUBLISHED`. The report records four `REUSED` active publications and nine newly completed publication lifecycles.

The final live package evidence is in `databricks-fga07-all-packages.json`.

### Post-load reconciliation and repeatability

1. Package-count reconciliation passed for all `32` physical tables with `0` mismatches.
2. Ten repeat runs completed with two package workers: `10` attempts × `13` packages, `0` failures. Active publications were reused idempotently.
3. Failure injection passed: the failed run was not active and the active publication pointer was unchanged before and after the rejection.
4. Security qualification was executed with profile `fga` and correctly returned `not_qualified`; the principal is an admin, so the run cannot prove non-admin denial.

Evidence files: `databricks-fga07-counts.json`, `databricks-fga07-repeat.json`, `databricks-fga07-failure.json`, and `databricks-fga07-security.json`.

## Still pending after this log entry

- Non-admin security qualification. Current `fga` remains administrator-only evidence.
- Request-level performance and large-graph qualification.
- Manual accessibility/product-owner acceptance.
- Current-SHA cumulative release manifest is now generated and clean; formal closure remains false because security is `not_qualified`.
- Final article reconciliation and rendered article review.

## OpenAPI contract drift found and corrected

The first single-command Python regression run after the prior split validation completed with `183 passed, 1 failed` in `16:51`. The only failure was `tests/iteration_01/test_openapi_contract.py::test_committed_openapi_matches_application_contract`: the checked-in `contracts/openapi-v1.json` was stale compared with the schema generated by the current application, including missing `additionalProperties` constraints.

The repository's canonical exporter, `scripts/export_openapi.py`, regenerated `contracts/openapi-v1.json`. The focused contract regression then passed (`1 passed`). This is a contract-artifact correction, not a relaxation of the test. The full suite must be rerun after committing this generated artifact; the prior full run is therefore recorded as `183 passed, 1 failed`, not as a green release.

The post-correction full Python suite was rerun against the committed artifact and passed: `184 passed in 986.70s (0:16:26)`.

The evidence index was then reconciled so it no longer presents the earlier failed Databricks attempts or the pre-contract-test counts as current results. The repository remains on branch `FGA-07`, with the pushed HEAD recorded by the final handoff checks, clean worktree, final live receipts, and explicit non-admin/manual-acceptance limitations above. The release manifest records the source tree SHA from the commit immediately before its own generated-artifact commit, as intended by the exporter.

The article was reconciled with this final evidence pass: it now records the OpenAPI artifact correction and the green `184`-test Python regression, while preserving the non-admin authorization limitation. No claim of total release closure was added.

The release-lineage verifier was rerun on the final branch and passed: immutable `fga-iteration-00-r1` is an ancestor of the current FGA-07 HEAD and its recorded FGA-00 evidence remains passing and closure-eligible.

## Cumulative FGA06 closure-validator repair

The next closure pass exposed a real tooling defect: `scripts/validate_iteration_06_closure.py` rejected the current FGA-07 branch because it required every path between the historical FGA06 source commit and the current descendant HEAD to live under `reports/iteration-06/`. That rule was valid only for the original two-commit FGA06 closure shape; it incorrectly rejected legitimate FGA07 source, test, and report descendants.

The validator now requires the source/evidence range to contain FGA06 evidence paths while allowing later cumulative paths. Empty ranges and ranges without FGA06 evidence still fail. Three regression cases were added, and the focused closure/renderer suite passed `5` tests. The clean-tree gate will be rerun after this correction is committed.

After commit `d786d17`, the clean-tree FGA06 closure validator passed with no errors; the historical source commit remains an ancestor of the cumulative FGA07 branch.

The complete Python regression suite was rerun after the validator repair and passed: `187 passed in 682.03s (0:11:22)`. This includes the three new cumulative-descendant scope tests.

The frontend qualification was rerun on the current HEAD and passed: Vitest `55/55` across 22 files, typecheck, production build, standard Playwright `15/15`, and qualification Playwright `11/11`. The qualification refreshed the committed FGA06 renderer-performance/comparison JSON and manual-capture PNG evidence; all generated qualification reports remained `PASS`.

## Final live rerun against commit `a2b35c5`

- Databricks profile `fga`, dedicated warehouse `eded42c9d0a69b84`, sandbox namespace `sda_dev.sandbox`.
- Topology recreation passed `44/44` with no missing objects, extras, or column mismatches.
- All 13 canonical packages completed the full lifecycle through `PUBLISHED`; the report is source-qualified against `a2b35c51f30454aba5676f9e8df3aa01b225c408`.
- Active package reconciliation passed for all 32 physical tables with `0` mismatches.
- Ten repeat rounds × 13 packages passed with two workers; all repeats reused the expected active publications and recorded `0` failures.
- Failure injection passed: the failed candidate remained inactive and the active publication pointer stayed identical before and after.
- Security remained `not_qualified` by design: profile `fga` is an administrator principal, so it cannot prove the non-admin denial requirement.
- The dedicated warehouse was stopped after the live qualification (`state: STOPPED`).

## Final repository and article handoff

- Final branch: `FGA-07`.
- Final pushed HEAD: `dbadea75bbeb9e1a6f53b7d8a01afbbdb75f40d0`; local HEAD and `origin/FGA-07` match; worktree clean.
- The FGA-07 article was updated with the verified corpus and Databricks qualification facts, while retaining the explicit limitation that admin evidence cannot prove non-admin denial.

## Candidate facts for later article reconciliation

These are notes, not yet final article prose:

- The live qualification found and repaired an activation `MERGE` alias defect.
- The live qualification found and repaired a validator bug that confused historical rows with candidate rows.
- Volume transfers required explicit directory creation and bounded per-file retries.
- The graph UI now exposes partial-projection omissions and clears selection when collapsing the selected evidence.
- The live Databricks run has proved all 13 packages, zero-mismatch counts, repeatability, and failure isolation. Non-admin denial remains unproved until a distinct non-admin identity is supplied.
- The first cumulative gate exposed and the repair closed a real timestamp-quality defect in the checked-in canonical corpus; this is now a regression-tested invariant.
- Graph DTOs now bound safe text fields as well as node/edge cardinality; the API regression suite verifies that an oversized safe summary is rejected (`23` focused graph tests passed).

## Evidence files

- [FGA-07 validation summary](./README.md)
- [local validation JSON](./local-validation.json)
- [Databricks schema evidence](./databricks-fga07-schema.json)
- [Databricks package evidence](./databricks-fga07-all-packages.json)
- [Databricks count evidence](./databricks-fga07-counts.json)
- [Databricks security evidence](./databricks-fga07-security.json)
