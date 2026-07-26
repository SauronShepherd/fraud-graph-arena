# Fraud Graph Arena — Save, Checkpoint, Draft History, and Recovery

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M15`  
**Module pair ID:** `FGA-MODULE-15-SAVE_RECOVERY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB and MAINTENANCE retention/recovery  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M15 — Save, Checkpoint, Draft History, and Recovery**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own autosave acknowledgements, manual ranked checkpoints, draft revision history, reversible restoration, practice forks, restart recovery, and conflict-safe persistence.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- save slots and checkpoint metadata
- draft revision history references
- practice fork lineage
- autosave status and revision
- retention/expiry metadata
- local-draft reconciliation envelope

### 2.2 Capabilities

- autosave reversible draft/UI state
- create and replace named checkpoints
- restore only reversible projections
- create full-state practice/academy forks
- recover after refresh, logout/login, restart, or database wake
- detect stale revisions
- retain bounded history
- expire abandoned private drafts under policy

### 2.3 Explicit non-goals

- credit, reveal, command, binding, submission, verdict, or progression rollback
- offline authoritative commit
- case-file business validation

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- AutosavePort
- CheckpointPort
- DraftHistoryPort
- PracticeForkPort
- RecoveryQueryPort

### 3.2 Required outbound collaborations

- Round revision/authorization M09
- visibility references M11
- case-file draft port M16
- client sync M06
- retention workflow M20

### 3.3 Domain events

- AutosaveAcknowledged
- CheckpointCreated
- CheckpointRestored
- PracticeForkCreated
- SaveConflictDetected
- DraftExpired

## 4. State model

The module recognizes these externally meaningful states or modes:

- SAVING
- SAVED
- RETRYING
- CONFLICT
- RECOVERY_REQUIRED
- EXPIRED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Ranked checkpoint restore MUST NOT alter monotonic evidence, commands, ledger, bindings, submission, verdict, or progression.
2. A full-state branch creates a new unranked round.
3. Server revision is authoritative.
4. Lost response replay is idempotent.
5. Private draft retention and cryptographic erasure follow the active policy.

## 6. Player-visible and operator-visible failure behavior

- Return conflict with current revision and safe merge/reload guidance.
- Retain local reversible edits as uncommitted during outage.
- Fail closed when referenced round/package is unavailable.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Private notes and draft prose are encrypted/erasable in PUBLIC_RANKED, excluded from general logs and caches, and owner-scoped.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Save + Client Sync: autosave and conflict UX.
2. Save + Round/Investigation/Economy: checkpoint isolation attack tests.
3. Save + Case File: revision restore.
4. Save + Platform: retention, restart, and erasure.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M15-FR-001` | Ranked checkpoint restore MUST NOT alter monotonic evidence, commands, ledger, bindings, submission, verdict, or progression. |
| `M15-FR-002` | A full-state branch creates a new unranked round. |
| `M15-FR-003` | Server revision is authoritative. |
| `M15-FR-004` | Lost response replay is idempotent. |
| `M15-FR-005` | Private draft retention and cryptographic erasure follow the active policy. |
| `M15-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M15. |
| `M15-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M15-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M15-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M15 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§21, 24, 31, 49, 53.
- Parent technical specification: Technical §§10–11, 22, 30, 35, 43, 53.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
