# Fraud Graph Arena — Audio and Radio

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M05`  
**Module pair ID:** `FGA-MODULE-05-AUDIO_RADIO-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB browser bundle  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M05 — Audio and Radio**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Provide optional persistent noir-radio playback with deterministic policy, browser-safe activation, multi-tab coordination, and complete gameplay independence.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- radio preference
- playlist traversal state
- playback-leader state
- current approved track reference
- safe audio availability state

### 2.2 Capabilities

- start only after a valid user gesture
- play an approved randomized nonrepeating playlist
- persist playback across SPA routes
- coordinate tabs so one tab leads playback
- handle track load/decode failures and skip safely
- provide on/off-only player control
- work with audio disabled or unavailable
- exclude playback from score, hints, timing, and evidence

### 2.3 Explicit non-goals

- music asset approval
- game timing
- route navigation
- credit or scoring effects
- persistent server-side player profiling

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- RadioController
- RadioPreferencePort
- PlaybackLeadershipPort

### 3.2 Required outbound collaborations

- AssetResolver for approved audio files
- ClientStateCoordinator for safe local preference persistence

### 3.3 Domain events

- RadioEnabled
- RadioDisabled
- PlaybackLeaderChanged
- TrackSkipped
- RadioUnavailable

## 4. State model

The module recognizes these externally meaningful states or modes:

- OFF
- ARMED_FOR_GESTURE
- PLAYING_LEADER
- FOLLOWER_SILENT
- UNAVAILABLE

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Audio MUST be optional.
2. Route changes MUST NOT restart the current track.
3. Multiple tabs MUST NOT produce uncontrolled simultaneous playback.
4. Track identity and timing MUST NOT affect gameplay.
5. All-track failure MUST degrade to a clear off/unavailable state.

## 6. Player-visible and operator-visible failure behavior

- Skip an unreadable track.
- Turn off cleanly when every track fails.
- Recover leadership after a tab closes without changing game state.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Audio URLs come only from the signed asset manifest.
- No microphone or other permission-gated API is used.
- No private state is encoded in playback metadata.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Radio + Shell: persistence across navigation.
2. Radio + Assets: digest-approved MP3 loading.
3. Radio + multi-tab browser harness: leader election and recovery.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M05-FR-001` | Audio MUST be optional. |
| `M05-FR-002` | Route changes MUST NOT restart the current track. |
| `M05-FR-003` | Multiple tabs MUST NOT produce uncontrolled simultaneous playback. |
| `M05-FR-004` | Track identity and timing MUST NOT affect gameplay. |
| `M05-FR-005` | All-track failure MUST degrade to a clear off/unavailable state. |
| `M05-FR-006` | The module MUST expose its capabilities only through the public contracts defined for M05. |
| `M05-FR-007` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M05-FR-008` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M05-FR-009` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M05 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §22 and §23.
- Parent technical specification: Technical §17, §21, §24.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
