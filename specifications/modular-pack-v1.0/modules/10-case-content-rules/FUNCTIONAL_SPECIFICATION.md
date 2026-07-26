# Fraud Graph Arena — Case Content and Rules

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M10`  
**Module pair ID:** `FGA-MODULE-10-CASE_CONTENT_RULES-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB reads; MIGRATE/publication compiles  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M10 — Case Content and Rules**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own the registry-driven definition of cases, investigation profiles, safe fields, starting evidence, action/rule configuration, content suitability, and evaluator/publication references.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- case registry and stable ordering
- case manifest schema
- investigation profile definitions
- safe record/document/relationship type dictionaries
- starting evidence and reveal prerequisites
- action caps and rule references
- content warnings, fictionalization, debrief metadata
- case-package compatibility declaration

### 2.2 Capabilities

- load a case by stable ID and immutable version
- validate complete manifests
- expose player-safe case metadata
- derive cumulative profile content
- provide allowed action and selection configuration
- provide evaluator and scoring bundle references without exposing truth
- support Academy and Kennel Lab through the same contract
- block incomplete or incompatible packages

### 2.3 Explicit non-goals

- active publication pointer authorization
- runtime workflow execution
- career progression
- hard-coded case-specific engine forks

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- CaseRegistryQuery
- CaseBindingPort
- CaseRulesPort
- SafeSchemaPort
- CasePackageValidator

### 3.2 Required outbound collaborations

- PublicationTrustPort from M20
- AssetManifestPort from M04
- Localization bundle from M03

### 3.3 Domain events

- CasePackageValidated
- CasePackageRejected
- CaseBindingResolved

## 4. State model

The module recognizes these externally meaningful states or modes:

- PLANNED
- VALIDATED
- PUBLISHED
- RETIRED
- QUARANTINED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Case behavior MUST be data-driven through stable extension points.
2. Missing required package content MUST disable publication.
3. Profiles MUST be cumulative and must not expose authoring-purpose metadata.
4. All playable data MUST be fictional and synthetic.
5. A case MUST have a provider-independent tested clean solve.

## 6. Player-visible and operator-visible failure behavior

- Return explicit unavailable/quarantined states.
- Preserve historical exact package references for existing rounds.
- Reject stable-ID/title/order mismatch and cross-profile leakage.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Player-safe projection excludes canonical identities, culpability, solve gates, scoring annotations, and purpose labels.
- Source/licensing/content approvals are release gates.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Case + Career: catalogue availability.
2. Case + Round: immutable binding.
3. Case + Investigation/Workspace: safe schema and rules.
4. Case + Evaluation: protected evaluator bundle reference under separate runtime.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M10-FR-001` | Case behavior MUST be data-driven through stable extension points. |
| `M10-FR-002` | Missing required package content MUST disable publication. |
| `M10-FR-003` | Profiles MUST be cumulative and must not expose authoring-purpose metadata. |
| `M10-FR-004` | All playable data MUST be fictional and synthetic. |
| `M10-FR-005` | A case MUST have a provider-independent tested clean solve. |
| `M10-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M10. |
| `M10-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M10-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M10-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M10 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§7–8, 26, 28–30, 39, 43, 51, 56–57, 87, 100–101.
- Parent technical specification: Technical §§8, 14–15, 31–32, 51–52, 57, 68–69, 81, 90, 93, 106.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
