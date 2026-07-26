# Fraud Graph Arena — Publication Trust, Durable Workflow, and Runtime Control

## Technical Architecture and Test Specification

**Document version:** 1.0  
**Module ID:** `M20`  
**Module pair ID:** `FGA-MODULE-20-PUBLICATION_WORKFLOW_RUNTIME_CONTROL-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Module type:** Platform bounded context  
**Runtime composition:** WEB safe queries, MAINTENANCE, EVALUATOR support, and MIGRATE  
**Date:** 26 July 2026

---

## 1. Architectural intent

Own signed publication trust, active pointers, policy/configuration bundles, durable work execution, leases/fencing/fairness, deployment epochs, migrations, admission, runtime hardening evidence, exports/deletion workflows, and release qualification.

M20 is a separately versioned module in a modular monolith. It MUST compile/build and run its automated tests independently. Runtime composition is performed only in application composition roots; independence does not imply a separately deployed network service.

## 2. Package layout

Proposed published/workspace packages:

- `fga_publication_workflow_runtime_control`
- `fga_publication_workflow_runtime_control_contracts`
- `fga_publication_workflow_runtime_control_testkit`

Each implementation module uses this internal shape where applicable:

```text
contracts/       # JSON Schema/OpenAPI/event schemas and compatibility fixtures
public/          # stable commands, queries, ports, DTOs, and error codes
domain/          # pure rules, aggregates, value objects, and state machines
application/     # use cases and transaction orchestration
adapters/        # database, browser, provider, filesystem, or framework adapters
testkit/         # builders, fakes, contract verifiers, deterministic clocks/randomness
tests/
  unit/
  property/
  contract/
  component/
  architecture/
```

Framework bootstrapping, route registration, database migrations, and provider clients remain in adapters or runtime composition packages, never in the domain layer.

## 3. Owned data and encapsulation

- case/asset/evaluator/policy publication metadata
- active pointers, signatures, verifier policy, revocation, quarantine, freshness, and anti-downgrade state
- durable workflow jobs, leases, attempts, deadlines, cancellation, and poison quarantine
- deployment epochs and compatibility matrix
- migration state/barriers
- runtime role health and admission projection
- export artifacts/manifests and deletion/retention tombstones
- release evidence and chaos qualification records

- Only this module's repositories may write its owned tables/state.
- Cross-module reads use a public query port, immutable event projection, or explicitly owned read model.
- Direct imports from another module's `domain`, `application`, `adapters`, or migrations are forbidden.
- Architecture tests MUST enforce the dependency rule.

## 4. Public interfaces

### 4.1 Inbound ports

- PublicationTrustPort
- PolicyBundlePort
- WorkflowSubmissionPort
- WorkLeasePort
- RuntimeAdmissionPort
- DeploymentEpochPort
- UnitOfWorkPort
- ExportDeliveryPort
- RetentionDeletionPort

### 4.2 Outbound ports

- storage/database/secret/signing/time/provider infrastructure adapters
- module-specific workflow handlers registered through public contracts

### 4.3 Published events

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

Contracts MUST use stable opaque identifiers, explicit versions, exact numeric/time semantics, typed enums, and player-safe error codes. Contract changes follow the parent N-1/N compatibility policy.

## 5. Dependency rule

Allowed direct module-contract dependencies:

- foundation only; all modules consume its public platform contracts or register workflow handlers

The implementation depends only on public contract packages. Cycles between implementation packages are forbidden. Cyclic business workflows are resolved through events, an application coordinator, or a transaction-participant port rather than reciprocal internal imports.

## 6. Persistence and transaction design

- The module owns its schema/table namespace or browser-storage namespace.
- Mutable aggregates use explicit revisions or equivalent compare-and-swap semantics.
- Append-only histories remain append-only.
- External network, provider, filesystem, or audio I/O MUST NOT occur inside a database transaction.
- Cross-module atomic invariants use the project `UnitOfWorkPort` and public transaction-participant interfaces; participants never access one another's tables.
- Durable external work uses an outbox/job record and fenced executor.

Module-specific states:

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

## 7. Failure, resilience, and observability

- Fail admission closed when executor/evaluator/publication/policy/migration readiness is unsafe.
- Retry only within signed work policy; quarantine poison jobs.
- Preserve immutable historical pointers and provide rollback.
- Expose safe status/correlation without internals.

Observability exposes safe low-cardinality module, operation, state, version, latency, and outcome metadata. It excludes private prose, credentials, protected truth, raw evidence, generated SQL, and raw provider content.

## 8. Security and trust-boundary controls

- Rootless/read-only/drop-capability runtime, secret separation, signed verifier policy, trusted time, secure export capabilities, cryptographic erasure, audit and least privilege.

## 9. Independent test harness

The module MUST provide a reusable test kit containing:

- deterministic clock, randomness, ID, and correlation-ID fakes;
- public DTO/builders and canonical golden fixtures;
- in-memory or isolated-database adapters for every outbound port;
- public contract verifier functions usable by consumers and providers;
- failure-injection controls for timeout, stale revision, duplicate request, unavailable dependency, and malformed response;
- fixture reset with no dependency on global test order;
- no need to boot unrelated modules for unit or component qualification.

## 10. Module test suites

- signature/verifier/freshness tests
- publication atomicity and rollback tests
- lease/fencing/duplicate-worker tests
- fairness/starvation/cancellation model tests
- poison-work tests
- migration N-1/N compatibility tests
- role-secret/network authorization tests
- runtime hardening/image inspection tests
- export integrity/expiry tests
- deletion/restore/erasure tests
- backup/PITR/failover tests
- chaos game-day scenarios
- architecture tests forbidding cross-module table access

### 10.1 Required test layers

| Requirement ID | Requirement |
|---|---|
| `M20-TST-001` | Pure domain unit tests execute without database, network, browser, or framework bootstrapping. |
| `M20-TST-002` | Property/model tests cover state transitions and critical invariants. |
| `M20-TST-003` | Public contract tests validate schemas, error codes, canonicalization, and compatibility. |
| `M20-TST-004` | Component tests run the real application layer with real owned persistence where applicable and fake outbound ports. |
| `M20-TST-005` | Architecture tests reject forbidden imports and cross-module table/repository access. |
| `M20-TST-006` | Security and privacy negative tests exercise authorization, leakage, injection, and data-minimization boundaries. |
| `M20-TST-007` | Pairwise integration tests run real producer and consumer modules for every declared edge. |
| `M20-TST-008` | At least one relevant cluster or end-to-end journey proves the module in the complete runtime composition. |

### 10.2 Mutation and negative assurance

For critical rules, mutation testing or an equivalent fault-injection suite MUST demonstrate that tests fail when authorization, idempotency, monotonicity, exact arithmetic, truth isolation, signature verification, or state-transition checks are removed.

## 11. Cross-module integration obligations

1. Platform + Case/Assets: signed activation, rollback, quarantine.
2. Platform + Command/Retrieval: outbox, leases, QoS, capacity admission.
3. Platform + Evaluation/Career: safe finalization across roles.
4. Platform + Identity: policy, export, deletion, erasure.
5. Platform + all roles: deployment epoch, migration, readiness, chaos.

Each integration edge has both a producer-side and consumer-side contract suite. Pairwise tests use real modules with all other dependencies replaced by test-kit fakes. Cluster tests use the real database and runtime composition required for the workflow.

## 12. Performance and capacity

- workflow deadline/SLO by class
- queue/backlog/capacity budgets
- deployment drain and rollback targets
- RPO/RTO and restore evidence

Performance tests use deterministic fixture sizes and publish p50/p95/p99 or bounded-operation evidence as applicable. A performance failure cannot justify weakening correctness, accessibility, security, privacy, or fairness.

## 13. Technical requirements

| Requirement ID | Requirement |
|---|---|
| `M20-TR-001` | The module MUST publish versioned public contracts separately from implementation packages. |
| `M20-TR-002` | The module MUST own and migrate only its declared persistence namespace. |
| `M20-TR-003` | The module MUST support deterministic clocks, identifiers, and randomness through injected ports. |
| `M20-TR-004` | The module MUST expose health/readiness only for dependencies needed by its own operation. |
| `M20-TR-005` | The module MUST not import another module implementation package. |
| `M20-TR-006` | The module MUST provide a test kit and contract verifier for its public interfaces. |
| `M20-TR-007` | The module MUST emit safe structured observability for every externally visible use case. |
| `M20-TR-008` | The module MUST define idempotency, concurrency, retry, and cancellation semantics for side effects. |
| `M20-TR-009` | The module MUST preserve parent normative-pair version bindings in relevant stored and emitted artifacts. |

## 14. Definition of done

1. Independent build, lint, static analysis, unit, property, contract, component, architecture, and security tests pass.
2. Owned migrations or browser-storage schemas are forward tested and isolated.
3. Consumer and provider contract suites pass for every public port/event.
4. Required pairwise and cluster integration scenarios pass with fault injection.
5. No forbidden dependency, cross-module data access, protected-data leakage, or stale contract reference is present.
6. Documentation, contracts, tests, and implementation share the module pair ID and appear in the conformance export.

## 15. Traceability

- Parent functional specification: Functional §§24, 31, 34, 38, 44–45, 49, 51, 53, 61, 64, 71, 75, 82, 87, 90, 96, 98–99.
- Parent technical specification: Technical §§3–4, 7–8, 10, 22–27, 30–31, 35–37, 47–49, 51, 53, 60–62, 65, 70–72, 74, 76–77, 80, 82–84, 86–90, 92, 94–95, 98, 100–105, 107–108.
- Companion functional document: `FUNCTIONAL_SPECIFICATION.md` in this module directory.
- Public schemas, tests, and architecture rules MUST be represented in the generated conformance graph for `FGA-MODULE-20-PUBLICATION_WORKFLOW_RUNTIME_CONTROL-1.0-20260726`.
