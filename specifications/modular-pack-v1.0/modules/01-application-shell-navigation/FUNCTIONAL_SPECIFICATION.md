# Fraud Graph Arena — Application Shell and Navigation

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M01`  
**Module pair ID:** `FGA-MODULE-01-APPLICATION_SHELL_NAVIGATION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB browser bundle  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M01 — Application Shell and Navigation**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own the application bootstrap, route lifecycle, global navigation policy, shell-level error recovery, and composition of independently implemented UI modules.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- route intent and browser-history projection
- shell bootstrap state
- global overlay and announcement state
- safe public build/capability projection
- composition-root registrations

### 2.2 Capabilities

- bootstrap the signed client and verify compatibility
- define public and authenticated route trees
- apply authentication and round-state route guards
- preserve intended destinations across sign-in and recovery
- coordinate loading, degraded, stale-client, and fatal-error screens
- mount persistent cross-route facilities such as the radio
- restore focus after navigation and modal transitions
- reject routes that would disclose object existence or protected identifiers

### 2.3 Explicit non-goals

- authentication credential validation
- game-rule decisions
- credit, evidence, submission, or progression authority
- asset-byte ownership
- localization catalogue ownership

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- ShellBootstrapPort — returns session, build, policy, and capability projections
- NavigationPolicyPort — decides allowed destination from safe state
- RouteContribution — allows another frontend module to register routes without shell internals
- GlobalNoticePort — accepts safe status and incident notices

### 3.2 Required outbound collaborations

- IdentityClient for session queries and logout
- ClientCompatibilityClient for build/policy compatibility
- MessageResolver for localized shell copy
- AssetResolver for public shell assets
- RadioController and ClientStateCoordinator through public interfaces

### 3.3 Domain events

- ShellBootstrapped
- RouteChanged
- NavigationDenied
- SessionExpired
- StaleClientDetected
- GlobalRecoveryRequested

## 4. State model

The module recognizes these externally meaningful states or modes:

- BOOTING
- PUBLIC_READY
- AUTHENTICATED_READY
- DEGRADED
- STALE_CLIENT
- FATAL_SAFE_STOP

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. A route guard MUST use server-authoritative safe projections, never client-owned entitlement flags.
2. Navigation MUST NOT reveal whether another player object exists.
3. A stale or incompatible client MUST be blocked from ranked mutations.
4. Route transitions MUST preserve accessible focus and announcement semantics.
5. Persistent shell facilities MUST NOT become game-state authorities.

## 6. Player-visible and operator-visible failure behavior

- Show a recoverable global error with correlation ID for transient failure.
- Show an explicit sign-in path after session expiry without discarding acknowledged server state.
- Show a mandatory reload/update state for incompatible client versions.
- Fail closed to a safe public route when route authorization cannot be established.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No protected truth, credentials, tokens, private notes, or raw provider output in route state or URLs.
- History entries and analytics use opaque safe identifiers only.
- Open redirects and arbitrary route injection are prohibited.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Shell + Identity: sign-in redirect and expired-session recovery.
2. Shell + Career/Round: deep-link guards for open, review, and unavailable rounds.
3. Shell + Client Sync: stale revision and incompatible-client recovery.
4. Shell + Radio: route transitions do not restart audio.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M01-FR-001` | A route guard MUST use server-authoritative safe projections, never client-owned entitlement flags. |
| `M01-FR-002` | Navigation MUST NOT reveal whether another player object exists. |
| `M01-FR-003` | A stale or incompatible client MUST be blocked from ranked mutations. |
| `M01-FR-004` | Route transitions MUST preserve accessible focus and announcement semantics. |
| `M01-FR-005` | Persistent shell facilities MUST NOT become game-state authorities. |
| `M01-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M01. |
| `M01-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M01-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M01-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M01 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§9, 22–24, 45–46, 98.
- Parent technical specification: Technical §§6, 16, 21–25, 44, 75, 88, 102.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
