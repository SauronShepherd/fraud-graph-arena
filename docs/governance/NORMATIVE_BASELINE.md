# Normative Baseline

**Baseline ID:** `FGA-BASELINE-1.0-20260726`
**Iteration:** `I00`
**State:** blocked pending the parent v9.0 pair

## Purpose

This baseline fixes the authority, integrity, precedence, and supersession rules used to build Fraud Graph Arena. The machine-readable registry is [`config/governance/baseline.json`](../../config/governance/baseline.json).

## Authority and precedence

1. `FGA-NORMATIVE-PAIR-9.0-20260726` is the primary product and technical authority.
2. `FGA-MODULAR-SPEC-PACK-1.0-20260726` decomposes the parent pair into twenty independently testable modules and four runtime roles. It cannot override the parent pair.
3. `FGA-END-TO-END-BUILD-PLAN-1.0-20260726` governs tasks, stages, iterations, cumulative gates, and evidence.
4. Repository decisions implement those authorities. A repository decision that changes a constitutional invariant requires explicit change classification and approval.

When two lower-ranked artifacts conflict, the higher-ranked artifact controls. Ambiguity is recorded as a decision or risk; it is never resolved silently in code.

## Registered supplied artifacts

The baseline registry records the supplied build plan, the original modular-pack archive, and every unpacked pack file with SHA-256. Validation recalculates every available digest.

## Missing prerequisite

The modular pack explicitly states that it does not replace `FGA-NORMATIVE-PAIR-9.0-20260726`. Those two source documents were not included in the supplied build inputs. Their absence is a blocking governance fact, not a digest placeholder. I00 may not be formally closed until both files are supplied, registered, and verified.

## Constitutional invariants

- The target is a twenty-module modular monolith composed into `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE` roles.
- Modules collaborate only through public contracts, immutable events, durable jobs, or explicit unit-of-work participant ports.
- Module-owned tables, repositories, migrations, internal classes, browser stores, and files are not shared.
- Protected truth is unavailable to public runtime roles.
- An iteration advances only after cumulative applicable gates pass from a clean checkout and evidence is reproducible.
- Critical tests cannot be skipped, quarantined, muted, or converted to expected failure.

## Supersession

A new baseline must identify every superseded artifact, preserve historical digests, state the change classification, include migration consequences, and generate a new baseline ID. Existing records are immutable; supersession adds a new record rather than rewriting history.
