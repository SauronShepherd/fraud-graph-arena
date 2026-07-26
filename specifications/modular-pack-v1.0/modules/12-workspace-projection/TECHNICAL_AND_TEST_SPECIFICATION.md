# Fraud Graph Arena — Workspace Projection: List, Graph, Documents, and Semantic Navigation

## Technical Architecture and Test Specification

**Document version:** 1.0  
**Module ID:** `M12`  
**Module pair ID:** `FGA-MODULE-12-WORKSPACE_PROJECTION-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Module type:** Read-model and frontend feature  
**Runtime composition:** WEB server projection plus browser bundle  
**Date:** 26 July 2026

---

## 1. Architectural intent

Convert one authoritative revealed state into equivalent bounded list, graph, document, and semantic-navigation projections without granting new evidence.

M12 is a separately versioned module in a modular monolith. It MUST compile/build and run its automated tests independently. Runtime composition is performed only in application composition roots; independence does not imply a separately deployed network service.

## 2. Package layout

Proposed published/workspace packages:

- `@fga/workspace-projection-contracts`
- `@fga/workspace-projection-ui`
- `fga_workspace_projection`
- `@fga/workspace-projection-testkit`

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

- projection schemas
- column and sort definitions
- safe graph node/edge view models
- document view models
- filter/group/selection projection
- semantic graph navigation model
- view explanation summary

- Only this module's repositories may write its owned tables/state.
- Cross-module reads use a public query port, immutable event projection, or explicitly owned read model.
- Direct imports from another module's `domain`, `application`, `adapters`, or migrations are forbidden.
- Architecture tests MUST enforce the dependency rule.

## 4. Public interfaces

### 4.1 Inbound ports

- WorkspaceQueryPort
- ListProjectionPort
- GraphProjectionPort
- DocumentProjectionPort
- SemanticNavigatorPort

### 4.2 Outbound ports

- VisibilityQueryPort from M11
- Case safe schema from M10
- AssetResolver from M04
- MessageResolver from M03

### 4.3 Published events

- WorkspaceProjectionBuilt
- ViewFilterChanged
- SelectionChanged
- DocumentUnavailable

Contracts MUST use stable opaque identifiers, explicit versions, exact numeric/time semantics, typed enums, and player-safe error codes. Contract changes follow the parent N-1/N compatibility policy.

## 5. Dependency rule

Allowed direct module-contract dependencies:

- M03 Localization
- M04 Assets
- M10 Case safe schema
- M11 Investigation

The implementation depends only on public contract packages. Cycles between implementation packages are forbidden. Cyclic business workflows are resolved through events, an application coordinator, or a transaction-participant port rather than reciprocal internal imports.

## 6. Persistence and transaction design

- The module owns its schema/table namespace or browser-storage namespace.
- Mutable aggregates use explicit revisions or equivalent compare-and-swap semantics.
- Append-only histories remain append-only.
- External network, provider, filesystem, or audio I/O MUST NOT occur inside a database transaction.
- Cross-module atomic invariants use the project `UnitOfWorkPort` and public transaction-participant interfaces; participants never access one another's tables.
- Durable external work uses an outbox/job record and fenced executor.

Module-specific states:

- LIST
- GRAPH
- DOCUMENT
- SEMANTIC_GRAPH

## 7. Failure, resilience, and observability

- Fall back from graph failure to list/semantic projection.
- Show explicit unavailable evidence states.
- Reject oversized projections with a safe bounded-refinement response.

Observability exposes safe low-cardinality module, operation, state, version, latency, and outcome metadata. It excludes private prose, credentials, protected truth, raw evidence, generated SQL, and raw provider content.

## 8. Security and trust-boundary controls

- No active document content, raw HTML, external loads, or protected metadata.
- Tooltips and diagnostics are safe projections only.

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

- projection unit/golden tests
- deterministic sorting and null tests
- Unicode/bidi tests
- list/graph set-equivalence property tests
- graph cap and dense-case performance tests
- document sandbox tests
- keyboard/semantic navigator tests
- 320px/zoom/accessibility flow tests
- missing asset fallback tests

### 10.1 Required test layers

| Requirement ID | Requirement |
|---|---|
| `M12-TST-001` | Pure domain unit tests execute without database, network, browser, or framework bootstrapping. |
| `M12-TST-002` | Property/model tests cover state transitions and critical invariants. |
| `M12-TST-003` | Public contract tests validate schemas, error codes, canonicalization, and compatibility. |
| `M12-TST-004` | Component tests run the real application layer with real owned persistence where applicable and fake outbound ports. |
| `M12-TST-005` | Architecture tests reject forbidden imports and cross-module table/repository access. |
| `M12-TST-006` | Security and privacy negative tests exercise authorization, leakage, injection, and data-minimization boundaries. |
| `M12-TST-007` | Pairwise integration tests run real producer and consumer modules for every declared edge. |
| `M12-TST-008` | At least one relevant cluster or end-to-end journey proves the module in the complete runtime composition. |

### 10.2 Mutation and negative assurance

For critical rules, mutation testing or an equivalent fault-injection suite MUST demonstrate that tests fail when authorization, idempotency, monotonicity, exact arithmetic, truth isolation, signature verification, or state-transition checks are removed.

## 11. Cross-module integration obligations

1. Workspace + Investigation: projection contract and parity.
2. Workspace + Presentation: keyboard, focus, screen-reader navigation.
3. Workspace + Assets: safe document renditions and fallbacks.
4. Workspace + Client Sync: filters/selection persistence without visibility changes.

Each integration edge has both a producer-side and consumer-side contract suite. Pairwise tests use real modules with all other dependencies replaced by test-kit fakes. Cluster tests use the real database and runtime composition required for the workflow.

## 12. Performance and capacity

- bounded rows/nodes/edges
- stable pagination and sort
- frontend graph render/memory budgets

Performance tests use deterministic fixture sizes and publish p50/p95/p99 or bounded-operation evidence as applicable. A performance failure cannot justify weakening correctness, accessibility, security, privacy, or fairness.

## 13. Technical requirements

| Requirement ID | Requirement |
|---|---|
| `M12-TR-001` | The module MUST publish versioned public contracts separately from implementation packages. |
| `M12-TR-002` | The module MUST own and migrate only its declared persistence namespace. |
| `M12-TR-003` | The module MUST support deterministic clocks, identifiers, and randomness through injected ports. |
| `M12-TR-004` | The module MUST expose health/readiness only for dependencies needed by its own operation. |
| `M12-TR-005` | The module MUST not import another module implementation package. |
| `M12-TR-006` | The module MUST provide a test kit and contract verifier for its public interfaces. |
| `M12-TR-007` | The module MUST emit safe structured observability for every externally visible use case. |
| `M12-TR-008` | The module MUST define idempotency, concurrency, retry, and cancellation semantics for side effects. |
| `M12-TR-009` | The module MUST preserve parent normative-pair version bindings in relevant stored and emitted artifacts. |

## 14. Definition of done

1. Independent build, lint, static analysis, unit, property, contract, component, architecture, and security tests pass.
2. Owned migrations or browser-storage schemas are forward tested and isolated.
3. Consumer and provider contract suites pass for every public port/event.
4. Required pairwise and cluster integration scenarios pass with fault injection.
5. No forbidden dependency, cross-module data access, protected-data leakage, or stale contract reference is present.
6. Documentation, contracts, tests, and implementation share the module pair ID and appear in the conformance export.

## 15. Traceability

- Parent functional specification: Functional §§12–13, 22–23, 46, 55, 76.
- Parent technical specification: Technical §§14, 16, 21, 24–25, 34, 44, 55, 79.
- Companion functional document: `FUNCTIONAL_SPECIFICATION.md` in this module directory.
- Public schemas, tests, and architecture rules MUST be represented in the generated conformance graph for `FGA-MODULE-12-WORKSPACE_PROJECTION-1.0-20260726`.
