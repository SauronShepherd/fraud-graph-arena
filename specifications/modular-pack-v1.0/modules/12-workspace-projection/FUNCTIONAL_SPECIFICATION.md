# Fraud Graph Arena — Workspace Projection: List, Graph, Documents, and Semantic Navigation

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M12`  
**Module pair ID:** `FGA-MODULE-12-WORKSPACE_PROJECTION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB server projection plus browser bundle  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M12 — Workspace Projection: List, Graph, Documents, and Semantic Navigation**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Convert one authoritative revealed state into equivalent bounded list, graph, document, and semantic-navigation projections without granting new evidence.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- projection schemas
- column and sort definitions
- safe graph node/edge view models
- document view models
- filter/group/selection projection
- semantic graph navigation model
- view explanation summary

### 2.2 Capabilities

- render deterministic list pages and sorts
- render bounded graph projection
- synchronize selection across list and graph
- show relationship family and provenance
- provide semantic graph neighbor navigation
- render documents through safe viewers/transcripts
- explain active filters, hidden-by-filter counts, and selection
- preserve view state without affecting evidence

### 2.3 Explicit non-goals

- reveal authority
- manual hypothesis business rules
- case-file scoring
- graph layout as evidence

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- WorkspaceQueryPort
- ListProjectionPort
- GraphProjectionPort
- DocumentProjectionPort
- SemanticNavigatorPort

### 3.2 Required outbound collaborations

- VisibilityQueryPort from M11
- Case safe schema from M10
- AssetResolver from M04
- MessageResolver from M03

### 3.3 Domain events

- WorkspaceProjectionBuilt
- ViewFilterChanged
- SelectionChanged
- DocumentUnavailable

## 4. State model

The module recognizes these externally meaningful states or modes:

- LIST
- GRAPH
- DOCUMENT
- SEMANTIC_GRAPH

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. All core graph tasks MUST have an equivalent list/semantic path.
2. Sorting MUST use deterministic safe-ID tie-breaks and versioned null/Unicode rules.
3. Layout coordinates, node size, color, or degree MUST NOT encode guilt.
4. Filtering and grouping MUST operate only on revealed data.
5. Graph/list views MUST represent the same visible objects and selection.

## 6. Player-visible and operator-visible failure behavior

- Fall back from graph failure to list/semantic projection.
- Show explicit unavailable evidence states.
- Reject oversized projections with a safe bounded-refinement response.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No active document content, raw HTML, external loads, or protected metadata.
- Tooltips and diagnostics are safe projections only.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Workspace + Investigation: projection contract and parity.
2. Workspace + Presentation: keyboard, focus, screen-reader navigation.
3. Workspace + Assets: safe document renditions and fallbacks.
4. Workspace + Client Sync: filters/selection persistence without visibility changes.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M12-FR-001` | All core graph tasks MUST have an equivalent list/semantic path. |
| `M12-FR-002` | Sorting MUST use deterministic safe-ID tie-breaks and versioned null/Unicode rules. |
| `M12-FR-003` | Layout coordinates, node size, color, or degree MUST NOT encode guilt. |
| `M12-FR-004` | Filtering and grouping MUST operate only on revealed data. |
| `M12-FR-005` | Graph/list views MUST represent the same visible objects and selection. |
| `M12-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M12. |
| `M12-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M12-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M12-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M12 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§12–13, 22–23, 46, 55, 76.
- Parent technical specification: Technical §§14, 16, 21, 24–25, 34, 44, 55, 79.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
