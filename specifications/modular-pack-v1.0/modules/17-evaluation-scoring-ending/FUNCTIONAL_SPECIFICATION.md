# Fraud Graph Arena — Evaluation, Scoring, Endings, Verdicts, and Amendments

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M17`  
**Module pair ID:** `FGA-MODULE-17-EVALUATION_SCORING_ENDING-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** EVALUATOR plus MAINTENANCE safe finalization  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M17 — Evaluation, Scoring, Endings, Verdicts, and Amendments**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own protected-truth evaluation, deterministic score/gates/penalties/endings, safe verdict envelope, declassification, amendment lineage, and oracle-resistance.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- protected evaluator truth access adapter
- evaluator bundle and version
- evaluation request/result
- score component breakdown
- solve gates and penalties
- ending code
- safe coaching/debrief references
- signed verdict envelope
- amendment lineage and validity state

### 2.2 Capabilities

- verify immutable submission and binding digests
- evaluate deterministically against protected truth
- select exactly one ending by versioned precedence
- emit only schema-limited safe verdict
- sign/bind verdict lineage
- support replay and historical versioning
- create linked amendments without overwrite
- enforce declassification manifest
- resist adaptive oracle leakage

### 2.3 Explicit non-goals

- player-facing record retrieval
- career progression table mutation inside evaluator
- nondeterministic model authority over score
- public truth repository access

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- PrivateEvaluationPort
- VerdictEnvelopePort
- EvaluationReplayPort
- AmendmentPort

### 3.2 Required outbound collaborations

- immutable SubmissionContract M16
- protected case/evaluator bundle M10/M20
- private key/time/trust services M20

### 3.3 Domain events

- EvaluationStarted
- SafeVerdictProduced
- EvaluationFailedSafe
- VerdictAmended
- VerdictInvalidated

## 4. State model

The module recognizes these externally meaningful states or modes:

- PENDING
- EVALUATED_SAFE
- UNDER_REVIEW
- INVALIDATED
- SUPERSEDED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Identical canonical inputs and versions MUST produce identical output.
2. A generative model MUST NOT decide score, gates, ending, progression, or eligibility.
3. Public web identity MUST never possess truth credentials or evaluator signing keys.
4. Original verdicts are immutable; corrections are linked amendments.
5. Safe outputs and support/appeal surfaces MUST NOT become truth oracles.

## 6. Player-visible and operator-visible failure behavior

- Produce a safe typed failure and retain immutable request for retry.
- Do not expose truth on evaluator failure.
- Require compatible evaluator/policy/declassification lineage before finalization.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Separate runtime identity/network/credentials, least-privilege truth read, signed safe envelope, no truth payload logs, phishing-resistant privileged operations.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Evaluation + Submission: digest/version verification.
2. Evaluation + Maintenance/Career: safe verdict finalization and progression.
3. Evaluation + Leaderboard: eligibility/result event.
4. Evaluation + Publication: old bundle replay and amendments.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M17-FR-001` | Identical canonical inputs and versions MUST produce identical output. |
| `M17-FR-002` | A generative model MUST NOT decide score, gates, ending, progression, or eligibility. |
| `M17-FR-003` | Public web identity MUST never possess truth credentials or evaluator signing keys. |
| `M17-FR-004` | Original verdicts are immutable; corrections are linked amendments. |
| `M17-FR-005` | Safe outputs and support/appeal surfaces MUST NOT become truth oracles. |
| `M17-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M17. |
| `M17-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M17-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M17-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M17 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§18–19, 33, 50, 63, 87, 90.
- Parent technical specification: Technical §§4, 6, 9, 11, 20, 46, 49–50, 64, 89–90, 102.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
