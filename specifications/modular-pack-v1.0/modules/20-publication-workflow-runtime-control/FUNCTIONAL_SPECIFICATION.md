# Fraud Graph Arena — Publication Trust, Durable Workflow, and Runtime Control

## Functional Specification

**Document version:** 1.0  
**Module ID:** `M20`  
**Module pair ID:** `FGA-MODULE-20-PUBLICATION_WORKFLOW_RUNTIME_CONTROL-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Runtime scope:** WEB safe queries, MAINTENANCE, EVALUATOR support, and MIGRATE  
**Date:** 26 July 2026

---

## 1. Authority and purpose

This document refines the Fraud Graph Arena v9.0 functional specification for **M20 — Publication Trust, Durable Workflow, and Runtime Control**. It is subordinate to the parent normative pair and cannot weaken hidden-truth isolation, deterministic ranked evidence, monotonic ranked state, exact ledger semantics, accessibility equivalence, immutable submission/evaluation, or signed publication rules.

**Purpose:** Own signed publication trust, active pointers, policy/configuration bundles, durable work execution, leases/fencing/fairness, deployment epochs, migrations, admission, runtime hardening evidence, exports/deletion workflows, and release qualification.

The module is independently implementable and testable behind its public contracts. Other modules may depend on those contracts, but MUST NOT depend on this module's internal classes, tables, files, caches, or implementation-specific error messages.

## 2. Functional boundary

### 2.1 Owned concepts

- case/asset/evaluator/policy publication metadata
- active pointers, signatures, verifier policy, revocation, quarantine, freshness, and anti-downgrade state
- durable workflow jobs, leases, attempts, deadlines, cancellation, and poison quarantine
- deployment epochs and compatibility matrix
- migration state/barriers
- runtime role health and admission projection
- export artifacts/manifests and deletion/retention tombstones
- release evidence and chaos qualification records

### 2.2 Capabilities

- verify and atomically activate signed packages
- roll back or quarantine without rewriting history
- load immutable policy/configuration bundles
- schedule and execute durable workflows with fairness and fencing
- provide shared transaction/unit-of-work infrastructure without owning business tables
- enforce role-specific admission and readiness
- coordinate N-1/N deployment and migration barriers
- generate secure expiring exports
- complete retention/deletion/cryptographic-erasure workflows
- record game-day, backup/restore, and release evidence

### 2.3 Explicit non-goals

- player game rules
- score calculation
- direct ownership of another module’s domain tables
- one public process holding evaluator or migration secrets

## 3. Actors and collaborators

The primary actors are the player, authorized operator where applicable, automated runtime roles, and consuming modules. Cross-module collaboration occurs only through the public ports and events below.

### 3.1 Inbound functional contracts

- PublicationTrustPort
- PolicyBundlePort
- WorkflowSubmissionPort
- WorkLeasePort
- RuntimeAdmissionPort
- DeploymentEpochPort
- UnitOfWorkPort
- ExportDeliveryPort
- RetentionDeletionPort

### 3.2 Required outbound collaborations

- storage/database/secret/signing/time/provider infrastructure adapters
- module-specific workflow handlers registered through public contracts

### 3.3 Domain events

- PublicationActivated
- PublicationQuarantined
- PolicyBundleActivated
- WorkflowDue
- WorkflowCompleted
- WorkflowEscalated
- DeploymentEpochStarted
- MigrationBarrierChanged
- AdmissionClosed
- ExportReady
- DeletionCompleted

## 4. State model

The module recognizes these externally meaningful states or modes:

- BUILT
- VALIDATED
- SIGNED
- STAGED
- PUBLISHED
- RETIRED
- QUARANTINED
- ROLLED_BACK
- WORK_DUE
- WORK_LEASED
- WORK_RETRY
- WORK_POISONED
- DEPLOYING
- DRAINING
- READY

State transitions MUST be deterministic, authorization-aware, revision-safe where mutable, and observable through stable status codes rather than inferred prose.

## 5. Functional rules and invariants

1. Unsigned, revoked, stale, quarantined, or downgraded packages cannot start new rounds.
2. Correctness MUST NOT depend on browser polling, player traffic, process memory, local disk, database session state, or one executor.
3. Leases use fencing; stale workers cannot commit.
4. Queue policy prevents starvation and supports bounded cancellation.
5. A deployment cannot mix incompatible schema, policy, evaluator, or ranking contracts for one accepted workflow.
6. Runtime roles use separate identities, secrets, networks, and hardening profiles.

## 6. Player-visible and operator-visible failure behavior

- Fail admission closed when executor/evaluator/publication/policy/migration readiness is unsafe.
- Retry only within signed work policy; quarantine poison jobs.
- Preserve immutable historical pointers and provide rollback.
- Expose safe status/correlation without internals.

Failures MUST use stable problem/status codes, a safe explanation, and a correlation identifier when useful. They MUST NOT expose protected truth, secrets, internal hosts, database details, generated SQL, provider reasoning, or another player's object existence.

## 7. Security, privacy, fairness, and accessibility

- Rootless/read-only/drop-capability runtime, secret separation, signed verifier policy, trusted time, secure export capabilities, cryptographic erasure, audit and least privilege.

The module MUST apply the project-wide owner-isolation, data-minimization, Unicode/bidirectional safety, no-store private response, accessibility, and audit rules that are applicable to its surface.

## 8. Cross-module functional scenarios

1. Platform + Case/Assets: signed activation, rollback, quarantine.
2. Platform + Command/Retrieval: outbox, leases, QoS, capacity admission.
3. Platform + Evaluation/Career: safe finalization across roles.
4. Platform + Identity: policy, export, deletion, erasure.
5. Platform + all roles: deployment epoch, migration, readiness, chaos.

## 9. Functional requirements

| Requirement ID | Requirement |
|---|---|
| `M20-FR-001` | Unsigned, revoked, stale, quarantined, or downgraded packages cannot start new rounds. |
| `M20-FR-002` | Correctness MUST NOT depend on browser polling, player traffic, process memory, local disk, database session state, or one executor. |
| `M20-FR-003` | Leases use fencing; stale workers cannot commit. |
| `M20-FR-004` | Queue policy prevents starvation and supports bounded cancellation. |
| `M20-FR-005` | A deployment cannot mix incompatible schema, policy, evaluator, or ranking contracts for one accepted workflow. |
| `M20-FR-006` | Runtime roles use separate identities, secrets, networks, and hardening profiles. |
| `M20-FR-007` | The module MUST expose its capabilities only through the public contracts defined for M20. |
| `M20-FR-008` | The module MUST be independently testable with all outbound collaborators replaced by deterministic test doubles. |
| `M20-FR-009` | Cross-module integration behavior MUST be verified by executable producer/consumer contracts and at least one real pairwise integration suite. |
| `M20-FR-010` | The module MUST publish safe operational status without leaking protected or private data. |

## 10. Functional acceptance criteria

A release of this module is acceptable only when:

1. All M20 functional requirements pass against the module component harness.
2. Public command/query/event schemas validate and compatibility tests pass.
3. Unauthorized, stale, duplicate, malformed, and unavailable-dependency paths fail safely.
4. Required accessibility, privacy, security, fairness, and deterministic behavior tests pass.
5. Every declared integration scenario passes in the pairwise or cluster integration pipeline.
6. The module can be built and tested without starting the complete application.

## 11. Traceability

- Parent functional specification: Functional §§24, 31, 34, 38, 44–45, 49, 51, 53, 61, 64, 71, 75, 82, 87, 90, 96, 98–99.
- Parent technical specification: Technical §§3–4, 7–8, 10, 22–27, 30–31, 35–37, 47–49, 51, 53, 60–62, 65, 70–72, 74, 76–77, 80, 82–84, 86–90, 92, 94–95, 98, 100–105, 107–108.
- Companion technical/test document: `TECHNICAL_AND_TEST_SPECIFICATION.md` in this module directory.
- Every requirement and acceptance criterion MUST map to at least one executable test, evidence owner, and contract/schema identifier in the generated conformance graph.
