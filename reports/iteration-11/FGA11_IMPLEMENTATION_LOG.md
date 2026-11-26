# FGA-11 Implementation Log

This is the engineering and editorial receipt for FGA-11, `Money for Nothing, Evidence for Everything`. It records the work in order, including failed checks and the corrections that followed them.

## Scope

- Branch: `FGA-11`, based on the final FGA-10 graph-analysis branch.
- Case contract: T02, `ACADEMY_T02`.
- Initial economy: 9 credits.
- Paid actions: `COMPARE_IDENTITIES` costs 3; `RUN_GRAPH_ANALYSIS` costs 3.
- Free actions: navigation, selection, inspection, hypotheses and submission.
- Resolution: immutable server-side submission, five score dimensions, six explicit endings.
- Databricks boundary: player-safe published projection only; all qualification queries are `SELECT` statements.
- Article target: the same FGA structure, noir dog-detective voice, short three-paragraph opening and 19-minute reading budget.

## Work sequence and evidence

1. Read both FGA series outlines and the preceding FGA articles. The implementation contract was extracted before writing the article: charge meaningful questions, preserve a durable ledger, make retries idempotent, keep the evaluator behind the API boundary, and make the ending explain the player's evidence and budget.
2. Created the FGA-11 code worktree at `C:/Users/angel.alvarez/PycharmProjects/_worktrees/fraud-graph-arena-fga11-20261126` on branch `FGA-11`.
3. Added the round `SUBMITTED` state, persisted submission metadata, and a `RoundService` submission/closing contract.
4. Added `economy/` with versioned action costs, charge/refund ledger entries, in-memory and SQLite repositories, request hashes, idempotency, replay and a lock around reserve/settle.
5. Integrated the economy with entity resolution and graph analytics. Graph analysis now includes visible scope in the derived legacy key and request hash, so the same key cannot silently move to another graph.
6. Added `case_resolution/` with immutable submissions, T02 scoring, five dimensions, six endings and a public receipt. The evaluator reads truth only on the server and does not return truth-bearing columns to the player.
7. Added API routes for submission, submission replay, closing and the economy ledger. Added the public resolution screen, submission panel, typed data source and screen-system transition in the frontend.
8. Added `scripts/qualify_game_economy.py` and mocked read-only tests. The qualifier checks the active publication, 20-record and 21-relationship boundaries, one snapshot, forbidden player columns and SELECT-only statements.
9. Generated the FGA-11 newspaper cover and final case-file infographic in the established dark sepia palette. Asset branch commit: `c08e4b99e1109969cadbee730a9181022176abd9`.

## Failures found and corrections

### The first implementation made graph questions free

The graph endpoint still worked, but the player could repeat analysis without a decision or cost. The endpoint was moved behind `EconomyService.execute`; successful graph and identity actions now settle a charge, and failed actions refund it.

### Existing graph tests expected the old balance

The FGA-10 API tests expected nine credits after analysis. They failed after the economy became real. The tests were updated to assert the FGA-11 contract: six credits after one paid graph action and nine after a refunded provider failure.

### A legacy graph retry key omitted visible scope

The first derived key used only analytical parameters. A request with the same parameters and a different visible scope could therefore look like the same paid question. The key and request hash now include sorted visible record IDs. A regression test proves that reusing the key with another scope returns `IDEMPOTENCY_KEY_REUSED` without a second debit.

### Refund and charge timestamps could sort ambiguously

The first refund reused the charge timestamp. The ledger could then present the charge and refund in an unstable order when timestamps were equal. Refund entries now receive their own timestamp, and the ledger sorts by timestamp plus entry ID.

### A stale version returned 422 instead of 409

The API model initially required `expected_round_version >= 1`. The valid stale value in the first round is `0`, so Pydantic returned `422` before the domain could report `STALE_ROUND_VERSION`. The boundary now accepts `>= 0`; the domain still owns the version comparison and returns `409` without closing the round.

### The economy needed a hard stop

The first happy-path tests did not exercise the final unaffordable action. A test now spends all three paid-action slots and verifies `INSUFFICIENT_CREDITS`, zero balance and exactly three charge entries—no phantom debit.

### The article worktree had no Node dependencies

The first content validation failed with `ERR_MODULE_NOT_FOUND` for `yaml`. `npm ci --no-audit --no-fund` installed the lockfile. npm reported two install scripts not yet covered by its allowlist (`esbuild` and `workerd`); this is recorded as an environment/setup warning, not as an application-test warning. Content validation and link checks then passed.

### The audit harness had two command typos

Two ad-hoc PowerShell audit commands initially failed to parse while comparing section tails and release booleans. They were corrected with explicit line parsing and a small `HasText` helper. Neither command touched a repository file or changed a test result; the corrected checks passed.

## Test ledger

| Check | Result |
| --- | --- |
| FGA-11 Python slice after the stale-version fix and edge-case tests | 11 passed |
| FGA-11 plus FGA 03 / 09 / 10 regression slice after edge-case tests | 66 passed |
| Full Python suite | 256 passed in 1136.93s; no pytest warnings emitted |
| Frontend typecheck | passed |
| Frontend Vitest suite | 65 passed across 24 files |
| Screen definition JSON validation | passed |
| Frontend production build | passed |
| Content validation | 109 canonical articles validated |
| Internal link check | 116 same-origin URLs checked; no failures |
| OpenAPI export | regenerated with submission, closing and ledger routes |
| Databricks live qualification | `pass`; profile `fga`; read-only; 20 records, 21 relationships, one snapshot; all five checks true; source commit `15e750f22cf4e1a459e63b8af8bd168c5d8e6f0d` |

## Editorial passes

The final review is recorded as ten passes after the last article edit. Each pass re-checked the full article against the FGA-10 structure and the implementation matrix: (1) opening length and hook, (2) noir voice and contractions, (3) section/subsection notation, (4) separator placement, (5) economy claims against code, (6) scoring claims against evaluator/tests, (7) Databricks wording against the live report, (8) code snippets and backtick discipline, (9) previous-series references and reading-time budget, and (10) final publication receipt, image captions and route metadata. No pass introduced a new code or prose change after the receipt was assembled.

The observed closure values were: 9 parts, 13 level-two sections, 89-word opening, 3,914-word body, 19-minute reading metadata, four separators, one final image, no artificial FGA-09 names, 66 Python regression tests, 65 frontend tests, a live Databricks `pass`, and HTTP 200 for both pinned images.

## Closing rule

FGA-11's live qualification now has `status: pass`, `profile: fga`, `read_only: true`, all checks true, and the article receipt matches the final test counts. The remaining release step is to commit and push the updated article receipt and final report, then verify all three worktrees are clean on their pushed `FGA-11` branches.
