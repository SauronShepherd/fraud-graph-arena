# Fraud Graph Arena — Client State and Synchronization

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M06`  
**Module pair ID:** `FGA-MODULE-06-CLIENT_STATE_SYNCHRONIZATION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB browser bundle  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M06 — Client State and Synchronization**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Coordinate server-authoritative state, revisions, request lifecycle, local convenience drafts, conflicts, stale clients, and degraded connectivity without becoming an authority for ranked state.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- client query cache metadata
- pending UI mutation state
- server revision projections
- local convenience draft envelope
- conflict and retry state
- request cancellation handles

### 2.2 Capabilities

- fetch and cache safe server projections
- attach expected revisions and idempotency keys
- debounce autosave independently of UI editing
- recover authoritative state after lost responses
- detect conflicts and present merge/reload paths
- prevent service-worker caching of authenticated responses
- abort obsolete requests
- surface offline, retrying, conflict, and stale-client states
- invalidate cache by contract/publication version

### 2.3 Explicit non-goals

- authoritative credits, evidence, commands, submissions, or progression
- offline ranked commit
- provider polling authority
- domain conflict resolution without module policy

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- QueryCachePort
- MutationCoordinator
- RevisionConflictHandler
- LocalDraftPort
- ClientCompatibilityGuard

### 3.2 Required outbound collaborations

- public client contracts from domain modules
- Shell global notice port
- browser network/cache adapters

### 3.3 Domain events

- SyncStateChanged
- ConflictDetected
- AuthoritativeStateRecovered
- ClientMutationAcknowledged

## 4. State model

The module recognizes these externally meaningful states or modes:

- SYNCED
- SAVING
- RETRYING
- OFFLINE_UNCOMMITTED
- CONFLICT
- STALE_CLIENT

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. A browser acknowledgement is required before a ranked mutation is shown as committed.
2. A local draft cannot change ledger, reveal, command, or submission history.
3. Conflicting writes MUST NOT overwrite newer server state.
4. Authenticated responses MUST be `no-store` and bypass service-worker caches.
5. Idempotent replay MUST preserve the original authorization and request fingerprint.

## 6. Player-visible and operator-visible failure behavior

- Retain unsent reversible draft edits locally and label them uncommitted.
- Reload authoritative state after timeout or conflict.
- Block mutation and require refresh when compatibility fails.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No credential, recovery code, protected truth, raw provider output, or export bytes in general client caches.
- Local storage, when used, is limited to approved non-sensitive preference/draft envelopes.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Client Sync + Save: autosave, conflict, and restore.
2. Client Sync + Command: lost response and idempotent replay.
3. Client Sync + Submission: single-winner concurrent submit.
4. Client Sync + Shell: stale-client blocking.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M06-FR-001` | A browser acknowledgement is required before a ranked mutation is shown as committed. |
| `M06-FR-002` | A local draft cannot change ledger, reveal, command, or submission history. |
| `M06-FR-003` | Conflicting writes MUST NOT overwrite newer server state. |
| `M06-FR-004` | Authenticated responses MUST be `no-store` and bypass service-worker caches. |
| `M06-FR-005` | Idempotent replay MUST preserve the original authorization and request fingerprint. |
| `M06-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M06. |
| `M06-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M06-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M06-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M06 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§21, 24, 46, 97–98.
- Parent technical specification: Technical §§16, 22, 34, 40, 44, 99, 102.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
