# Fraud Graph Arena — Action, Quote, Command, and Settlement Orchestration

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M13`  
**Module pair ID:** `FGA-MODULE-13-ACTION_COMMAND-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB acceptance plus MAINTENANCE execution/reconciliation  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M13 — Action, Quote, Command, and Settlement Orchestration**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own the four action-family protocol, authoritative quotes, idempotent acceptance, command lifecycle, durable dispatch intent, reconciliation, cancellation, and pre-reveal noninterference.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- quotes
- commands
- idempotency records
- outbox intents and provider state references
- command result cache
- reconciliation event history
- work-class and deadline binding

### 2.2 Capabilities

- validate the four action families
- create player-visible-input-only quotes
- accept a quote exactly once
- atomically coordinate debit, command, and outbox intent
- dispatch or resolve commands through adapters
- reconcile unknown outcomes before retry
- settle success, valid no-result, failure, refund, or manual review
- return deterministic cached results without a new charge
- apply bounded cancellation rules

### 2.3 Explicit non-goals

- credit ledger implementation
- record visibility implementation
- provider-specific API logic
- score calculation

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- ActionQuotePort
- CommandExecutionPort
- CommandStatusPort
- ReconciliationPort
- CancellationPort

### 3.2 Required outbound collaborations

- RoundAuthorizationPort M09
- SelectionValidation/RevealParticipant M11
- EconomySettlementPort M14
- RetrievalGateway M19
- Workflow/Clock/Idempotency support M20

### 3.3 Domain events

- QuoteIssued
- CommandAccepted
- DispatchRequested
- CommandPending
- CommandSucceeded
- CommandNoResult
- CommandRefunded
- CommandRecoveryRequired
- CommandCancelled

## 4. State model

The module recognizes these externally meaningful states or modes:

- QUOTED
- EXPIRED
- ACCEPTED
- DISPATCH_PENDING
- PROVIDER_PENDING
- SUCCEEDED
- NO_RESULT
- FAILED_REFUNDABLE
- REFUNDED
- CANCELLED_REFUNDED
- MANUAL_RECONCILIATION_REQUIRED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Every paid action requires an authoritative unexpired quote.
2. Quote and pre-settlement behavior MUST NOT depend on hidden cardinality or unrevealed facts.
3. Idempotency scope includes principal, operation, key, and canonical request hash.
4. Unknown external outcome MUST be reconciled before resubmission.
5. No network I/O occurs inside the debit/command database transaction.
6. A settled deterministic repeat returns the persisted result at zero additional game-credit cost.

## 6. Player-visible and operator-visible failure behavior

- Use player-safe typed failure classes.
- Hold economic state during unknown provider outcome.
- Quarantine poison work after bounded attempts.
- Enter round recovery when command settlement cannot be established.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No generated SQL, reasoning traces, hidden fields, provider credentials, or raw responses in public results/logs.
- Authorization is rechecked on replay and status.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Command + Economy + Investigation: atomic debit/command and terminal settlement/reveal.
2. Command + Retrieval: isolated provider/deterministic resolver protocol.
3. Command + Workflow: leases, fairness, retry, cancellation.
4. Command + Client Sync: duplicate click, timeout, exact replay.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M13-FR-001` | Every paid action requires an authoritative unexpired quote. |
| `M13-FR-002` | Quote and pre-settlement behavior MUST NOT depend on hidden cardinality or unrevealed facts. |
| `M13-FR-003` | Idempotency scope includes principal, operation, key, and canonical request hash. |
| `M13-FR-004` | Unknown external outcome MUST be reconciled before resubmission. |
| `M13-FR-005` | No network I/O occurs inside the debit/command database transaction. |
| `M13-FR-006` | A settled deterministic repeat returns the persisted result at zero additional game-credit cost. |
| `M13-FR-007` | The module MUST expose its capabilities only through the public contracts defined for M13. |
| `M13-FR-008` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M13-FR-009` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M13-FR-010` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M13 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§14–15, 24, 43, 49, 62, 83–84, 89, 95, 97–98.
- Parent technical specification: Technical §§11–13, 30, 40, 46, 49, 63, 85–86, 89, 97, 99, 103.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
