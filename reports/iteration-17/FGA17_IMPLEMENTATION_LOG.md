# FGA-17 implementation and test log

## Scope

FGA-17 implements the updated master-outline item “Docker? I Hardly Know Her”: make the local container story explicit, reproducible and honest about its boundaries. The work covers the implementation repo, the article repo and the separate assets repo. The article is kept under 20 minutes and follows the established FGA newspaper/noir structure: three short italic opening paragraphs, Parts I–VIII, an arrest, a case-status section, next-case handoff, source code, release receipt and final infographic.

The article and implementation are deliberately narrower than the original browser symptom. This branch proves local player/session board access, not an external identity provider or a PostgreSQL application adapter. The Databricks run is a read-only public-boundary qualification through profile `fga`; Docker is exercised locally, not inside SQL Warehouse.

## Branches and worktrees

| Repository | Branch | Worktree |
| --- | --- | --- |
| `fraud-graph-arena` | `FGA-17` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\fraud-graph-arena-fga17-20261127` |
| `articles` | `FGA-17` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\articles-fga17-20261127` |
| `angelic-assets` | `FGA-17` | `C:\Users\angel.alvarez\PycharmProjects\_worktrees\angelic-assets-fga17-20261127` |

All three branches were created from the preceding FGA-16 line. The implementation and asset branches were pushed before the final article pass; the three final branch commits and remote heads are recorded in the closure section after the article and evidence commits.

## Outline and editorial contract

- Read `Fraud Graph Arena — Master Series Outline Updated.md` and `FGA_Development_Series_Outline_07-19.md`.
- The master outline is authoritative for the current numbering: FGA-16 is the Detective Academy article, FGA-17 is the Docker article and FGA-18 is the observability article. The older development outline still labels the Docker block as FGA-16 and the observability block as FGA-17; that numbering discrepancy is retained here as a planning note, not silently merged into the article.
- Read the FGA-15 and FGA-16 articles and checked the recurring three-paragraph opening, `Part I`–`Part VIII` notation, short `###` subsections, noir narration, restrained dog humour, tables for contracts, the separator before `Source Code` and the separator before the final image.
- Applied the editorial-review skill using the novela panel for promise, opening, voice, exposition, atmosphere, humour, genre, rhythm, line, grammar, punctuation, lexical precision and production; and the humanization panel for intention, audience, specificity, paragraph architecture, transitions, repetition, idiom, certainty, regression and format.
- Kept the article in English, with the FGA series voice rather than a generic technical tutorial. It has no fenced code blocks, uses inline code only for exact identifiers and commands, and keeps `readingTime: 18`.

## Chronological record

### 1. Baseline and first implementation pass

The baseline Compose file could build the application, but it did not distinguish a local source build from a published image. The runtime image boundary was also implicit, and the original incident had collapsed Compose interpolation, image construction, container startup, database health, application readiness and board access into one vague “Docker failed” report.

FGA-17 added:

- a `local-build` profile with an explicit multi-stage build and local image tag;
- a separate `published-image` override that requires `FGA_IMAGE` before Compose can resolve the service and has no build context;
- a named host workflow and host/container hostname guidance;
- `docker/runtime.env` for small non-secret runtime injection, with `.env.example` reserved for Compose interpolation defaults;
- a Dockerfile source-revision label through the harmless `FGA_SOURCE_REVISION` build argument;
- application and PostgreSQL health boundaries;
- a static Compose contract checker and a board-access startup smoke test;
- focused FGA-17 tests and a read-only Databricks qualification wrapper.

The application’s supported local durable store remains SQLite. PostgreSQL is an optional `pg_isready` witness for the dependency boundary, not a newly claimed application adapter.

### 2. The first image built and the first container failed

The first clean Docker build passed. The first container boot did not. The runtime process raised `FileNotFoundError` for `/app/case-packages` while constructing the catalogue. The Dockerfile had copied source, contracts, configuration and case data, but not the package registry the application loads at startup. The `.dockerignore` had also not re-included that directory.

The correction added `case-packages/` to the runtime image and explicitly re-included it in the Docker build context. The validator was tightened to require every runtime directory actually used by the image. The image was rebuilt and the service was recreated instead of treating the first green build as sufficient evidence.

### 3. Static Compose and fail-fast checks

The final static contract run passed with `errors: []`.

- `docker compose --profile local-build config --quiet` passed.
- `docker compose --profile postgres config --quiet` passed.
- The published override failed as designed when `FGA_IMAGE` was absent, before any container was created, with the explicit required-variable error.
- The same published configuration passed when supplied an immutable digest-shaped value.
- The static validator confirmed the health boundaries, runtime directories, no secret-like runtime variables and no accidental published build context.

The negative configuration check is part of the receipt. A deliberately early failure is more useful than a container whose image provenance is unclear.

### 4. Final local Docker run

The final local image build completed with the Docker, npm and pip update/version notices suppressed at their respective command boundaries. The earlier build output had exposed npm deprecation and pip root/version notices; they were recorded, the build commands were made explicit and the final image build completed without those notices or application warnings.

The recreated `fga17-local` web container became `healthy`. The real startup smoke passed liveness, readiness, the Academy catalogue, round creation, round start, opening retrieval, opening completion and workspace access. Readiness reported `round_repository: ready` and `frontend_distribution: ready`.

The optional `fga17-postgres` service also became healthy. An explicit `pg_isready -U fga -d fga` reported that PostgreSQL was accepting connections. This evidence is intentionally kept separate from the application’s SQLite repository.

### 5. Focused, regression and browser verification

The focused FGA-17 backend suite initially passed `4 tests` and still passed after the startup smoke assertions were tightened to check every intermediate status rather than only the final workspace response.

The full implementation regression passed:

| Surface | Final result |
| --- | --- |
| Backend full suite | `297 passed in 707.89s (0:11:47)`; no warnings or exceptions in the final output |
| FGA-17 focused backend suite | `4 passed in 15.03s` |
| Frontend typecheck | PASS |
| Frontend screen validation | PASS |
| Frontend Vite build | PASS; no Vite build warnings |
| Frontend Vitest | `26 files, 70 passed` |
| Browser E2E | `17 passed`; no warnings or exceptions in the final run |

The fresh frontend install still emitted the existing `whatwg-encoding@3.1.1` deprecation notice. The article-repo install emitted the existing install-script notices for `esbuild` and `workerd`. Those are dependency-environment notices, not application test failures, and remain visible here rather than being presented as a clean install that did not occur.

### 6. Article-repo and visual pass

- Content validation passed for `115 canonical articles`.
- The Astro build generated `/fga/17-docker-i-hardly-know-her/index.html` and completed successfully.
- Pagefind indexed 100 pages. Its existing default-UI informational note was recorded as an integration note, not a build failure.
- Same-origin link validation passed with `116` checked URLs and no failing internal URLs.
- The two immutable GitHub Raw image URLs returned HTTP 200.
- The article keeps the direct route unlisted, matching the preceding direct-route publication workflow.
- The final text pass checked the intro length, heading notation, separator positions, inline-code convention, repeated `FGA-17` framing and the explicit “not claimed” boundaries. No fenced snippets were introduced.
- The site estimator was rerun against the final markdown after the editorial trim: `3,515` words and `18` minutes at 200 words per minute. The first independent estimate was `4,085` words / `21` minutes; it triggered the reduction rather than being overridden by frontmatter.

The generated `1.png` is the newspaper/preview image. The generated `2.png` is the darker top-down case-file infographic. Both use the established muted sepia/charcoal palette, old-paper print treatment, noir office and recognisable Spanish Water Dog detective; neither introduces a bright neon palette or a wolf-like character.

### 7. Databricks qualification through profile `fga`

The requested profile was authenticated with `databricks current-user me --profile fga`. The final qualification command was:

```text
python scripts/qualify_fga17_environment.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --report reports/iteration-17/databricks-fga17-environment-current.json
```

The receipt at `reports/iteration-17/databricks-fga17-environment-current.json` records:

| Field | Result |
| --- | --- |
| Status | `pass` |
| Run | `2026-11-27T01:58:20.274153+00:00` |
| Source commit used by qualification | `33014199661e922b1dee851164fd01ecfc34e51a` |
| Profile / catalog / schema | `fga` / `sda_dev` / `sandbox` |
| Warehouse | `eded42c9d0a69b84` |
| Read-only | `true` |
| Protected truth source | `false` — not queried |
| Actual graph-engine run | `false` — not claimed |
| Remote public boundary | `pass`; 13 canonical packages |
| Docker on Databricks | `false` |

The qualification checks the active public projections, snapshots, counts, connected endpoints and allowlisted player-safe columns. It does not mutate the warehouse, inspect protected truth or pretend that Docker ran inside SQL Warehouse. The receipt stores only an authentication result for the profile, not SCIM email or group metadata.

### 8. Editorial review and regression decision

The integrated article was checked in four passes:

1. **Structure and series voice:** compared the opening, `Part I`–`Part VIII`, subsection density, noir dog narration, technical-table use, arrest, case status, next-case handoff, source-code section, receipt and final separator against FGA-15/FGA-16.
2. **Claim-to-branch consistency:** matched every implementation claim to code, focused tests, real Docker output, the optional PostgreSQL run or the Databricks receipt; downgraded the browser “login” incident to the explicit local player/session boundary.
3. **Line and rhythm:** removed generic tutorial phrasing, kept paragraphs short, varied sentence length, retained the series’ dry canine humour and checked that inline identifiers remain readable without fenced snippets.
4. **Production and accessibility:** checked the final 18-minute budget, heading order, table headers, direct route, source links, raw image URLs, alt text, image captions and the exact separator locations.

The independent lower-capacity editorial read found that the earlier draft was over the time budget, repeated the missing-package failure and used an intro sentence that implied incompatible states without naming their workflow boundary. The evidence-file concern was produced before the evidence commit was visible in that reviewer checkout; it was closed by the committed log, matrix and receipt. The final article changed the intro, kept the full failure only where it teaches the repair, reduced the later recaps and passed the estimator at 18 minutes. This was a read-only contrast, not a human-reader study or a 100-reviewer panel. Human reception remains not evaluated.

## Residual limits kept visible

FGA-17 does not prove that every registry, proxy, identity provider or production database will behave like the local stack. It does not add external authentication, cookie/session validation or a PostgreSQL application adapter. It does not claim GraphFrames or Zingg execution in SQL Warehouse. It does prove the smaller contract: named local workflows, fail-fast published image selection, a complete runtime image, bounded health signals, explicit network guidance, a reproducible board smoke and a read-only public Databricks boundary.

## Closure

FGA-17 is closed only after the article branch, implementation branch and assets branch have clean working trees, their remote heads are recorded below and the article/implementation matrix contains no unexplained claim.

| Repository | Final recorded commit |
| --- | --- |
| `fraud-graph-arena` | implementation/evidence commit `c075642` |
| `articles` | `5c50511` |
| `angelic-assets` | `507f68b04594a95772d0250e069518eab4ce29c8` |
