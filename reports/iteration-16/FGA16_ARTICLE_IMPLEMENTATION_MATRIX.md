# FGA-16 article / implementation matrix

This matrix is the closure check for FGA-16. Every promise in the article must point to implementation evidence, and every FGA-16 implementation surface must be explained by the article.

| Outline requirement | Implementation evidence | Article location | Verification | Status |
| --- | --- | --- | --- | --- |
| Turn the hidden validation level into a player-facing Academy and a machine-facing suite | Public curriculum embedded in the Detective Academy catalogue; private runner and golden contracts under `contracts/academy/` | Part I, Part VII | `tests/iteration_16/test_academy_contract.py`; catalogue/e2e assertions | PASS |
| Cover the named micro-cases | Nine versioned scenarios for node selection, edge inspection, entity resolution, traversal, resources, contradictory evidence, correct/incorrect accusation and complete loop | Part II | 9 scenario contract assertions; shared runner | PASS |
| Give every scenario a stable contract | JSON Schema, scenario registry, version, objective, case, seed, visible evidence, actions, transitions, guidance and protected outcome | Part II–III | schema validation and public-redaction tests | PASS |
| Keep expected state separate from expected screen | State-transition runner and golden final state/transition counts; no screenshot-only assertion | Part III, Part V | scenario runner and browser semantic assertions | PASS |
| Make runs deterministic and replayable | Fixed scenario seeds, action histories, correlation IDs and golden results | Part III, Part V | runner report and failure-diagnostic test | PASS |
| Compare component, API and full-loop validation | `COMPONENT_MOCK`, `API_CONTRACT` and `COMPLETE_LOOP` execution modes | Part IV | 9 scenario runner; backend suite | PASS |
| Exercise persistence and idempotency | Isolated SQLite restart probe; cached graph replay; paid-action idempotency | Part IV, Part VIII | runner persistence report | PASS |
| Diagnose the smallest broken mechanic | Failure report includes scenario/version/seed, action history, correlation IDs, expected/actual state and evidence diff | Part V | broken-transition diagnostic test | PASS |
| Regression-test released cases | 14 local package manifests and core create/start/open/workspace smoke path | Part VI, Part VIII | regression runner and Databricks receipt | PASS |
| Add the Academy to the product surface | Academy qualification track rendered in the case catalogue with 9 mechanics and player guidance | Part II, Part VII | navigation unit test; walking-skeleton E2E | PASS |
| Preserve accessibility and reset behaviour | Semantic content, keyboard/reduced-motion coverage, fresh API rounds and isolated persistence state | Part V, Part VII | frontend tests and 16 Playwright tests | PASS |
| Qualify the public Databricks boundary without overstating providers | Read-only `fga` qualification of 13 canonical projections in `sda_dev.sandbox` | Part VIII, Release Receipt | `databricks-fga16-academy-current.json` | PASS |
| Publish coherent series visuals | Newspaper cover and dark sepia case-file infographic in the FGA visual language | Release Receipt / final image | assets branch commit `f0ae64e9f03e7aadaa4e0122475903fee9b65c62` | PASS |

## Closure rule

FGA-16 is ready to hand off only when this matrix is all PASS, the article build contains `/fga/16-test-me-baby-one-more-time/`, the three `FGA-16` branches are pushed, and the final qualification receipt is preserved with its read-only/provider limits.
