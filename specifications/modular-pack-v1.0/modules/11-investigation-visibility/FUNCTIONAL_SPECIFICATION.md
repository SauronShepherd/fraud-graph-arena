# Fraud Graph Arena — Investigation and Visibility Engine

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M11`  
**Module pair ID:** `FGA-MODULE-11-INVESTIGATION_VISIBILITY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB plus MAINTENANCE settlement  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M11 — Investigation and Visibility Engine**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own the authoritative revealed-state model, visibility grants, direct and analytical relationship provenance, manual hypotheses, selections, and ranked monotonicity.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- revealed records, documents, and relationships
- reveal provenance
- manual hypotheses and audit history
- safe record/relationship references
- visibility revision
- selection validation rules

### 2.2 Capabilities

- initialize starting evidence
- grant deterministic record/document/relationship visibility
- derive direct relationships when prerequisites are visible
- create/edit/delete manual hypotheses
- validate action selections against visible compatible objects
- deduplicate repeated reveals
- preserve ranked reveal monotonicity
- provide normalized read model input for list/graph projection

### 2.3 Explicit non-goals

- credit settlement
- provider interpretation
- case-file claims
- visual layout
- protected canonical entity merges

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- InvestigationCommandPort
- VisibilityQueryPort
- SelectionValidationPort
- RevealSettlementParticipant
- HypothesisPort

### 3.2 Required outbound collaborations

- RoundAuthorizationPort from M09
- CaseRules/SafeSchema from M10
- settlement commands from M13

### 3.3 Domain events

- RecordRevealed
- DocumentRevealed
- RelationshipRevealed
- ManualHypothesisCreated
- ManualHypothesisRetired
- VisibilityRevisionAdvanced

## 4. State model

The module recognizes these externally meaningful states or modes:

- INITIALIZING
- ACTIVE_MONOTONIC
- CLOSED_READ_ONLY

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Ranked evidence MUST be monotonic.
2. Manual hypotheses MUST remain visibly distinct from source and analytical facts.
3. Analytical results MUST reveal only contract-authorized endpoints and provenance.
4. Identity, role, culpability, and harm MUST remain separate.
5. Switching or filtering views MUST NOT grant visibility.

## 6. Player-visible and operator-visible failure behavior

- Reject selections containing unrevealed, incompatible, cross-case, or over-cap objects.
- Return prior persisted reveal for deterministic duplicate commands.
- Fail closed when publication/version provenance is inconsistent.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No protected truth, canonical identity, red-herring purpose, or scoring annotations in public state.
- Owner/round scope enforced in every query.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Investigation + Command/Economy: atomic successful settlement and reveal.
2. Investigation + Workspace: projection parity.
3. Investigation + Save: checkpoints cannot roll back reveals.
4. Investigation + Case File: evidence references must be visible and owned.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M11-FR-001` | Ranked evidence MUST be monotonic. |
| `M11-FR-002` | Manual hypotheses MUST remain visibly distinct from source and analytical facts. |
| `M11-FR-003` | Analytical results MUST reveal only contract-authorized endpoints and provenance. |
| `M11-FR-004` | Identity, role, culpability, and harm MUST remain separate. |
| `M11-FR-005` | Switching or filtering views MUST NOT grant visibility. |
| `M11-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M11. |
| `M11-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M11-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M11-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M11 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§12–14, 21, 25, 43, 94–95.
- Parent technical specification: Technical §§9–14, 30, 32, 46, 52, 89, 96–97.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
