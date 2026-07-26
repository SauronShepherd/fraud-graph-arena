# Fraud Graph Arena — Investigation Economy and Credit Ledger

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M14`  
**Module pair ID:** `FGA-MODULE-14-ECONOMY_CREDIT-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB and MAINTENANCE settlement  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M14 — Investigation Economy and Credit Ledger**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own fictional investigation credits, exact append-only ledger semantics, debit/refund invariants, balance projection, quote-cost validation, and efficiency snapshot inputs.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- credit ledger entries
- materialized/derived balance
- debit and refund correlation
- economy policy/version reference
- efficiency accounting projection

### 2.2 Capabilities

- authorize and append debit
- append unique refund
- derive or reconcile balance
- validate quoted game-credit cost
- produce immutable command/submission economy snapshot
- detect impossible negative or duplicate state
- support exact deterministic arithmetic

### 2.3 Explicit non-goals

- real provider currency/cost accounting
- quote lifecycle
- command dispatch
- leaderboard rank computation

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- EconomySettlementPort
- BalanceQueryPort
- LedgerQueryPort
- EconomySnapshotPort
- LedgerReconciliationPort

### 3.2 Required outbound collaborations

- signed economy policy from M10/M20
- transaction context from M20

### 3.3 Domain events

- CreditDebited
- CreditRefunded
- LedgerInvariantViolation
- EconomySnapshotCreated

## 4. State model

The module recognizes these externally meaningful states or modes:

- AVAILABLE
- ZERO_CREDITS
- HELD_PENDING_RECONCILIATION
- CLOSED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Balance MUST never become negative.
2. Ledger history is append-only.
3. A debit references exactly one accepted command; a refund references exactly one debit and reason.
4. Investigation credits MUST never represent money or provider cost.
5. Zero credits MUST not prevent free work or submission.

## 6. Player-visible and operator-visible failure behavior

- Fail the entire acceptance transaction when debit cannot commit.
- Alert and fail closed on invariant mismatch.
- Hold rather than guess during indeterminate external outcome.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Owner/round scope, exact numeric types, no client price authority, no mutable balance-only update path.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Economy + Command: shared transaction for debit and command creation.
2. Economy + Investigation: terminal charge/refund/reveal finalization.
3. Economy + Save: checkpoint cannot restore ledger.
4. Economy + Submission/Evaluation: immutable efficiency snapshot.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M14-FR-001` | Balance MUST never become negative. |
| `M14-FR-002` | Ledger history is append-only. |
| `M14-FR-003` | A debit references exactly one accepted command; a refund references exactly one debit and reason. |
| `M14-FR-004` | Investigation credits MUST never represent money or provider cost. |
| `M14-FR-005` | Zero credits MUST not prevent free work or submission. |
| `M14-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M14. |
| `M14-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M14-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M14-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M14 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§15, 21, 52, 84.
- Parent technical specification: Technical §§10, 13, 35, 50, 86, 89.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
