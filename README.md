# Fraud Graph Arena

This repository contains the FGA 03–06 implementation on top of the qualified Iteration 00 governance baseline. The Academy journey uses a frontend-owned declarative screen system; the canonical case-data and candidate-aware persistence subsystems are implemented behind explicit contract and security boundaries. FGA-06 adds a renderer-neutral graph investigation lab, a visible graph auto-test suite and current live qualification evidence from the `fga` Databricks profile. The historical FGA05 immutable closure record and a local Astra publication target remain explicit limitations.

## Playable result

`launch → select Detective Academy → select training case → create/start round → opening comic → enter board → retain context`

Every production screen is resolved through the versioned screen set, closed registries, semantic action boundary, deterministic machine, route codec, shared lifecycle host, and centralized transition effect. `CASE_RESOLUTION` is registered as an internal reusable family but remains unreachable in I03.

The Academy board is intentionally almost empty. The route, comic contract, state ownership, persistence boundary, composition root and tests are real.

## Why the Academy comes first

Iteration 01 does not open a ranked case. Detective Academy is the public development laboratory where the real mechanics can be built, explained, screenshotted and tested without revealing anthology names, clues, suspects, fraud structures or endings.

The ranked paths remain visible because their canonical identities are part of the product contract, but their availability is server-owned:

- `DETECTIVE_ACADEMY` — `OPEN`;
- `PUPPY` — `COMING_SOON`;
- `ADULT_DOG` — `LOCKED`;
- `SENIOR_DOG` — `LOCKED`.

The only playable file is the spoiler-free `ACADEMY_001 — The Case of the Empty Evidence Board`.

## What is implemented

- React/TypeScript presentation under `apps/web`;
- FastAPI/Python backend under `src/fraud_graph_arena`;
- modular-monolith boundaries between catalogue, narrative, round/game state, persistence adapters, analytics boundary and web presentation;
- canonical path IDs, availability and access messages supplied by the catalogue API;
- one Academy training case and no published ranked-case details;
- a generic opening/closing comic-sequence domain contract;
- two accessible opening comic pages with narration, alt text, URL-addressable page position and image fallback;
- a registered Academy closing sequence reserved for the later submission/evaluation flow;
- an enforced round lifecycle: `CREATED → INTRO_PENDING → ACTIVE`;
- board access blocked until the opening comic is completed or skipped;
- server-authoritative round state with memory and SQLite adapters;
- refresh-safe comic and board recovery from URL plus backend state;
- versioned `/api/v1` health, catalogue, round, opening and workspace contracts;
- explicit mapping between domain, API, persistence and presentation models;
- RFC 9457-style `application/problem+json` failures with correlation IDs;
- typed environment configuration and explicit dependency composition;
- a production image that serves the same built React application and API;
- explicit WEB, MAINTENANCE, EVALUATOR and MIGRATE runtime roots;
- a 1600×900 board geometry mapper, semantic board regions, asset hashes and release validation;
- keyboard-reachable unavailable investigation controls with typed semantic action IDs;
- Python, React component, screen-system and Playwright qualification tests;
- versioned declarative screen definitions with schema and graph validation;
- centralized navigation, cancellable screen data loading, semantic actions, lifecycle hooks and transition effects.
- FGA-18 structured observability with request correlation, safe traces, aggregate metrics, frontend error boundaries and declarative instrumentation selection;
- separate observability events from player-visible investigation history, with redaction and sync/async behaviour-preservation tests;
- FGA-19 release bindings for frontend, backend, migrations, case packages, graph assets and analytics jobs;
- immutable round/package version binding with forward-only SQLite migration and bind-or-freeze compatibility;
- machine-readable release manifests, explicit CI stages and a local promotion/rollback drill that keeps data rollback separate;
- Canonical Model v1 packages, typed registry, registered converters and strict package validation;
- candidate-aware case-version-scoped persistence, typed DDL, active-pointer publication and recovery primitives;
- registry-generated physical targets and least-privilege layer grants for Databricks deployment.

## Install the Python application and tests

```text
python -m pip install -e ".[test]"
```

## Run the backend

```text
python -m fraud_graph_arena.runtime
```

The API is available under `http://127.0.0.1:8000/api/v1`.

## Run the frontend

```text
cd apps/web
npm ci
npm run dev
```

Vite proxies `/api` to the backend on port `8000`.

## Run the tests

```text
python -m pytest -v

cd apps/web
npm run typecheck
npm run test
npm run test:e2e

python scripts/validate_screen_definitions.py
python scripts/run_iteration_03_gate.py --report reports/iteration-03/gate.json
```

The Playwright test proves that Hercule can enter Detective Academy, select `ACADEMY_001`, read multiple opening pages, refresh on page two, enter the empty board, refresh again and recover the same training case from authoritative state. It also proves that Puppy is not selectable yet.

## Run the Iteration 01 gate

After Python and frontend dependencies are installed:

```text
python scripts/run_iteration_01_gate.py --report reports/iteration-01/gate.json
```

The gate runs Python tests, frontend typechecking, component tests and Playwright. The iteration is not formally closed until every reported check has status `passed`.

## Run the FGA-17 container workflows

The local workflow is explicit about what Compose is resolving and what the
container receives at runtime:

```text
docker compose --profile local-build up --build
python scripts/fga17_startup_smoke.py --base-url http://127.0.0.1:8000
```

Open `http://127.0.0.1:8000` after the smoke test passes. The image is built
from the checked-out source, tagged as `fraud-graph-arena:local` by default,
and stores rounds in the `fga-local-data` volume. `FGA_SOURCE_REVISION` is a
non-secret build label; it is not a substitute for a release digest.

The published-image workflow is a separate Compose file. It cannot silently
fall back to a local build or an image that happens to be in the developer's
cache:

```text
$env:FGA_IMAGE = "registry.example/fga@sha256:..."
docker compose -f compose.yaml -f compose.published.yaml --profile published-image up
```

If `FGA_IMAGE` is absent, Compose fails before a container is created. A value
from `env_file` would arrive too late to fix that interpolation. The optional
PostgreSQL witness can be inspected independently:

```text
docker compose --profile postgres up -d postgres
docker compose --profile postgres ps
```

Its `pg_isready` result proves that PostgreSQL accepts a connection. It does
not prove that this repository's SQLite-backed application is ready, migrated,
authenticated or reachable from a browser. The app and the witness are kept
separate until a PostgreSQL application adapter exists.

The host workflow remains a third choice: load `.env`, start the Python API
and the frontend with their native commands, and use `127.0.0.1` for both.
Do not mix a host backend with a container-only hostname such as `web`, or a
browser on the host with a frontend URL that only exists inside the Compose
network.

Stop local services with `docker compose --profile local-build down`; add
`--volumes` only when intentionally resetting the local round file. The
static contract can be checked without Docker:

```text
python scripts/fga17_compose_contract.py
```

## Run the FGA-18 observability smoke

The observability recorder is deliberately local and in-process. It follows one
training action through the HTTP boundary, selected domain methods, SQLite
round/ledger operations and the deterministic analytics result. The smoke also
checks that raw round and player identifiers and protected truth do not appear
in the trace:

```text
python scripts/fga18_observability_smoke.py
python -m pytest -q tests/iteration_18
python scripts/qualify_fga18_observability.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --report reports/iteration-18/databricks-fga18-observability-current.json
```

The Databricks command is a read-only public-boundary qualification. It does
not execute the local recorder, Docker or a hidden-truth query. The JSON
instrumentation catalogue selects registered instrumentation IDs; it never
contains Python code or executable expressions. Logs, metrics, traces and
game-event history remain separate surfaces.

## Run the FGA-19 release candidate checks

FGA-19 treats a release as a compatible set of immutable units. The generated
manifest hashes the frontend, Python backend, migration, case-package, graph
asset and analytics boundaries. A round records the release, case package,
rules, scoring, economy, screen and API versions that created it. The next
release may improve the board; it does not silently rewrite that round.

```text
python scripts/generate_fga19_release_manifest.py --output reports/iteration-19/fga19-release-manifest-current.json
python scripts/validate_fga19_release.py --manifest reports/iteration-19/fga19-release-manifest-current.json
python scripts/fga19_release_smoke.py
python -m pytest -q tests/iteration_19
python scripts/qualify_fga19_release.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --manifest reports/iteration-19/fga19-release-manifest-current.json --report reports/iteration-19/databricks-fga19-release-current.json
```

The CI contract is in `contracts/release/fga19-ci-pipeline.json`. It names the
blocking stages from lint and unit tests through case validation, end-to-end,
container build and deployment smoke. The release smoke first migrates an old
round database, then rejects a deliberately corrupted digest, promotes a valid
candidate and moves the application pointer back. It does not pretend that an
application pointer rollback restores database state.

The Databricks command uses profile `fga` only for the read-only public case
boundary in `sda_dev.sandbox`. It does not mutate a publication, run Docker in
SQL Warehouse or query protected truth. The local release manifest, SQLite
migration and rollback pointer remain local evidence.

## Export the OpenAPI contract

```text
python scripts/export_openapi.py
```

The generated contract is written to `contracts/openapi-v1.json`.

## Boundaries

- **Presentation** renders state and sends commands; it does not own path availability, catalogue or progression rules.
- **Round/game state** owns the selected path, selected case and `CREATED → INTRO_PENDING → ACTIVE` journey.
- **Case content** owns canonical path and spoiler-free Academy metadata.
- **Narrative** owns versioned opening and closing comic sequences, page order, transcript text and alt text.
- **Persistence** implements the round repository port; it does not invent game rules.
- **Analytics** has a port but no implementation or authority in I01.

## Deliberate non-goals

There is no real ranked case content or player-facing evaluator behaviour. The graph gallery remains a safe presentation/interaction lab and does not authorize investigation or mutate canonical evidence. The `fga` Databricks evidence covers the current sandbox qualification, while the administrator identity cannot prove non-admin denial.

## Release status

The current FGA-06 release line is qualified locally and tagged through the release evidence workflow. Strict delivery status remains 24/25 in-scope obligations (96%) because the historical FGA05 immutable closure cannot be reconstructed from the current identity; Astra is not claimed because no local target or registered tooling exists.

Iteration 01 proves architectural continuity without spending any real-case spoilers.

The skeleton walks into class. It still solves nothing.
