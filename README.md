# Fraud Graph Arena

This candidate implements `I01 — Academy walking skeleton and application baseline` on top of the qualified Iteration 00 governance baseline.

## Playable result

`launch → select Detective Academy → select training case → create/start round → opening comic → enter board → retain context`

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
- Python, React component and Playwright Academy walking-skeleton tests.

## Install the Python application and tests

```text
python -m pip install -e ".[test]"
```

## Run the backend

```text
python -m uvicorn fraud_graph_arena.web.main:app --reload
```

The API is available under `http://127.0.0.1:8000/api/v1`.

## Run the frontend

```text
cd apps/web
npm install
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
```

The Playwright test proves that Hercule can enter Detective Academy, select `ACADEMY_001`, read multiple opening pages, refresh on page two, enter the empty board, refresh again and recover the same training case from authoritative state. It also proves that Puppy is not selectable yet.

## Run the Iteration 01 gate

After Python and frontend dependencies are installed:

```text
python scripts/run_iteration_01_gate.py --report reports/iteration-01/gate.json
```

The gate runs Python tests, frontend typechecking, component tests and Playwright. The iteration is not formally closed until every reported check has status `passed`.

## Run the production-equivalent image

```text
docker compose up --build
```

Open `http://127.0.0.1:8000`. The final image contains the built frontend and backend and stores rounds in the `fga-data` volume.

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

There is no real ranked case content, evidence, graph, entity resolution, retrieval provider, economy, scoring, submission or evaluator behaviour yet. The Academy closing sequence is registered but not player-reachable until verdict selection exists.

Iteration 01 proves architectural continuity without spending any real-case spoilers.

The skeleton walks into class. It still solves nothing.
