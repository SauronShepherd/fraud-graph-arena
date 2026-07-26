# Fraud Graph Arena — Retrieval, Deterministic Resolver, and Provider Gateway

## Technical Architecture and Test Specification

**Document version:** 1.0  
**Module ID:** `M19`  
**Module pair ID:** `FGA-MODULE-19-RETRIEVAL_PROVIDER_GATEWAY-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Module type:** Backend integration domain  
**Runtime composition:** MAINTENANCE primarily; WEB for free deterministic planning only  
**Date:** 26 July 2026

---

## 1. Architectural intent

Own bounded natural-language planning/clarification, deterministic ranked result resolution, provider adapters, conversation isolation, result firewall, parity evidence, capability/capacity, and real provider-cost accounting.

M19 is a separately versioned module in a modular monolith. It MUST compile/build and run its automated tests independently. Runtime composition is performed only in application composition roots; independence does not imply a separately deployed network service.

## 2. Package layout

Proposed published/workspace packages:

- `fga_retrieval_provider_gateway`
- `fga_retrieval_provider_gateway_contracts`
- `fga_retrieval_provider_gateway_testkit`

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

- canonical retrieval plans
- ambiguity/clarification classes
- ranked retrieval parity manifest references
- provider capability snapshots
- provider conversation records
- provider cost ledger and price catalogue
- safe normalized retrieval results
- provider adapter correlation state

- Only this module's repositories may write its owned tables/state.
- Cross-module reads use a public query port, immutable event projection, or explicitly owned read model.
- Direct imports from another module's `domain`, `application`, `adapters`, or migrations are forbidden.
- Architecture tests MUST enforce the dependency rule.

## 4. Public interfaces

### 4.1 Inbound ports

- IntentPlanningPort
- ClarificationPort
- RetrievalExecutionPort
- CapabilityQueryPort
- ConversationLifecyclePort
- ProviderCostPort

### 4.2 Outbound ports

- case safe schema/publication M10/M20
- command context M13
- deterministic player-safe data adapter
- external provider APIs behind private adapters

### 4.3 Published events

- IntentPlanned
- ClarificationRequired
- RetrievalAbstained
- DeterministicResultResolved
- ProviderConversationCreated
- ProviderResultRejected
- ProviderCostReconciled
- ConversationDeletionConfirmed

Contracts MUST use stable opaque identifiers, explicit versions, exact numeric/time semantics, typed enums, and player-safe error codes. Contract changes follow the parent N-1/N compatibility policy.

## 5. Dependency rule

Allowed direct module-contract dependencies:

- M10 Case safe interface
- M13 Command
- M20 Publication/Workflow/Capability

The implementation depends only on public contract packages. Cycles between implementation packages are forbidden. Cyclic business workflows are resolved through events, an application coordinator, or a transaction-participant port rather than reciprocal internal imports.

## 6. Persistence and transaction design

- The module owns its schema/table namespace or browser-storage namespace.
- Mutable aggregates use explicit revisions or equivalent compare-and-swap semantics.
- Append-only histories remain append-only.
- External network, provider, filesystem, or audio I/O MUST NOT occur inside a database transaction.
- Cross-module atomic invariants use the project `UnitOfWorkPort` and public transaction-participant interfaces; participants never access one another's tables.
- Durable external work uses an outbox/job record and fenced executor.

Module-specific states:

- PLANNING
- CLARIFICATION
- READY
- EXECUTING
- VALIDATING
- SUCCEEDED
- NO_RESULT
- REJECTED
- CAPACITY_CLOSED

## 7. Failure, resilience, and observability

- Abstain before debit when ambiguity or safety cannot be resolved.
- Fail closed and follow command refund/reconciliation policy for malformed/unsafe output.
- Close admission before capacity/budget/privacy limits are threatened.
- Persist deletion and unknown-outcome state.

Observability exposes safe low-cardinality module, operation, state, version, latency, and outcome metadata. It excludes private prose, credentials, protected truth, raw evidence, generated SQL, and raw provider content.

## 8. Security and trust-boundary controls

- No truth, private notes, account identity, credentials, generated SQL, reasoning, active content, or cross-case data in provider boundary/logs.
- LLMSVS/AISVS threat tests and prompt/data-injection controls.

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

- planner/clarification unit tests
- canonical plan golden tests
- ranked answer-set parity tests
- provider fake contract tests
- prompt/data-injection tests
- result-firewall schema/row/byte tests
- conversation isolation/deletion tests
- capacity/budget admission tests
- provider cost reconciliation tests
- no-rich-output/no-SQL tests
- outage/timeout/unknown-outcome tests
- cross-player equality E2E

### 10.1 Required test layers

| Requirement ID | Requirement |
|---|---|
| `M19-TST-001` | Pure domain unit tests execute without database, network, browser, or framework bootstrapping. |
| `M19-TST-002` | Property/model tests cover state transitions and critical invariants. |
| `M19-TST-003` | Public contract tests validate schemas, error codes, canonicalization, and compatibility. |
| `M19-TST-004` | Component tests run the real application layer with real owned persistence where applicable and fake outbound ports. |
| `M19-TST-005` | Architecture tests reject forbidden imports and cross-module table/repository access. |
| `M19-TST-006` | Security and privacy negative tests exercise authorization, leakage, injection, and data-minimization boundaries. |
| `M19-TST-007` | Pairwise integration tests run real producer and consumer modules for every declared edge. |
| `M19-TST-008` | At least one relevant cluster or end-to-end journey proves the module in the complete runtime composition. |

### 10.2 Mutation and negative assurance

For critical rules, mutation testing or an equivalent fault-injection suite MUST demonstrate that tests fail when authorization, idempotency, monotonicity, exact arithmetic, truth isolation, signature verification, or state-transition checks are removed.

## 11. Cross-module integration obligations

1. Retrieval + Command: accepted plan and durable execution.
2. Retrieval + Publication: parity manifests and deterministic resolver.
3. Retrieval + Workflow: timeouts, reconciliation, capacity, deletion.
4. Retrieval + Investigation: safe result IDs only through command settlement.

Each integration edge has both a producer-side and consumer-side contract suite. Pairwise tests use real modules with all other dependencies replaced by test-kit fakes. Cluster tests use the real database and runtime composition required for the workflow.

## 12. Performance and capacity

- bounded clarification turns
- row/byte/time/query budgets
- provider capacity headroom
- deterministic resolver latency target

Performance tests use deterministic fixture sizes and publish p50/p95/p99 or bounded-operation evidence as applicable. A performance failure cannot justify weakening correctness, accessibility, security, privacy, or fairness.

## 13. Technical requirements

| Requirement ID | Requirement |
|---|---|
| `M19-TR-001` | The module MUST publish versioned public contracts separately from implementation packages. |
| `M19-TR-002` | The module MUST own and migrate only its declared persistence namespace. |
| `M19-TR-003` | The module MUST support deterministic clocks, identifiers, and randomness through injected ports. |
| `M19-TR-004` | The module MUST expose health/readiness only for dependencies needed by its own operation. |
| `M19-TR-005` | The module MUST not import another module implementation package. |
| `M19-TR-006` | The module MUST provide a test kit and contract verifier for its public interfaces. |
| `M19-TR-007` | The module MUST emit safe structured observability for every externally visible use case. |
| `M19-TR-008` | The module MUST define idempotency, concurrency, retry, and cancellation semantics for side effects. |
| `M19-TR-009` | The module MUST preserve parent normative-pair version bindings in relevant stored and emitted artifacts. |

## 14. Definition of done

1. Independent build, lint, static analysis, unit, property, contract, component, architecture, and security tests pass.
2. Owned migrations or browser-storage schemas are forward tested and isolated.
3. Consumer and provider contract suites pass for every public port/event.
4. Required pairwise and cluster integration scenarios pass with fault injection.
5. No forbidden dependency, cross-module data access, protected-data leakage, or stale contract reference is present.
6. Documentation, contracts, tests, and implementation share the module pair ID and appear in the conformance export.

## 15. Traceability

- Parent functional specification: Functional §§14, 24, 38, 41, 43, 62, 65, 72, 77, 83–84, 89, 94–95, 98.
- Parent technical specification: Technical §§13, 23–24, 30, 33, 42, 56, 63, 67, 73, 78, 85–86, 91, 96–97, 103.
- Companion functional document: `FUNCTIONAL_SPECIFICATION.md` in this module directory.
- Public schemas, tests, and architecture rules MUST be represented in the generated conformance graph for `FGA-MODULE-19-RETRIEVAL_PROVIDER_GATEWAY-1.0-20260726`.
