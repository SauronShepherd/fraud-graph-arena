# Change Classification

**Policy ID:** `FGA-CHANGE-CLASSIFICATION-1.0-20260726`

| Class | Meaning | Minimum consequence |
|---|---|---|
| Editorial | Wording or formatting with no semantic effect | Owner review, document validation, link and digest refresh |
| Compatible | Additive behavior or contract field that preserves supported consumers | Owner and consumer review, N-1/N compatibility tests |
| Migration-required | State, schema, event, or API change needing coexistence or transformation | Architecture and data review, migration/replay/rollback tests |
| Ranking-affecting | Changes evidence, costs, scoring, eligibility, provider mode, or leaderboard comparability | Product, evaluator, fairness, security, and release review; segment/version migration |
| Constitutional | Changes module boundaries, truth isolation, exact-once economics, immutable bindings, or no-pass-no-progress | Normative artifact revision, independent architecture/security approval, full qualification |
| Emergency | Time-critical containment for security, privacy, integrity, or availability | Incident authority, bounded change, immediate evidence, follow-up root cause and permanent fix |

## Decision rule

Classify by the highest applicable consequence, not the smallest edited diff. A textual change that alters scoring meaning is ranking-affecting; a one-line dependency that exposes evaluator truth to `WEB` is constitutional.

## Required record

Every non-editorial change records classification, rationale, affected requirements/modules/interactions, compatibility and migration impact, tests, risk owner, reviewer, and evidence. Emergency changes additionally record incident ID, expiry, rollback, and follow-up tasks.
