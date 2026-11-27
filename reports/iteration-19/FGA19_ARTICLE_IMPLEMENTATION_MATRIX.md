# FGA-19 article ↔ implementation ↔ evidence matrix

| Article promise | Implementation | Test or receipt | Article location |
| --- | --- | --- | --- |
| Six release units are named and reproducibly identified | `release_engineering.manifest.UNIT_DEFINITIONS`, tree/package SHA-256 digests and `fga19-release.schema.json` | Manifest generation and validation: `pass`, 6 units; focused manifest test | Parts I–II |
| Frontend, backend, migration, case, graph and analytics versions travel together | `fga19-runtime.json`, `ReleaseContext` and the six unit declarations | Runtime/context tests and the final manifest receipt | Parts I–II |
| A new round remembers the release that created it | `Round` binding fields, `RoundService`, SQLite adapter and `RoundResponse`/OpenAPI contract | `test_round_binds_release_and_package_versions`; full backend regression `313 passed` | Part III |
| A restart does not erase the round's version boundary | SQLite persistence of all nine binding fields | `test_restart_preserves_release_binding` | Part III |
| Old databases can be upgraded without pretending the change is reversible | `apply_round_migrations`, `schema_migrations`, legacy markers and nine additive columns | Old SQLite migration test; release smoke | Part IV |
| Compatibility distinguishes replay, migration and freeze | `evaluate_saved_round` with `PLAYABLE`, `MIGRATE` and `FROZEN` decisions | Exact-package playable and missing-package frozen tests | Part IV |
| CI is a sequence of blocking gates | `fga19-ci-pipeline.json`, manifest CI stages and validator | Stage-order/uniqueness test; manifest validator | Part V |
| Candidate mechanics can remain disabled without disappearing from the release record | `fga19.release_candidate` flag in the manifest/schema, disabled by default | Manifest schema validation and release receipt | Part VI |
| A bad release is rejected before promotion | Digest comparison in `ReleasePromotion` | Release smoke corrupts the frontend digest and records `REJECTED` | Part VI |
| Rollback moves the application pointer without silently rewriting data | Local immutable promotion pointer and explicit rollback boundary | Release smoke records `ROLLED_BACK`; no Databricks mutation | Part VI, Case Closed? |
| The real player path still works after the version binding | Application wiring passes `ReleaseContext`; TestClient journey exercises create/start/opening/complete/workspace | Release smoke and full backend regression | Part VII |
| The container actually starts with the new release code | Existing Compose/Docker contract plus the FGA-19 manifest/release modules included in the image | Compose contract, image build, startup smoke on port `8019` | Part VII |
| Databricks qualification uses the requested profile honestly | `qualify_fga19_release.py` delegates to the canonical package public-boundary checks | `databricks-fga19-release-current.json`: `pass`, profile `fga`, 13 packages, read-only | Part VIII, The Arrest |
| The article stays in the established FGA reading shape and budget | FGA-19 Markdown with the same headings/separators, 15-minute frontmatter and two image slots | 2878-word estimate; content validation; Astro build; link check; direct preview | Source Code, Release Receipt |
| The visual story has the newspaper cover and final case-file infographic | `angelic-assets` FGA-19 `1.png`/`2.png`, commit-pinned in article frontmatter/body | Both jsDelivr asset URLs returned `200 image/png` | Cover, final infographic |

## Deliberate non-claims

- The article does not claim that a SQL Warehouse executed GraphFrames, Docker or protected truth.
- The article does not claim a production registry signature, multi-region deployment, distributed migration coordinator or automatic data rollback.
- The article does not claim that `MIGRATE` already transforms arbitrary old saved rounds; only exact replay and safe freeze are implemented and tested.
- Dependency audit notices are recorded as environment/dependency debt, not hidden behind a claim of a perfectly clean install.
