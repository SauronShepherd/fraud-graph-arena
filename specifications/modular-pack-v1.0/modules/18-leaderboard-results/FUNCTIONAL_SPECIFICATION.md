# Fraud Graph Arena — Leaderboard, Public Results, Moderation, and Disputes

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M18`  
**Module pair ID:** `FGA-MODULE-18-LEADERBOARD_RESULTS-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB plus MAINTENANCE reindex/moderation  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M18 — Leaderboard, Public Results, Moderation, and Disputes**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own ranking eligibility projections, segment-compatible ranking, shared ties, optional public alias publication, withdrawal, moderation, disputes, and amendment-aware reindexing.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- ranking segments and keys
- leaderboard entries
- publication/withdrawal state
- public alias projection
- moderation and dispute events
- rank index and season/version scope

### 2.2 Capabilities

- evaluate result eligibility from safe verdict metadata
- rank within immutable compatible segment
- apply deterministic tie rules and shared ranks
- publish only after explicit opt-in
- withdraw without deleting private result
- moderate aliases and entries
- support disputes and audited reason codes
- reindex after valid amendments/invalidation

### 2.3 Explicit non-goals

- authentication identifier ownership
- score calculation
- career progression
- anti-cheat conclusion from accessibility behavior

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- LeaderboardQueryPort
- LeaderboardPublicationPort
- ModerationPort
- DisputePort
- RankingProjectionPort

### 3.2 Required outbound collaborations

- SafeVerdict event M17
- PublicAlias identity M07
- segment/policy data M09/M20

### 3.3 Domain events

- LeaderboardEntryEligible
- LeaderboardEntryPublished
- LeaderboardEntryWithdrawn
- EntryModerated
- DisputeOpened
- RankingReindexed

## 4. State model

The module recognizes these externally meaningful states or modes:

- PRIVATE_ELIGIBLE
- PUBLIC
- WITHDRAWN
- UNDER_REVIEW
- DISQUALIFIED
- INVALIDATED

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Only compatible ranking segments may share a pool.
2. Wall-clock time, provider latency, accessibility settings, and input method MUST NOT affect rank.
3. Identical ranking keys share rank.
4. Publication is opt-in and private login identifiers never appear.
5. Detection signals are not automatic proof of cheating.

## 6. Player-visible and operator-visible failure behavior

- Remove public projection promptly on withdrawal/deletion.
- Mark/reindex safely after amendment or invalidation.
- Provide player-safe dispute status without exposing security internals.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Minimal public fields, moderated aliases, owner-scoped private results, no prompts/private prose/protected truth.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Leaderboard + Evaluation: eligibility and amendment.
2. Leaderboard + Identity: alias, deletion, and withdrawal.
3. Leaderboard + Client/UI: pagination and exact ties.
4. Leaderboard + Platform: season/version activation and reindex.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M18-FR-001` | Only compatible ranking segments may share a pool. |
| `M18-FR-002` | Wall-clock time, provider latency, accessibility settings, and input method MUST NOT affect rank. |
| `M18-FR-003` | Identical ranking keys share rank. |
| `M18-FR-004` | Publication is opt-in and private login identifiers never appear. |
| `M18-FR-005` | Detection signals are not automatic proof of cheating. |
| `M18-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M18. |
| `M18-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M18-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M18-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M18 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§20, 32–33, 54.
- Parent technical specification: Technical §§6, 9–12, 20, 23, 54.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
