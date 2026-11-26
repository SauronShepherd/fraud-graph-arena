# FGA-15 implementation log

## Scope

FGA-15 is the experience-layer case: the opening comic, the closure variants, transcripts, captions, sensory controls, optional audio governance and the boundary between atmosphere and evidence. The implementation deliberately does not claim that the complete future audio library or the complete 130-panel visual programme has shipped. Those remain governed backlog items.

The work was made on branch `FGA-15`, based on the FGA-14 documentation commit `dfe14c8`. The corresponding article and asset worktrees use the same branch name in their respective repositories.

## Implementation receipt

| Article promise | Implementation | Verification |
| --- | --- | --- |
| A case package declares its narrative | `CasePackage.narrative`, manifest generation and `fga15-narrative-v1` schema | Published-package validation and the iteration-15 manifest review |
| The opening comic is skippable and inspectable | `OpeningComicPage`, panel navigation, skip, preload of the next panel, caption, transcript and image fallback | Full Playwright suite and frontend Vitest |
| Closures vary by outcome | `EXCELLENT`, `PARTIAL` and `FAILED` variants mapped from the existing ending codes | Manifest review, API contract tests and browser coverage |
| Audio is optional and independently controllable | `AudioManager` with master/music/voice/effects buses, persistence, mute and reduced-sensory suppression | `audio.test.ts`; no enabled binary audio is shipped |
| Audio and visuals cannot become hidden evidence | disabled optional slots carry provenance, rights, approval and fallback metadata; the schema rejects an enabled asset without a file and license | adversarial fixtures and review script |
| Failure is visible and recoverable | missing asset, autoplay blocked, concurrency and fallback events are observable; text and visual state remain usable | audio tests, Playwright suite and review script |
| Accessibility is part of the case | captions, transcripts, alt text, reduced motion/sensory behaviour and no-autoplay default | manifest review, frontend tests and browser checks |

## Chronological log

### 1. Baseline and branch creation

- Created `FGA-15` worktrees in the implementation, article and assets repositories from their FGA-14 tips.
- Read the master FGA outline as authoritative for FGA-15. The older development-outline label is not used as the article title because the master outline now defines the published sequence as `The World Around the Case`.
- Preserved the existing case-package shape and the historical Academy opening rather than changing the public entry flow without evidence.

### 2. First implementation pass

- Added the narrative domain model, schema and validator.
- Added narrative data to every published case package and made the package generator reproduce it.
- Added API fields for captions, transcripts, closure variants, fictionalization, preload and audio references.
- Added the frontend audio manager, persistent preferences and accessible controls.
- Added opening and resolution rendering for transcripts, fallback state, closure variants and reduced-sensory behaviour.
- Added focused tests, adversarial fixtures and a local narrative review script.

### 3. Failures and corrections

#### Frontend dependencies were not installed

The first frontend typecheck/test attempt could not start because the worktree did not contain `node_modules`. This was an environment-preparation failure, not a product failure. Running `npm ci` restored the declared dependency graph.

`npm ci` reported the repository's existing dependency notices: the deprecated `whatwg-encoding@3.1.1` package and five audit findings (two moderate and three high). No automatic audit fix was applied because that would change the dependency graph outside the article's scope. The notices remain recorded here for the next dependency-maintenance pass.

#### The first browser pass exposed an opening-flow regression

The first Playwright run failed four assertions. The generated narrative had replaced every historical opening with two panels, while the existing browser contract expects the Academy case to keep its original two named panels and the other legacy cases to retain their one-step opening flow. The generator was corrected to special-case `ACADEMY_001` with its original titles and to keep one opening panel for the other legacy packages.

#### The first browser process used the wrong environment

One manual browser pass started the backend in development mode. That made the Puppy path appear disabled and exposed stale browser expectations. The backend was restarted in the intended test environment with the SQLite test repository. The current catalogue marks Puppy, Adult and Senior paths as open, so the two stale `toBeDisabled()` assertions were synchronised to the current product contract. The final run then passed all 15 browser tests.

#### A harmless Playwright runtime warning remained

The final Playwright invocation emitted Node's environment warning that `NO_COLOR` is ignored while `FORCE_COLOR` is set. It did not affect execution or assertions. It is recorded rather than misreported as a warning-free process.

### 4. Local verification after correction

The following results are from the FGA-15 worktree:

| Check | Result |
| --- | --- |
| `npm run typecheck` | PASS |
| `npm test -- --run src/narrative/audio.test.ts` | 3 passed |
| full frontend Vitest (`npm test`) | 25 files, 68 passed |
| `npm run build` | PASS; Vite completed without build warnings |
| backend focused suite (`tests/iteration_01`, `11`, `14`, `15`) | 56 passed |
| `tests/iteration_15/test_narrative_experience.py` | 3 passed |
| `python scripts/review_fga15_narrative.py` | PASS; 14 packages, no fixture errors |
| full Playwright suite (`npm run test:e2e`) | 15 passed |

The browser run used a test-only SQLite repository and a missing frontend distribution path. It did not write production data.

### 5. Databricks boundary

The remote qualification is run separately with `databricks ... --profile fga` and the SQL Warehouse qualification path. The qualification is read-only: it validates the published case-package contracts and narrative metadata, not hidden fraud truth or an unshipped audio library. Its result and source commit are appended to this receipt after the remote run.

### 6. Asset receipt

The assets branch contains:

- `images/articles/fga/15-the-world-around-the-case/1.png`: opening newspaper/preview image.
- `images/articles/fga/15-the-world-around-the-case/2.png`: final case-file infographic.

Both were visually inspected against the dark sepia/umber FGA reference set. The character is the Spanish Water Dog detective, not a wolf-like substitute; the imagery carries the narrative layer without presenting audio or atmosphere as evidence.

## Scope honesty

The release contains the contracts, controls, transcripts, fallback behaviour, governance metadata and tests needed to make the experience layer safe. It does not pretend that optional music, voice or effects are production evidence. The four audio slots are explicitly disabled and marked deferred until each has a real file, provenance, licence and approval. The larger visual backlog remains visible rather than being silently folded into the implementation claim.
