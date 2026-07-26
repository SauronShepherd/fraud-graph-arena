# Normative Baseline

**Baseline ID:** `FGA-BASELINE-1.0-20260726`
**Iteration:** `I00`
**State:** blocked until the exact v9.0 pair and approvals are present

## Purpose

This baseline fixes the authority, integrity, precedence, and supersession rules used to build Fraud Graph Arena. The executable registry is [`config/governance/baseline.json`](../../config/governance/baseline.json).

## Authority and precedence

1. `FGA-NORMATIVE-PAIR-9.0-20260726` is the primary product and technical authority.
2. `FGA-MODULAR-SPEC-PACK-1.0-20260726` decomposes the parent pair into twenty independently testable modules and four runtime roles. It cannot override the parent pair.
3. `FGA-END-TO-END-BUILD-PLAN-1.0-20260726` governs tasks, stages, iterations, cumulative gates, evidence, and no-pass-no-progress behaviour.
4. Repository decisions implement those authorities and cannot silently redefine a constitutional requirement.

When lower-ranked artefacts conflict, the higher-ranked authority controls. Ambiguity becomes an explicit decision, risk, or blocking defect; it is never resolved silently in code.

## Normative pair membership

The pair is registered as two independently content-addressed source artefacts:

- `FGA-NORMATIVE-FUNCTIONAL-9.0-20260726`;
- `FGA-NORMATIVE-TECHNICAL-9.0-20260726`.

Formal closure requires both exact source files. The importer rejects files that do not contain the expected title, document version, pair ID, and a plausible complete document body. A pair summary, placeholder, reconstructed document, or guessed digest cannot satisfy the baseline.

Import instructions are in [`specifications/normative-pair-v9.0/README.md`](../../specifications/normative-pair-v9.0/README.md).

## Registered supplied artefacts

The registry contains the build plan, original modular-pack archive, architecture pair, module specification pairs, manifest, integrity listing, and eventually both v9.0 normative sources. Validation recalculates every available SHA-256 digest.

## Constitutional invariants

- The target is a twenty-module modular monolith composed into `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE` roles.
- Modules collaborate only through public contracts, immutable events, durable jobs, or explicit unit-of-work participant ports.
- Module-owned tables, repositories, migrations, internal classes, browser stores, and files are not shared.
- Protected truth is unavailable to public runtime roles.
- An iteration advances only after cumulative applicable gates pass from a clean checkout and evidence is reproducible.
- Critical tests cannot be skipped, quarantined, muted, or converted to expected failure.
- An immutable release tag is created only after the closure record passes.

## Supersession

A new baseline must identify every superseded artefact, preserve historical digests, state the change classification, include migration consequences, and generate a new baseline ID. Existing records remain immutable; supersession adds a new record rather than rewriting history.
