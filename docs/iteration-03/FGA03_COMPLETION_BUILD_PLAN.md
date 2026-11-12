# FGA 03 Completion Build Plan

## Objective

Implement only the requirements stated in **FGA 03 — Screen Me Up Before You Go Go**. The production flow must be driven by the declarative screen contract, state machine, action registry, data-source registry, and transition coordinator. FGA 04+ features remain out of scope.

## Required implementation

1. Preserve the finite screen contract and its screen families: launch, path selection, case selection, case introduction, investigation board, and internal case resolution.
2. Add explicit schema, document, and minimum-runtime version metadata; validate the JSON Schema at build time and runtime compatibility and registries at startup.
3. Load screen models through the runtime data-source registry, abort obsolete requests, and execute declared lifecycle hooks from `ScreenHost`.
4. Route user intent through registered actions, convert action results into machine events, resolve a `TransitionPlan`, and submit that plan to one transition coordinator.
5. Make the coordinator own effect timing, history policy, destination navigation, and transition locking.
6. Keep page components focused on rendering and dispatching semantic actions; remove page-local screen navigation and data orchestration.
7. Keep the internal case-resolution definition registered but unreachable from the production graph.

## Evidence required

- TypeScript typecheck passes.
- Unit and integration tests cover contract validation, machine resolution, lifecycle/data loading, action dispatch, history policy, reduced motion, and coordinator locking.
- Registry audit tests reject public screens with no outgoing transition and cycles outside the reviewed navigation journey.
- Navigation tests cover the full FGA 03 walking skeleton and URL reconstruction.
- Static architecture checks confirm pages do not import API clients or perform route orchestration directly.
- Screen-set schema and repository gate checks pass.

## Completion boundary

The work is complete when every item above is implemented and all evidence checks pass. Do not add ranked progression, multiplayer, advanced graph analysis, or other FGA 04+ behavior.
