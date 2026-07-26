# Fraud Graph Arena — Identity, Account, Policy Receipt, and Privacy Requests

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M07`  
**Module pair ID:** `FGA-MODULE-07-IDENTITY_ACCOUNT_SECURITY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB and MAINTENANCE for long-running privacy workflows  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M07 — Identity, Account, Policy Receipt, and Privacy Requests**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own authentication identity, credentials, sessions, recovery, policy receipts, account status, privacy preferences, and authenticated requests for export/deletion.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- accounts and normalized login identifiers
- password and passkey credentials
- sessions and device projections
- recovery-code sets and verifiers
- account security state
- policy receipts and feature consent state
- privacy preferences and GPC observation
- export/deletion request ownership

### 2.2 Capabilities

- explicit registration and sign-in
- password validation and compromised-password screening
- session creation, rotation, expiry, and revocation
- one-time recovery-code lifecycle
- optional passkey registration and revocation
- restricted exceptional recovery
- policy/notice acknowledgement and consent withdrawal
- session/device review
- privacy preference management
- authenticated export and deletion request initiation

### 2.3 Explicit non-goals

- civil identity proofing
- email-based recovery
- game progression
- export artifact generation
- leaderboard alias publication rules

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- IdentityCommandPort
- SessionQueryPort
- PolicyReceiptPort
- PrivacyRequestPort
- PublicAliasIdentityPort

### 3.2 Required outbound collaborations

- PolicyBundlePort and workflow scheduling from M20
- secure secret/hash adapters
- public-alias collaboration with M18

### 3.3 Domain events

- AccountRegistered
- SessionStarted
- SessionRevoked
- RecoveryLimitedEntered
- PolicyReceiptRecorded
- ConsentWithdrawn
- ExportRequested
- DeletionRequested

## 4. State model

The module recognizes these externally meaningful states or modes:

- ACTIVE
- LOCKED
- RECOVERY_LIMITED
- DELETION_PENDING
- DELETED_PSEUDONYMIZED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Sign-in failure MUST NOT create an account.
2. Login identifiers MUST never be public aliases.
3. Recovery codes are one-time secrets and stored only as protected verifiers.
4. Exceptional recovery MUST restrict sensitive operations until step-up/cooldown succeeds.
5. Policy acceptance MUST bind the exact immutable version and locale shown.
6. Applicable privacy signals MUST narrow optional processing without reducing core play.

## 6. Player-visible and operator-visible failure behavior

- Use generic enumeration-resistant authentication errors.
- Revoke sessions after security-sensitive recovery.
- Keep export/deletion jobs resumable and player-visible through safe status codes.
- Fail closed when the active policy bundle cannot be established.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Secure HTTP-only same-site cookies, CSRF/origin/host controls, rate limits, Argon2id-first hashing, phishing-resistant operator authentication, owner-scoped queries, no secrets in logs.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Identity + Shell/Client Sync: register, login, expiry, logout.
2. Identity + Policy Platform: version change, re-consent, withdrawal.
3. Identity + Workflow: export/deletion completion and cryptographic erasure.
4. Identity + Leaderboard: alias separation and withdrawal.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M07-FR-001` | Sign-in failure MUST NOT create an account. |
| `M07-FR-002` | Login identifiers MUST never be public aliases. |
| `M07-FR-003` | Recovery codes are one-time secrets and stored only as protected verifiers. |
| `M07-FR-004` | Exceptional recovery MUST restrict sensitive operations until step-up/cooldown succeeds. |
| `M07-FR-005` | Policy acceptance MUST bind the exact immutable version and locale shown. |
| `M07-FR-006` | Applicable privacy signals MUST narrow optional processing without reducing core play. |
| `M07-FR-007` | The module MUST expose its capabilities only through the public contracts defined for M07. |
| `M07-FR-008` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M07-FR-009` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M07-FR-010` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M07 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§10, 25, 27, 31, 42, 53, 74, 85, 96.
- Parent technical specification: Technical §§12, 18–19, 35, 41, 53, 76, 87, 98, 100.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
