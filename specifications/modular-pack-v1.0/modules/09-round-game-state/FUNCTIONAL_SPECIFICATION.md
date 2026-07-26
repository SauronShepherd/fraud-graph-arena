# Fraud Graph Arena — Round and Game-State Engine

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M09`  
**Module pair ID:** `FGA-MODULE-09-ROUND_GAME_STATE-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB plus MAINTENANCE recovery/finalization  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M09 — Round and Game-State Engine**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own one immutable-version-bound investigation attempt, its lifecycle, mode, ranking segment, compatibility bindings, and authorization of lifecycle-dependent operations.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- round aggregate
- immutable version binding set
- round lifecycle and phase detail
- mode and career linkage
- provider mode/capability binding
- ranking segment
- recovery reason
- round revision

### 2.2 Capabilities

- create ranked, practice, academy, revisit, and review rounds
- bind case, snapshot, profile, policy, rules, economy, scoring, provider, asset, and contract versions
- start and resume a round
- authorize operations by lifecycle
- enter and leave recovery states safely
- block mutation after submission
- preserve provider-mode continuity
- expire or abandon according to policy

### 2.3 Explicit non-goals

- record visibility details
- credit ledger
- case-file contents
- provider execution
- evaluation truth

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- RoundCommandPort
- RoundQueryPort
- RoundAuthorizationPort
- RoundBindingPort
- RoundFinalizationParticipant

### 3.2 Required outbound collaborations

- CareerEligibilityPort from M08
- CaseBindingPort from M10
- RuntimeAdmission/PolicyPort from M20

### 3.3 Domain events

- RoundCreated
- RoundActivated
- RoundRecoveryRequired
- SubmissionCommitted
- EvaluationPending
- RoundClosed
- RoundAbandoned
- RoundExpired

## 4. State model

The module recognizes these externally meaningful states or modes:

- CREATED
- ACTIVE
- SUBMISSION_PENDING
- EVALUATION_PENDING
- CLOSED
- ABANDONED
- EXPIRED
- RECOVERY_REQUIRED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Round bindings MUST be immutable after creation.
2. A round MUST NOT change provider mode or ranking segment.
3. Submission is blocked while accepted paid work is nonterminal or economically indeterminate.
4. Zero credits MUST NOT prevent free work or submission.
5. A stale/incompatible client cannot mutate a round.

## 6. Player-visible and operator-visible failure behavior

- Enter RECOVERY_REQUIRED for uncertain economic, provider, publication, or evaluation state.
- Return player-safe recovery actions without exposing internal details.
- Reject invalid state transitions deterministically.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Owner-scoped round access, opaque identifiers, no protected truth or authoring metadata in public bindings.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Round + Investigation: lifecycle gates all reveals and hypotheses.
2. Round + Command/Economy: submission block and recovery.
3. Round + Save: revisions and monotonic state.
4. Round + Submission/Evaluation: single immutable close path.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M09-FR-001` | Round bindings MUST be immutable after creation. |
| `M09-FR-002` | A round MUST NOT change provider mode or ranking segment. |
| `M09-FR-003` | Submission is blocked while accepted paid work is nonterminal or economically indeterminate. |
| `M09-FR-004` | Zero credits MUST NOT prevent free work or submission. |
| `M09-FR-005` | A stale/incompatible client cannot mutate a round. |
| `M09-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M09. |
| `M09-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M09-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M09-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M09 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§5, 11, 21, 38, 43, 49, 98.
- Parent technical specification: Technical §§8–13, 35, 40, 43, 46, 49, 89, 102.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
