# Traceability Model

**Model ID:** `FGA-TRACEABILITY-MODEL-1.0-20260726`

The executable graph is [`config/governance/traceability.json`](../../config/governance/traceability.json) and is validated by [`schemas/governance/traceability.schema.json`](../../schemas/governance/traceability.schema.json).

## Required chain

`requirement → module/interaction → stage → task → test → evidence → release`

A requirement may govern multiple modules or interactions. A task implements one or more requirements but changes one file. Tests verify requirements, modules, interactions, stages, or tasks. Evidence records exact test outcomes. A release qualifies only evidence bundles whose required gates pass.

## Graph rules

- Node IDs are globally unique.
- Every edge endpoint exists.
- Every current requirement has at least one outgoing implementation or governance edge.
- Every task has exactly one repository path and at least one verifying test.
- Every test is recorded in evidence.
- Every one of `M01`–`M20` and `I01`–`I19` exists and participates in at least one edge.
- Orphan nodes are prohibited.
- Historical superseded nodes remain traceable and are never silently deleted.

## I00 scope

I00 creates governance traceability rather than product implementation. All twenty modules and nineteen interactions are registered as governed architecture objects; their executable product tests appear in later iterations. I00 tests the completeness and integrity of that registration.
