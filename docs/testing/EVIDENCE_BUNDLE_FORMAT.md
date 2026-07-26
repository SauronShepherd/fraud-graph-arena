# Iteration Evidence Bundle Format

**Format ID:** `FGA-EVIDENCE-FORMAT-1.0-20260726`

The normative machine-readable schema is [`schemas/testing/iteration-evidence.schema.json`](../../schemas/testing/iteration-evidence.schema.json).

## Required contents

- Evidence and iteration IDs.
- UTC generation time and exact source commit.
- Overall status and formal closure eligibility.
- Operating system, runtime/tool versions, and clean-checkout fact.
- Exact commands executed.
- Governing source artifact status and digests.
- One result for each universal gate `G01`–`G15`.
- Normalized test records including status, command, result, duration, seed where relevant, and report path.
- Temporary exceptions, known gaps, owners, expiry, and closure effect.
- Required approvals.
- Canonical SHA-256 of the bundle excluding its own `bundle_digest` field.

## Status semantics

- `passing`: all applicable gates pass and no blocking gap remains.
- `failing`: at least one executed applicable gate fails.
- `blocked`: verification is structurally sound but a prerequisite or required authority is unavailable.
- `not_applicable`: a capability does not yet exist; a reason is mandatory. Once introduced, its gate remains cumulative.

## Integrity

Evidence is generated, not hand-waved. The validator recalculates available source digests, schema-validates the bundle, verifies all fifteen gate IDs exactly once, rejects hidden critical skips/quarantines, and recalculates the bundle digest.

## I00 rule

Documentation-only I00 explicitly marks executable product layers not applicable. The absent v9.0 parent pair blocks `G01` and therefore `G15`; the bundle remains valid but cannot claim iteration closure.
