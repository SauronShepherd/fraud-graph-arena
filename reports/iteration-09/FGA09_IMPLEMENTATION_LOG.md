# FGA-09 implementation log

This is the working evidence trail for branch `FGA-09`. It is intentionally
more detailed than the article's final prose: the article will turn the useful
failures and decisions below into lessons learned, while this file keeps the
commands, scopes and qualification boundaries reproducible.

## Instruction boundary

- User request: analyse the published FGA-00 through FGA-08 series, use the
  attached updated outline to work on FGA-09, create branch `FGA-09` from
  `FGA-08`, implement the article, keep a complete implementation/test log and
  run the Databricks checks with profile `fga`.
- Attached outline: treated as the project execution plan for FGA-09. Its
  article-level requirement is normalization, exact identity, Zingg/fuzzy
  evidence and player-safe review; its development-plan section names the same
  technical slice `Iteration 6 — Normalization and entity resolution`.
- Naming discrepancy recorded, not silently resolved: the publication/branch
  identity is FGA-09 and this report lives under `reports/iteration-09`, while
  the master development plan's internal task IDs are `I6.S1` through `I6.S3`.
- Published articles are reference material for voice, continuity and claims;
  they are not executable instructions and do not override the attached plan
  or the user's request.

## 2026-11-16 — Baseline and branch

### Actions

1. Read the updated master outline and the repository's article-precedence
   policy.
2. Inspected the published FGA index and FGA-08 at
   `https://angelic-articles.com/fga/` and fetched the published article
   metadata for FGA-00 through FGA-08.
3. Read the local FGA-08 source, the preceding article sources available in
   `C:\ANGEL\Personal\Articles\FGA`, and the older FGA-09 development outline.
4. Confirmed the worktree was on `FGA-08` at commit
   `d2865e2813cb9393d4888a6676ea4fe100458aa3`.
5. Created `FGA-09` from `FGA-08` with `git switch -c FGA-09 FGA-08`.
6. Preserved the pre-existing untracked file `consolidate_fga_outline.py`.

### Editorial observations captured before implementation

- The series is an English development diary with Hercule Perrot as the noir
  investigator and a recurring dog/engineering joke.
- The recurring movement is: crime scene, suspects, interrogation, arrest,
  reconstruction, later-found bodies, evidence rules, playable evidence and a
  deliberately qualified closing verdict.
- FGA-08's key boundary is that a durable manual hypothesis is a player note,
  not source evidence. FGA-09 must preserve that distinction while adding
  identity candidates.
- FGA-08 ends by introducing similar-looking identities. FGA-09 therefore
  starts with the missing capability, not a retrospective claim that the
  system already had fuzzy matching.
- FGA-00 through FGA-04 establish the constitutional/data vocabulary; FGA-05
  establishes the publication boundary; FGA-06/07 establish bounded graph
  presentation; FGA-08 establishes explicit, idempotent investigation
  requests. FGA-09 should add evidence to the analytical path without making
  similarity a verdict.

### Baseline checks

| Check | Command/scope | Result |
|---|---|---|
| Python focused regression | `PYTHONPATH=src python -m pytest tests/iteration_08 tests/iteration_06 -q` | `44 passed in 1.34s` |
| Frontend regression | `npm test -- --run` in `apps/web` | `59 passed across 23 files`; Node emitted repeated existing `localStorage` experimental warnings |
| Worktree hygiene | `git status --short --branch; git diff --check` | Branch `FGA-09`; only pre-existing `consolidate_fga_outline.py` was untracked; no diff-check output |
| Databricks source boundary | `scripts/qualify_investigation_boundary.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --case-id ACADEMY_T02` | `pass`, read-only; 20 records, 21 relationships, one snapshot, zero dangling endpoints |

The machine-readable baseline receipt is
`reports/iteration-09/baseline-databricks-fga08-boundary.json`.

### Baseline limitation confirmed

The active T02 publication contains two player-safe candidate rows and five
exact shared-field rows, but both are marked `actual_engine_run=false` and the
candidate semantics are curated/Zingg-like. FGA-08 still exposes
`COMPARE_IDENTITIES` as unavailable. This branch must not present those rows as
proof that a Zingg job has already run.

## Scope to implement

The implementation slice is deliberately bounded to the outline's FGA-09
coverage: deterministic normalization and placeholder classification, strict
identity rules, explainable candidate generation, player review outcomes,
idempotent persistence, the T02 action/API/UI, and a read-only Databricks
qualification. GraphFrames, a real Zingg cluster job, Genie and cross-player
authentication remain outside this slice; the public response says when the
deterministic fallback is being used.

## 2026-11-16/17 — Implementation passes and observed failures

### Normalization and engine

- Added `src/fraud_graph_arena/entity_resolution/normalization.py` with Unicode
  NFKC/casefold normalization, field-specific email/phone/text handling,
  explicit `MISSING`, `EMPTY`, `PLACEHOLDER` and `INVALID` classifications, a
  versioned placeholder registry, and original-presence metadata kept inside
  the analytical model rather than exposed to the player.
- Added the deterministic FGA-09 engine. It uses only player-safe published
  T02 identity attributes, strict verified email/phone rules for exact identity,
  name blocking plus explainable field comparisons for candidates, stable pair
  IDs, model/threshold/normalization versions, and `actual_engine_run=false`
  because this is not a Zingg job.
- Golden result: `T2-P-CIPHER-A` ↔ `T2-P-CIPHER-B` is HIGH with email/phone
  agreement. Hard counterexample: `T2-P-CIPHER-A` ↔ `T2-P-CYPHER` is MEDIUM
  with surname/name similarity but conflicting email/phone and mandatory review.
- First engine attempt failed the focused API probe because the focus filter
  tested each candidate against its own neighbour set and removed every
  neighbour. The filter was corrected to compute the block once from the
  selected record. The regression now returns the golden and hard-negative
  pairs.
- Shared device/IP/address rows are never consumed by the identity engine;
  the exact-match test asserts that exact infrastructure relationships cannot
  become identity matches.

### Persistence, economy and API

- Added durable/in-memory resolution repositories, run/review idempotency,
  SQLite restart coverage, accepted/rejected/unresolved review outcomes, and a
  player-review graph edge that explicitly says it is not a canonical merge or
  fraud verdict.
- T02 starts with the configured nine-credit Academy budget and each new
  identity analysis costs three credits. Same-key replay returns the stored
  analysis without a second charge; concurrent same-key tests settle on one
  analysis and one debit.
- First SQLite durability attempt passed in-process but failed on restart: a
  new repository context manager closed connections without committing writes.
  It now commits on success, rolls back on error, and closes the connection.
- Updated the OpenAPI contract and the superseded FGA-08 action assertion to
  include `COMPARE_IDENTITIES` alongside the existing manual hypothesis action.

### Frontend

- Added typed client contracts and a bounded investigation panel: run analysis,
  display exact observations and candidate explanations, accept/reject/leave
  unresolved, show the deterministic fallback boundary, and state the cost and
  no-merge/no-verdict rule.
- Existing frontend tests stayed green after the new imports because the new
  history call is only made when the action is actually available. Added a
  focused UI test for analysis plus candidate rejection.

### Test receipts so far

| Check | Result |
|---|---|
| `pytest tests/iteration_09 -q` | `12 passed` after the final normalization/exact-rule review |
| `pytest tests/iteration_09 tests/iteration_08 tests/iteration_01/test_openapi_contract.py -q` | `25 passed` |
| `python -m compileall -q src scripts tests/iteration_09` | pass |
| `npm run typecheck` in `apps/web` | pass |
| focused UI test `InvestigationActions.test.tsx` | `4 passed` |
| full frontend suite after the added UI test | `60 passed across 23 files`; repeated pre-existing Node localStorage warnings |

The full Python suite and live qualification are recorded below; the complete
article/source delivery is recorded in the final evidence index.

### Post-implementation qualification notes

- Full repository Python suite: post-implementation runs were `212 passed in
  605.21s (0:10:05)` and `212 passed in 904.50s (0:15:04)` before adding the
  offline evaluation regression; the final-state run including that test was
  `213 passed in 538.04s (0:08:58)` and the final exact-state run was `213
  passed in 589.86s (0:09:49)`. The long and variable duration includes
  existing live qualification/generation tests; it is not attributed to the
  FGA-09 unit tests.
- First direct invocation of the new Databricks script failed before querying
  the warehouse because a script executed by path does not import the `scripts`
  namespace the same way as pytest. Added a direct-execution fallback import;
  the retry reached the warehouse and passed.
- Live command:
  `PYTHONPATH=src python scripts/qualify_entity_resolution.py --profile fga
  --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84
  --case-id ACADEMY_T02 --report reports/iteration-09/databricks-fga09-entity-resolution.json`
  returned `status=pass`, read-only, active publication
  `3.0.0-canonical.1`/snapshot `2026.07.19.1`, 2 unique candidates, the
  golden and hard-negative pairs, 5 unique exact shared-field rows, one
  snapshot, no forbidden columns, and all observed engine flags false.
- The live exact rows are `SAME_DEVICE`, `SAME_LOGIN_IP` and
  `SAME_REGISTERED_ADDRESS`; they are deliberately not identity matches.
- The live compatibility result is
  `UNRESOLVED_SQL_WAREHOUSE_ONLY`: the `fga` profile exposes a SQL Warehouse,
  not a cluster with a qualified Zingg library. No install, job submission or
  Databricks mutation was attempted. The player/runtime therefore labels the
  deterministic fallback rather than claiming an actual Zingg run.
- A final semantic review tightened the local exact rule: one shared email or
  phone is only a candidate signal; the exact T02 identity observation needs
  the normalized contact pair (or a validated unique identifier). The public
  reason no longer calls a bare field “verified” without evidence of that
  validation.
- A contract review then added safe source provenance references to exact-match
  observations. The API exposes source refs, rule/version and field families,
  but still never exposes the normalized contact values themselves.

The implementation is complete only when the following are executable and
covered by tests:

- deterministic, idempotent field normalization with original-value
  preservation;
- a versioned placeholder registry that contributes neither exact edges nor
  fuzzy confidence;
- canonical, deduplicated exact identity evidence with provenance and masked
  player-safe summaries;
- deterministic candidate generation with blocking, field-level explanations,
  hard negatives, versioned configuration and no fraud/ground-truth features;
- reproducible offline evaluation with precision/recall, false merges, false
  splits and difficult counterexamples kept outside player responses;
- a player-facing compare-identities action, candidate review outcomes
  `ACCEPTED`, `REJECTED` and `UNRESOLVED`, and a round-scoped graph mark that is
  visibly a player review rather than a canonical merge;
- API, persistence, frontend and restart/idempotency coverage;
- a read-only Databricks qualification using profile `fga` against the active
  player-safe T02 publication.

## Test ledger

| Time | Area | Command or experiment | Result | Lesson |
|---|---|---|---|---|
| 2026-11-16 | Baseline | `pytest tests/iteration_08 tests/iteration_06 -q` | `44 passed` | FGA-08 is a clean starting point. |
| 2026-11-16 | Baseline | `npm test -- --run` | `59 passed across 23 files` | Existing localStorage warnings are environmental. |
| 2026-11-16 | Baseline | `qualify_investigation_boundary.py --profile fga ...` | `pass`, read-only | Active T02 graph was intact before edits. |
| 2026-11-16 | Engine | First focused API probe | Failed with empty candidate list | Compute the focus block once; do not test each record against its own neighbours. |
| 2026-11-16 | Persistence | First SQLite restart test | Failed after restart | A successful HTTP response is not a durability receipt; commit explicitly. |
| 2026-11-16 | Contract | FGA-08 action regression | Failed on stale available-action assertion | Iteration boundaries need contract updates when a later slice unlocks a capability. |
| 2026-11-16 | Script | First direct qualification invocation | Failed before SQL with import error | Test qualification scripts by their operator-facing invocation too. |
| 2026-11-17 | FGA-09 | `pytest tests/iteration_09 -q` | `13 passed in 1.02s` before provenance; `26 passed in 1.10s` with iteration-08/OpenAPI regression | Golden, hard-negative, offline metrics, truth firewall, provenance, idempotency, review, credits and restart are green. |
| 2026-11-17 | Evaluation | `python scripts/evaluate_entity_resolution.py --report reports/iteration-09/entity-resolution-evaluation.json` | `regression_pass=true`; precision 1.0, recall 1.0, false merges 0, false splits 0 on 3 synthetic T02 pairs | Metrics are an offline regression receipt, not a production model-quality claim. |
| 2026-11-17 | Regression | `pytest tests/iteration_09 tests/iteration_08 tests/iteration_01/test_openapi_contract.py -q` | `25 passed in 3.82s` | New API and contract coexist with the previous investigation workflow. |
| 2026-11-17 | Frontend | `npm run typecheck` | Pass | New typed identity surface compiles. |
| 2026-11-17 | Frontend | `npm run build` in `apps/web` | Pass; 61 modules transformed | Production bundle compiles after the provenance contract addition. |
| 2026-11-17 | Frontend | `npm test -- --run` | final `60 passed across 23 files` in 35.92s | Candidate review UI is covered; repeated Node localStorage warnings remain pre-existing. |
| 2026-11-17 | Full suite | `PYTHONPATH=src python -m pytest -q` | Final exact-state run `213 passed in 589.86s (9:49)`; earlier runs also green at 538.04s, 605.21s and 904.50s | Live legacy qualification makes the complete suite slow and variable but green. |
| 2026-11-17 | Databricks | `qualify_entity_resolution.py --profile fga ...` | `pass`, read-only | Two live candidates, golden/hard-negative pairs, five infrastructure exact rows, one snapshot, no forbidden columns. |
| 2026-11-17 | Hygiene | `git diff --check` | Pass | No whitespace errors in the repository diff. |
| 2026-11-17 | Tooling | `npm run typecheck` from repository root | Failed: no root `package.json` | The frontend command must run from `apps/web`; rerun there passed. |

## Final evidence index

- Branch: `FGA-09`, created from FGA-08 commit
  `d2865e2813cb9393d4888a6676ea4fe100458aa3`.
- Article source: `C:\ANGEL\Personal\Articles\FGA\FGA_09_Zingg_Me_a_River_Checked_Improved_Shortened.md`.
- Implementation log: this file.
- Databricks receipt: `reports/iteration-09/databricks-fga09-entity-resolution.json`.
- Offline evaluation receipt: `reports/iteration-09/entity-resolution-evaluation.json`.
- Baseline graph receipt: `reports/iteration-09/baseline-databricks-fga08-boundary.json`.
- Local FGA-09 tests: `tests/iteration_09/`.
- Read-only qualification script: `scripts/qualify_entity_resolution.py`.
- Runtime inventory receipt: `reports/iteration-09/databricks-fga09-runtime-inventory.json`.
- Scope limit kept explicit: actual Zingg/GraphFrames compatibility is not
  qualified by the SQL Warehouse-only `fga` profile, so the runtime uses and
  labels a deterministic fallback; no live Databricks data was mutated.

## 2026-11-17 — Second iteration cycle

### Pass 1/10 — integral review, model actual

Reviewed the article, the FGA-09 outline slice, the full entity-resolution
service/repository/API/UI surface, the existing reports and the live Databricks
profile inventory.

The pass found one valid implementation defect: `graph_with_reviews()` filtered
only `ACCEPTED` reviews before building its candidate map. If a player accepted
a candidate and later submitted a newer `REJECTED` or `UNRESOLVED` review under
a new idempotency key, the old accepted edge remained in the graph. That made
the graph disagree with the visible review history.

The pass also confirmed a material environment fact: `databricks clusters list
--profile fga` returns no clusters, while the configured resource is a stopped
SQL Warehouse. This supports the existing `UNRESOLVED_SQL_WAREHOUSE_ONLY`
compatibility boundary; it does not justify claiming a Zingg or GraphFrames
runtime.

The clean-pass counter is reset to zero because the review found a defect that
requires correction.

### Correction after pass 1

`graph_with_reviews()` now resolves the latest review per candidate before
projecting accepted player-review edges. Added an API regression covering
accepted-then-rejected review history; the latest rejection removes the review
edge from the workspace projection. The article now states this latest-outcome
rule explicitly.

The ten-pass counter remains zero and starts again after this correction.

The same pass also caught a stale player-safe reason in the engine: it still
said `Verified contact fields disagree` after the exact-rule review had removed
unproven verification language. The reason is now `Contact fields disagree;
review is required.` Unused imports in the service and qualification script
were removed. The clean-pass counter remains zero after this additional
correction.

### Clean-pass ledger after correction

1. **Pass 1/10 — functional contract:** clean. Re-read the resolution service,
   routes, response mapping, review-edge projection and API regressions after
   the correction; `27 passed` in the focused FGA-09/FGA-08/OpenAPI run. Latest
   review outcomes now agree with graph edges and no stale “verified” reason
   remains.

### Pass 2 finding and correction — training-label traceability

The next pass compared the article and implementation against I6.S3.T3 in the
master outline. The article and evaluator had a reproducible matching label
set, but the code did not expose a separate balanced training-label manifest
or verify that training pairs were disjoint from matching pairs. That left the
leakage-safe claim implicit rather than executable.

The offline evaluator now keeps two synthetic training labels outside the web
application, records positive/negative counts, checks balance and checks pair
disjointness against the matching dataset. The test asserts one positive, one
hard negative, balanced labels and `leakage_safe=True`. The article now states
the same boundary. This was a valid correction, so the ten-pass clean counter
is reset to zero again.

The focused regression suite after the correction is `27 passed in 5.62s`.

### Pass 2 additional finding — publication-boundary qualification

The Databricks qualification previously verified that each table had one
snapshot, but it did not compare that snapshot to the active publication row.
It also did not assert that every candidate was a `PERSON` or that the exact
rows remained association rows rather than identity edges. Those omissions
could let a stale snapshot or a semantically stronger relationship pass while
the receipt still looked healthy.

The read-only qualification now selects the candidate entity type and exact
snapshot, compares both table projections with the active publication
snapshot, and rejects identity-labelled exact relationships. The fixtures and
the article's live-check list were updated. This is another valid correction,
so the clean-pass counter remains zero.

### Pass 2 additional finding — latest review in the UI

The same latest-outcome rule was correct in the backend graph projection, but
the React panel used the first review returned for a candidate. After a
restart, the API history can contain an older `ACCEPTED` review followed by a
newer `REJECTED` or `UNRESOLVED` review, so the panel could display a stale
status even while the graph correctly removed the edge.

The UI now selects the latest review by timestamp and review id, and a frontend
regression covers the accepted-then-rejected history. The stale test fixture
phrase `Verified contact fields disagree` was corrected as well. This valid
correction resets the clean-pass counter to zero again.

### Pass 2 additional finding — UI retry idempotency

The next resilience check found that the UI created a fresh idempotency key on
every identity-analysis or candidate-review click. The API was safe if the
same key was retried, but the UI did not preserve that key after an ambiguous
transport failure; a player could therefore pay twice or record a duplicate
review while trying to recover a lost response.

The panel now keeps a key per unchanged analysis focus or review outcome until
the server confirms the operation, and clears it only after success. A
frontend regression simulates a failed analysis response and verifies that
the second click reuses the exact key. This valid correction resets the clean
pass counter to zero once more.

### Pass 2 additional finding — person-only focus validation

The boundary review noticed that the endpoint validated a focus against every
published record id, while the engine then discarded all non-person records.
Selecting an organization or event could therefore silently fall back to the
full person analysis instead of returning a clear subject error.

The service now accepts a focus only when its published type is
`PERSON_RECORD`; the API regression covers an organization focus and expects
`SUBJECT_NOT_AVAILABLE`. The article now makes the person-only scope explicit.
This valid correction resets the clean-pass counter to zero again.

### Pass 2 additional finding — single-field candidate generation

The exact-rule review found that the engine comment and article distinguished
single shared contact fields from exact identity, but the candidate loop
discarded a pair when that was the only signal and the names did not agree.
That made a documented review candidate disappear instead of remaining a
low-confidence, review-required observation.

The engine now treats one shared normalized email, phone or identifier as a
candidate signal while keeping the strict exact rule unchanged. A regression
proves that a shared email with conflicting names and phones is LOW,
review-required and not exact. The article now describes that boundary. This
valid correction resets the clean-pass counter to zero again.

### Pass 2 additional finding — charge/persistence failure boundary

The lifecycle review found that credits were decremented before the engine and
run repository completed. A synthetic engine failure could therefore consume
three credits without leaving a durable analysis to replay.

The round port and both adapters now support a compensating refund. Analysis
refunds the charge when computation or persistence raises and also refunds a
cross-worker duplicate that loses the idempotency race. A regression injects an
engine failure and confirms that the round returns to nine credits. The article
now records the budget boundary. This valid correction resets the clean-pass
counter to zero again.

### Pass 2 additional finding — feature configuration was implicit

The outline's I6.S3.T2 asks for an explicit, versioned feature configuration
with placeholders excluded and fraud/tactic truth fields absent. The evaluator
had the version string, but the engine's allowed identity fields were spread
across implementation details. That made the receipt less auditable than the
article claimed.

The branch now exports `fga09-identity-fields-v1` and its exact T02 allowlist
(`given_name`, `surname`, `email`, `phone`, `identifier`); the evaluator imports
the same constant, and tests assert that address/device/IP and protected fields
are excluded. The article names the same configuration and clarifies the
boundary. This valid correction resets the clean-pass counter to zero again.

The focused suite after the boundary hardening is `33 passed in 1.98s`; the
live qualification was rerun read-only and passed with the active snapshot
`2026.07.19.1`.

### Pass 2 additional finding — fuzzy-publication shape

The publication review found that candidate uniqueness alone did not prove a
safe candidate shape. A malformed row could still carry an unsupported
confidence band or blank generation metadata while satisfying the count
checks.

The read-only Databricks qualification now requires non-empty candidate IDs,
the three supported confidence bands, and explicit generation mode and
framework semantics. A fixture with `UNKNOWN` confidence now fails. This
valid correction resets the clean-pass counter to zero again.

### Clean-pass ledger restarted after the last correction

All earlier clean-pass entries above are historical and were invalidated by
later findings. The counter is zero here. From this point, each numbered pass
must review the complete current slice and remain free of a valid correction.

1. **Pass 1/10 — functional and source integrity:** clean. Re-ran the focused
   FGA-09/FGA-08/OpenAPI suite (`35 passed in 1.65s`), Python compilation and
   `git diff --check`. The current source compiles, the test contract is green,
   and no new correction was justified. Clean counter: 1/10.

2. **Pass 2/10 — frontend contract and build:** clean. `npm run typecheck`
   passed, the full frontend suite passed with `62 tests across 23 files`, and
   `npm run build` transformed 61 modules successfully. The expected Node
   `localStorage` warning remained environmental; no new correction was
   justified. Clean counter: 2/10.

3. **Pass 3/10 — offline evaluation and leakage firewall:** clean. Rebuilt the
   evaluation receipt and asserted the versioned dataset/configuration, one
   positive plus one negative training label, `balanced_training_labels=true`,
   `leakage_safe=true`, precision/recall 1.0, zero false merges/splits,
   `regression_pass=true` and `actual_engine_run=false`. The hard-negative
   bucket remains clean and no new correction was justified. Clean counter:
   3/10.

4. **Pass 4/10 — Databricks runtime and live publication:** clean. Profile
   `fga` authenticated; `clusters list` returned zero clusters; the six
   warehouses included the running `FGA-07-qualification` PRO warehouse. The
   read-only entity-resolution qualification passed with two candidates, five
   association rows, active snapshot `2026.07.19.1`, all strengthened shape
   checks true, no forbidden columns and `actual_zingg_run=false`. The runtime
   inventory is saved in `databricks-fga09-runtime-inventory.json`; no new
   correction was justified. Clean counter: 4/10.

5. **Pass 5/10 — API lifecycle, persistence and budget:** clean. The entity
   resolution API/persistence slice passed `12 tests`: one charge per unchanged
   request, conflict on changed reuse, concurrent idempotency, person-only
   focus, review revision, latest graph projection, SQLite restart durability,
   and refund after injected engine failure in both memory and SQLite. No new
   correction was justified. Clean counter: 5/10.

6. **Pass 6/10 — normalization and engine semantics:** clean. The dedicated
   engine suite passed `7 tests`: Unicode/idempotent normalization, original
   preservation, placeholder exclusion, versioned feature allowlist, strict
   contact-pair identity, association-vs-identity separation, single-field
   review candidate, golden match and hard-negative protection. No new
   correction was justified. Clean counter: 6/10.

7. **Pass 7/10 — operator-facing qualification scripts:** clean. The three
   Databricks qualification tests passed, and both qualification/evaluation
   scripts executed directly by path with their CLI help. The direct-import
   boundary remains healthy and no new correction was justified. Clean
   counter: 7/10.

### Pass 8 finding — order-dependent script imports

The isolated contract command
`pytest tests/iteration_01/test_openapi_contract.py tests/iteration_08 -q`
failed during collection because `scripts` had no package marker and the
legacy Databricks boundary test depended on another test importing the module
first. The broader mixed command had hidden that order dependency.

Added `scripts/__init__.py` so the operator scripts are a stable package in
every pytest collection order. This is a valid correction; the clean-pass
counter resets to zero.

The package marker alone did not solve an isolated pytest invocation because
that invocation did not put the repository root on `sys.path`. The pytest
configuration now declares both `.` and `src` in `pythonpath`, making script
imports deterministic with or without `PYTHONPATH=src`. The counter remains
zero until the corrected isolated command is green.

The corrected isolated command now passes `13 tests in 3.31s`, and the mixed
FGA-09/FGA-08/OpenAPI command passes `35 tests in 3.52s`. The correction is
verified; the clean-pass counter is still zero because those commands validate
the fix rather than constitute a post-correction clean ledger.

### Clean-pass ledger restarted after the import-path correction

All earlier numbered clean passes are historical and invalidated by the
order-dependent import finding. The counter is zero here again.

1. **Pass 1/10 — post-correction functional integrity:** clean. Re-ran the
   complete focused FGA-09/FGA-08/OpenAPI slice (`35 passed in 3.01s`), Python
   compilation, and `git diff --check`. No new correction was justified. Clean
   counter: 1/10.

2. **Pass 2/10 — post-correction frontend:** clean. `npm run typecheck`, the
   full Vitest suite (`62 tests across 23 files`) and `npm run build` all
   passed; the build transformed 61 modules. Only the known Node
   `localStorage` warning appeared. No new correction was justified. Clean
   counter: 2/10.

3. **Pass 3/10 — post-correction offline receipt:** clean. Rebuilt and checked
   the evaluation artifact: balanced training labels `1/1`, leakage-safe true,
   precision/recall `1.0`, zero false merges/splits, regression pass true,
   feature config `fga09-identity-fields-v1`, and actual engine run false. No
   new correction was justified. Clean counter: 3/10.

4. **Pass 4/10 — post-correction Databricks boundary:** clean. Profile `fga`
   authenticated, `clusters list` returned zero clusters, and the latest
   inventory saw six warehouses with `FGA-07-qualification` `STOPPED` by
   auto-stop. The read-only qualification nonetheless passed with the active
   publication snapshot, two candidates, five association rows, all shape and
   masking checks true, and `actual_zingg_run=false`. The runtime receipt and
   article were corrected to record the latest state; no implementation
   correction was justified. Clean counter: 4/10.

### Pass 4 finding — volatile warehouse status documentation

The live inventory changed from `RUNNING` to `STOPPED` through the warehouse's
auto-stop while the qualification still passed. The receipt and article were
updated to the latest observed state rather than retaining the earlier status.
This is a valid evidence/documentation correction, so the clean-pass counter
resets to zero again. No Databricks mutation was used to control the state.

The next clean ledger will start only after the final broad test/evidence
refresh, so volatile runtime observations are not silently mixed with an older
counter.

The final qualification woke the auto-stopped warehouse; the immediate
inventory then observed `RUNNING`. The runtime receipt was updated to that
latest observation, and the article was made state-neutral so a later auto-stop
does not change the compatibility claim. This is the last evidence wording
correction before the clean-pass ledger; the counter remains zero.

The shell-level command `PYTHONPATH=src python -m pytest -q` was also tried in
PowerShell and failed before pytest because Bash environment-assignment syntax
is not valid there. The corrected `python -m pytest -q` run used the declared
pytest paths and completed successfully.

### Final broad refresh before the clean ledger

- Full Python suite: `222 passed in 826.49s (0:13:46)`.
- Frontend refresh after the import-path correction: `62 tests across 23
  files`, typecheck and build passed.
- Focused FGA-09/FGA-08/OpenAPI refresh: `35 passed`; isolated FGA-08/OpenAPI
  invocation: `13 passed`.

### Clean-pass ledger restarted after the final broad refresh

No further code, article, report or configuration correction is planned during
the following ledger. The counter starts at zero from this exact state.

1. **Pass 1/10 — complete Python focal slice:** clean. The current source
   passes `35 tests in 3.66s`, Python compilation is clean, and `git diff
   --check` reports no whitespace errors. The CRLF warning is Git's existing
   normalization notice for OpenAPI, not a test failure. Clean counter: 1/10.

2. **Pass 2/10 — complete frontend slice:** clean. Typecheck passed, the full
   suite passed `62 tests across 23 files`, and production build transformed
   61 modules successfully. Only the known Node `localStorage` warning
   appeared. No new correction was justified. Clean counter: 2/10.

3. **Pass 3/10 — complete offline evidence receipt:** clean. The evaluator
   rebuilt the report with balanced labels `1/1`, leakage-safe true,
   precision/recall `1.0`, zero false merges/splits, regression pass true,
   feature config `fga09-identity-fields-v1` and `actual_engine_run=false`.
   Independent JSON invariants passed; no new correction was justified. Clean
   counter: 3/10.

4. **Pass 4/10 — complete Databricks evidence boundary:** clean. `fga`
   authentication succeeded, the cluster inventory remained empty, and the
   final qualification receipt remained `pass`, read-only, with active
   publication `2026.07.19.1`, two candidates, five exact association rows,
   every strengthened check true, and unresolved SQL-Warehouse-only Zingg
   compatibility. No Databricks mutation was made and no new correction was
   justified. Clean counter: 4/10.

5. **Pass 5/10 — complete API and persistence lifecycle:** clean. API and
   SQLite tests passed `12 tests`, covering single charge, unchanged replay,
   changed-key conflicts, concurrency, person-only focus, review revision,
   latest graph projection, restart durability and failure refunds. No new
   correction was justified. Clean counter: 5/10.

6. **Pass 6/10 — complete engine semantics:** clean. The dedicated engine
   suite passed `7 tests` for Unicode/idempotency, original preservation,
   placeholder exclusion, explicit feature allowlist, strict contact-pair
   identity, infrastructure separation, single-field LOW candidates, golden
   match and hard-negative protection. No new correction was justified. Clean
   counter: 6/10.

7. **Pass 7/10 — complete operator script surface:** clean. Databricks mock
   qualification tests passed `3 tests`, and both qualification/evaluation
   scripts executed directly by path with their CLI help. Imports no longer
   depend on collection order. No new correction was justified. Clean counter:
   7/10.

8. **Pass 8/10 — complete contract and iteration regression:** clean. The
   previously order-sensitive isolated command passed `13 tests in 2.82s`, and
   an independent OpenAPI inspection found all three entity-resolution paths:
   analysis, review and history. No new correction was justified. Clean
   counter: 8/10.

9. **Pass 9/10 — article, outline and privacy audit:** clean after narrowing
   the scan to the application surface. The first broad grep correctly found
   the offline evaluator's own `t02_training_examples` definition and was a
   false positive, not an app leak; the corrected audit passed. Article tokens,
   outline gates, current test counts, fallback wording and stale phrase scans
   all agree. No new correction was justified. Clean counter: 9/10.

10. **Pass 10/10 — final completion audit:** clean. Branch is `FGA-09`; final
    receipts are parseable and consistent: Databricks `pass/read_only` on
    profile `fga`, active snapshot `2026.07.19.1`, two candidates, five exact
    association rows, actual Zingg false, offline regression/leakage checks
    true, zero clusters and no mutations attempted. The full Python evidence
    is `222 passed in 826.49s`, frontend evidence is `62 passed across 23
    files`, the article has no stale final counts or wording, and `git diff
    --check` is clean apart from Git's existing CRLF normalization warning.
    No new correction was justified. Clean counter: 10/10.

### Lower-capacity audit invalidated that ledger

The required lower-capacity review was run by `Ptolemy` on `gpt-6-luna`. It
performed ten independent read-only passes over the current implementation,
article, outline and receipts. It made no file or Databricks changes. Its result
was `0/10` clean because it found valid issues that the current-model ledger had
not caught:

- `regression_pass` did not actually gate on balanced training labels or the
  leakage result, and leakage checked disjoint pairs but not shared record IDs;
- focused analysis only blocked by matching surnames, so a cross-surname shared
  email/phone/identifier candidate disappeared when the player selected one
  record;
- any equal identifier was treated as an exact identity rule even when that
  identifier was duplicated in the active snapshot;
- `phonetic_given_name` described a `SequenceMatcher` ratio, not a phonetic
  algorithm;
- browser retry keys lived only in a component ref and therefore did not survive
  an unmount/reload while the article described the interaction as safely
  idempotent;
- the article had no near-end repository/test/result receipt required by the
  outline, linked an unverified GitHub branch, and did not explicitly record the
  bounded approval decision for using the fallback while Zingg compatibility
  remained unresolved.

These are implementation, evidence and editorial corrections, not stylistic
preferences. The previous `10/10` is retained as history but is no longer a
completion claim. The clean counter resets to zero after the fixes below.

### Corrections integrated after the lower-capacity audit

1. **Evaluation firewall:** `evaluate_t02()` now requires balanced training
   labels, pair disjointness and record-ID disjointness before setting
   `regression_pass=true`. A regression test proves that an unbalanced,
   record-leaky manifest fails the gate.
2. **Focused candidate parity:** the focus path now uses the same name/contact/
   identifier candidate signal as the global pair loop. A cross-surname shared
   email remains a LOW review candidate when the player focuses either record.
3. **Identifier validation:** normalized identifiers are counted across the
   complete active person snapshot before focus filtering. A duplicated value is
   candidate evidence, not a single-field exact match. The policy is versioned
   as `fga09-unique-identifier-snapshot-v1`.
4. **Explanation honesty:** the `SequenceMatcher` signal is now named
   `similar_given_name`; no phonetic algorithm is implied.
5. **Browser retry durability:** pending identity-analysis and review keys are
   stored in round-scoped `sessionStorage`, with an in-memory fallback. Success
   removes the key; failure preserves it. A frontend test unmounts and remounts
   the panel before retrying.
6. **Compatibility decision:** the bounded fallback approval and its remaining
   Zingg gate are recorded in
   `reports/iteration-09/FGA09_COMPATIBILITY_DECISION.md`.
7. **Article correction:** the hard-negative explanation, uniqueness policy,
   fallback decision, browser-session boundary and lower-audit lessons are now
   written into the FGA-09 manuscript. The final source-code section is being
   extended with a visible branch/test/result receipt; the branch remains local
   and unpushed in this run.

### Immediate post-correction checks

- Focused Python slice: `38 passed in 6.11s`.
- Python compilation: clean for `src`, `scripts` and `tests/iteration_09`.
- Frontend typecheck: passed.
- Frontend suite: `63 passed across 23 files`.
- Frontend production build: passed; Vite transformed 61 modules.

These checks validate the corrections but do not start the new clean ledger.

### Final broad refresh after the lower-capacity corrections

- Full Python suite: `225 passed in 939.23s (0:15:39)`.
- Focused FGA-09/FGA-08/OpenAPI slice: `38 passed in 6.11s`.
- Python compilation: clean for `src`, `scripts` and `tests/iteration_09`.
- Frontend: typecheck passed, `63 passed across 23 files`, production build
  passed with 61 transformed modules. The existing Node `localStorage`
  experimental warning remains the only known warning.
- Offline evaluator receipt: balanced labels `1/1`, record- and pair-level
  leakage-safe `true`, precision/recall `1.0`, zero false merges/splits and
  `regression_pass=true`.
- Databricks `fga` qualification at `2026-11-17T17:34:20Z`: `pass`,
  `read_only=true`, active publication snapshot `2026.07.19.1`, two candidate
  rows, five association rows, all strengthened checks true, and
  `actual_zingg_run=false`. The runtime inventory still reports zero clusters,
  six warehouses and the volatile qualification warehouse as `RUNNING` at that
  observation.
- `git diff --check`: no whitespace errors; Git continues to print its existing
  CRLF normalization warning for `contracts/openapi-v1.json`.

No Databricks mutation, package installation, cluster creation or publication
write was attempted.

### Clean-pass ledger restarted after the lower-capacity corrections

The previous ledgers are historical and invalidated by the lower-capacity
findings. This ledger starts at zero from the corrected source, article and
receipts above. A pass is clean only when it finds no justified correction.

1. **Pass 1/10 — focal regression and syntax:** clean. The corrected
   FGA-09/FGA-08/OpenAPI command passed `38 tests in 1.86s`; compilation of
   `src`, `scripts` and `tests/iteration_09` passed; `git diff --check` found no
   whitespace error. The CRLF notice is Git's existing normalization warning.
   Clean counter: 1/10.

2. **Pass 2/10 — offline receipt and article count consistency:** clean. The
   JSON receipt independently confirms balanced `1/1` labels, record- and
   pair-level leakage safety, `1.0` precision/recall, zero false merges/splits
   and `regression_pass=true`. The manuscript contains the refreshed `225/38/63`
   results, the explicit `actual_zingg_run=false` boundary and the compatibility
   decision receipt. Clean counter: 2/10.

3. **Pass 3/10 — frontend contract and delivery:** clean. In the second
   post-correction frontend run, `npm run typecheck` passed, Vitest passed `63
   tests across 23 files`, and `npm run build` passed with 61 transformed
   modules. Only the pre-existing Node `localStorage` experimental warning was
   emitted. Clean counter: 3/10.

4. **Pass 4/10 — normalization and engine semantics:** clean. The dedicated
   engine file passed `10 tests`, including Unicode/idempotency, placeholder
   exclusion, the explicit feature allowlist, cross-surname focused candidates,
   duplicate-identifier protection, strict contact-pair identity, the golden
   match and hard-negative protection. `similar_given_name` is the only label
   for the ratio-based name signal. Clean counter: 4/10.

5. **Pass 5/10 — evaluation firewall:** clean. The targeted evaluation checks
   passed, and source inspection confirmed that `regression_pass` consumes both
   the balanced-label and record/pair leakage gates rather than merely
   reporting them. The unbalanced, record-leaky manifest regression remains red
   by construction. Clean counter: 5/10.

6. **Pass 6/10 — API lifecycle and persistence:** clean. The entity-resolution
   API and SQLite restart suites passed `12 tests`, covering one charge per
   unchanged request, changed-key conflicts, concurrent idempotency,
   person-only focus, latest review projection, restart durability and credit
   refunds after injected engine failure. No canonical merge or hidden truth
   crossed the response boundary. Clean counter: 6/10.

7. **Pass 7/10 — Databricks profile and qualification boundary:** clean.
   `databricks auth describe --profile fga` authenticated, `clusters list`
   returned zero clusters, and the final qualification receipt independently
   verified `pass/read_only`, publication snapshot `2026.07.19.1`, two
   candidates, five association rows, every check true and
   `UNRESOLVED_SQL_WAREHOUSE_ONLY` with `actual_zingg_run=false`. No mutation
   command was issued. Clean counter: 7/10.

8. **Pass 8/10 — browser retry envelope:** clean. The focused
   `InvestigationActions` suite passed `7 tests`, including the new unmount/
   remount analysis retry. The component persists pending keys per round in
   session storage, deletes them only after success and keeps an in-memory
   fallback when storage is unavailable; the article describes exactly that
   boundary. Clean counter: 8/10.

9. **Pass 9/10 — article, outline and claim audit:** clean after correcting the
   audit command's own heading-depth assumption. The first scan looked for
   `## The Read-Only Room at Databricks`, while the manuscript intentionally
   uses the Part heading `# Part VIII — The Read-Only Room at Databricks`; no
   artifact correction was needed. The corrected scan found the FGA-09 coverage,
   release receipt, FGA-10 hand-off, fallback boundary, uniqueness policy,
   session-storage wording and all outline requirements. No unverified GitHub
   branch link remains. Clean counter: 9/10.

10. **Pass 10/10 — final completion audit:** clean. Branch is `FGA-09`; the
    offline and Databricks receipts are parseable and internally consistent; the
    article has the final `225/38/63` counts, the local-branch qualification and
    no stale final counts or remote-branch claim; and `git diff --check` is clean
    apart from Git's existing OpenAPI CRLF normalization warning. The worktree
    contains the intended uncommitted implementation/report changes plus the
    pre-existing `consolidate_fga_outline.py`; no unrelated destructive action
    was performed. Clean counter: 10/10.

### Second lower-capacity audit invalidated that ledger

The required follow-up audit by `Ptolemy` on `gpt-6-luna` completed ten
read-only passes and returned `0/10` clean. The earlier lower-audit fixes were
mostly correct, but it found three valid gaps:

- counting identifier occurrences in the snapshot made the documented exact
  identifier exception mathematically unreachable: two records sharing a value
  necessarily made its count `2`;
- the regression-gate test combined unbalanced labels, pair leakage and record
  leakage, so it did not prove that each guard independently protected the
  release boolean;
- the outline's literal repository-tag requirement was not met, and the final
  frontend commands omitted their required `apps/web` working directory.

No files or Databricks resources were changed by that audit. The previous
`10/10` remains historical evidence only; the clean counter resets to zero for
the corrections below.

### Corrections after the second lower-capacity audit

1. **Identifier contract:** snapshot occurrence counting was removed. A
   normalized pair can use the single-field exact exception only when both
   records carry the explicit source-contract flag `identifier_validated`; the
   policy version is now `fga09-identifier-contract-v1`. Tests cover both the
   formerly missing positive exact path and the unvalidated duplicate path.
2. **Independent evaluation gates:** the regression tests now cover an
   unbalanced-but-disjoint manifest, a balanced pair-leaky manifest and a
   balanced record-ID-leaky manifest with pair-disjoint examples. The
   pair-level and record-level checks are both retained; the latter catches
   reuse even when the pair itself changes.
3. **Repository receipt:** the article now names the local implementation tag
   `fga09-v1`. It will be created only after the corrected implementation is
   committed, so the tag points to a reproducible state rather than to the
   current base commit.
4. **Frontend command reproducibility:** the release receipt now states that
   all `npm` commands run from `apps/web`, matching the operator failure already
   captured in the earlier test ledger.

The clean counter remains zero until the corrected suite, receipts, commit/tag
and article are all refreshed.

### Immediate checks after the second lower-audit fixes

- Focal FGA-09/FGA-08/OpenAPI slice: `41 passed in 3.81s`.
- Offline evaluator: passed; it now records
  `identifier_validation_version=fga09-identifier-contract-v1`.
- A deliberately parallel `compileall` invocation failed once with Windows
  `WinError 5` while pytest and the evaluator concurrently replaced the same
  `.pyc` file. The exact serial command immediately passed, as did
  `git diff --check`; no source or test failure was involved.

These checks validate the targeted corrections but do not start the next clean
ledger.

### Final broad refresh after the second lower-capacity corrections

- Full Python suite: `228 passed in 897.60s (0:14:57)`.
- Focused FGA-09/FGA-08/OpenAPI slice: `41 passed in 3.81s`.
- Python compilation: clean when run serially; the earlier concurrent `.pyc`
  collision is recorded above.
- Offline evaluator receipt: `identifier_validation_version` is
  `fga09-identifier-contract-v1`; balanced labels `1/1`, leakage-safe true,
  precision/recall `1.0`, zero false merges/splits and `regression_pass=true`.
- Databricks `fga` qualification at `2026-11-17T18:08:23Z`: `pass`,
  `read_only=true`, publication snapshot `2026.07.19.1`, two candidate rows,
  five association rows, every strengthened check true and
  `actual_zingg_run=false`. The runtime receipt observed zero clusters, six
  warehouses and the auto-stop qualification warehouse as `RUNNING` at that
  moment.
- Local repository commit: `a5f572a` (`Implement FGA-09 entity resolution
  slice`); local tag `fga09-v1` points to that implementation commit. The
  pre-existing `consolidate_fga_outline.py` remains intentionally untracked.

No Databricks mutation, package installation, cluster creation or publication
write was attempted.

### Clean-pass ledger restarted after the second lower-capacity corrections

All previous ledgers are historical and invalidated by the identifier-contract,
independent-gate, tag and command-directory corrections. This ledger starts at
zero from the corrected committed implementation and refreshed receipts.

1. **Pass 1/10 — focal regression, compilation and hygiene:** clean. The
   corrected FGA-09/FGA-08/OpenAPI command passed `41 tests in 22.02s`; serial
   compilation passed; and `git diff --check` found no whitespace error. The
   only Git output remains the existing OpenAPI CRLF normalization warning.
   Clean counter: 1/10.

2. **Pass 2/10 — offline receipt and article continuity:** clean. The receipt
   contains `fga09-identifier-contract-v1`, balanced `1/1` labels, leakage-safe
   true, perfect fixture precision/recall, zero false merges/splits and
   `regression_pass=true`. The manuscript's final `228/41/63` counts, local
   `fga09-v1` tag and identifier policy agree with the machine-readable evidence.
   Clean counter: 2/10.

3. **Pass 3/10 — frontend contract and delivery:** clean. From `apps/web`,
   `npm run typecheck` passed, Vitest passed `63 tests across 23 files`, and
   `npm run build` passed with 61 transformed modules. The only output beyond
   the successful result was the known Node `localStorage` experimental warning.
   Clean counter: 3/10.

4. **Pass 4/10 — normalization, identifier contract and engine semantics:**
   clean. The dedicated engine file passed `13 tests`, including the reachable
   source-validated identifier exact path, unvalidated duplicate protection,
   cross-surname focused candidates, placeholder handling, strict contact-pair
   identity, the golden match, hard negative and player-safe field allowlist.
   Clean counter: 4/10.

5. **Pass 5/10 — evaluation firewall and regression gates:** clean. The four
   targeted evaluation tests passed, including the golden regression and the
   isolated unbalanced, pair-leaky and record-ID-leaky manifests. A direct
   metrics check confirms the live fixture is balanced, leakage-safe and green.
   Clean counter: 5/10.

6. **Pass 6/10 — API lifecycle and persistence:** clean. The API and SQLite
   restart suites passed `12 tests`: one charge per unchanged analysis,
   conflicts for changed requests, concurrency, person-only focus, latest
   review projection, restart durability and refunds after engine failure all
   remain intact. Clean counter: 6/10.

7. **Pass 7/10 — Databricks profile and read-only boundary:** clean.
   `databricks auth describe --profile fga` authenticated, `clusters list`
   returned zero clusters, and the final receipt verified `pass/read_only`,
   publication snapshot `2026.07.19.1`, two candidates, five association rows,
   every check true and the unresolved SQL-Warehouse-only Zingg status with
   `actual_zingg_run=false`. No mutation command was issued. Clean counter:
   7/10.

8. **Pass 8/10 — browser retry envelope:** clean. The focused
   `InvestigationActions` suite passed `7 tests`, including the remount retry
   that reads the same pending key from round-scoped session storage. Success
   deletes the key, failure preserves it, and the in-memory fallback remains
   documented. Clean counter: 8/10.

9. **Pass 9/10 — article, outline, tag and claim audit:** clean. The corrected
   scan found the release receipt, local branch, local `fga09-v1` tag, explicit
   `apps/web` working directory, identifier-contract version, FGA-10 hand-off,
   fallback boundary and all FGA-09 outline requirements. No stale final count
   or unverified remote-branch claim remains, and the tag resolves to `HEAD`.
   Clean counter: 9/10.

10. **Pass 10/10 — final completion audit:** clean before packaging the final
    ledger commit. Branch is `FGA-09`; the local tag resolves to the current
    implementation commit; offline and Databricks receipts are parseable and
    green; the article has the final `228/41/63` evidence, repository tag and
    frontend working directory; and `git diff --check` is clean apart from
    Git's known OpenAPI CRLF normalization warning. The only untracked path is
    the preserved pre-existing `consolidate_fga_outline.py`. Clean counter:
    10/10.

### Third lower-capacity audit found a receipt traceability gap

The third required audit by `Ptolemy` found one valid issue after ten passes:
the Databricks receipt still carried the pre-implementation `source_commit`
`d2865e2`, even though the local implementation tag pointed to `a5f572a`. The
SQL result itself was green and read-only, but the artifact could not yet prove
that it had been generated from the tagged implementation.

This is a provenance correction, not a Databricks data correction. The clean
counter resets to zero again.

### Receipt traceability correction

The read-only qualification was rerun from the committed implementation at
`a5f572a`, which is the commit addressed by local tag `fga09-v1`. The refreshed
receipt now records:

```text
run_at_utc:    2026-11-17T18:18:00.388009+00:00
source_commit: a5f572a1f97db73c938c99f58e1f7808939c74c0
status:       pass
read_only:    true
actual_zingg_run: false
```

The runtime inventory was refreshed at `2026-11-17T18:18:00Z`; it observed zero
clusters, six warehouses and the auto-stop qualification warehouse as
`RUNNING`. The article now names the same source commit beside the tag. A later
documentation-only commit will not change the code commit that the receipt
qualifies.

### Clean-pass ledger restarted after receipt traceability correction

All prior ledgers are historical and invalidated by the provenance gap. This
final ledger starts at zero from the corrected receipt, article and tag.

1. **Pass 1/10 — focal regression, compilation and hygiene:** clean. The
   focused FGA-09/FGA-08/OpenAPI command passed `41 tests in 7.65s`, serial
   compilation passed, and `git diff --check` found no whitespace errors. Git's
   only output was the expected CRLF normalization notice for the refreshed
   Databricks JSON. Clean counter: 1/10.

2. **Pass 2/10 — receipt-to-tag traceability:** clean. The offline receipt is
   balanced, leakage-safe and green; the Databricks receipt is `pass/read_only`,
   all checks are true, and its `source_commit` exactly matches the commit
   addressed by `fga09-v1`. The article names the same commit beside the local
   tag. Clean counter: 2/10.

3. **Pass 3/10 — frontend retry surface:** clean. From `apps/web`, typecheck
   passed and the focused `InvestigationActions` suite passed `7 tests`; the
   known Node `localStorage` experimental warning remains environmental. The
   session-storage implementation and remount test still match the article's
   stated retry boundary. Clean counter: 3/10.

4. **Pass 4/10 — engine rules:** clean. The dedicated normalization/engine
   suite passed `13 tests`, including the positive source-validated identifier
   path, the duplicate-without-contract negative, focus candidate parity,
   exact contact-pair semantics, placeholders, golden match and hard negative.
   Clean counter: 4/10.

5. **Pass 5/10 — evaluation gates:** clean. The four targeted gate tests passed
   and a direct metrics calculation confirmed that the fixture remains balanced,
   pair/record leakage-safe and green. No guard is merely displayed without
   feeding the regression boolean. Clean counter: 5/10.

6. **Pass 6/10 — API lifecycle and persistence:** clean. The API and SQLite
   suites passed `12 tests`, retaining idempotent charging, conflict detection,
   concurrency protection, person-only focus, latest-review projection,
   restart durability and failure refunds. Clean counter: 6/10.

7. **Pass 7/10 — final Databricks provenance and boundary:** clean. Profile
   `fga` authenticated, `clusters list` returned zero clusters, and the
   refreshed receipt is `pass/read_only`, source-linked to `a5f572a`, with two
   candidates, five associations, all checks true and no actual Zingg run. The
   SQL-Warehouse-only compatibility limit remains explicit. Clean counter:
   7/10.

8. **Pass 8/10 — player-safe contract and Databricks masking:** clean. The
   three Databricks entity-resolution tests passed, and an application-surface
   scan found no `identifier_validated` contract metadata leaking through the
   service, API models, mappers or frontend contracts. The receipt still has no
   forbidden player columns. Clean counter: 8/10.

9. **Pass 9/10 — article, outline and continuity audit:** clean. The manuscript
   contains the FGA-09 structure, final release receipt, local branch/tag,
   source-commit linkage, `apps/web` command directory, fallback limitation and
   FGA-10 hand-off. The updated outline's required FGA-09 vocabulary, evidence,
   tag, command and runnable-result rules are all covered. No stale count or
   remote-branch claim remains. Clean counter: 9/10.

10. **Pass 10/10 — final completion audit:** clean. Branch `FGA-09` and local
    tag `fga09-v1` are stable; the refreshed Databricks receipt is source-linked
    to `a5f572a`, the offline receipt is green, the final article contains
    `228/41/63`, and `git diff --check` has no whitespace errors beyond the
    known CRLF normalization warning. The only untracked path remains the
    preserved pre-existing `consolidate_fga_outline.py`; the refreshed receipt,
    runtime inventory and this final ledger are the intended documentation
    changes awaiting their final commit. Clean counter: 10/10.

### Final lower-capacity audit

`Ptolemy`/`gpt-6-luna` repeated ten independent read-only passes after the
receipt traceability correction and found `10/10` clean with no valid issue.
It verified that:

- the Databricks receipt is `pass/read_only` on profile `fga`, and every check
  is true;
- `source_commit=a5f572a1f97db73c938c99f58e1f7808939c74c0` equals the commit
  addressed by local tag `fga09-v1`;
- the SQL-Warehouse-only Zingg boundary and `actual_zingg_run=false` remain
  explicit;
- the article's `228/41/63` counts, `apps/web` directory, tag and source
  commit are consistent;
- the identifier contract, duplicate protection and separate gate tests remain
  present.

This audit made no file, SQL or Databricks change. The documentation commit
that follows is deliberately separate from the implementation tag: the tag
continues to identify the code commit that the receipt qualifies.
## 2026-11-26 — Bidirectional article/implementation consistency pass

The article was audited against the checked-out `FGA-09` branch in both
directions: every technical claim was traced to code and a test/receipt, and
the implemented entity-resolution surface was checked for coverage in the
article.

### Findings and corrections

- The article had incorrectly said that the example did not claim or test
  Unicode NFKC. The branch does use `unicodedata.normalize("NFKC", ...)` in
  `entity_resolution/normalization.py`; the normalization regression now
  explicitly covers full-width characters and a ligature, in addition to
  idempotency and original preservation. The article now explains that this is
  FGA's fallback preprocessing, versioned as `fga09-norm-v1`, not a Zingg
  default.
- The feature description incorrectly implied that `identifier` was admitted
  only after source validation. The implementation allows it as a candidate
  signal, while `fga09-identifier-contract-v1` is required before a single
  identifier can create an exact identity observation. The article now states
  that distinction.
- The article incorrectly said that the action appeared only with a selected
  PERSON record. The API/UI makes it available for active T02, with an optional
  PERSON focus; an un-focused bounded analysis is also implemented and tested.
- The article claimed same-tab reload coverage although the regression directly
  covers panel unmount/remount. The wording now matches the executed test.
- The local fallback's `similar_given_name` label is now explicitly separated
  from the live curated publication's `phonetic_given_name` label; the latter
  is not presented as fallback or Zingg execution.
- The Databricks compatibility wording now records only the inventory checks
  actually executed. Spark/Scala/artifact/job compatibility remains unresolved
  because profile `fga` exposes no qualified cluster.

### Checks rerun after the corrections

| Check | Result |
|---|---|
| Focused Python regression | `41 passed in 6.47s` (`iteration_09`, `iteration_08`, OpenAPI contract) |
| Offline evaluator | `regression_pass=true`; balanced `1/1`, leakage-safe, precision/recall `1.0`, zero false merges/splits; receipt refreshed |
| Unicode coverage | Full-width and ligature NFKC cases pass; the test count remains within the 41-test focused slice because assertions were added to the existing normalization test |
| Frontend | `npm run typecheck` passed; `63 passed across 23 files` from `apps/web` |
| Databricks recheck | Read-only qualification stopped before SQL with `invalid_grant` during token refresh; no mutation attempted |

The current failed Databricks receipt is
`reports/iteration-09/databricks-fga09-entity-resolution-current.json`.
The historical 17 November receipt remains the only green live qualification
and continues to carry `actual_engine_run=false`.

### Additional UI consistency correction

The article also described the player panel distinguishing missing fields from
disagreements. The API and engine already carried both arrays, but the React
panel did not render `missing_fields`. The panel now renders a player-safe
`missing: ...` line, and the existing identity-panel test supplies a missing
phone and asserts that it is visible.

After this correction:

- the focused Python slice remained `41 passed`;
- the frontend typecheck passed;
- the frontend suite passed `63 tests across 23 files`;
- the production frontend build passed with 61 transformed modules.

The bidirectional traceability receipt is
`reports/iteration-09/FGA09_ARTICLE_IMPLEMENTATION_MATRIX.md`; the article's
source list now points to it alongside the implementation log and qualification
receipts.

## Final ten-pass consistency closure

After the UI and test corrections, ten complete review passes were performed
from the same final state. The passes covered article/code anchors, focused
Python tests and compilation, API/persistence, frontend, Databricks boundaries,
fixture/evaluator semantics, player-safe output, editorial structure,
receipt/tag traceability and final hygiene. Two audit false positives were
corrected in the audit procedure itself: one searched for a matrix-only phrase,
and one compared an annotated tag object instead of `fga09-v1^{commit}`;
neither required an artifact change.

The final broad run was:

- full Python suite: `228 passed in 862.25s (0:14:22)`;
- focused FGA-09/FGA-08/OpenAPI slice: `41 passed`;
- frontend: typecheck passed, `63 passed across 23 files`, production
  build passed;
- article content validation: 108 canonical articles validated;
- offline evaluator: `regression_pass=true`, precision/recall `1.0`,
  zero false merges/splits;
- Databricks recheck: `invalid_grant` before SQL, read-only, no mutation.

The ten-pass sequence ended clean. The current working tree contains only the
intended FGA-09 consistency changes plus pre-existing unrelated untracked
review-render files; no unrelated file was altered.

## 2026-11-26 — Editorial density pass

The supplied local preview showed that `### The first suspect was punctuation` had
too much explanatory weight in three long italic paragraphs. The content was
correct, but the paragraph architecture made the reader process the case, the
NFKC definition, the field rules and the idempotency proof in large blocks.

The article was revised without changing the implementation claim or adding
new behavior: the scenario is now one paragraph, the normalization pipeline
and NFKC explanation each have their own paragraph, the four field rules are
a short scan-friendly list, and the idempotency test lands in two shorter
beats. The noir voice and the final joke were preserved.

Checks after the edit:

- `npm run content:validate` — 108 canonical articles validated.
- Article slice inspection — all normalization anchors remain present:
  `unicodedata.normalize("NFKC", ...)`, `fga09-norm-v1`, field-specific
  rules, engine identity allowlist and the Zingg-default caveat.
- Scope — no implementation, test, fixture or Databricks artifact changed in
  this editorial pass.
