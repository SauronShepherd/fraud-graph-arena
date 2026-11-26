# FGA-11 Article ↔ Implementation Matrix

The article and the branch are two views of one contract. Every material promise in the article maps to an implementation and a test; every new implementation surface is named in the article.

## Article claim to branch evidence

| Article section/claim | Implementation | Verification |
| --- | --- | --- |
| Part I: nine credits, paid questions and free navigation | `economy/models.py`, `EconomyService`, `Round.credits_remaining` | `test_six_case_doors_have_explicit_scores_and_endings`, insufficient-credit test |
| Part II: reserve, settle and refund | `economy/service.py`, `economy/repository.py` | provider-failure refund test; SQLite ledger test |
| Part III: one key means one question; save/reload | request hashes, unique ledger key, SQLite persistence | replay test, changed-scope conflict test, restart test |
| Part IV: five score dimensions; evaluator behind the wall | `case_resolution/evaluator.py`, `models.py`, public response models | six-door score test and truth-leak assertions |
| Part V: six endings and exact T02 scores | evaluator's six ending branches | score/ending/credits/false-accusation assertions for all six doors |
| Part VI: immutable submission and public resolution | `case_resolution/service.py`, `RoundStatus.SUBMITTED`, submission/closing routes, `CaseResolutionPage` | immutable replay test, stale-version test, screen-system tests |
| Part VII: implementation failures and fixes | final code includes scope in retry hash, timestamped refunds, charged graph action and retry boundary | regression tests for each failure; full Python suite |
| Part VIII: Databricks is the read-only witness | `scripts/qualify_game_economy.py` | `test_databricks_game_economy.py` plus live `profile fga` report |
| Part IX: playable evidence and limits | API/frontend panel, public receipt, no truth columns, `actual_engine_run=false` | frontend 65-test suite, build, live report, full Python suite |
| Source Code: code, logs and report are available | FGA-11 code branch and `reports/iteration-11/` | pushed branch and clean worktree check |

## Branch capability to article coverage

| Branch capability | Where it is explained |
| --- | --- |
| `SUBMITTED` round status and persisted submission metadata | Part VI, “The round changed its status” |
| `COMPARE_IDENTITIES` and `RUN_GRAPH_ANALYSIS` cost three credits | Parts I–II and the release receipt |
| Charge/refund ledger with versioned rules | Part II and Part III |
| Replay of the same successful paid result | Part III, “The same key means the same question” |
| New key required after a refunded failed attempt | Part III and Part VII failure notes |
| Visible graph scope in the identity material | Part III and Part VII scope failure |
| Five scoring dimensions and six named endings | Parts IV–V |
| Server-side truth boundary and no truth leak | Part IV and Part IX limits |
| Submission idempotency, stale-version protection and immutable receipt | Part VI |
| Public resolution UI and ledger view | Part VI and Part IX |
| Read-only Databricks qualification against 20 records / 21 relationships | Part VIII |
| GraphFrames compatibility remains unresolved in SQL Warehouse | Part VIII and Part IX |
| FGA-11 tests, regression tests, frontend checks and content checks | Part IX and Release Receipt |

## Publication and asset evidence

- Direct article route: `/fga/11-money-for-nothing-evidence-for-everything/`.
- Article branch: `FGA-11` in `angelic-articles`.
- Asset branch: `FGA-11`, commit `c08e4b99e1109969cadbee730a9181022176abd9`.
- Image 1: newspaper preview/fallback at `images/articles/fga/11-money-for-nothing-evidence-for-everything/1.png`.
- Image 2: final infographic at `images/articles/fga/11-money-for-nothing-evidence-for-everything/2.png`.
- The article uses the pinned jsDelivr asset commit for both images and includes captions in the established FGA format.
