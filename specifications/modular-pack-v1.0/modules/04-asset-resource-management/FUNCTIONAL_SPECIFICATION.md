# Fraud Graph Arena — Asset and Resource Management

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M04`  
**Module pair ID:** `FGA-MODULE-04-ASSET_RESOURCE_MANAGEMENT-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB and MIGRATE/publication tooling  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M04 — Asset and Resource Management**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own signed asset manifests, content-addressed resolution, variants, transcripts/alternatives, loading policy, integrity verification, caching eligibility, and safe fallback.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- asset identifiers and manifest schema
- asset variant metadata
- digests, media types, dimensions, purposes, and approval state
- alt text/transcript linkage
- public immutable cache manifest
- asset creation/provenance records

### 2.2 Capabilities

- resolve assets by stable identifier
- verify digest and manifest compatibility
- select responsive variants without changing semantics
- distinguish decorative from essential evidence assets
- preload bounded route-critical assets
- provide safe fallback and unavailable states
- enforce public-only immutable caching
- validate transcript/visual equivalence and spoiler boundaries
- surface supplementary provenance without treating it as authority

### 2.3 Explicit non-goals

- business visibility of evidence
- localization of live functional text
- audio playback lifecycle
- dynamic fetching from arbitrary player URLs

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- AssetResolver
- AssetPreloadPort
- AssetIntegrityVerifier
- AssetFallbackPort
- AssetManifestCompiler

### 3.2 Required outbound collaborations

- PublicationTrustPort from M20
- MessageResolver for live labels
- browser cache adapter

### 3.3 Domain events

- AssetResolved
- AssetIntegrityFailed
- EssentialAssetUnavailable
- FallbackRendered

## 4. State model

The module recognizes these externally meaningful states or modes:

- AVAILABLE
- LOADING
- FALLBACK
- UNAVAILABLE
- QUARANTINED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Functional text MUST remain live and accessible.
2. Essential evidence assets MUST fail closed when integrity or availability is uncertain.
3. Decorative asset failure MUST NOT block play.
4. Only content-addressed approved public assets may be cached by a service worker.
5. A content credential is supplementary and cannot authorize an asset alone.

## 6. Player-visible and operator-visible failure behavior

- Render project-owned fallback for decorative failure.
- Pause or incident-handle a ranked round when required evidence bytes are unavailable.
- Reject digest, media-type, or manifest mismatch.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- No active scripts, macros, remote loads, embedded credentials, or executable content.
- Asset paths cannot traverse the package root.
- Private evidence and exports are never placed in the public asset cache.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Assets + Shell: bootstrap and route assets.
2. Assets + Workspace: evidence document rendition and transcript.
3. Assets + Radio: approved audio manifest.
4. Assets + Publication: atomic activation, rollback, and quarantine.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M04-FR-001` | Functional text MUST remain live and accessible. |
| `M04-FR-002` | Essential evidence assets MUST fail closed when integrity or availability is uncertain. |
| `M04-FR-003` | Decorative asset failure MUST NOT block play. |
| `M04-FR-004` | Only content-addressed approved public assets may be cached by a service worker. |
| `M04-FR-005` | A content credential is supplementary and cannot authorize an asset alone. |
| `M04-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M04. |
| `M04-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M04-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M04-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M04 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§22, 24–26, 39, 46, 51, 55, 73, 87, 97.
- Parent technical specification: Technical §§14–17, 34, 52, 55, 74–75, 90, 100.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
