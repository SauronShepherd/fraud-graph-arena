# Fraud Graph Arena — Presentation System and Accessibility

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M02`  
**Module pair ID:** `FGA-MODULE-02-PRESENTATION_ACCESSIBILITY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB browser bundle  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M02 — Presentation System and Accessibility**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Provide reusable semantic UI primitives and enforce accessibility, interaction, responsive, and visual-consistency contracts independently of game-domain rules.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- design tokens and semantic component contracts
- focus-management policy
- live-region and status-announcement primitives
- accessible modal and disclosure stack
- responsive layout primitives
- accessibility preference projection

### 2.2 Capabilities

- render forms, dialogs, tables, tabs, notices, tooltips, and status controls
- provide visible focus and deterministic keyboard behavior
- support high contrast, forced colors, reduced motion, touch, zoom, and reflow
- provide semantic graph-navigation primitives without owning graph data
- standardize validation and error-summary behavior
- emit dynamic accessibility trace hooks
- support live functional text rather than baked text
- prevent color-only or audio-only meaning

### 2.3 Explicit non-goals

- business validation
- route ownership
- translation catalogue ownership
- record visibility or graph semantics
- asset approval

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- ComponentProps contracts
- AccessibilityPreferencesPort
- AnnouncerPort
- FocusRestorationPort
- SemanticGraphWidgetPort

### 3.2 Required outbound collaborations

- MessageResolver
- AssetResolver for decorative icons only
- safe telemetry event sink for component failures

### 3.3 Domain events

- AccessibilityPreferenceChanged
- FocusRestored
- LiveAnnouncementIssued
- ComponentErrorCaptured

## 4. State model

The module recognizes these externally meaningful states or modes:

- NORMAL
- HIGH_CONTRAST
- FORCED_COLORS
- REDUCED_MOTION
- REFLOW_NARROW

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Every core control MUST be keyboard operable.
2. Every visual state MUST have text and/or shape semantics.
3. Modal focus MUST be trapped, restored, and announced.
4. Components MUST remain usable at 320 CSS pixels and 200% zoom.
5. Automated accessibility results MUST NOT replace human conformance review.

## 6. Player-visible and operator-visible failure behavior

- Fallback to native HTML behavior when an enhancement fails.
- Suppress nonessential motion when requested.
- Render textual alternatives when a visual widget cannot initialize.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No unsafe HTML sinks or string-to-script behavior.
- Trusted Types/CSP compatibility must be testable.
- Component diagnostics must exclude private player content.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Presentation + Workspace: list and semantic graph offer equivalent core tasks.
2. Presentation + Shell: route and modal focus lifecycle.
3. Presentation + Case File: accessible validation summary and evidence mapping.
4. Presentation + Localization: pseudo-localization and bidirectional text.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M02-FR-001` | Every core control MUST be keyboard operable. |
| `M02-FR-002` | Every visual state MUST have text and/or shape semantics. |
| `M02-FR-003` | Modal focus MUST be trapped, restored, and announced. |
| `M02-FR-004` | Components MUST remain usable at 320 CSS pixels and 200% zoom. |
| `M02-FR-005` | Automated accessibility results MUST NOT replace human conformance review. |
| `M02-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M02. |
| `M02-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M02-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M02-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M02 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§13, 22–23, 46, 54–55, 76.
- Parent technical specification: Technical §§16, 21, 24–25, 55, 75, 79.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
