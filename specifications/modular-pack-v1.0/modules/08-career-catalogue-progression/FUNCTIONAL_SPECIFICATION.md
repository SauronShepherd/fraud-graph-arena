# Fraud Graph Arena — Career, Catalogue, and Progression

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M08`  
**Module pair ID:** `FGA-MODULE-08-CAREER_CATALOGUE_PROGRESSION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB and MAINTENANCE finalization  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M08 — Career, Catalogue, and Progression**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own named careers, fixed entry tiers and paths, catalogue state derivation, practice/revisit eligibility, atomic progression, and default-resume preference.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- careers
- career path and current unlocked position
- career case progress
- career events
- default-resume pointer
- derived case-card state and availability reason

### 2.2 Capabilities

- create multiple independent careers
- select immutable entry tier
- derive OPEN/CLOSED/LOCKED state separately from availability
- resume or archive careers
- offer practice and revisit according to policy
- apply family presentation transitions
- unlock exactly the next eligible published case
- complete final career
- preserve skipped earlier cases as not completed

### 2.3 Explicit non-goals

- case-package publication
- round lifecycle internals
- score calculation
- leaderboard ranking
- destructive replacement of prior careers

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- CareerCommandPort
- CareerQueryPort
- ProgressionPort
- CatalogueProjectionPort
- RoundEligibilityPort

### 3.2 Required outbound collaborations

- CaseAvailabilityPort from M10/M20
- EvaluationFinalized event from M17
- Identity ownership principal from M07

### 3.3 Domain events

- CareerCreated
- DefaultResumeChanged
- CaseOpened
- CaseClosed
- NextCaseUnlocked
- CareerCompleted
- CareerArchived

## 4. State model

The module recognizes these externally meaningful states or modes:

- ACTIVE
- COMPLETED
- ARCHIVED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Creating a career MUST NOT archive or overwrite another career.
2. Entry tier and fixed path are immutable.
3. Progression advances only from eligible ranked production results.
4. Exactly one next case may unlock; retries are idempotent.
5. Practice, Academy, revisit, reviewer, and invalidated results MUST NOT advance progression.

## 6. Player-visible and operator-visible failure behavior

- Expose stable availability reason codes for unpublished, quarantined, retired, and incompatible cases.
- Keep historical review available when new starts are disabled.
- Enter recovery rather than skip progression when atomic finalization cannot complete.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Owner-scoped career access, opaque identifiers, no hidden truth in catalogue projections, audited operator corrections only.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Career + Case/Publication: catalogue projection.
2. Career + Round: create/resume eligible round.
3. Career + Evaluation: atomic or coordinated verdict/progression finalization.
4. Career + Leaderboard: eligibility remains separate from progression.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M08-FR-001` | Creating a career MUST NOT archive or overwrite another career. |
| `M08-FR-002` | Entry tier and fixed path are immutable. |
| `M08-FR-003` | Progression advances only from eligible ranked production results. |
| `M08-FR-004` | Exactly one next case may unlock; retries are idempotent. |
| `M08-FR-005` | Practice, Academy, revisit, reviewer, and invalidated results MUST NOT advance progression. |
| `M08-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M08. |
| `M08-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M08-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M08-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M08 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§5–9, 20, 33, 38.
- Parent technical specification: Technical §§6, 8–12, 35, 46.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
