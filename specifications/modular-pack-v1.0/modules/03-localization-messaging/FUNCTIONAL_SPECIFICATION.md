# Fraud Graph Arena — Localization and Messaging

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M03`  
**Module pair ID:** `FGA-MODULE-03-LOCALIZATION_MESSAGING-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB plus server-side safe message catalogues  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M03 — Localization and Messaging**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own locale negotiation, versioned message catalogues, safe error-code translation, formatting, Unicode/bidirectional behavior, and deterministic fallback.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- message keys and catalogue versions
- locale and fallback policy
- formatting profiles
- public error-code mappings
- pseudo-locales and missing-key reports
- case-content translation bundle metadata

### 2.2 Capabilities

- resolve stable message keys with parameters
- format dates, exact amounts, counts, and plural forms
- support Unicode normalization and bidirectional isolation
- provide deterministic locale fallback
- validate that functional text is not baked into raster assets
- compile case and policy messages into signed bundles
- provide pseudo-localization and expansion testing
- map server problem codes to player-safe copy

### 2.3 Explicit non-goals

- machine translation at player request time
- translation of protected truth in public runtimes
- ownership of business error classification
- locale-dependent scoring or sorting semantics

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- MessageResolver
- LocaleNegotiationPort
- ProblemMessageMapper
- CatalogueValidationPort

### 3.2 Required outbound collaborations

- signed policy/case catalogue loader from M20
- safe time/amount values from owning modules

### 3.3 Domain events

- LocaleSelected
- CatalogueLoaded
- MissingMessageDetected
- FallbackUsed

## 4. State model

The module recognizes these externally meaningful states or modes:

- LOCALE_RESOLVED
- FALLBACK_ACTIVE
- CATALOGUE_INCOMPATIBLE

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Missing required functional messages MUST fail qualification.
2. Locale MUST NOT alter authoritative score, rank, evidence order, or identifiers.
3. Bidi isolation MUST be applied to untrusted/user-visible identifiers.
4. Fallback MUST be deterministic and visible only when useful.
5. Exact amount formatting MUST preserve currency and scale supplied by the domain.

## 6. Player-visible and operator-visible failure behavior

- Use the signed default locale when a requested catalogue is unavailable.
- Render safe generic copy for an unknown problem code and retain correlation ID.
- Block a case/policy activation when mandatory translated content is incomplete.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Parameters are data, never executable markup.
- No raw HTML from translations without an approved sanitizer and schema.
- Logs store message keys, not sensitive rendered copy.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Localization + every UI module: key completeness contract.
2. Localization + Case: case bundle activation and fallback.
3. Localization + Identity: policy receipt records exact locale/version shown.
4. Localization + Workspace: deterministic Unicode sorting uses domain keys, not translated labels.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M03-FR-001` | Missing required functional messages MUST fail qualification. |
| `M03-FR-002` | Locale MUST NOT alter authoritative score, rank, evidence order, or identifiers. |
| `M03-FR-003` | Bidi isolation MUST be applied to untrusted/user-visible identifiers. |
| `M03-FR-004` | Fallback MUST be deterministic and visible only when useful. |
| `M03-FR-005` | Exact amount formatting MUST preserve currency and scale supplied by the domain. |
| `M03-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M03. |
| `M03-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M03-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M03-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M03 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§22–23, 27, 46, 52, 55, 96.
- Parent technical specification: Technical §§16, 40, 50, 55, 72, 98.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
