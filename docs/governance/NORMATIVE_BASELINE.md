# Normative Baseline

**Baseline ID:** `FGA-BASELINE-10.0-20260726`
**Iteration:** `I00`
**State:** active after the exact v10.0 pair, source digests, approvals, and clean qualification evidence are present

## Purpose

This baseline fixes the authority, integrity, precedence, and supersession rules used to build Fraud Graph Arena. The executable registry is [`config/governance/baseline.json`](../../config/governance/baseline.json).

## Authority and precedence

1. `FGA-NORMATIVE-PAIR-10.0-20260726` is the primary product and technical authority. It explicitly supersedes the paired v9.0 specifications.
2. `FGA-MODULAR-SPEC-PACK-1.0-20260726` remains a useful historical decomposition of twenty modules and four runtime roles where compatible with v10.0. It cannot override the current pair.
3. `FGA-END-TO-END-BUILD-PLAN-1.0-20260726` governs the Iteration-00 delivery sequence, cumulative gates, evidence, and no-pass-no-progress behaviour where compatible with v10.0.
4. Repository decisions implement those authorities and cannot silently redefine a constitutional requirement.

When lower-ranked artefacts conflict, the higher-ranked authority controls. Ambiguity becomes an explicit decision, risk, migration, or blocking defect; it is never resolved silently in code.

## Normative pair membership

The current pair is registered as two independently content-addressed source artefacts:

- `FGA-NORMATIVE-FUNCTIONAL-10.0-20260726`;
- `FGA-NORMATIVE-TECHNICAL-10.0-20260726`.

Both documents declare `FGA-NORMATIVE-PAIR-10.0-20260726`, identify version 10.0, and explicitly supersede version 9.0. Validation checks the expected title, document version, pair ID, filename, plausible completeness, and exact SHA-256 digest.

Re-import instructions are in [`specifications/normative-pair-v10.0/README.md`](../../specifications/normative-pair-v10.0/README.md).

## Registered supporting artefacts

The registry also contains the build plan, original modular-pack archive, architecture pair, twenty module specification pairs, manifest, and integrity listing. These supporting artefacts remain required for Iteration-00 traceability but are subordinate to the v10.0 normative pair.

## Constitutional invariants

- The target is a twenty-module modular monolith composed into `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE` roles.
- Modules collaborate only through public contracts, immutable events, durable jobs, or explicit unit-of-work participant ports.
- Module-owned tables, repositories, migrations, internal classes, browser stores, and files are not shared.
- Protected truth is unavailable to public runtime roles.
- An iteration advances only after cumulative applicable gates pass from a clean checkout and evidence is reproducible.
- Critical tests cannot be skipped, quarantined, muted, or converted to expected failure.
- An immutable release tag is created only after the closure record passes.

## Supersession

A new baseline must identify every superseded artefact, preserve historical identities and digests where available, state the change classification, include migration consequences, and generate a new baseline ID. Existing release records remain immutable; supersession adds a new baseline rather than rewriting a historical tag.
