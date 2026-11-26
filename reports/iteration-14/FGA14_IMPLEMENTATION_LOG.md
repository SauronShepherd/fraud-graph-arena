# FGA14 implementation log

## Scope

FGA14 turns ethical uncertainty into an executable case-resolution contract. The
implementation must keep suspicion, evidence, responsibility and adjudication
separate; cite player-visible evidence; preserve protected evaluator truth; make
unsupported accusations consequential; review benign adversarial cases; and
qualify the published boundary in Databricks through profile `fga`.

The code, article and assets were worked on independent `FGA-14` branches:

- `fraud-graph-arena-fga14-20261126`
- `articles-fga14-20261126`
- `angelic-assets-fga14-20261126`

The branches were created from the closed FGA13 commits. The main checkouts had
unrelated dirty work and were left untouched.

## Chronological record

### 1. Baseline and Databricks access

- Read both FGA outlines and compared FGA11–FGA13 structure, separators,
  captions, release receipts and source-code sections.
- Confirmed `databricks current-user me --profile fga` before qualification.
- Databricks identity: `angel.alvarez.pascua@gmail.com`.
- No Databricks mutation was authorised or performed.

### 2. First implementation slice

- Added `src/fraud_graph_arena/ethics/` with the versioned assessment and
  publication-review boundary.
- Added optional `evidence_record_ids` to submissions while preserving legacy
  `CLAIM_DECLARATIONS` clients and FGA11 scoring doors.
- Added safe nested API output, repository round-trip serialisation and the six
  adversarial fixture contract.
- Existing FGA11 resolution tests: **8 passed**.
- Compile check: **passed**.

### 3. First failures and corrections

| Failure | Evidence | Correction | Rerun |
| --- | --- | --- | --- |
| Direct review command could not import `fraud_graph_arena` | `ModuleNotFoundError: No module named 'fraud_graph_arena'` | Review and qualification scripts now establish the repository `src` path explicitly | Direct review passed |
| Claim-type review rejected package-specific labels such as `BANK_CHRONOLOGY` | Initial review reported `ETHICS.CLAIM_TYPES` failures on older packages | Added deterministic mapping to the small public vocabulary: actor, role, behaviour, mechanism, beneficiary, affected party and evidence | All 14 package reviews passed |
| New FGA14 tests could not find the `client` fixture | First run: **1 passed, 3 errors** with `fixture 'client' not found` | Added `tests/iteration_14/conftest.py` and a local active-T02 helper | FGA14 slice: **4 passed** |
| OpenAPI contract was stale after adding evidence anchors and ethical output | Full suite: **276 passed, 1 failed** in `test_committed_openapi_matches_application_contract` | Made `scripts/export_openapi.py` directly runnable and regenerated `contracts/openapi-v1.json` | Focused OpenAPI plus FGA14 slice: **5 passed** |
| Article validation had six tags | `content:validate` rejected the front matter: expected 1–5 tags | Reduced FGA14 to five tags, matching the site contract | Content validation passed |
| Article worktree had no Node dependencies | `content:validate` initially failed because `yaml` was missing | Ran `npm ci` from the lockfile before site validation | Content validation and build passed |

### 4. Ethical contract hardening

The independent review found that a list of constants was not enough evidence
for a versioned role model. FGA14 now carries
`contracts/ethics/fga14-ethical-contract.json`, validates its exact role and
impact dimensions, and returns those dimensions in the player-safe assessment.

Additional regression coverage now checks:

- insufficient explicit anchors remain `INCOMPLETE`;
- changing evidence anchors under an existing idempotency key is rejected;
- the 64-anchor limit is enforced;
- a SQLite restart restores nested ethical statements;
- the public payload contains none of the protected-truth marker fields used by
  the canonical truth layer;
- the ethical contract and six adversarial fixtures are valid.

### 5. Local and site verification

- FGA14 focused tests after hardening: **5 passed**.
- Content validation: **112 canonical articles validated**.
- Static build: **102 pages built**, Pagefind indexed 97 pages in two languages.
- Internal links: **116 same-origin URLs checked; no failures**.
- The build emitted the repository's existing npm audit and Pagefind advisory
  messages; neither was a test failure. No pytest warning summary was emitted.

### 6. Live Databricks qualification

The qualification ran with:

```text
python scripts/qualify_fga14_ethics.py --profile fga
```

The script uses read-only `SELECT` statements against the active public
projection for all thirteen canonical packages. It deliberately excludes the
published empty compatibility shell `academy-001` from the remote data check;
the local review still covers all fourteen manifests. The report records:

- profile `fga`;
- catalog `sda_dev`, schema `sandbox`, warehouse `eded42c9d0a69b84`;
- 13 active canonical public boundaries;
- one active publication and one snapshot per case;
- exact records and relationships, no dangling endpoints and no forbidden
  player-facing columns;
- `truth_source_queried=false`;
- `actual_engine_run=false`;
- `graphframes_compatibility=UNRESOLVED_SQL_WAREHOUSE_ONLY`.

The durable receipt is
`reports/iteration-14/databricks-fga14-ethics-current.json`.

The post-commit live rerun passed with source commit
`202bd8cd49e13753b90f7ab4c3cdf9b900f1233b` and profile `fga`.

### 7. Final closure rerun

- OpenAPI plus FGA14 focused slice after contract hardening: **9 passed**.
- Full Python suite after the final code commit: **281 passed in 9:28:53**.
- No pytest warning summary, exception or failure remained.
- Static route visual check: `/fga/14-nobody-expects-the-fraud-inquisition/`
  returned HTTP 200 and rendered the cover, article body, release receipt and
  final infographic. The development server also logged the site's existing
  static `/api/metrics` and `/api/comments` 404 probes; those are outside the
  FGA14 article route and were not changed by this iteration.
- Asset branch: `9d504954cb483d780027de0ae327f3961e4f719e`.

## Final closure fields

## Final closure

- implementation commit: `202bd8cd49e13753b90f7ab4c3cdf9b900f1233b`;
- full Python suite: **281 passed**, no pytest warning summary;
- final Databricks source commit: `202bd8cd49e13753b90f7ab4c3cdf9b900f1233b`;
- final Databricks status: **pass**, profile `fga`, read-only, 13 canonical
  public boundaries;
- asset commit: `9d504954cb483d780027de0ae327f3961e4f719e`.
