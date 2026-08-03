# I01 — Academy walking skeleton and application baseline

## Qualified scope

Iteration 01 implements one deliberately thin, spoiler-free player journey:

`launch → Detective Academy → ACADEMY_001 → create/start round → opening comic → board → recover context`

The Academy board is intentionally empty. The integration boundaries are not.

## Academy-first policy

The public development series uses Detective Academy for examples, screenshots and automated journeys. Ranked paths remain visible but unavailable, and no real anthology case identifiers or content are published by this iteration.

Academy uses the same contracts and runtime path intended for later cases. It is not a second simplified game.

## Boundaries established

- **Presentation:** React renders server-provided path, case, comic and workspace DTOs.
- **Game state:** the rounds capability owns the selected path/case and the `CREATED → INTRO_PENDING → ACTIVE` lifecycle.
- **Case content:** the catalogue capability owns canonical path availability and Academy metadata.
- **Narrative:** versioned opening and closing sequences sit behind a dedicated public contract.
- **Persistence:** round repositories sit behind a port; memory and SQLite adapters are supplied by the composition root.
- **Analytics:** a port exists, but no provider is allowed to acquire game-state authority in this iteration.

## Public API

- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`
- `GET /api/v1/health/version`
- `GET /api/v1/catalogue/sections`
- `GET /api/v1/catalogue/{section}`
- `POST /api/v1/rounds`
- `POST /api/v1/rounds/{round_id}/start`
- `GET /api/v1/rounds/{round_id}/opening`
- `POST /api/v1/rounds/{round_id}/opening/complete`
- `GET /api/v1/rounds/{round_id}/workspace`

Failures use `application/problem+json`. Domain, API, persistence and presentation models are mapped explicitly rather than sharing one accidental representation.

## Comic contract

Every published case is validated to have at least one versioned `OPENING` sequence and one versioned `CLOSING` sequence. Every page requires contiguous ordering, narration and alt text.

Iteration 01 exposes only the opening sequence. The Academy closing sequence is registered now so case completeness is designed in, but it remains unreachable until submission, evaluation and ending selection exist.

The browser keeps comic page position in the URL query. Refreshing `/rounds/{round_id}/intro?page=2` reconstructs the same page from the server-owned sequence rather than component-local memory.

## State ownership

The browser stores only a round identifier as a convenience. The intro and board routes reconstruct case context from the backend. With the SQLite adapter, the same Academy round and intro-completion state survive browser refresh and application recomposition.

The board rejects `INTRO_PENDING` rounds with the deliberate `INTRO_REQUIRED` problem contract.

## Qualification

The Iteration 01 gate includes:

- Python boot, architecture, API, narrative, persistence and journey tests;
- TypeScript typechecking;
- React component/navigation tests;
- Playwright browser automation from launch to comic to board, including refresh at both stages.

## Non-goals

No ranked case data, real evidence, graph, entity resolution, analytics provider, economy, scoring, submission or evaluator behaviour is implemented. The Academy proves the functional route without revealing the anthology.
