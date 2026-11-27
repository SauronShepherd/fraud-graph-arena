# FGA-17 article / implementation matrix

This matrix is the closure check for the bidirectional rule: every material article claim has implementation evidence, and every material FGA-17 implementation or test result is explained in the article. “Limitation” is a deliberate boundary, not an unfinished claim.

| Article claim or promise | Implementation / source of truth | Verification / receipt | Status |
| --- | --- | --- | --- |
| PostgreSQL health is narrower than application readiness | `compose.yaml` optional `postgres` profile; `pg_isready`; web service keeps SQLite repository | Real `fga17-postgres` health and `pg_isready`; `tests/iteration_17/test_compose_contract.py` | PASS |
| Compose resolves image/build values before container runtime injection | `compose.yaml`, `compose.published.yaml`, `.env.example`, `docker/runtime.env` | `scripts/fga17_compose_contract.py`; local and published `docker compose config` checks | PASS |
| Missing `FGA_IMAGE` fails fast | Required interpolation in `compose.published.yaml` | Negative published-config run without `FGA_IMAGE`; focused contract test | PASS |
| Local build and published image are separate workflows | `local-build` profile with `build`; `published-image` override without build context | Static contract validator; positive published config with immutable digest-shaped value | PASS |
| Host process is a named third workflow | README FGA-17 workflow section; hostname boundary documentation | Article section “Host process”; static contract and article matrix | PASS |
| Runtime injection is explicit and non-secret | `docker/runtime.env`, service `environment`, no `.env` copy, no secret-like runtime variables | Static contract validator and Dockerfile inspection | PASS |
| Source revision is provenance, not a secret | `FGA_SOURCE_REVISION` build arg and OCI label | Dockerfile contract checks; final image build | PASS |
| A successful image build can still omit runtime data | Dockerfile runtime copies and `.dockerignore` re-inclusions | First boot failure for missing `/app/case-packages`; corrected rebuild recorded in log | PASS |
| The final image includes the package registry | Dockerfile `COPY case-packages/ ./case-packages/`; `.dockerignore` exceptions | Final Docker build, healthy container and startup smoke | PASS |
| Liveness and readiness name different boundaries | Dockerfile and Compose call `/api/v1/health/ready`; smoke calls live and ready separately | Static validator; real container health; focused test | PASS |
| Application readiness includes repository and frontend distribution | Existing health route plus production-shaped container settings | Smoke receipt reports `round_repository: ready` and `frontend_distribution: ready` | PASS |
| Host and container hostnames are not interchangeable | README network workflow guidance; Compose service/network definitions | Focused contract tests and article network-boundary section | PASS |
| The branch does not invent external authentication | No external IdP/auth adapter added; smoke reports local player/session boundary | Real startup smoke; article states “external authentication is not claimed” | PASS / LIMITATION |
| The branch does not claim a PostgreSQL application adapter | Web service remains on SQLite; Postgres is opt-in witness only | Compose contract test asserts no web dependency on Postgres; article and log state limit | PASS / LIMITATION |
| One command reaches the playable board path | `scripts/fga17_startup_smoke.py` | Real Docker smoke: liveness, readiness, catalogue, create, start, open, complete, workspace | PASS |
| Intermediate smoke failures are not swallowed | Smoke script checks every status and names the checkpoint | `tests/iteration_17/test_startup_smoke.py`; real smoke receipt | PASS |
| The branch is regression-safe | FGA-17 tests plus existing backend/frontend/browser suites | `297 passed`; 4 focused; 70 Vitest; 17 Playwright; typecheck/build/screen validation PASS | PASS |
| Databricks uses profile `fga` | `scripts/qualify_fga17_environment.py` | Receipt authenticated `profile=fga`; `status=pass` | PASS |
| Databricks qualification is read-only | Qualification queries public projections only; no mutation path | Receipt `read_only=true`, `truth_source_queried=false`, `actual_engine_run=false` | PASS |
| Databricks covers the active public boundary | Existing qualification plus FGA-17 wrapper | 13 canonical packages; counts/endpoints/safe columns PASS | PASS |
| Docker did not run inside Databricks | Explicit boundary in qualification report | Receipt `docker_execution_on_databricks=false`; article states local Docker/remote qualification split | PASS / LIMITATION |
| Article route and article structure match the series | Article markdown; `unlistedArticleSlugs` entry | 115 canonical validation; Astro route; 116 internal URLs; 3,515 words / 18-minute estimator | PASS |
| Article images are the FGA newspaper and final infographic pair | Assets branch `FGA-17`: `1.png`, `2.png` | Immutable GitHub Raw URLs return 200; article frontmatter/final image use commit `507f68b...` | PASS |
| Implementation failures and fixes are part of the lesson | `FGA17_IMPLEMENTATION_LOG.md` | First missing-directory boot failure, correction, rerun and notices recorded | PASS |

## Bidirectional closure

- Every article-specific technical promise above points to a file, test, real run or explicit limitation.
- Every new FGA-17 implementation surface — Compose profiles, runtime file, image boundary, health checks, smoke test, static validator, Databricks wrapper, tests, reports and artwork — is named in the article or its source-code receipt.
- No row is closed by an unverified assertion, and no external authentication or PostgreSQL adapter is implied by the local evidence.
