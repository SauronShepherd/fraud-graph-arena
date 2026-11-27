# FGA-20 article ↔ implementation ↔ evidence matrix

| Article promise | Implementation | Test or receipt | Article location |
| --- | --- | --- | --- |
| The retrospective has an explicit contract rather than a loose conclusion | `contracts/retrospective/fga20-mvp-acceptance.schema.json` | Schema validation in `test_acceptance_report_matches_schema_and_passes`; generated report status `pass` | Parts I–II, Source Code |
| Plan and reality are compared without rewriting the original promise | `_plan_vs_reality()` in `scripts/qualify_fga20_mvp.py` | Report contains `delivered`, `limited` and `deferred` statuses and the focused acceptance tests | Part I |
| The MVP is judged by a complete player journey | `AcademyValidationRunner`, complete-loop scenario and `_player_journey()` | Academy `PASS`; `academy-complete-game-loop`; 12 scenarios; persistence and replay pass | Parts II–III |
| Entry, case selection, round binding and opening are executable | Existing catalogue, round lifecycle and FGA-19 release binding | Academy complete loop and inherited FGA-19 release tests | Part II |
| Bounded evidence, identity analysis and graph work remain authoritative API actions | Existing workspace, investigation-command, identity and graph boundaries | Academy complete loop; FGA-18/FGA-19 focused receipts | Parts II–III |
| Paid actions have an explicit ledger and safe replay | Existing economy, idempotency and ledger services | Academy action-history receipt and inherited backend regression | Part III |
| Submission resolves publicly without exposing protected truth | Existing case-resolution/evaluator boundary | Academy `CLEAN_COLLAR` receipt; Databricks `truth_source_queried=false` | Parts III, VI |
| Restart recovery is part of the MVP, not a footnote | Existing SQLite repository and Academy persistence probe | `round_recovered=true`, `idempotent_replay=true` | Part III |
| The final architecture is a bounded modular monolith | Existing application modules, release manifest and container wiring | FGA-19 release manifest, container build and startup smoke receipts | Part IV |
| Versioned release binding survived into the MVP | FGA-19 `ReleaseContext`, round binding, migration and promotion pointer | FGA-19 focused tests, release smoke and inherited `313 passed` receipt | Part IV |
| Decisions that aged well are named | Case packages, public/protected projection, deterministic fallback, observability boundary and release passport | Local package regression, Databricks boundary and release receipts | Part V |
| Temporary shortcuts and debt are named as limits | Acceptance report `not_measured`, exclusions and next-season fields | FGA-20 schema/tests require explicit unproven questions and hypotheses | Parts V, VIII |
| The case-library numbers are measured, not invented | `_case_shape()` derived from the Databricks receipt | `databricks-fga20-public-boundary-current.json`: 13 packages, 35,874 records, 80,349 relationships | Part VII |
| Databricks qualification uses the requested profile honestly | `qualify_fga19_release.py` executed from the FGA-20 worktree with `--profile fga` | `PASS`; 13 packages; read-only `SELECT`; no forbidden columns; no mutation | Part VII, Release Receipt |
| Test numbers distinguish inherited evidence from the FGA-20 delta | `test_receipts` in the acceptance report and deterministic focused command | 313 inherited backend tests; 20 focused checks; 3 new acceptance tests | Part VII, Release Receipt |
| The article keeps the established FGA reading shape and budget | FGA-20 Markdown follows the prior headings, separators and image slots | 4 separators, 12 H2 headings, 30 H3 headings, no fences, 17-minute frontmatter; content/build/link checks | Source Code |
| The visual story has a newspaper cover and final case-file infographic | `angelic-assets` FGA-20 `1.png`/`2.png`, pinned to commit `eb7b295d7c573679594f0b95d5efa17b34bb4673` | Both asset URLs returned HTTP 200 `image/png` | Cover, final infographic |

## Deliberate non-claims

- The article does not claim that local acceptance equals production-scale reliability or player research.
- The article does not claim that `actual_engine_run=false` is a hidden engine success; it is an explicit boundary.
- The article does not claim that the next season already exists as implementation. Its items remain hypotheses with evidence requirements.
