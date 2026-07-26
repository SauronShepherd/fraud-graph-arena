# Fraud Graph Arena — Retrieval, Deterministic Resolver, and Provider Gateway

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M19`  
**Module pair ID:** `FGA-MODULE-19-RETRIEVAL_PROVIDER_GATEWAY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** MAINTENANCE primarily; WEB for free deterministic planning only  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M19 — Retrieval, Deterministic Resolver, and Provider Gateway**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own bounded natural-language planning/clarification, deterministic ranked result resolution, provider adapters, conversation isolation, result firewall, parity evidence, capability/capacity, and real provider-cost accounting.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- canonical retrieval plans
- ambiguity/clarification classes
- ranked retrieval parity manifest references
- provider capability snapshots
- provider conversation records
- provider cost ledger and price catalogue
- safe normalized retrieval results
- provider adapter correlation state

### 2.2 Capabilities

- plan safe intent without data access
- offer bounded free clarification or abstain
- use a live provider only for approved interpretation/validation
- resolve authoritative ranked rows deterministically from immutable safe data
- execute qualified unranked/live modes where allowed
- validate row/column/case/profile/intent boundaries
- isolate one conversation per accepted ranked command
- track capacity headroom, retention, and deletion
- reserve and reconcile real provider cost separately from game credits
- strip SQL, reasoning, visualizations, comments, and rich output

### 2.3 Explicit non-goals

- command quote/debit authority
- visibility grant authority
- score or culpability inference
- cross-command memory as gameplay
- arbitrary SQL or file upload

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- IntentPlanningPort
- ClarificationPort
- RetrievalExecutionPort
- CapabilityQueryPort
- ConversationLifecyclePort
- ProviderCostPort

### 3.2 Required outbound collaborations

- case safe schema/publication M10/M20
- command context M13
- deterministic player-safe data adapter
- external provider APIs behind private adapters

### 3.3 Domain events

- IntentPlanned
- ClarificationRequired
- RetrievalAbstained
- DeterministicResultResolved
- ProviderConversationCreated
- ProviderResultRejected
- ProviderCostReconciled
- ConversationDeletionConfirmed

## 4. State model

The module recognizes these externally meaningful states or modes:

- PLANNING
- CLARIFICATION
- READY
- EXECUTING
- VALIDATING
- SUCCEEDED
- NO_RESULT
- REJECTED
- CAPACITY_CLOSED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Every supported ranked canonical intent MUST map to one stable ordered answer-set digest.
2. A live provider cannot authoritatively select ranked evidence.
3. Clarification is free, bounded, accessible, and equivalent for equivalent ambiguity.
4. Provider conversations are isolated and cross-command history is disabled.
5. Provider result schema and size are allowlisted.
6. Real provider cost is private operational accounting and never investigation credits.

## 6. Player-visible and operator-visible failure behavior

- Abstain before debit when ambiguity or safety cannot be resolved.
- Fail closed and follow command refund/reconciliation policy for malformed/unsafe output.
- Close admission before capacity/budget/privacy limits are threatened.
- Persist deletion and unknown-outcome state.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No truth, private notes, account identity, credentials, generated SQL, reasoning, active content, or cross-case data in provider boundary/logs.
- LLMSVS/AISVS threat tests and prompt/data-injection controls.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Retrieval + Command: accepted plan and durable execution.
2. Retrieval + Publication: parity manifests and deterministic resolver.
3. Retrieval + Workflow: timeouts, reconciliation, capacity, deletion.
4. Retrieval + Investigation: safe result IDs only through command settlement.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M19-FR-001` | Every supported ranked canonical intent MUST map to one stable ordered answer-set digest. |
| `M19-FR-002` | A live provider cannot authoritatively select ranked evidence. |
| `M19-FR-003` | Clarification is free, bounded, accessible, and equivalent for equivalent ambiguity. |
| `M19-FR-004` | Provider conversations are isolated and cross-command history is disabled. |
| `M19-FR-005` | Provider result schema and size are allowlisted. |
| `M19-FR-006` | Real provider cost is private operational accounting and never investigation credits. |
| `M19-FR-007` | The module MUST expose its capabilities only through the public contracts defined for M19. |
| `M19-FR-008` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M19-FR-009` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M19-FR-010` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M19 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§14, 24, 38, 41, 43, 62, 65, 72, 77, 83–84, 89, 94–95, 98.
- Parent technical specification: Technical §§13, 23–24, 30, 33, 42, 56, 63, 67, 73, 78, 85–86, 91, 96–97, 103.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
