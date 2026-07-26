# Fraud Graph Arena — Case File, Claims, Evidence Mapping, and Submission

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M16`  
**Module pair ID:** `FGA-MODULE-16-CASE_FILE_SUBMISSION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB plus MAINTENANCE finalization  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M16 — Case File, Claims, Evidence Mapping, and Submission**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own the structured investigative argument, warnings, evidence-to-claim mapping, immutable canonical submission, evidence-root binding, and submission review lifecycle.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- case-file draft
- claims and classifications
- identity, role, culpability, harm, and context conclusions
- evidence links
- uncertainty and alternatives
- submission payload and canonical digest
- submission evidence Merkle root
- submission revision/state

### 2.2 Capabilities

- edit structured case-file fields
- attach visible evidence to explicit claims
- warn about unsupported, circular, duplicate, contradictory, or overbroad reasoning
- review required fields and pending work
- canonicalize the submission
- commit exactly one immutable submission
- bind economy/command snapshot and immutable versions
- expose read-only historical submission

### 2.3 Explicit non-goals

- score calculation
- protected truth
- progression
- record visibility grants
- generative prose as scoring authority

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- CaseFileCommandPort
- CaseFileQueryPort
- SubmissionReviewPort
- SubmissionCommitPort
- SubmissionContract

### 3.2 Required outbound collaborations

- RoundAuthorization/Finalization M09
- Visibility/EvidenceReference M11
- Economy/Command snapshots M13/M14
- Canonicalization/integrity M20

### 3.3 Domain events

- CaseFileChanged
- SubmissionReviewProduced
- SubmissionCommitted
- EvaluationRequested

## 4. State model

The module recognizes these externally meaningful states or modes:

- DRAFT
- REVIEW_BLOCKED
- REVIEW_READY
- SUBMISSION_PENDING
- SUBMITTED_IMMUTABLE

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Identity, role, culpability, harm, accusation, and context MUST remain separate.
2. Evidence MUST be attached to explicit claims.
3. Submission is free, explicit, irreversible, canonical, and idempotent.
4. Submission is blocked by nonterminal/economically indeterminate paid work.
5. Equivalent ordering/formatting MUST canonicalize identically.

## 6. Player-visible and operator-visible failure behavior

- Return safe warnings without answer-key leakage.
- Recover an already committed submission after a lost response.
- Enter recovery when finalization transaction is indeterminate.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Owner scope, protected private text, no truth fields, digest/Merkle lineage, no raw prose in telemetry, active-content-safe exports.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Case File + Investigation: visible evidence references.
2. Case File + Command/Round: submission block.
3. Case File + Evaluation: immutable canonical contract.
4. Case File + Save: reversible draft history but immutable submission.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M16-FR-001` | Identity, role, culpability, harm, accusation, and context MUST remain separate. |
| `M16-FR-002` | Evidence MUST be attached to explicit claims. |
| `M16-FR-003` | Submission is free, explicit, irreversible, canonical, and idempotent. |
| `M16-FR-004` | Submission is blocked by nonterminal/economically indeterminate paid work. |
| `M16-FR-005` | Equivalent ordering/formatting MUST canonicalize identically. |
| `M16-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M16. |
| `M16-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M16-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M16-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M16 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§16–18, 21, 50, 52, 87, 97.
- Parent technical specification: Technical §§9–12, 20, 50, 52, 90, 99–100.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
