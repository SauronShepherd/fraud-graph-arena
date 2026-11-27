# FGA-20 implementation log — Nothing Compares 2 MVP

## Scope and authority

- Implementation branch: `FGA-20`, based on the final FGA-19 implementation branch. Functional implementation commit: `8afe50ca12ec574b7a539370b0987610a7870402`.
- Article branch: `FGA-20` in the `angelic-articles` checkout. Article commit: `b8ff2a9ab46bb7cc850a182c54fe234c405f5e8d`.
- Assets branch: `FGA-20` in the `angelic-assets` checkout. Artwork commit: `eb7b295d7c573679594f0b95d5efa17b34bb4673`.
- The Master Series Outline is authoritative and names this retrospective FGA-20. The older Development outline labels the same retrospective block FGA-19; the discrepancy is recorded rather than silently renumbering the series.
- FGA-20 is a retrospective and acceptance article. It adds a release-level evidence contract and report; it does not invent another product feature or claim that the existing Databricks boundary executed a graph engine.
- The article claims only behaviour represented in this branch or in a stored test/qualification receipt. The release implementation remains inherited from FGA-19; the new FGA-20 delta is the acceptance contract, reproducible report, focused tests and article evidence trail.

## Branches created before implementation

| Repository | Branch | Base | Remote status |
| --- | --- | --- | --- |
| `fraud-graph-arena` | `FGA-20` | `origin/FGA-19` | Created and pushed before code changes |
| `articles` | `FGA-20` | `origin/FGA-19` | Created and pushed before article changes |
| `angelic-assets` | `FGA-20` | `origin/FGA-19` | Created and pushed before artwork changes |

## What was implemented

1. Added `contracts/retrospective/fga20-mvp-acceptance.schema.json`, a strict report contract for plan-versus-reality, the qualified player journey, measurable outcomes, exclusions, next-season hypotheses and the final verdict.
2. Added `scripts/qualify_fga20_mvp.py`, which validates the FGA-19 release manifest, consumes the read-only Databricks receipt, reruns the Academy validation runner, validates all local case packages, cross-checks the public boundary and writes a schema-validated FGA-20 acceptance report.
3. Added three FGA-20 tests covering the report schema and pass status, the local/remote boundary, and explicit unmeasured questions and next-season hypotheses.
4. Added the final report at `reports/iteration-20/fga20-mvp-acceptance-current.json`.
5. Added the article ↔ implementation matrix and this implementation log so every material article claim points to code and evidence.
6. Added the newspaper cover and final case-file infographic in the assets branch, pinned to the exact artwork commit from the article.
7. Added the direct, unlisted article route and kept the series publication conventions intact.

## Iteration and failure ledger

### Baseline and branch discipline

- The previous FGA-19 release was inspected before branching. Its final receipts remain the inherited baseline: `313 passed` in the full Python regression, `27` frontend files/`71` tests, `18` browser E2E tests, container startup smoke and the read-only Databricks qualification.
- FGA-20 branches were created and pushed in all three repositories before implementation. No previous branch was renamed, reused or overwritten.
- The structure comparison against FGA-16 through FGA-19 established the article invariant: three short italic opening paragraphs; Parts I–VIII; `The Arrest`; `Case Closed?`; `Next in the Series`; one separator; `Source Code`; a release receipt; one separator; final infographic and caption.

### Acceptance implementation

- The first report was generated against the FGA-20 functional revision and validated as `pass`.
- The first report still pointed at the inherited FGA-19 Databricks receipt. The report builder was corrected to consume the FGA-20-named remote receipt, and the report was regenerated with source revision `8afe50ca12ec574b7a539370b0987610a7870402`.
- The final checked-in script content is identical to the working tree that produced the passing report. After the script/report commit (`3a2baef`), the report's `source_revision` was aligned to that published branch HEAD and rechecked through the strict report schema and focused acceptance tests.
- The report deliberately separates local player-journey evidence from the remote public data boundary. `actual_engine_run=false`, `truth_source_queried=false` and `databricks_read_only=true` remain explicit.
- The latest local Academy qualification returned `PASS`, twelve scenarios, a passing complete game loop, fourteen local package smoke journeys, persistence recovery and idempotent replay. The current run took `72.31 seconds`; the article uses a deliberately rounded description rather than presenting that duration as an SLO.

### Databricks qualification

- Command run from this branch:

  `python scripts/qualify_fga19_release.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --manifest reports/iteration-19/fga19-release-manifest-current.json --report reports/iteration-20/databricks-fga20-public-boundary-current.json`

- Result: `PASS`; profile authentication succeeded; thirteen canonical packages passed active-publication, snapshot, count, endpoint and safe-column checks; the query policy remained `SELECT`-only; no protected truth was queried; no mutation was performed; no real graph-engine execution was claimed.
- The remote receipt reports `35,874` public-boundary records and `80,349` relationships across the thirteen qualified packages. The smallest case has ten records/fourteen relationships; the largest has `9,537` records/`25,112` relationships.
- The FGA-20 acceptance report consumes this receipt and cross-checks its status, profile, read-only boundary, forbidden columns and package results.

### Test runner findings and repair

- The new FGA-20 test file passed independently: `3 passed in 0.29s`.
- The inherited FGA-19/FGA-18/OpenAPI focused set passed with the FGA-20 tests when the third-party `pytest-randomly` plugin was disabled: `20 passed in 2.37s` on the final run. The default randomized combined invocation exited without a failure summary after thirteen dots; the tests themselves passed independently and in the deterministic focused invocation. This is recorded as a runner/plugin interaction, not hidden as a product failure.
- A default full backend run collected `316` tests but terminated while the inherited narrative-package validator was validating the large case packages. The process ended with exit code `-1` and no assertion traceback. `faulthandler` snapshots showed the existing validator inside CSV receipt counting, SQL lexical validation and safe-projection scanning; no FGA-20 assertion failed.
- A detached per-package diagnostic confirmed zero validation errors for every package reached, including `senior-crypto-kennel-long-con` and `senior-love-leashes-offshore`. The FGA-20 acceptance runner subsequently completed the complete fourteen-package local regression with `status=PASS`, `errors=[]` and a passing persistence probe.
- The inherited full regression receipt remains valid because FGA-20 does not modify the application, case-data validator, frontend or release runtime. The new branch delta is independently covered by the deterministic `20 passed` focused receipt and the acceptance runner.

### Article worktree and editorial corrections

- The first article-worktree content check found no installed Node dependencies. `npm ci` installed the lockfile dependencies. npm emitted the environment notices already seen in prior series articles: five audit vulnerabilities (`4 moderate`, `1 high`) and install-script notices for optional tooling. No `audit fix` was applied because changing the dependency graph is outside the article scope; the notices remain recorded here.
- The first reading-time estimate was `16`; the frontmatter was corrected to `17` after the article was edited. The article remains below the twenty-minute requirement.
- Final structural comparison: `4` separators, `12` level-two section headings, `30` level-three subsection headings and `0` fenced code blocks. The opening remains three short italic paragraphs, matching the established series rhythm.
- The article uses inline backticks for code identifiers, keeps the noir detective narration and dry canine humour, and reserves technical claims for the implementation/evidence matrix.
- The direct route is `/fga/20-nothing-compares-2-mvp/`; the article is unlisted from the homepage catalogue, as with the preceding release-by-release articles.

### Artwork and asset verification

- The newspaper cover is `images/articles/fga/20-nothing-compares-2-mvp/1.png`; the final infographic is `.../2.png`.
- Both images use the established dark sepia/charcoal newspaper and case-file visual language, restrained brightness, the Spanish Water Dog detective and the FGA-20 acceptance theme.
- Both jsDelivr URLs pinned to `eb7b295d7c573679594f0b95d5efa17b34bb4673` returned HTTP `200` with `image/png`. An earlier guessed short/incorrect revision returned `404`; the article was corrected to the exact full asset commit.

## Final receipts

| Area | Receipt |
| --- | --- |
| FGA-20 acceptance tests | `20 passed` in deterministic focused run; the three new FGA-20 tests pass independently |
| Inherited backend regression | `313 passed` on the final FGA-19 runtime baseline |
| Local Academy | `PASS`; 12 scenarios, complete loop, 14 package smoke journeys, persistence and idempotent replay |
| Databricks | profile `fga`; `PASS`; 13 packages; read-only `SELECT` boundary; no truth source; no mutation |
| Case shape | 35,874 records and 80,349 relationships in the qualified public boundary |
| Frontend/runtime inheritance | 27 files/71 unit tests, 18 browser E2E tests, build and container startup smoke pass from FGA-19 |
| Article | 17-minute frontmatter, 4 separators, 12 H2 headings, 30 H3 headings, no fenced snippets |
| Artwork | `1.png` and `2.png` available from the pinned FGA-20 asset commit |

## Deliberate non-claims

- The article does not claim production-scale performance, concurrency, retention, multi-region recovery, reader engagement or operational staffing cost.
- The article does not claim that Databricks executed GraphFrames, Zingg, Docker or protected truth for this MVP receipt.
- The article does not claim that a retrospective is a new feature; FGA-20 implements the acceptance report and evidence contract that make the retrospective reproducible.
- The article does not hide the runner/plugin interaction or npm audit notices behind an artificial claim of a perfectly clean environment.
