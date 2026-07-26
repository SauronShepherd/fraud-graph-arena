# Fraud Graph Arena

## Complete End-to-End Build and Qualification Plan

**Document version:** 1.0  
**Plan ID:** `FGA-END-TO-END-BUILD-PLAN-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Parent modular pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Architecture pair:** `FGA-MODULAR-ARCHITECTURE-1.0-20260726`  
**Date:** 26 July 2026  
**Status:** Complete implementation, integration, qualification, deployment, and handover plan  

---

## 1. Purpose

This plan turns the normative product and modular architecture specifications into a step-by-step implementation sequence. It builds Fraud Graph Arena as a **multi-module modular monolith** composed into four isolated runtime roles: `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE`.

The plan is deliberately test-gated. **An iteration is not complete merely because its code exists. It is complete only after every required task and stage is complete, the complete cumulative solution implemented to that point passes all applicable gates, and a reproducible evidence bundle is generated from a clean checkout.**

## 2. Delivery hierarchy

### 2.1 Task

A **task** is one small, reviewable modification to exactly one file. A task may create a new file or modify an existing file, but it MUST NOT change two files. A cross-file change is split into multiple tasks inside one stage.

Every task has:

- a stable task ID;
- one exact repository path;
- one bounded change;
- one file-local acceptance statement;
- a requirement, module, interaction, or quality attribute to which it traces.

### 2.2 Stage

A **stage** is a functionally cohesive set of file-atomic tasks. A stage normally changes contracts, implementation, adapters, UI, tests, and documentation in different files to deliver one coherent capability.

A stage closes only when:

1. every task is complete and reviewed;
2. file-local and stage-specific tests pass;
3. affected public contracts are compatible or explicitly migrated;
4. no stage-created defect remains deferred to a later iteration.

### 2.3 Iteration

An **iteration** is a set of stages that adds a new feature, improves an existing feature, or increases its production qualification. An iteration must leave the repository in a coherent, runnable, demonstrable, and fully passing state.

### 2.4 No Pass, No Progress

1. A failed test creates a corrective task in the **same iteration**.
2. The iteration remains open until the defect is fixed and the complete iteration gate passes again.
3. A rerun that happens to pass does not erase the first failure; the cause must be identified and fixed.
4. Critical tests for constitutional invariants cannot be skipped, muted, quarantined, marked expected-failure, or replaced with manual confidence.
5. A temporary exception is allowed only for a noncritical check, must be signed, time-limited, linked to a risk owner, and cannot be carried into release qualification.
6. Advancing to the next iteration with red tests, missing evidence, stale contracts, unreviewed migrations, or unresolved severity-1/2 defects is prohibited.

## 3. Target repository structure

```text
fraud-graph-arena/
  apps/
    web/                         # public FastAPI composition
    web-ui/                      # React/Vite browser composition
    maintenance/                 # private durable workflow executor
    evaluator/                   # private truth broker and evaluator
    migrate/                     # release-only migrations/publication
  foundation/
    contracts/                   # language-neutral schemas
    python/                      # common Python values, persistence, testkits
    typescript/                  # common browser values/contracts
    typescript-testkit/
    test-fixtures/
  modules/
    m01-application-shell-navigation/
    m02-presentation-accessibility/
    ...
    m20-publication-workflow-runtime-control/
  cases/
    academy/
    kennel-lab/
    production/
  assets/
    manifests/
  config/
    architecture/
    database/
    governance/
    performance/
    privacy/
    runtime/
    security/
    supply-chain/
    testing/
  infra/
    local/
    deployment/
  schemas/
  tests/
    architecture/
    contracts/
    integration/pairs/
    integration/clusters/
    e2e/
    accessibility/
    security/
    privacy/
    performance/
    resilience/
    chaos/
    deployment/
  tools/
  scripts/
  docs/
  reports/
```

## 4. Module independence contract

Every module MUST provide, as applicable:

```text
contracts/       public schemas, DTOs, events, error codes, compatibility fixtures
frontend/        browser implementation when applicable
backend/         domain, application, adapters, and owned migrations
testkit/         deterministic builders, fakes, failure injection, contract verifiers
tests/
  unit/
  property/
  contract/
  component/
  architecture/
  security/
```

Module qualification must not require the complete application, a live external provider, another module implementation, global test order, or shared mutable fixture state. A component test starts the module's real domain/application layer, its real owned persistence adapter where relevant, and deterministic fake outbound ports.

## 5. Cross-module integration rules

Cross-module collaboration is permitted only through:

- synchronous public command/query ports;
- versioned immutable events;
- durable workflow jobs with leases and fencing;
- signed immutable publications;
- explicit transaction-participant ports under the shared unit of work.

Direct access to another module's tables, repositories, internal classes, migrations, browser stores, files, or framework callbacks is forbidden.

### 5.1 Interaction catalogue

| ID | Producer/orchestrator | Consumer/participant | Style | Purpose |
|---|---|---|---|---|
| I01 | M01 | M07 | Synchronous query/command | Session bootstrap, sign-in routing, expiry and logout |
| I02 | M01 | M08/M09 | Synchronous query | Catalogue/round route guard and deep-link recovery |
| I03 | M01 | M02/M03/M04/M05/M06 | In-process UI ports | Shell composition without domain ownership |
| I04 | M07 | M20 | Command + durable workflow | Policy receipt, export, deletion, erasure and account recovery support |
| I05 | M08 | M10/M20 | Query | Published-case availability and catalogue state |
| I06 | M09 | M08/M10/M20 | Transactional query/command | Round eligibility and immutable binding creation |
| I07 | M11 | M09/M10 | Synchronous domain ports | Visibility and selection rules under round/case policy |
| I08 | M12 | M11 | Read-model contract | List/graph/document/semantic projections from one revealed state |
| I09 | M13 | M09/M11/M14 | Cross-module Unit of Work | Quote acceptance, debit, command, outbox intent and later settlement/reveal |
| I10 | M13 | M19/M20 | Durable job | Provider/deterministic retrieval dispatch, reconciliation and cancellation |
| I11 | M15 | M09/M11/M16 | Synchronous domain ports | Save reversible draft state without monotonic-state rollback |
| I12 | M16 | M09/M11/M13/M14 | Cross-module Unit of Work | Immutable submission with pending-work and evidence checks |
| I13 | M17 | M16/M10/M20 | Private protocol | Truth-bound deterministic evaluation and signed safe verdict |
| I14 | M20 | M17/M08/M09 | Cross-role finalization Unit of Work | Commit safe verdict, close round and advance progression exactly once |
| I15 | M18 | M17/M07/M09 | Event + query | Eligibility, segment ranking, public alias, withdrawal and amendment reindex |
| I16 | M19 | M10/M20 | Artifact/query | Safe schema, capability, parity manifest and immutable deterministic data |
| I17 | M04 | M20 | Signed artifact | Asset activation, digest, quarantine and rollback |
| I18 | All | M03/M20 | Signed catalogue/policy | Localized policy, case and status text with version receipt |
| I19 | All backend modules | M20 | Platform port | Transactions, clock, IDs, leases, workflows, readiness and deployment epoch |
| I20 | All modules | Contract/Testkit packages | Build-time contract | No implementation imports; producer/consumer test verification |

### 5.2 Atomic workflows

The following workflows require one database transaction across public participant ports while each participant writes only its owned tables:

1. M13 command/idempotency/outbox plus M14 debit.
2. M13 terminal settlement plus M14 charge/refund plus M11 visibility grant.
3. M16 immutable submission plus M09 lifecycle transition after M13/M14 checks.
4. M17 safe verdict projection plus M09 closure plus M08 progression, orchestrated after the private truth-reading step.
5. M20 publication activation plus trust, freshness, compatibility, revocation, and anti-downgrade checks.

External network, filesystem, provider, or audio I/O is forbidden inside these transactions.

## 6. Universal iteration test gate

Every iteration executes **all gates applicable to the complete implemented solution to date**, not only tests for files changed in that iteration. A gate may be recorded as not applicable only before its capability exists; once introduced, it remains cumulative and mandatory.

| Gate | Area | Required evidence |
|---|---|---|
| `G01` | Governance and traceability | Markdown/schema/config validation; current IDs; requirement/test/evidence links; no stale normative reference. |
| `G02` | Static quality and build | Format, lint, typecheck, package build, dependency graph, dead-code/config validation. |
| `G03` | Independent module qualification | For every implemented/changed module: unit, property/model, contract, component, architecture, security, and performance smoke using its own testkit. |
| `G04` | Contract compatibility | Producer and consumer verifiers, canonicalization, N-1/N, stored event replay, incompatible-change negatives. |
| `G05` | Persistence and migration | Owned-schema checks, apply from zero, upgrade from previous, expand/contract, grants, constraints, rollback/forward-fix, connection/transaction leak checks. |
| `G06` | Pairwise integration | Real producer and consumer for every affected interaction edge, with unrelated modules faked and failure injection. |
| `G07` | Capability-cluster integration | All previously introduced mandatory clusters plus the cluster changed by the iteration, with real PostgreSQL and deterministic fakes. |
| `G08` | Runtime-role integration | All implemented WEB/MAINTENANCE/EVALUATOR/MIGRATE compositions, identities, grants, readiness, epoch, and private-boundary checks. |
| `G09` | End-to-end product journeys | Real browser against the exact production-like image for every implemented principal journey and cumulative Academy/production case path. |
| `G10` | Accessibility and localization | Keyboard, focus, accessibility tree, live regions, reflow, zoom, contrast, reduced motion, touch, noaudio/noncanvas alternatives, locale/Unicode/bidi. |
| `G11` | Security, privacy, and leakage | IDOR, CSRF, XSS/injection, cache/service-worker, prompt/data injection, truth/secret/private-data scans, redaction, retention/export/deletion where implemented. |
| `G12` | Concurrency and resilience | Duplicate clicks, two tabs, stale revisions, timeouts, crash points, restart, DB wake/failover, executor/provider/evaluator/key outage, exact replay. |
| `G13` | Performance and capacity | Declared API/DB/browser/graph/evaluator/resolver/queue budgets, resource leaks, workload bounds, admission and fairness. |
| `G14` | Supply chain and release integrity | Locks, registries, dependency identity, vulnerability policy, SBOM/provenance/signatures, image inspection, verifier/revocation/anti-downgrade as implemented. |
| `G15` | Evidence and closure | Clean-checkout execution, normalized results, seeds/environments, digests, no hidden skips/quarantines/rerun-only green, approvals, iteration evidence bundle. |

### 6.1 Required closure command

From I04 onward, the authoritative closure command is conceptually:

```bash
./scripts/verify iteration IXX --clean --all-implemented --no-critical-skips --no-quarantine --evidence reports/iteration-XX
```

Before I04, the same gate is executed through the documented individual commands and normalized manually into the evidence schema.

### 6.2 Clean-run rule

An iteration closes only when the gate passes from a clean checkout with fresh generated state and isolated test databases. Release-candidate qualification requires two independent clean runs using the same frozen inputs.

### 6.3 Capability clusters

| Cluster | Real modules in the cluster test |
|---|---|
| Access | M01, M03, M06, M07, M20 |
| Catalogue | M01, M08, M09, M10, M20 |
| Investigation | M09–M14, M19, M20 |
| Save/submission | M06, M09, M11, M15, M16 |
| Evaluation/progression | M08, M09, M16–M18, M20 |
| Media/accessibility | M01–M05, M12 |
| Privacy lifecycle | M07, M15, M16, M18, M20 |
| Operational resilience | M13, M17, M19, M20 plus real database and failure injection |

## 7. Iteration roadmap

| Iteration | Outcome | Principal scope | Stages | File-atomic tasks |
|---|---|---|---:|---:|
| `I00` | Normative baseline and delivery constitution | All modules (governance only) | 4 | 16 |
| `I01` | Polyglot modular workspace and dependency enforcement | M01–M20 scaffolds, Foundation packages | 4 | 18 |
| `I02` | Shared contracts, deterministic primitives, and module test kits | Foundation, All module contract/testkit packages | 4 | 19 |
| `I03` | Persistence ownership and M20 transaction/runtime kernel | M20, Backend modules (persistence contracts) | 4 | 20 |
| `I04` | CI/CD orchestration and executable evidence | All modules, M20 evidence support | 4 | 19 |
| `I05` | Localization, presentation system, and accessibility foundation | M02, M03 | 4 | 19 |
| `I06` | Asset/resource management and persistent radio | M04, M05 | 4 | 18 |
| `I07` | Identity, accounts, sessions, policy receipts, and recovery | M07, M20 policy/workflow contracts, M03/M02 surfaces | 4 | 20 |
| `I08` | Application shell, client synchronization, and authenticated dashboard | M01, M06, M07 | 4 | 19 |
| `I09` | Case content compiler, publication trust, and Academy fixture framework | M10, M20, M03, M04 | 4 | 20 |
| `I10` | Career, catalogue, and progression eligibility foundation | M08, M01, M10, M20 | 4 | 18 |
| `I11` | Round engine, immutable bindings, and starting investigation | M09, M08, M10, M11 bootstrap, M20 | 4 | 19 |
| `I12` | Investigation visibility and manual hypotheses | M11, M09, M10, M12 contract, M13 manual contract | 4 | 18 |
| `I13` | Workspace list, document inspection, and read-model projection | M12, M11, M02, M03, M04 | 4 | 18 |
| `I14` | Graph visualization, semantic navigation, and list/graph parity | M12, M11, M02, M04 | 4 | 17 |
| `I15` | Investigation economy and append-only credit ledger | M14, M10, M20 | 4 | 18 |
| `I16` | Quote, command, outbox, settlement, and reconciliation core | M13, M14, M11, M09, M20 | 4 | 20 |
| `I17` | Deterministic materialized retrieval resolver | M19, M10, M13, M20 | 4 | 19 |
| `I18` | Live provider interpretation, capacity, privacy, and cost accounting | M19, M13, M20 | 4 | 20 |
| `I19` | Complete four-action investigation loop | M11, M12, M13, M14, M19, M10 | 4 | 20 |
| `I20` | Autosave, checkpoints, draft history, and recovery | M15, M06, M09, M11, M16 draft contract, M20 | 4 | 20 |
| `I21` | Structured case file, claims, classifications, and evidence mapping | M16, M11, M15, M02/M03 | 4 | 19 |
| `I22` | Immutable submission and evaluation-pending workflow | M16, M09, M13, M14, M20, M17 contract | 4 | 19 |
| `I23` | Private evaluator, deterministic scoring, endings, and safe verdict | M17, M10, M16, M20, M09 | 4 | 20 |
| `I24` | Atomic progression, results, amendments, and leaderboards | M08, M09, M17, M18, M07, M20 | 4 | 20 |
| `I25` | Detective Academy and Kennel Lab conformance suite | M01–M20 | 4 | 25 |
| `I26` | Puppy family production packages P1–P3 | M10 case packages, All gameplay modules | 4 | 25 |
| `I27` | Adult family production packages A1–A4 | M10 case packages, All gameplay modules | 4 | 24 |
| `I28` | Senior family production packages V1–V3 | M10 case packages, All gameplay modules | 4 | 20 |
| `I29` | Privacy lifecycle, export, deletion, erasure, and consent migration | M07, M15, M16, M18, M20, All data-owning modules | 4 | 20 |
| `I30` | Runtime role isolation, deployment epochs, migrations, and container hardening | All modules, Four runtime roles | 4 | 20 |
| `I31` | Security, browser isolation, LLM assurance, and software supply chain | All modules, M19, M20, Runtime roles | 4 | 20 |
| `I32` | Full accessibility, localization, and inclusive interaction qualification | M01–M06, M12, M16–M18, All cases | 4 | 19 |
| `I33` | Performance, capacity, queue fairness, and long-session resilience | All modules, M12, M13, M17, M19, M20 | 4 | 20 |
| `I34` | Chaos, disaster recovery, key loss, and operational game days | All modules, All runtime roles | 4 | 20 |
| `I35` | Release candidate convergence, freeze, and immutable evidence | All modules, All cases, All roles | 4 | 19 |
| `I36` | Production deployment, verification, and operational handover | All roles, All modules, Operations | 4 | 18 |

**Total:** 37 iterations, 148 stages, and 723 file-atomic tasks.

## 8. Detailed iteration plan

## I00 — Normative baseline and delivery constitution

**Objective:** Establish the immutable requirements baseline, delivery vocabulary, repository constitution, traceability rules, and iteration closure policy before implementation begins.

**Principal modules:** All modules (governance only)

**Principal interactions:** Architecture pair and normative pair

**Prerequisites:**

- Approved v9.0 functional/technical pair and modular specification pack are available.

**Iteration outputs:**

- `I00-S01` — Baseline registration: Every governing artifact is registered by digest and authority.
- `I00-S02` — Delivery hierarchy: Tasks, stages, and iterations have enforceable meanings.
- `I00-S03` — Traceability and change control: Every implementation change can be traced to requirements and tests.
- `I00-S04` — Initial evidence tooling contract: Define how later iterations prove completion.

### I00-S01 — Baseline registration

**Stage outcome:** Every governing artifact is registered by digest and authority.

**Tasks:**

- [ ] **`I00-S01-T01`**
  - **File:** `docs/governance/NORMATIVE_BASELINE.md`
  - **Change:** Record the v9.0 pair, modular pack, precedence rules, constitutional invariants, and supersession policy.
  - **File-level acceptance:** Document lint passes; every referenced artifact has an ID and SHA-256 placeholder resolved by the baseline script.
- [ ] **`I00-S01-T02`**
  - **File:** `docs/governance/REQUIREMENT_ID_POLICY.md`
  - **Change:** Define stable IDs for requirements, tasks, stages, iterations, tests, interactions, risks, decisions, and evidence.
  - **File-level acceptance:** No duplicate prefixes; examples validate against the ID-pattern test.
- [ ] **`I00-S01-T03`**
  - **File:** `config/governance/baseline.json`
  - **Change:** Create the machine-readable artifact registry with document IDs, paths, versions, dates, and digests.
  - **File-level acceptance:** Schema validation and digest verification pass.
- [ ] **`I00-S01-T04`**
  - **File:** `schemas/governance/baseline.schema.json`
  - **Change:** Define the JSON Schema for the baseline registry.
  - **File-level acceptance:** Positive and negative schema fixtures pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I00-S02 — Delivery hierarchy

**Stage outcome:** Tasks, stages, and iterations have enforceable meanings.

**Tasks:**

- [ ] **`I00-S02-T01`**
  - **File:** `docs/delivery/TASK_STAGE_ITERATION_MODEL.md`
  - **Change:** Define a task as one atomic modification to one file, a stage as functionally related tasks across files, and an iteration as a releasable set of stages.
  - **File-level acceptance:** Examples contain no multi-file task; governance tests detect violations.
- [ ] **`I00-S02-T02`**
  - **File:** `docs/delivery/DEFINITION_OF_READY.md`
  - **Change:** Define entry conditions for tasks, stages, and iterations.
  - **File-level acceptance:** Checklist is referenced by the plan validator.
- [ ] **`I00-S02-T03`**
  - **File:** `docs/delivery/DEFINITION_OF_DONE.md`
  - **Change:** Define completion rules, including clean checkout, cumulative tests, evidence, and zero hidden failures.
  - **File-level acceptance:** No iteration may close with failed, skipped-critical, quarantined-critical, or rerun-only-green tests.
- [ ] **`I00-S02-T04`**
  - **File:** `config/governance/iteration-policy.yaml`
  - **Change:** Encode mandatory gates, evidence fields, and failure handling.
  - **File-level acceptance:** Policy schema passes and includes the no-pass-no-progress rule.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I00-S03 — Traceability and change control

**Stage outcome:** Every implementation change can be traced to requirements and tests.

**Tasks:**

- [ ] **`I00-S03-T01`**
  - **File:** `docs/governance/TRACEABILITY_MODEL.md`
  - **Change:** Define requirement → module → contract → task → test → evidence → release relationships.
  - **File-level acceptance:** Traceability graph rules cover all twenty modules and nineteen interaction edges.
- [ ] **`I00-S03-T02`**
  - **File:** `schemas/governance/traceability.schema.json`
  - **Change:** Define the machine-readable conformance graph schema.
  - **File-level acceptance:** Graph fixtures validate; orphan requirement fixture fails.
- [ ] **`I00-S03-T03`**
  - **File:** `config/governance/owners.yaml`
  - **Change:** Assign owners and reviewers for architecture, modules, security, privacy, accessibility, data, evaluator, and release.
  - **File-level acceptance:** Every governed path has at least one owner and one independent reviewer.
- [ ] **`I00-S03-T04`**
  - **File:** `docs/governance/CHANGE_CLASSIFICATION.md`
  - **Change:** Define editorial, compatible, migration-required, ranking-affecting, constitutional, and emergency changes.
  - **File-level acceptance:** Each class has required review and test consequences.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I00-S04 — Initial evidence tooling contract

**Stage outcome:** Define how later iterations prove completion.

**Tasks:**

- [ ] **`I00-S04-T01`**
  - **File:** `docs/testing/EVIDENCE_BUNDLE_FORMAT.md`
  - **Change:** Specify iteration evidence contents: commit, environment, commands, results, reports, digests, exceptions, and approvals.
  - **File-level acceptance:** Evidence schema covers every universal gate.
- [ ] **`I00-S04-T02`**
  - **File:** `schemas/testing/iteration-evidence.schema.json`
  - **Change:** Create the evidence bundle JSON Schema.
  - **File-level acceptance:** Valid sample passes; missing test result or digest fails.
- [ ] **`I00-S04-T03`**
  - **File:** `reports/iteration-00/evidence.json`
  - **Change:** Create the first evidence bundle using the new schema.
  - **File-level acceptance:** Evidence validates and references only passing documentation/governance checks.
- [ ] **`I00-S04-T04`**
  - **File:** `reports/iteration-00/README.md`
  - **Change:** Summarize baseline decisions, tests, known nonimplementation status, and next prerequisites.
  - **File-level acceptance:** Links and IDs validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I00 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Validate Markdown, links, IDs, schemas, JSON/YAML syntax, baseline digests, ownership coverage, and traceability samples.
- Run repository secret and protected-truth scans even though implementation is absent.
- Run the universal gate in documentation-only mode and record explicit N/A reasons only for not-yet-implemented executable layers.
- Rebuild the evidence bundle from a clean checkout and verify its digest.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I00 exit criteria

- All governing documents and schemas pass validation.
- The no-pass-no-progress policy is machine-readable and approved.
- No duplicate or orphan governance IDs remain.
- Iteration evidence is reproducible from a clean checkout.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I01 — Polyglot modular workspace and dependency enforcement

**Objective:** Create the multi-module repository, build graph, runtime composition roots, and machine-enforced boundaries without implementing product behavior.

**Principal modules:** M01–M20 scaffolds, Foundation packages

**Principal interactions:** Compile-time dependency graph

**Prerequisites:**

- I00 is closed.

**Iteration outputs:**

- `I01-S01` — Root workspace: Python and TypeScript packages build under one pinned workspace.
- `I01-S02` — Module scaffolds: Every logical module has contracts, implementation, testkit, and tests.
- `I01-S03` — Runtime composition roots: Four runtime roles are explicit from the start.
- `I01-S04` — Architecture fitness: Forbidden implementation coupling fails immediately.

### I01-S01 — Root workspace

**Stage outcome:** Python and TypeScript packages build under one pinned workspace.

**Tasks:**

- [ ] **`I01-S01-T01`**
  - **File:** `pyproject.toml`
  - **Change:** Declare the Python workspace, pinned interpreter range, shared tooling, and package discovery.
  - **File-level acceptance:** Workspace resolves with one lock and imports no module implementation implicitly.
- [ ] **`I01-S01-T02`**
  - **File:** `package.json`
  - **Change:** Declare root scripts for build, lint, typecheck, test, affected selection, and evidence.
  - **File-level acceptance:** Every root command returns deterministic exit codes.
- [ ] **`I01-S01-T03`**
  - **File:** `pnpm-workspace.yaml`
  - **Change:** Register frontend, contracts, testkits, and application packages.
  - **File-level acceptance:** Workspace listing includes all declared TypeScript packages and no generated directories.
- [ ] **`I01-S01-T04`**
  - **File:** `tsconfig.base.json`
  - **Change:** Define strict TypeScript compiler settings and path policy.
  - **File-level acceptance:** Typecheck rejects implicit any and forbidden cross-module aliases.
- [ ] **`I01-S01-T05`**
  - **File:** `.editorconfig`
  - **Change:** Set repository-wide encoding, newline, indentation, and final-newline rules.
  - **File-level acceptance:** Formatting check passes on all text files.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I01-S02 — Module scaffolds

**Stage outcome:** Every logical module has contracts, implementation, testkit, and tests.

**Tasks:**

- [ ] **`I01-S02-T01`**
  - **File:** `tools/scaffold/module-template.json`
  - **Change:** Define the standard module directory and package metadata template.
  - **File-level acceptance:** Template validation confirms contracts, implementation, testkit, tests, docs, and ownership entries.
- [ ] **`I01-S02-T02`**
  - **File:** `config/modules/module-catalog.yaml`
  - **Change:** Register M01–M20, package names, languages, runtime roles, owners, and declared dependencies.
  - **File-level acceptance:** Catalogue matches the modular manifest exactly.
- [ ] **`I01-S02-T03`**
  - **File:** `scripts/scaffold_modules.py`
  - **Change:** Generate or verify all module skeletons idempotently.
  - **File-level acceptance:** Second run produces no diff; missing module is detected.
- [ ] **`I01-S02-T04`**
  - **File:** `modules/README.md`
  - **Change:** Document module packaging rules and public-versus-internal namespaces.
  - **File-level acceptance:** Architecture lint links every module to its pair specification.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I01-S03 — Runtime composition roots

**Stage outcome:** Four runtime roles are explicit from the start.

**Tasks:**

- [ ] **`I01-S03-T01`**
  - **File:** `apps/web/pyproject.toml`
  - **Change:** Create the WEB backend composition package with no evaluator/private-truth dependency.
  - **File-level acceptance:** Dependency audit confirms only player-safe packages.
- [ ] **`I01-S03-T02`**
  - **File:** `apps/web-ui/package.json`
  - **Change:** Create the browser application package and frontend composition root.
  - **File-level acceptance:** Build produces an empty accessible shell bundle.
- [ ] **`I01-S03-T03`**
  - **File:** `apps/maintenance/pyproject.toml`
  - **Change:** Create the nonpublic MAINTENANCE composition package.
  - **File-level acceptance:** Package depends only on registered workflow handlers.
- [ ] **`I01-S03-T04`**
  - **File:** `apps/evaluator/pyproject.toml`
  - **Change:** Create the private EVALUATOR composition package.
  - **File-level acceptance:** Package can depend on M17 private adapters but no public ingress package.
- [ ] **`I01-S03-T05`**
  - **File:** `apps/migrate/pyproject.toml`
  - **Change:** Create the release-only MIGRATE composition package.
  - **File-level acceptance:** Package contains migration/publication tooling only.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I01-S04 — Architecture fitness

**Stage outcome:** Forbidden implementation coupling fails immediately.

**Tasks:**

- [ ] **`I01-S04-T01`**
  - **File:** `config/architecture/allowed-dependencies.yaml`
  - **Change:** Encode the complete allowed M01–M20 public-contract dependency graph.
  - **File-level acceptance:** Graph is acyclic at implementation level and matches architecture documentation.
- [ ] **`I01-S04-T02`**
  - **File:** `tests/architecture/test_module_dependencies.py`
  - **Change:** Reject imports of another module's domain, application, adapters, migrations, or repositories.
  - **File-level acceptance:** Known forbidden-import fixtures fail.
- [ ] **`I01-S04-T03`**
  - **File:** `tests/architecture/test_runtime_composition.py`
  - **Change:** Verify WEB, MAINTENANCE, EVALUATOR, and MIGRATE dependency allowlists.
  - **File-level acceptance:** WEB fixture importing evaluator truth fails.
- [ ] **`I01-S04-T04`**
  - **File:** `tests/architecture/test_owned_paths.py`
  - **Change:** Ensure every module-owned path has exactly one owner and generated files are isolated.
  - **File-level acceptance:** Unowned and multiply owned fixtures fail.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I01 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run clean Python and TypeScript dependency resolution, format, lint, typecheck, empty package builds, and module discovery.
- Run all architecture fitness tests, including injected forbidden imports and a synthetic dependency cycle.
- Build all four role packages and inspect dependency trees.
- Run baseline secret/truth scans and documentation/schema validation.
- Run the complete I00 regression suite.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I01 exit criteria

- All twenty module skeletons build independently.
- The dependency graph and four role boundaries are machine-enforced.
- No implementation cycle, cross-module internal import, or unowned path exists.
- Clean workspace bootstrap is reproducible.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I02 — Shared contracts, deterministic primitives, and module test kits

**Objective:** Implement the language-neutral contracts and deterministic testing primitives required by every independent module.

**Principal modules:** Foundation, All module contract/testkit packages

**Principal interactions:** I18/I19 public contract conventions

**Prerequisites:**

- I01 is closed.

**Iteration outputs:**

- `I02-S01` — Core value contracts: IDs, time, exact numbers, versions, and errors behave identically across languages.
- `I02-S02` — Canonicalization and idempotency: Cross-module side effects have one deterministic representation.
- `I02-S03` — Deterministic test harness: Each module can test without the full application.
- `I02-S04` — Contract verification API: Producers and consumers share executable verifiers.

### I02-S01 — Core value contracts

**Stage outcome:** IDs, time, exact numbers, versions, and errors behave identically across languages.

**Tasks:**

- [ ] **`I02-S01-T01`**
  - **File:** `foundation/contracts/opaque-id.schema.json`
  - **Change:** Define opaque identifier syntax and length limits.
  - **File-level acceptance:** Python and TypeScript golden fixtures agree.
- [ ] **`I02-S01-T02`**
  - **File:** `foundation/contracts/problem-details.schema.json`
  - **Change:** Define RFC-9457-style project problem details and extension fields.
  - **File-level acceptance:** Valid and invalid error payload fixtures pass.
- [ ] **`I02-S01-T03`**
  - **File:** `foundation/python/fga_foundation/value_objects.py`
  - **Change:** Implement opaque IDs, exact decimals, UTC instants, local dates, and semantic versions.
  - **File-level acceptance:** Unit/property tests cover boundaries and canonical equality.
- [ ] **`I02-S01-T04`**
  - **File:** `foundation/typescript/src/valueObjects.ts`
  - **Change:** Implement matching browser/client value-object parsing and serialization.
  - **File-level acceptance:** Cross-language golden corpus is byte-equivalent.
- [ ] **`I02-S01-T05`**
  - **File:** `foundation/contracts/event-envelope.schema.json`
  - **Change:** Define versioned event envelope, correlation, causation, aggregate revision, and payload digest.
  - **File-level acceptance:** Canonicalization tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I02-S02 — Canonicalization and idempotency

**Stage outcome:** Cross-module side effects have one deterministic representation.

**Tasks:**

- [ ] **`I02-S02-T01`**
  - **File:** `foundation/python/fga_foundation/canonical_json.py`
  - **Change:** Implement canonical JSON serialization and digest calculation.
  - **File-level acceptance:** RFC-compatible golden vectors and Unicode ordering tests pass.
- [ ] **`I02-S02-T02`**
  - **File:** `foundation/typescript/src/canonicalJson.ts`
  - **Change:** Implement matching canonical serialization for client-visible hashes.
  - **File-level acceptance:** Cross-language digest vectors match.
- [ ] **`I02-S02-T03`**
  - **File:** `foundation/contracts/idempotency.schema.json`
  - **Change:** Define principal, operation, key, request hash, retention, and replay result.
  - **File-level acceptance:** Conflicting-key fixture is rejected.
- [ ] **`I02-S02-T04`**
  - **File:** `foundation/python/fga_foundation/idempotency.py`
  - **Change:** Implement request fingerprint and replay decision primitives.
  - **File-level acceptance:** Property tests prove stable fingerprinting and conflicting reuse detection.
- [ ] **`I02-S02-T05`**
  - **File:** `foundation/contracts/contract-version.schema.json`
  - **Change:** Define N-1/N compatibility metadata and retirement date.
  - **File-level acceptance:** Compatibility fixtures validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I02-S03 — Deterministic test harness

**Stage outcome:** Each module can test without the full application.

**Tasks:**

- [ ] **`I02-S03-T01`**
  - **File:** `foundation/python/fga_testkit/determinism.py`
  - **Change:** Provide fake clock, ID factory, randomness, correlation IDs, and failure points.
  - **File-level acceptance:** Unit tests prove reset and order independence.
- [ ] **`I02-S03-T02`**
  - **File:** `foundation/typescript-testkit/src/determinism.ts`
  - **Change:** Provide equivalent browser deterministic controls.
  - **File-level acceptance:** Vitest fixtures are stable across repeated runs.
- [ ] **`I02-S03-T03`**
  - **File:** `foundation/python/fga_testkit/ports.py`
  - **Change:** Provide configurable fake outbound-port base classes and call recording.
  - **File-level acceptance:** Unknown calls fail by default; expected calls are asserted.
- [ ] **`I02-S03-T04`**
  - **File:** `foundation/typescript-testkit/src/browserHarness.ts`
  - **Change:** Provide route, focus, media, network, and storage fakes without service-worker authority.
  - **File-level acceptance:** Harness tests cover reset and failure injection.
- [ ] **`I02-S03-T05`**
  - **File:** `foundation/test-fixtures/cross-language-golden.json`
  - **Change:** Create shared identifiers, times, decimals, events, errors, and canonical JSON vectors.
  - **File-level acceptance:** Both language test suites consume the same file.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I02-S04 — Contract verification API

**Stage outcome:** Producers and consumers share executable verifiers.

**Tasks:**

- [ ] **`I02-S04-T01`**
  - **File:** `foundation/python/fga_contracts/verifier.py`
  - **Change:** Implement JSON Schema validation, version negotiation, canonical digest checks, and fixture discovery.
  - **File-level acceptance:** Provider and consumer sample suites pass.
- [ ] **`I02-S04-T02`**
  - **File:** `foundation/typescript-contracts/src/verifier.ts`
  - **Change:** Implement the corresponding TypeScript verifier.
  - **File-level acceptance:** Schema failures produce stable codes.
- [ ] **`I02-S04-T03`**
  - **File:** `docs/contracts/CONTRACT_EVOLUTION.md`
  - **Change:** Document compatible and incompatible changes, replay, retirement, and migration.
  - **File-level acceptance:** Examples map to executable diff classifications.
- [ ] **`I02-S04-T04`**
  - **File:** `tests/contracts/test_cross_language_compatibility.py`
  - **Change:** Compare Python and TypeScript golden serialization and validation.
  - **File-level acceptance:** All vectors match exactly.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I02 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run foundation unit, property, mutation-smoke, schema, canonicalization, and cross-language tests.
- Run every module's empty contract and testkit build to prove independent consumption.
- Run N-1/N positive and incompatible-change negative fixtures.
- Run architecture, secret/truth, documentation, and all earlier iteration suites.
- Repeat deterministic suites with randomized test order and at least two seeds.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I02 exit criteria

- Canonical values and event/error contracts are byte-compatible across Python and TypeScript.
- All modules can consume deterministic testkit primitives independently.
- Contract verifiers detect incompatible and malformed payloads.
- No nondeterministic test-order dependency remains.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I03 — Persistence ownership and M20 transaction/runtime kernel

**Objective:** Create the PostgreSQL foundation, module-owned migration model, cross-module unit-of-work boundary, durable workflow kernel, and role-aware runtime configuration.

**Principal modules:** M20, Backend modules (persistence contracts)

**Principal interactions:** I19 platform port, Atomic collaborations foundation

**Prerequisites:**

- I02 is closed; a qualified local PostgreSQL container is available.

**Iteration outputs:**

- `I03-S01` — Database foundation: Database access is external, bounded, and role-aware.
- `I03-S02` — Migration ownership: Each module evolves only its own schema.
- `I03-S03` — Unit of work and lock policy: Constitutional transactions coordinate without table sharing.
- `I03-S04` — Durable workflow kernel: Accepted work survives process loss.

### I03-S01 — Database foundation

**Stage outcome:** Database access is external, bounded, and role-aware.

**Tasks:**

- [ ] **`I03-S01-T01`**
  - **File:** `infra/local/postgres/compose.yaml`
  - **Change:** Define isolated local PostgreSQL with health check and disposable test database.
  - **File-level acceptance:** Fresh start, stop, wipe, and health tests pass.
- [ ] **`I03-S01-T02`**
  - **File:** `foundation/python/fga_persistence/config.py`
  - **Change:** Implement validated connection and pool configuration without secrets in logs.
  - **File-level acceptance:** Invalid DSN and oversized pool fixtures fail safely.
- [ ] **`I03-S01-T03`**
  - **File:** `foundation/python/fga_persistence/session.py`
  - **Change:** Implement transaction context, isolation selection, rollback, and connection lifecycle.
  - **File-level acceptance:** Crash/exception tests leave no open transaction.
- [ ] **`I03-S01-T04`**
  - **File:** `config/database/roles.yaml`
  - **Change:** Declare WEB, MAINTENANCE, EVALUATOR, MIGRATE, backup, and diagnostic grants.
  - **File-level acceptance:** Privilege-model test proves least privilege.
- [ ] **`I03-S01-T05`**
  - **File:** `docs/architecture/DATABASE_OWNERSHIP.md`
  - **Change:** Map schemas/tables/migrations to M07–M20 owners and forbid cross-module repositories.
  - **File-level acceptance:** Every planned table has one owner.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I03-S02 — Migration ownership

**Stage outcome:** Each module evolves only its own schema.

**Tasks:**

- [ ] **`I03-S02-T01`**
  - **File:** `foundation/python/fga_migrations/registry.py`
  - **Change:** Register module migration providers and ordering constraints.
  - **File-level acceptance:** Duplicate version and cross-owner migration fixtures fail.
- [ ] **`I03-S02-T02`**
  - **File:** `apps/migrate/src/fga_migrate/main.py`
  - **Change:** Implement release-only migration command with advisory lock and compatibility checks.
  - **File-level acceptance:** Concurrent migration attempt is rejected.
- [ ] **`I03-S02-T03`**
  - **File:** `tests/database/test_migration_ownership.py`
  - **Change:** Verify file paths, SQL targets, grants, and owner metadata.
  - **File-level acceptance:** Cross-schema DDL fixture fails.
- [ ] **`I03-S02-T04`**
  - **File:** `tests/database/test_expand_contract.py`
  - **Change:** Provide generic expand/contract compatibility harness.
  - **File-level acceptance:** Destructive-before-window fixture fails.
- [ ] **`I03-S02-T05`**
  - **File:** `config/database/schema-compatibility.yaml`
  - **Change:** Define supported application/schema deployment epochs.
  - **File-level acceptance:** N-1/N role startup matrix is executable.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I03-S03 — Unit of work and lock policy

**Stage outcome:** Constitutional transactions coordinate without table sharing.

**Tasks:**

- [ ] **`I03-S03-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/unit_of_work.py`
  - **Change:** Implement public UnitOfWorkPort and participant registration.
  - **File-level acceptance:** Participants can mutate only their repositories in one transaction.
- [ ] **`I03-S03-T02`**
  - **File:** `config/database/lock-order.yaml`
  - **Change:** Declare global lock order for account, career, round, command, ledger, submission, verdict, and publication resources.
  - **File-level acceptance:** Static test detects inversion.
- [ ] **`I03-S03-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/retry_policy.py`
  - **Change:** Implement bounded serialization/deadlock retry with deterministic jitter port.
  - **File-level acceptance:** Property tests prove bounded attempts and stable terminal error.
- [ ] **`I03-S03-T04`**
  - **File:** `tests/database/test_cross_module_uow.py`
  - **Change:** Exercise synthetic participants, rollback, deadlock, and partial failure.
  - **File-level acceptance:** No partial commit occurs.
- [ ] **`I03-S03-T05`**
  - **File:** `docs/architecture/TRANSACTION_MODEL.md`
  - **Change:** Document atomic workflows, isolation, no-network-I/O rule, and fencing.
  - **File-level acceptance:** Architecture test links each atomic workflow to a test.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I03-S04 — Durable workflow kernel

**Stage outcome:** Accepted work survives process loss.

**Tasks:**

- [ ] **`I03-S04-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/workflow.schema.json`
  - **Change:** Define job, step, class, deadline, lease, fence, attempt, cancellation, and terminal states.
  - **File-level acceptance:** Schema fixtures pass.
- [ ] **`I03-S04-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/workflow.py`
  - **Change:** Implement durable job aggregate and transition rules.
  - **File-level acceptance:** Model tests cover all transitions.
- [ ] **`I03-S04-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/migrations/0001_workflow_kernel.sql`
  - **Change:** Create owned workflow, lease, and event tables.
  - **File-level acceptance:** Migration applies and rolls forward from empty DB.
- [ ] **`I03-S04-T04`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/lease_repository.py`
  - **Change:** Implement claim, renew, release, expiry, and fencing token checks.
  - **File-level acceptance:** Two-executor concurrency test prevents double ownership.
- [ ] **`I03-S04-T05`**
  - **File:** `modules/m20-publication-workflow-runtime-control/testkit/src/fga_platform_testkit/workflow.py`
  - **Change:** Provide deterministic workflow executor and crash-point controls.
  - **File-level acceptance:** Consumers can test without MAINTENANCE runtime.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I03 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run migration ownership, apply-from-zero, N-1 upgrade, rollback/forward-fix, lock-order, isolation, and connection-leak suites.
- Run M20 unit, property/model, contract, component, architecture, security, and concurrency tests.
- Run pairwise synthetic UnitOfWork participant tests and workflow lease/fencing tests.
- Kill the workflow process at every persisted transition and verify exact recovery.
- Run all I00–I02 cumulative tests and scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I03 exit criteria

- Database roles, schema ownership, migrations, and lock order are enforceable.
- Cross-module atomic work has a tested public unit-of-work mechanism.
- Durable jobs survive crash and cannot be settled by a stale lease holder.
- No external I/O can occur inside the tested transaction scope.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I04 — CI/CD orchestration and executable evidence

**Objective:** Automate independent module, contract, pairwise, cluster, system, and release gates so later iterations cannot bypass testing.

**Principal modules:** All modules, M20 evidence support

**Principal interactions:** All test layers

**Prerequisites:**

- I03 is closed.

**Iteration outputs:**

- `I04-S01` — Unified test command: One command can verify any task, stage, module, interaction, cluster, iteration, or release.
- `I04-S02` — Pipeline lanes: Every required layer has a dedicated lane.
- `I04-S03` — Impact and coverage graph: Optimized lanes never omit mandatory regressions.
- `I04-S04` — Quality reporting: Failures are visible and actionable.

### I04-S01 — Unified test command

**Stage outcome:** One command can verify any task, stage, module, interaction, cluster, iteration, or release.

**Tasks:**

- [ ] **`I04-S01-T01`**
  - **File:** `tools/fga_verify/cli.py`
  - **Change:** Implement verification target parsing, clean mode, gate selection, failure propagation, and evidence output.
  - **File-level acceptance:** CLI unit tests cover invalid targets and nonzero child results.
- [ ] **`I04-S01-T02`**
  - **File:** `tools/fga_verify/catalog.py`
  - **Change:** Load modules, interactions, clusters, iterations, and test commands from governed configuration.
  - **File-level acceptance:** Catalogue cross-checks modular manifest.
- [ ] **`I04-S01-T03`**
  - **File:** `tools/fga_verify/executor.py`
  - **Change:** Run commands without hiding failures, capture environment and digests, and prohibit rerun-to-green closure.
  - **File-level acceptance:** Injected flaky test marks the iteration failed.
- [ ] **`I04-S01-T04`**
  - **File:** `tools/fga_verify/evidence.py`
  - **Change:** Write schema-valid evidence bundles and report inventory.
  - **File-level acceptance:** Generated I04 evidence validates.
- [ ] **`I04-S01-T05`**
  - **File:** `scripts/verify`
  - **Change:** Add the repository entry point for local and CI execution.
  - **File-level acceptance:** Works from clean checkout with no shell-specific assumptions.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I04-S02 — Pipeline lanes

**Stage outcome:** Every required layer has a dedicated lane.

**Tasks:**

- [ ] **`I04-S02-T01`**
  - **File:** `.github/workflows/pr-fast.yml`
  - **Change:** Add changed-module static, unit, property-smoke, contract, and architecture lane.
  - **File-level acceptance:** Synthetic changed-file matrix selects expected modules.
- [ ] **`I04-S02-T02`**
  - **File:** `.github/workflows/module.yml`
  - **Change:** Run full independent module qualification for each module.
  - **File-level acceptance:** Matrix can run one module without booting unrelated modules.
- [ ] **`I04-S02-T03`**
  - **File:** `.github/workflows/contracts.yml`
  - **Change:** Run producer/consumer, canonicalization, N-1/N, and replay tests.
  - **File-level acceptance:** Incompatible fixture blocks merge.
- [ ] **`I04-S02-T04`**
  - **File:** `.github/workflows/integration.yml`
  - **Change:** Run affected pairwise and all mandatory cluster suites.
  - **File-level acceptance:** Dependency-edge selection is validated.
- [ ] **`I04-S02-T05`**
  - **File:** `.github/workflows/system-release.yml`
  - **Change:** Run role, E2E, accessibility, security, performance, chaos, migration, and release evidence lanes.
  - **File-level acceptance:** Workflow refuses unsigned or untraceable artifact.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I04-S03 — Impact and coverage graph

**Stage outcome:** Optimized lanes never omit mandatory regressions.

**Tasks:**

- [ ] **`I04-S03-T01`**
  - **File:** `config/testing/interactions.yaml`
  - **Change:** Encode I01–I19 producers, consumers, criticality, pairwise suites, and fault profiles.
  - **File-level acceptance:** Every declared edge has a test target.
- [ ] **`I04-S03-T02`**
  - **File:** `config/testing/clusters.yaml`
  - **Change:** Encode the eight required capability clusters and members.
  - **File-level acceptance:** Membership matches architecture specification.
- [ ] **`I04-S03-T03`**
  - **File:** `tools/fga_verify/impact.py`
  - **Change:** Compute affected modules, consumers, interactions, clusters, and cross-cutting mandatory suites.
  - **File-level acceptance:** Golden change scenarios produce expected selection.
- [ ] **`I04-S03-T04`**
  - **File:** `tests/governance/test_requirement_coverage.py`
  - **Change:** Require every current requirement and interaction to map to one or more tests.
  - **File-level acceptance:** Orphan fixture fails.
- [ ] **`I04-S03-T05`**
  - **File:** `config/testing/mandatory-regressions.yaml`
  - **Change:** Always include identity, credits/commands, truth isolation, submission/evaluation, publication trust, accessibility, and migrations.
  - **File-level acceptance:** Impact optimizer cannot remove these.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I04-S04 — Quality reporting

**Stage outcome:** Failures are visible and actionable.

**Tasks:**

- [ ] **`I04-S04-T01`**
  - **File:** `config/testing/test-result.schema.json`
  - **Change:** Define normalized result status, duration, seed, environment, retry history, and artifact links.
  - **File-level acceptance:** Schema rejects ambiguous pass/fail.
- [ ] **`I04-S04-T02`**
  - **File:** `tools/fga_verify/report.py`
  - **Change:** Generate Markdown and JSON summaries with failed-task ownership and no hidden skipped tests.
  - **File-level acceptance:** Sample failure report identifies exact owner.
- [ ] **`I04-S04-T03`**
  - **File:** `docs/testing/TEST_FAILURE_POLICY.md`
  - **Change:** Define failure triage, same-iteration fixes, flake treatment, quarantine prohibition for critical tests, and rerun rules.
  - **File-level acceptance:** Policy is referenced by the verifier.
- [ ] **`I04-S04-T04`**
  - **File:** `reports/iteration-04/evidence.json`
  - **Change:** Record the first fully automated cumulative gate.
  - **File-level acceptance:** Evidence includes all prior iteration results.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I04 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run the verifier's own unit/property/component tests and inject child process failures, timeouts, malformed reports, flaky tests, and missing artifacts.
- Run all pipeline definitions through syntax validation and local workflow simulation where available.
- Run changed-module impact golden tests for every module and interaction.
- Execute the complete cumulative suite through the new unified command from a clean checkout.
- Verify that one deliberate failing test prevents evidence status from becoming complete.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I04 exit criteria

- One command produces authoritative evidence for the implemented solution.
- All test lanes and impact rules are executable and cannot suppress mandatory regressions.
- A failure, flaky rerun, missing report, or skipped critical test blocks iteration closure.
- I04 evidence is generated solely by the automated verifier.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I05 — Localization, presentation system, and accessibility foundation

**Objective:** Deliver M03 and M02 as independently testable foundations for all later player-facing work.

**Principal modules:** M02, M03

**Principal interactions:** I03, I18

**Prerequisites:**

- I04 is closed.

**Iteration outputs:**

- `I05-S01` — Localization contracts and catalogues: Functional text is externalized, versioned, and deterministic.
- `I05-S02` — Design-system primitives: Reusable controls expose consistent semantics and focus behavior.
- `I05-S03` — Layout and input foundations: Forms and page layouts remain usable at supported sizes.
- `I05-S04` — Independent and pairwise qualification: M02 and M03 are consumable without an application shell.

### I05-S01 — Localization contracts and catalogues

**Stage outcome:** Functional text is externalized, versioned, and deterministic.

**Tasks:**

- [ ] **`I05-S01-T01`**
  - **File:** `modules/m03-localization-messaging/contracts/message.schema.json`
  - **Change:** Define stable message keys, parameters, locale, fallback, severity, and rich-text restrictions.
  - **File-level acceptance:** Schema rejects undeclared parameters and raw HTML.
- [ ] **`I05-S01-T02`**
  - **File:** `modules/m03-localization-messaging/frontend/src/messageResolver.ts`
  - **Change:** Implement catalogue lookup, interpolation, pluralization, and fallback.
  - **File-level acceptance:** Unit tests cover missing keys, Unicode, plural forms, and parameter escaping.
- [ ] **`I05-S01-T03`**
  - **File:** `modules/m03-localization-messaging/backend/src/fga_localization/message_catalog.py`
  - **Change:** Implement server-side safe catalogue resolution for notices and exports.
  - **File-level acceptance:** Python and browser fixtures produce equivalent plain text.
- [ ] **`I05-S01-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Create the baseline English catalogue for shell, authentication, errors, accessibility, and generic gameplay.
  - **File-level acceptance:** Completeness and unused-key checks pass.
- [ ] **`I05-S01-T05`**
  - **File:** `modules/m03-localization-messaging/testkit/src/catalogueBuilder.ts`
  - **Change:** Provide catalogue builders, fake locales, and missing-key injection.
  - **File-level acceptance:** Consumer modules can test messages independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I05-S02 — Design-system primitives

**Stage outcome:** Reusable controls expose consistent semantics and focus behavior.

**Tasks:**

- [ ] **`I05-S02-T01`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/theme.css`
  - **Change:** Define theme tokens, noir presentation variables, contrast-safe states, reduced motion, and forced-colors fallbacks.
  - **File-level acceptance:** Automated contrast/token tests pass.
- [ ] **`I05-S02-T02`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/Button.tsx`
  - **Change:** Implement the accessible button primitive with pending, disabled, danger, and icon-label states.
  - **File-level acceptance:** Keyboard, focus, name, and disabled-state tests pass.
- [ ] **`I05-S02-T03`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/Dialog.tsx`
  - **Change:** Implement focus-trapped modal behavior and restoration.
  - **File-level acceptance:** Escape, focus order, screen-reader labelling, and nested-dialog rejection pass.
- [ ] **`I05-S02-T04`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/StatusMessage.tsx`
  - **Change:** Implement polite/assertive live-region status messages using M03 keys.
  - **File-level acceptance:** Announcement deduplication tests pass.
- [ ] **`I05-S02-T05`**
  - **File:** `modules/m02-presentation-accessibility/testkit/src/a11yHarness.ts`
  - **Change:** Provide focus-order, live-region, zoom/reflow, contrast, and reduced-motion assertions.
  - **File-level acceptance:** Harness self-tests detect deliberate violations.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I05-S03 — Layout and input foundations

**Stage outcome:** Forms and page layouts remain usable at supported sizes.

**Tasks:**

- [ ] **`I05-S03-T01`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/FormField.tsx`
  - **Change:** Implement labels, descriptions, validation, and error association.
  - **File-level acceptance:** Accessible-name and error-link tests pass.
- [ ] **`I05-S03-T02`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/PageLayout.tsx`
  - **Change:** Implement responsive shell content regions without horizontal overflow.
  - **File-level acceptance:** 320 CSS px and 200% zoom visual/DOM tests pass.
- [ ] **`I05-S03-T03`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/components/DataState.tsx`
  - **Change:** Implement loading, empty, unavailable, degraded, and recovery states.
  - **File-level acceptance:** Each state has non-color text semantics.
- [ ] **`I05-S03-T04`**
  - **File:** `modules/m02-presentation-accessibility/frontend/src/index.ts`
  - **Change:** Publish only supported presentation contracts and components.
  - **File-level acceptance:** Public API snapshot contains no internals.
- [ ] **`I05-S03-T05`**
  - **File:** `docs/frontend/PRESENTATION_ACCESSIBILITY_RULES.md`
  - **Change:** Document mandatory component use, no baked functional text, and review checklist.
  - **File-level acceptance:** Architecture lint references the rule set.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I05-S04 — Independent and pairwise qualification

**Stage outcome:** M02 and M03 are consumable without an application shell.

**Tasks:**

- [ ] **`I05-S04-T01`**
  - **File:** `modules/m03-localization-messaging/tests/contract/test_catalogue_contract.py`
  - **Change:** Verify catalogue schema, parameter compatibility, and version evolution.
  - **File-level acceptance:** N-1 fixture passes; removed required key fails.
- [ ] **`I05-S04-T02`**
  - **File:** `modules/m02-presentation-accessibility/tests/component/presentation.spec.tsx`
  - **Change:** Exercise components under fake catalogues and assets.
  - **File-level acceptance:** No application package is required.
- [ ] **`I05-S04-T03`**
  - **File:** `tests/integration/pairs/I18-localized-catalogue.spec.ts`
  - **Change:** Run real M02 and M03 with signed-catalogue fake from M20.
  - **File-level acceptance:** Version receipt and fallback behavior pass.
- [ ] **`I05-S04-T04`**
  - **File:** `tests/accessibility/foundation-critical-journeys.spec.ts`
  - **Change:** Run keyboard, focus, live-region, reflow, zoom, contrast, and reduced-motion journeys.
  - **File-level acceptance:** No serious/critical automated violation remains.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I05 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete M02 and M03 independent unit, property, contract, component, architecture, security, and accessibility suites.
- Run M02↔M03 pairwise integration with missing, stale, malformed, and incompatible catalogue fixtures.
- Run cross-language message parameter and Unicode normalization tests.
- Run visual regression at supported viewport/zoom/contrast/motion modes.
- Run the full cumulative I00–I04 gate.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I05 exit criteria

- M02 and M03 build and test without the shell or backend.
- All functional text in implemented UI primitives is catalogue-driven.
- Keyboard, focus, reflow, contrast, and live-region foundations pass.
- No consumer imports localization or presentation internals.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I06 — Asset/resource management and persistent radio

**Objective:** Deliver signed asset resolution and optional route-persistent audio without allowing media to become gameplay authority.

**Principal modules:** M04, M05

**Principal interactions:** I17, I03

**Prerequisites:**

- I05 is closed.

**Iteration outputs:**

- `I06-S01` — Asset manifest and resolver: All media is addressed by stable IDs and verified digests.
- `I06-S02` — Safe rendering and caching: Only approved public immutable resources are cacheable.
- `I06-S03` — Radio engine: Audio remains optional and persistent across routes.
- `I06-S04` — Media integration: Media foundations integrate without the final shell.

### I06-S01 — Asset manifest and resolver

**Stage outcome:** All media is addressed by stable IDs and verified digests.

**Tasks:**

- [ ] **`I06-S01-T01`**
  - **File:** `modules/m04-asset-resource-management/contracts/asset-manifest.schema.json`
  - **Change:** Define asset ID, type, digest, dimensions, variants, purpose, alt/transcript keys, approval, and fallback.
  - **File-level acceptance:** Schema rejects missing accessibility metadata for essential assets.
- [ ] **`I06-S01-T02`**
  - **File:** `modules/m04-asset-resource-management/frontend/src/assetResolver.ts`
  - **Change:** Implement manifest lookup, variant selection, integrity metadata, and safe fallback.
  - **File-level acceptance:** Unit tests cover missing/corrupt/unsupported assets.
- [ ] **`I06-S01-T03`**
  - **File:** `modules/m04-asset-resource-management/backend/src/fga_assets/manifest.py`
  - **Change:** Implement publication-side manifest validation and digest verification.
  - **File-level acceptance:** Tampered asset fixture fails.
- [ ] **`I06-S01-T04`**
  - **File:** `assets/manifests/core-assets.json`
  - **Change:** Register initial shell, placeholder comic, icon, and radio assets.
  - **File-level acceptance:** Manifest validates and contains no functional text rasterization.
- [ ] **`I06-S01-T05`**
  - **File:** `modules/m04-asset-resource-management/testkit/src/assetFixtures.ts`
  - **Change:** Provide valid, missing, corrupt, and quarantined asset manifests.
  - **File-level acceptance:** Consumers can inject every state.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I06-S02 — Safe rendering and caching

**Stage outcome:** Only approved public immutable resources are cacheable.

**Tasks:**

- [ ] **`I06-S02-T01`**
  - **File:** `modules/m04-asset-resource-management/frontend/src/Asset.tsx`
  - **Change:** Implement image/media rendering with alt/transcript and fallback behavior.
  - **File-level acceptance:** Broken network and missing variant tests pass.
- [ ] **`I06-S02-T02`**
  - **File:** `apps/web-ui/src/serviceWorkerPolicy.ts`
  - **Change:** Define public-content-addressed asset caching and authenticated-route bypass.
  - **File-level acceptance:** Cache test proves private/API responses are never stored.
- [ ] **`I06-S02-T03`**
  - **File:** `modules/m04-asset-resource-management/backend/src/fga_assets/headers.py`
  - **Change:** Emit immutable cache headers only for signed public digests.
  - **File-level acceptance:** Private or mutable fixture receives no-store.
- [ ] **`I06-S02-T04`**
  - **File:** `tests/security/test_asset_active_content.py`
  - **Change:** Reject scripts, macros, external loads, unsafe MIME, and oversized assets.
  - **File-level acceptance:** Malicious fixtures fail closed.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I06-S03 — Radio engine

**Stage outcome:** Audio remains optional and persistent across routes.

**Tasks:**

- [ ] **`I06-S03-T01`**
  - **File:** `modules/m05-audio-radio/contracts/radio-manifest.schema.json`
  - **Change:** Define approved tracks, digests, duration metadata, and nonrepeat policy.
  - **File-level acceptance:** Invalid or duplicate track entries fail.
- [ ] **`I06-S03-T02`**
  - **File:** `modules/m05-audio-radio/frontend/src/radioEngine.ts`
  - **Change:** Implement gesture-gated start, randomized nonrepeating sequence, skip-on-error, and off state.
  - **File-level acceptance:** Deterministic random fixture proves no immediate repeat.
- [ ] **`I06-S03-T03`**
  - **File:** `modules/m05-audio-radio/frontend/src/tabCoordinator.ts`
  - **Change:** Implement playback-leader coordination using a replaceable channel port.
  - **File-level acceptance:** Two-tab tests prove one audible leader.
- [ ] **`I06-S03-T04`**
  - **File:** `modules/m05-audio-radio/frontend/src/RadioControl.tsx`
  - **Change:** Implement accessible on/off-only control using M02/M03.
  - **File-level acceptance:** Keyboard, label, state, and failure announcement tests pass.
- [ ] **`I06-S03-T05`**
  - **File:** `assets/manifests/radio.json`
  - **Change:** Register the approved initial radio playlist.
  - **File-level acceptance:** Digest and licensing metadata validation passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I06-S04 — Media integration

**Stage outcome:** Media foundations integrate without the final shell.

**Tasks:**

- [ ] **`I06-S04-T01`**
  - **File:** `tests/integration/pairs/I17-asset-publication.spec.ts`
  - **Change:** Run real M04 with M20 signed-publication fake, including quarantine and rollback.
  - **File-level acceptance:** Resolver never serves revoked assets.
- [ ] **`I06-S04-T02`**
  - **File:** `tests/integration/pairs/I03-radio-assets.spec.ts`
  - **Change:** Run real M05 with M04 and deterministic browser media harness.
  - **File-level acceptance:** Missing tracks do not block gameplay UI.
- [ ] **`I06-S04-T03`**
  - **File:** `tests/accessibility/media-alternatives.spec.ts`
  - **Change:** Verify alt text, transcripts, skip/fallback, radio-off completion, and reduced motion.
  - **File-level acceptance:** All media-dependent journeys have an equivalent alternative.
- [ ] **`I06-S04-T04`**
  - **File:** `tests/security/service-worker-isolation.spec.ts`
  - **Change:** Attempt to cache authenticated evidence and API responses.
  - **File-level acceptance:** Every private request bypasses cache.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I06 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run M04/M05 independent suites, asset schema/digest scans, MIME/active-content negatives, and service-worker isolation.
- Run pairwise M04↔M20 and M05↔M04/M06-fake tests with corruption, missing resources, autoplay denial, and multiple tabs.
- Run media accessibility and no-audio journey tests.
- Run bundle inspection to ensure raw projects, unapproved assets, and credentials are absent.
- Run all prior cumulative gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I06 exit criteria

- All media resolves by stable signed identifiers with safe fallbacks.
- Authenticated data cannot enter asset or service-worker caches.
- Radio survives navigation, fails safely, and is fully optional.
- M04 and M05 remain independently testable.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I07 — Identity, accounts, sessions, policy receipts, and recovery

**Objective:** Deliver M07 as a complete secure account vertical slice with explicit registration/sign-in, recovery codes, sessions, and policy version receipts.

**Principal modules:** M07, M20 policy/workflow contracts, M03/M02 surfaces

**Principal interactions:** I01, I04, I18

**Prerequisites:**

- I06 is closed.

**Iteration outputs:**

- `I07-S01` — Account domain and persistence: Identity state and credentials are owner-scoped and independently testable.
- `I07-S02` — Registration, authentication, and sessions: Sign-in never creates an account and sessions are revocable.
- `I07-S03` — Player-facing identity surfaces: Authentication is accessible and policy-aware.
- `I07-S04` — Policy and privacy request initiation: The exact policy version is receipted before protected use.

### I07-S01 — Account domain and persistence

**Stage outcome:** Identity state and credentials are owner-scoped and independently testable.

**Tasks:**

- [ ] **`I07-S01-T01`**
  - **File:** `modules/m07-identity-account-security/contracts/account.schema.json`
  - **Change:** Define public account, status, session, policy receipt, recovery code, and privacy preference contracts.
  - **File-level acceptance:** Schema excludes password hashes and private security metadata.
- [ ] **`I07-S01-T02`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/domain/account.py`
  - **Change:** Implement account states, username normalization, and recovery-limited transitions.
  - **File-level acceptance:** Property tests cover valid/invalid transitions.
- [ ] **`I07-S01-T03`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/domain/password_policy.py`
  - **Change:** Implement length, compromised-password port, Unicode, and no-composition rules.
  - **File-level acceptance:** Boundary and normalization tests pass.
- [ ] **`I07-S01-T04`**
  - **File:** `modules/m07-identity-account-security/backend/migrations/0001_identity.sql`
  - **Change:** Create accounts, credentials, sessions, recovery verifiers, receipts, and security events.
  - **File-level acceptance:** Migration and privilege tests pass.
- [ ] **`I07-S01-T05`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/repository.py`
  - **Change:** Implement owner-safe repositories using only M07 tables.
  - **File-level acceptance:** IDOR component tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I07-S02 — Registration, authentication, and sessions

**Stage outcome:** Sign-in never creates an account and sessions are revocable.

**Tasks:**

- [ ] **`I07-S02-T01`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/registration.py`
  - **Change:** Implement explicit registration, password confirmation, receipt binding, and recovery-code generation.
  - **File-level acceptance:** Duplicate/invalid registration is enumeration-resistant.
- [ ] **`I07-S02-T02`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/authentication.py`
  - **Change:** Implement generic sign-in failures, rate-limit port, password verification, and session rotation.
  - **File-level acceptance:** Wrong user and wrong password are indistinguishable externally.
- [ ] **`I07-S02-T03`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/sessions.py`
  - **Change:** Implement idle/absolute expiry, rotation, revocation, and logout-all.
  - **File-level acceptance:** Fake-clock tests cover every boundary.
- [ ] **`I07-S02-T04`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/recovery.py`
  - **Change:** Implement one-time recovery-code reset and RECOVERY_LIMITED restrictions.
  - **File-level acceptance:** Reused code and concurrent use fail.
- [ ] **`I07-S02-T05`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/http.py`
  - **Change:** Expose versioned authentication/account endpoints with CSRF/origin contract hooks.
  - **File-level acceptance:** OpenAPI and problem-detail contract tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I07-S03 — Player-facing identity surfaces

**Stage outcome:** Authentication is accessible and policy-aware.

**Tasks:**

- [ ] **`I07-S03-T01`**
  - **File:** `modules/m07-identity-account-security/frontend/src/AuthScreen.tsx`
  - **Change:** Implement one surface with explicit Sign in and Create account actions.
  - **File-level acceptance:** Keyboard/screen-reader and typo-no-create tests pass.
- [ ] **`I07-S03-T02`**
  - **File:** `modules/m07-identity-account-security/frontend/src/RecoveryCodes.tsx`
  - **Change:** Implement accessible display, print/download preparation, confirmation, and regeneration warnings.
  - **File-level acceptance:** Codes are shown only in generation state.
- [ ] **`I07-S03-T03`**
  - **File:** `modules/m07-identity-account-security/frontend/src/AccountSecurity.tsx`
  - **Change:** Implement session list/revoke, password reset, recovery state, and privacy preference controls.
  - **File-level acceptance:** No sensitive metadata is exposed.
- [ ] **`I07-S03-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add identity, policy, recovery, session, and generic security messages.
  - **File-level acceptance:** Catalogue compatibility passes.
- [ ] **`I07-S03-T05`**
  - **File:** `modules/m07-identity-account-security/testkit/src/identityFixtures.ts`
  - **Change:** Publish fake session/account/recovery states for shell and consumer tests.
  - **File-level acceptance:** Fixtures contain no internal credential fields.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I07-S04 — Policy and privacy request initiation

**Stage outcome:** The exact policy version is receipted before protected use.

**Tasks:**

- [ ] **`I07-S04-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/policy-bundle.schema.json`
  - **Change:** Define signed policy bundle, materiality, jurisdiction, effective window, and required receipts.
  - **File-level acceptance:** Invalid signature/effective-window fixture fails.
- [ ] **`I07-S04-T02`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/policy_receipts.py`
  - **Change:** Implement receipt creation, withdrawal, and material-change reacknowledgement.
  - **File-level acceptance:** Receipt hash and account ownership tests pass.
- [ ] **`I07-S04-T03`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/privacy_requests.py`
  - **Change:** Implement authenticated export/deletion request initiation as durable-work commands.
  - **File-level acceptance:** Only request initiation is implemented; processing remains pending for I29.
- [ ] **`I07-S04-T04`**
  - **File:** `tests/integration/pairs/I04-identity-policy.spec.py`
  - **Change:** Run real M07 and M20 policy contracts with valid, stale, withdrawn, and changed policies.
  - **File-level acceptance:** Protected route access follows receipt state.
- [ ] **`I07-S04-T05`**
  - **File:** `tests/security/identity_negative_suite.py`
  - **Change:** Exercise enumeration, credential stuffing, fixation, CSRF/origin, IDOR, code reuse, and log redaction.
  - **File-level acceptance:** All attacks fail with safe responses.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I07 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M07 unit/property/model, contract, component, architecture, security/privacy, rate-limit, and concurrency suites.
- Run real PostgreSQL migration/upgrade tests and ownership/grant checks.
- Run pairwise M07↔M20 policy/workflow and M07↔M03/M02 UI tests.
- Run browser E2E for registration, recovery-code storage acknowledgement, logout/login, session expiry, reset, and RECOVERY_LIMITED.
- Run complete cumulative regression and leakage/secret scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I07 exit criteria

- Registration and sign-in are explicit and enumeration-resistant.
- Recovery codes are one-time protected secrets; exceptional reset reduces privileges.
- Sessions and policy receipts are versioned, revocable, and tested.
- M07 passes independently and through access-cluster integration.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I08 — Application shell, client synchronization, and authenticated dashboard

**Objective:** Compose M01 and M06 with M07 to create the first complete browser-to-database authenticated vertical slice.

**Principal modules:** M01, M06, M07

**Principal interactions:** I01, I02, I03

**Prerequisites:**

- I07 is closed.

**Iteration outputs:**

- `I08-S01` — Client synchronization contracts: Server state, revisions, and compatibility are client-authoritative only through explicit acknowledgements.
- `I08-S02` — Shell bootstrap and routes: The application starts safely and owns navigation only.
- `I08-S03` — Authenticated dashboard shell: A signed-in player sees safe account/capability state and navigation placeholders.
- `I08-S04` — Access-cluster integration: M01/M03/M06/M07/M20 operate as one capability.

### I08-S01 — Client synchronization contracts

**Stage outcome:** Server state, revisions, and compatibility are client-authoritative only through explicit acknowledgements.

**Tasks:**

- [ ] **`I08-S01-T01`**
  - **File:** `modules/m06-client-state-synchronization/contracts/client-state.schema.json`
  - **Change:** Define query state, mutation receipt, revision conflict, connectivity, and stale-client contracts.
  - **File-level acceptance:** Schema rejects missing revision on mutable data.
- [ ] **`I08-S01-T02`**
  - **File:** `modules/m06-client-state-synchronization/frontend/src/queryClient.ts`
  - **Change:** Implement owner-scoped server-state cache and invalidation rules.
  - **File-level acceptance:** Tests prove no private data persists after logout.
- [ ] **`I08-S01-T03`**
  - **File:** `modules/m06-client-state-synchronization/frontend/src/mutationCoordinator.ts`
  - **Change:** Implement idempotency keys, expected revisions, timeout-unknown state, and exact replay.
  - **File-level acceptance:** Duplicate and lost-response tests pass.
- [ ] **`I08-S01-T04`**
  - **File:** `modules/m06-client-state-synchronization/frontend/src/compatibility.ts`
  - **Change:** Implement build/policy/deployment epoch comparison and forced-safe reload state.
  - **File-level acceptance:** Stale incompatible client cannot mutate.
- [ ] **`I08-S01-T05`**
  - **File:** `modules/m06-client-state-synchronization/testkit/src/clientStateHarness.ts`
  - **Change:** Provide offline, timeout, stale revision, duplicate response, and tab-race controls.
  - **File-level acceptance:** Consumer tests remain deterministic.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I08-S02 — Shell bootstrap and routes

**Stage outcome:** The application starts safely and owns navigation only.

**Tasks:**

- [ ] **`I08-S02-T01`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/bootstrap.ts`
  - **Change:** Load safe build/capability/session/policy state and choose initial route.
  - **File-level acceptance:** Unauthenticated and recovery-limited fixtures route correctly.
- [ ] **`I08-S02-T02`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/router.tsx`
  - **Change:** Define public, authenticated, recovery-limited, and unavailable route groups.
  - **File-level acceptance:** Deep-link guard tests pass.
- [ ] **`I08-S02-T03`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/AppShell.tsx`
  - **Change:** Compose M02–M06 through public ports and keep radio above route boundaries.
  - **File-level acceptance:** Route transitions do not remount radio.
- [ ] **`I08-S02-T04`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/GlobalRecovery.tsx`
  - **Change:** Implement stale-client, expired-session, service-unavailable, and correlation-ID recovery UI.
  - **File-level acceptance:** Focus and announcement tests pass.
- [ ] **`I08-S02-T05`**
  - **File:** `apps/web-ui/src/main.tsx`
  - **Change:** Create the browser composition root with only public module APIs.
  - **File-level acceptance:** Architecture test rejects internal imports.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I08-S03 — Authenticated dashboard shell

**Stage outcome:** A signed-in player sees safe account/capability state and navigation placeholders.

**Tasks:**

- [ ] **`I08-S03-T01`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/Dashboard.tsx`
  - **Change:** Implement dashboard regions for careers, Academy, privacy, account, help, and service status.
  - **File-level acceptance:** No case data is inferred or hard-coded.
- [ ] **`I08-S03-T02`**
  - **File:** `apps/web/src/fga_web/main.py`
  - **Change:** Create FastAPI composition root, middleware, health, version, session, and static app hosting.
  - **File-level acceptance:** WEB has no evaluator or migration privilege.
- [ ] **`I08-S03-T03`**
  - **File:** `apps/web/src/fga_web/security_middleware.py`
  - **Change:** Add trusted host/origin, CSRF hook, correlation ID, secure cookie, body limit, and no-store policy.
  - **File-level acceptance:** Security middleware tests pass.
- [ ] **`I08-S03-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add shell, dashboard, compatibility, connectivity, and recovery messages.
  - **File-level acceptance:** Catalogue tests pass.
- [ ] **`I08-S03-T05`**
  - **File:** `tests/e2e/access-dashboard.spec.ts`
  - **Change:** Create first real-browser E2E from registration through dashboard and logout.
  - **File-level acceptance:** Exact production-like web composition is used.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I08-S04 — Access-cluster integration

**Stage outcome:** M01/M03/M06/M07/M20 operate as one capability.

**Tasks:**

- [ ] **`I08-S04-T01`**
  - **File:** `tests/integration/clusters/access/test_access_cluster.py`
  - **Change:** Boot real backend modules and PostgreSQL with deterministic policy/workflow fakes.
  - **File-level acceptance:** Registration, receipt, session, expiry, logout, and recovery pass.
- [ ] **`I08-S04-T02`**
  - **File:** `tests/integration/clusters/access/access-browser.spec.ts`
  - **Change:** Run real browser shell against access cluster.
  - **File-level acceptance:** Focus, history, refresh, offline, and stale-client scenarios pass.
- [ ] **`I08-S04-T03`**
  - **File:** `tests/security/test_authenticated_cache_isolation.py`
  - **Change:** Verify no-store headers, cache clearing on logout, and no service-worker interception.
  - **File-level acceptance:** Private identity data is absent from caches.
- [ ] **`I08-S04-T04`**
  - **File:** `tests/resilience/test_web_restart_access.py`
  - **Change:** Restart WEB between committed requests and resume session safely.
  - **File-level acceptance:** No duplicate registration or receipt occurs.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I08 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete M01 and M06 independent suites plus all M07 regressions.
- Run real access-cluster backend/browser tests with PostgreSQL, process restart, two tabs, timeout, stale revision, and incompatible client.
- Run accessibility, cache isolation, CSRF/origin/host, IDOR, and leakage suites.
- Build and inspect the WEB role dependency graph and browser bundle.
- Run all previous iteration gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I08 exit criteria

- The first authenticated vertical slice works from browser through durable state.
- Client timeouts, conflicts, stale versions, and logout cannot corrupt or retain private state.
- The shell composes modules without owning domain rules.
- Access cluster passes from a clean production-like build.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I09 — Case content compiler, publication trust, and Academy fixture framework

**Objective:** Implement M10 and the publication subset of M20 so signed immutable case packages can be built, validated, activated, quarantined, and rolled back.

**Principal modules:** M10, M20, M03, M04

**Principal interactions:** I05, I16, I17

**Prerequisites:**

- I08 is closed.

**Iteration outputs:**

- `I09-S01` — Case package contracts: Case content and rules are registry-driven.
- `I09-S02` — Hermetic publication compiler: Identical inputs produce identical signed package digests.
- `I09-S03` — Trust and active pointers: Only trusted compatible publications can start new rounds.
- `I09-S04` — Academy fixture framework: Create one minimal deterministic case package used by later engine work.

### I09-S01 — Case package contracts

**Stage outcome:** Case content and rules are registry-driven.

**Tasks:**

- [ ] **`I09-S01-T01`**
  - **File:** `modules/m10-case-content-rules/contracts/case-manifest.schema.json`
  - **Change:** Define case identity, family, order, profiles, versions, actions, economy, scoring references, assets, warnings, and publication metadata.
  - **File-level acceptance:** Incomplete package fixtures fail.
- [ ] **`I09-S01-T02`**
  - **File:** `modules/m10-case-content-rules/contracts/safe-record.schema.json`
  - **Change:** Define player-safe record, document, event, and relationship schemas without protected fields.
  - **File-level acceptance:** Truth-field negative fixtures fail.
- [ ] **`I09-S01-T03`**
  - **File:** `modules/m10-case-content-rules/contracts/evaluator-bundle.schema.json`
  - **Change:** Define protected evaluator package contract for private publication only.
  - **File-level acceptance:** Public package cannot reference private path.
- [ ] **`I09-S01-T04`**
  - **File:** `modules/m10-case-content-rules/backend/src/fga_cases/manifest.py`
  - **Change:** Implement typed manifest loading and compatibility validation.
  - **File-level acceptance:** Unit/property tests cover profile cumulative rules.
- [ ] **`I09-S01-T05`**
  - **File:** `modules/m10-case-content-rules/testkit/src/fga_cases_testkit/builders.py`
  - **Change:** Provide minimal valid/invalid case package builders.
  - **File-level acceptance:** Other modules can test without production cases.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I09-S02 — Hermetic publication compiler

**Stage outcome:** Identical inputs produce identical signed package digests.

**Tasks:**

- [ ] **`I09-S02-T01`**
  - **File:** `tools/case_compiler/main.py`
  - **Change:** Implement pinned-locale/timezone/seed ordered compilation from authoring inputs.
  - **File-level acceptance:** Two clean builds produce identical outputs.
- [ ] **`I09-S02-T02`**
  - **File:** `tools/case_compiler/canonicalizer.py`
  - **Change:** Canonicalize records, relationships, assets, manifests, and evidence object ordering.
  - **File-level acceptance:** Merkle-root golden test passes.
- [ ] **`I09-S02-T03`**
  - **File:** `tools/case_compiler/validators.py`
  - **Change:** Run schema, referential, temporal, profile, leakage, asset, licensing, and solvability hooks.
  - **File-level acceptance:** Each deliberate defect blocks publication.
- [ ] **`I09-S02-T04`**
  - **File:** `schemas/publication/publication-record.schema.json`
  - **Change:** Define hermetic build inputs, toolchain, seed, source-date epoch, digests, nondeterminism inventory, and approvals.
  - **File-level acceptance:** Schema validation passes.
- [ ] **`I09-S02-T05`**
  - **File:** `docs/cases/CASE_AUTHORING_GUIDE.md`
  - **Change:** Document package structure, safe/protected zones, profiles, fixtures, and publication gate.
  - **File-level acceptance:** Guide references all M10 contracts.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I09-S03 — Trust and active pointers

**Stage outcome:** Only trusted compatible publications can start new rounds.

**Tasks:**

- [ ] **`I09-S03-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/publication.py`
  - **Change:** Implement build/validate/sign/stage/publish/quarantine/retire/rollback state machine.
  - **File-level acceptance:** Model tests cover all transitions.
- [ ] **`I09-S03-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/migrations/0002_publication.sql`
  - **Change:** Create publication, signature, revocation, pointer, verifier-policy, and anti-downgrade tables.
  - **File-level acceptance:** Migration/grant tests pass.
- [ ] **`I09-S03-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/verifier.py`
  - **Change:** Verify digest, signer, workflow/source, freshness, compatibility, revocation, and downgrade floor.
  - **File-level acceptance:** Tampered, stale, unknown-signer, and revoked fixtures fail.
- [ ] **`I09-S03-T04`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/publication-status.schema.json`
  - **Change:** Define player-safe availability/quarantine/rollback projection.
  - **File-level acceptance:** No protected location or signer secret is exposed.
- [ ] **`I09-S03-T05`**
  - **File:** `tests/integration/pairs/I16-case-publication.py`
  - **Change:** Run real M10 compiler/loader with M20 activation and rollback.
  - **File-level acceptance:** Historical package remains addressable.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I09-S04 — Academy fixture framework

**Stage outcome:** Create one minimal deterministic case package used by later engine work.

**Tasks:**

- [ ] **`I09-S04-T01`**
  - **File:** `cases/academy/T01/case.yaml`
  - **Change:** Create T1 metadata, profiles, warnings, actions, and version references.
  - **File-level acceptance:** Case manifest validates.
- [ ] **`I09-S04-T02`**
  - **File:** `cases/academy/T01/player-safe.json`
  - **Change:** Create minimal legitimate-case starting records and direct relationships.
  - **File-level acceptance:** Safe schema and leakage scan pass.
- [ ] **`I09-S04-T03`**
  - **File:** `cases/academy/T01/truth.json`
  - **Change:** Create protected clean-closure truth and evaluator expectations.
  - **File-level acceptance:** File is excluded from WEB artifacts.
- [ ] **`I09-S04-T04`**
  - **File:** `cases/academy/T01/assets.json`
  - **Change:** Bind placeholder opening/closure assets and transcripts.
  - **File-level acceptance:** M04 manifest validation passes.
- [ ] **`I09-S04-T05`**
  - **File:** `tests/cases/test_t01_publication.py`
  - **Change:** Compile twice, sign, activate, quarantine, rollback, and compare digests.
  - **File-level acceptance:** All publication lifecycle steps pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I09 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete M10 and M20 publication independent suites, schema and hermetic reproducibility tests.
- Run pairwise M10↔M20, M10↔M03, and M10↔M04 integration.
- Run hidden-truth scans across public package, WEB dependencies, browser bundle, logs, and generated docs.
- Run signature, revocation, freshness, quarantine, rollback, and anti-downgrade negatives.
- Run full cumulative regression.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I09 exit criteria

- A minimal case package is reproducibly built and signed.
- Only trusted compatible packages can become active.
- Protected evaluator content is absent from WEB/public artifacts.
- M10 and publication trust are independently and pairwise qualified.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I10 — Career, catalogue, and progression eligibility foundation

**Objective:** Implement M08 catalogue and career creation using published case availability, without evaluation-driven progression yet.

**Principal modules:** M08, M01, M10, M20

**Principal interactions:** I02, I05

**Prerequisites:**

- I09 is closed.

**Iteration outputs:**

- `I10-S01` — Career domain: Multiple immutable-entry careers coexist safely.
- `I10-S02` — Catalogue projection: Card state is derived from career and publication facts.
- `I10-S03` — Shell integration: Dashboard and routes use career public contracts.
- `I10-S04` — Catalogue cluster: Access, publication, and career combine in real browser flow.

### I10-S01 — Career domain

**Stage outcome:** Multiple immutable-entry careers coexist safely.

**Tasks:**

- [ ] **`I10-S01-T01`**
  - **File:** `modules/m08-career-catalogue-progression/contracts/career.schema.json`
  - **Change:** Define career, entry tier, path, case progress, default resume pointer, and availability reasons.
  - **File-level acceptance:** Schema distinguishes state from availability.
- [ ] **`I10-S01-T02`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/domain/career.py`
  - **Change:** Implement career creation, archive/restore, fixed path, family presentation, and default pointer rules.
  - **File-level acceptance:** Property tests prove one career never mutates another.
- [ ] **`I10-S01-T03`**
  - **File:** `modules/m08-career-catalogue-progression/backend/migrations/0001_career.sql`
  - **Change:** Create careers, progress, events, and account default pointer.
  - **File-level acceptance:** Migration and ownership tests pass.
- [ ] **`I10-S01-T04`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/repository.py`
  - **Change:** Implement owner-scoped career persistence.
  - **File-level acceptance:** Cross-account IDOR tests pass.
- [ ] **`I10-S01-T05`**
  - **File:** `modules/m08-career-catalogue-progression/testkit/src/fga_career_testkit/builders.py`
  - **Change:** Provide career/path/availability builders for consumers.
  - **File-level acceptance:** M09 can test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I10-S02 — Catalogue projection

**Stage outcome:** Card state is derived from career and publication facts.

**Tasks:**

- [ ] **`I10-S02-T01`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/catalogue.py`
  - **Change:** Implement section catalogue, OPEN/CLOSED/LOCKED state, and independent availability reasons.
  - **File-level acceptance:** Decision-table tests cover every reason.
- [ ] **`I10-S02-T02`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/http.py`
  - **Change:** Expose dashboard, catalogue, career create/read/archive/resume endpoints.
  - **File-level acceptance:** OpenAPI contract tests pass.
- [ ] **`I10-S02-T03`**
  - **File:** `modules/m08-career-catalogue-progression/frontend/src/SectionSelector.tsx`
  - **Change:** Implement four equal-status accessible section choices.
  - **File-level acceptance:** Pointer, keyboard, touch, and screen-reader tests pass.
- [ ] **`I10-S02-T04`**
  - **File:** `modules/m08-career-catalogue-progression/frontend/src/CaseCatalogue.tsx`
  - **Change:** Render all cards with primary state, reason, and valid action.
  - **File-level acceptance:** State is not color-only.
- [ ] **`I10-S02-T05`**
  - **File:** `modules/m08-career-catalogue-progression/frontend/src/NewCareerDialog.tsx`
  - **Change:** Implement entry-tier/path confirmation without destructive replacement.
  - **File-level acceptance:** Multiple-career E2E passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I10-S03 — Shell integration

**Stage outcome:** Dashboard and routes use career public contracts.

**Tasks:**

- [ ] **`I10-S03-T01`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/Dashboard.tsx`
  - **Change:** Replace placeholders with M08 career summaries and section navigation.
  - **File-level acceptance:** No direct M08 internal import.
- [ ] **`I10-S03-T02`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/router.tsx`
  - **Change:** Add catalogue, career, and planned round routes with safe guards.
  - **File-level acceptance:** Unavailable case deep links fail safely.
- [ ] **`I10-S03-T03`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add career, catalogue, states, availability, and confirmation messages.
  - **File-level acceptance:** Message completeness passes.
- [ ] **`I10-S03-T04`**
  - **File:** `tests/integration/pairs/I05-career-publication.py`
  - **Change:** Run M08 against real M10/M20 active and quarantined publications.
  - **File-level acceptance:** Availability reacts correctly without mutating careers.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I10-S04 — Catalogue cluster

**Stage outcome:** Access, publication, and career combine in real browser flow.

**Tasks:**

- [ ] **`I10-S04-T01`**
  - **File:** `tests/integration/clusters/catalogue/test_catalogue_cluster.py`
  - **Change:** Boot M07/M08/M10/M20 with real DB and publication pointer.
  - **File-level acceptance:** Multiple careers and all availability reasons pass.
- [ ] **`I10-S04-T02`**
  - **File:** `tests/integration/clusters/catalogue/catalogue-browser.spec.ts`
  - **Change:** Exercise section selection, new career, archive/restore, and deep links.
  - **File-level acceptance:** Accessibility and history pass.
- [ ] **`I10-S04-T03`**
  - **File:** `tests/concurrency/test_career_creation.py`
  - **Change:** Race duplicate idempotency keys and simultaneous independent career creation.
  - **File-level acceptance:** No duplicate or destructive replacement occurs.
- [ ] **`I10-S04-T04`**
  - **File:** `tests/resilience/test_catalogue_publication_change.py`
  - **Change:** Quarantine publication during browsing and refresh safely.
  - **File-level acceptance:** New starts close; historical data remains.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I10 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M08 module suites and M01 affected regressions.
- Run M08↔M07/M10/M20 pairwise tests and catalogue cluster with real PostgreSQL/browser.
- Run ownership, concurrency, idempotency, publication-change, and accessibility tests.
- Run all previous cumulative suites and scans.
- Build exact WEB artifact and execute registration → dashboard → new career → catalogue journey.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I10 exit criteria

- Multiple named careers coexist and fixed paths are immutable.
- Catalogue state and availability are correctly separated.
- Quarantined/unpublished packages cannot be started.
- Catalogue cluster passes end to end.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I11 — Round engine, immutable bindings, and starting investigation

**Objective:** Implement M09 round lifecycle and immutable version binding, then open T1 with starting evidence.

**Principal modules:** M09, M08, M10, M11 bootstrap, M20

**Principal interactions:** I06, I07

**Prerequisites:**

- I10 is closed.

**Iteration outputs:**

- `I11-S01` — Round domain and bindings: A round binds every gameplay-affecting version at creation.
- `I11-S02` — Eligibility and initialization: Career and publication facts create exactly one valid round.
- `I11-S03` — Starting evidence grant: T1 becomes a real minimal investigation.
- `I11-S04` — First playable route: A player can start and inspect the minimal round shell.

### I11-S01 — Round domain and bindings

**Stage outcome:** A round binds every gameplay-affecting version at creation.

**Tasks:**

- [ ] **`I11-S01-T01`**
  - **File:** `modules/m09-round-game-state/contracts/round.schema.json`
  - **Change:** Define round identity, mode, lifecycle, immutable bindings, profile, as_of_time, provider mode, ranking segment, and revisions.
  - **File-level acceptance:** Schema requires all normative bindings.
- [ ] **`I11-S01-T02`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/domain/round.py`
  - **Change:** Implement CREATED, ACTIVE, pending, CLOSED, ABANDONED, EXPIRED, and RECOVERY_REQUIRED transitions.
  - **File-level acceptance:** Model/property tests reject illegal transitions.
- [ ] **`I11-S01-T03`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/domain/bindings.py`
  - **Change:** Implement immutable binding creation and canonical digest.
  - **File-level acceptance:** Mutation after creation fails.
- [ ] **`I11-S01-T04`**
  - **File:** `modules/m09-round-game-state/backend/migrations/0001_rounds.sql`
  - **Change:** Create rounds, binding, and event-history tables with immutability constraints.
  - **File-level acceptance:** Database update attempt on binding columns fails.
- [ ] **`I11-S01-T05`**
  - **File:** `modules/m09-round-game-state/testkit/src/fga_rounds_testkit/builders.py`
  - **Change:** Provide valid round and binding builders.
  - **File-level acceptance:** M11/M13/M15/M16 consumers run independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I11-S02 — Eligibility and initialization

**Stage outcome:** Career and publication facts create exactly one valid round.

**Tasks:**

- [ ] **`I11-S02-T01`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/create_round.py`
  - **Change:** Implement owner, career, case availability, mode, policy, publication, and capability checks.
  - **File-level acceptance:** Decision-table tests cover ranked/practice/academy.
- [ ] **`I11-S02-T02`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/start_round.py`
  - **Change:** Transition CREATED to ACTIVE and invoke starting-evidence participant once.
  - **File-level acceptance:** Idempotent retry returns same state.
- [ ] **`I11-S02-T03`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/http.py`
  - **Change:** Expose create, read, start, abandon, bindings, and workspace bootstrap endpoints.
  - **File-level acceptance:** Contract tests pass.
- [ ] **`I11-S02-T04`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/catalogue.py`
  - **Change:** Expose round-eligibility query and active-round availability reason.
  - **File-level acceptance:** Duplicate ranked start is blocked.
- [ ] **`I11-S02-T05`**
  - **File:** `tests/integration/pairs/I06-round-creation.py`
  - **Change:** Run real M09 with M08/M10/M20 and M11 fake participant.
  - **File-level acceptance:** Atomic binding and initialization pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I11-S03 — Starting evidence grant

**Stage outcome:** T1 becomes a real minimal investigation.

**Tasks:**

- [ ] **`I11-S03-T01`**
  - **File:** `modules/m11-investigation-visibility/contracts/starting-evidence.schema.json`
  - **Change:** Define records/documents/direct relationships granted at initialization.
  - **File-level acceptance:** Contract excludes analytical/truth metadata.
- [ ] **`I11-S03-T02`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/starting_evidence.py`
  - **Change:** Implement idempotent grant under round/case policy.
  - **File-level acceptance:** Repeated start creates no duplicate visibility rows.
- [ ] **`I11-S03-T03`**
  - **File:** `modules/m11-investigation-visibility/backend/migrations/0001_visibility.sql`
  - **Change:** Create revealed record/document/relationship and event tables.
  - **File-level acceptance:** Unique constraints enforce one grant.
- [ ] **`I11-S03-T04`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/start_round.py`
  - **Change:** Connect M11 starting-evidence public participant through UnitOfWorkPort.
  - **File-level acceptance:** Partial failure rolls back both modules.
- [ ] **`I11-S03-T05`**
  - **File:** `tests/integration/pairs/I07-round-visibility.py`
  - **Change:** Run real M09 and M11 using T1 publication.
  - **File-level acceptance:** Starting set matches signed package exactly.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I11-S04 — First playable route

**Stage outcome:** A player can start and inspect the minimal round shell.

**Tasks:**

- [ ] **`I11-S04-T01`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/router.tsx`
  - **Change:** Enable opening, briefing, and investigate routes for active rounds.
  - **File-level acceptance:** Route guard uses M09 public status.
- [ ] **`I11-S04-T02`**
  - **File:** `modules/m09-round-game-state/frontend/src/RoundOpening.tsx`
  - **Change:** Render opening notice, case/profile/mode, and accessible transcript path.
  - **File-level acceptance:** No hidden binding fields are shown.
- [ ] **`I11-S04-T03`**
  - **File:** `modules/m09-round-game-state/frontend/src/RoundBriefing.tsx`
  - **Change:** Render fictionalization, warnings, objectives, and start action.
  - **File-level acceptance:** Keyboard flow passes.
- [ ] **`I11-S04-T04`**
  - **File:** `tests/e2e/t01-start-round.spec.ts`
  - **Change:** Create account/career, start T1, refresh, and verify immutable bindings/starting evidence.
  - **File-level acceptance:** Journey passes after WEB restart.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I11 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run M09 full independent suites and M11 starting-evidence subset.
- Run M09↔M08/M10/M20 and M09↔M11 pairwise tests with stale publication, duplicate start, concurrent tabs, crash, and rollback.
- Run catalogue-cluster regression plus new round-start E2E against production-like WEB.
- Run database immutability, ownership, IDOR, temporal binding, and hidden-field scans.
- Run all earlier cumulative gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I11 exit criteria

- Round lifecycle and immutable bindings are durable and mutation-proof.
- T1 starts exactly once with the signed starting evidence.
- Practice/Academy/ranked eligibility is explicit.
- Round creation and initialization survive retries, crashes, and two tabs.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I12 — Investigation visibility and manual hypotheses

**Objective:** Complete M11 core visibility state, provenance, selections, and the free manual relationship action.

**Principal modules:** M11, M09, M10, M12 contract, M13 manual contract

**Principal interactions:** I07

**Prerequisites:**

- I11 is closed.

**Iteration outputs:**

- `I12-S01` — Visibility aggregate: All revealed investigation objects share one authoritative state.
- `I12-S02` — Selection and prerequisite rules: Actions operate only on compatible visible objects.
- `I12-S03` — Manual hypotheses: The player can create editable theories without promoting them to facts.
- `I12-S04` — Visibility integration: The first real investigation state is inspectable and mutable only through M11.

### I12-S01 — Visibility aggregate

**Stage outcome:** All revealed investigation objects share one authoritative state.

**Tasks:**

- [ ] **`I12-S01-T01`**
  - **File:** `modules/m11-investigation-visibility/contracts/revealed-state.schema.json`
  - **Change:** Define visible records, documents, direct/analytical relationships, provenance, and revision.
  - **File-level acceptance:** Schema distinguishes relationship families.
- [ ] **`I12-S01-T02`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/domain/visibility.py`
  - **Change:** Implement monotonic grant rules and visibility revision.
  - **File-level acceptance:** Property tests prove no ranked unreveal operation exists.
- [ ] **`I12-S01-T03`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/repository.py`
  - **Change:** Implement safe owner/round-scoped reads and writes.
  - **File-level acceptance:** Cross-round and cross-owner access fails.
- [ ] **`I12-S01-T04`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/provenance.py`
  - **Change:** Normalize source, command, publication, generator, and reveal provenance.
  - **File-level acceptance:** No protected purpose field leaks.
- [ ] **`I12-S01-T05`**
  - **File:** `modules/m11-investigation-visibility/testkit/src/fga_investigation_testkit/builders.py`
  - **Change:** Provide revealed-state and selection builders.
  - **File-level acceptance:** M12/M13 can test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I12-S02 — Selection and prerequisite rules

**Stage outcome:** Actions operate only on compatible visible objects.

**Tasks:**

- [ ] **`I12-S02-T01`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/selection.py`
  - **Change:** Implement selection caps, compatible types, visibility checks, and canonical ordering.
  - **File-level acceptance:** Boundary/property tests pass.
- [ ] **`I12-S02-T02`**
  - **File:** `modules/m11-investigation-visibility/contracts/selection.schema.json`
  - **Change:** Define selected safe IDs, revision, purpose, and validation result.
  - **File-level acceptance:** Stale or duplicate ID fixtures are normalized/rejected per contract.
- [ ] **`I12-S02-T03`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/query.py`
  - **Change:** Expose player-safe visible-state and selection-validation ports.
  - **File-level acceptance:** Response contains no unrevealed object count.
- [ ] **`I12-S02-T04`**
  - **File:** `tests/security/test_visibility_noninterference.py`
  - **Change:** Compare pre-reveal responses across hidden datasets with identical visible input.
  - **File-level acceptance:** Status, size class, and errors are indistinguishable.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I12-S03 — Manual hypotheses

**Stage outcome:** The player can create editable theories without promoting them to facts.

**Tasks:**

- [ ] **`I12-S03-T01`**
  - **File:** `modules/m11-investigation-visibility/contracts/manual-hypothesis.schema.json`
  - **Change:** Define endpoints, controlled type, uncertainty, note, revision, and player-created provenance.
  - **File-level acceptance:** Schema blocks protected/system relationship types.
- [ ] **`I12-S03-T02`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/manual_hypotheses.py`
  - **Change:** Implement create/update/delete with audit and optimistic concurrency.
  - **File-level acceptance:** Concurrent edits produce typed conflict.
- [ ] **`I12-S03-T03`**
  - **File:** `modules/m11-investigation-visibility/frontend/src/ManualHypothesisEditor.tsx`
  - **Change:** Implement accessible endpoint/type/uncertainty/note editor.
  - **File-level acceptance:** Keyboard and validation tests pass.
- [ ] **`I12-S03-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add investigation, provenance, selection, and hypothesis messages.
  - **File-level acceptance:** Catalogue checks pass.
- [ ] **`I12-S03-T05`**
  - **File:** `tests/integration/pairs/manual-hypothesis-round.py`
  - **Change:** Run real M11 with M09 active/closed/recovery states.
  - **File-level acceptance:** Only ACTIVE rounds allow edits.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I12-S04 — Visibility integration

**Stage outcome:** The first real investigation state is inspectable and mutable only through M11.

**Tasks:**

- [ ] **`I12-S04-T01`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/workspace.py`
  - **Change:** Expose M11 visible-state reference through the round public query.
  - **File-level acceptance:** M09 does not query M11 tables.
- [ ] **`I12-S04-T02`**
  - **File:** `tests/integration/clusters/investigation/test_visibility_core.py`
  - **Change:** Boot M09/M10/M11/M20 with T1 and real DB.
  - **File-level acceptance:** Starting evidence, selection, manual hypothesis, refresh, and owner isolation pass.
- [ ] **`I12-S04-T03`**
  - **File:** `tests/concurrency/test_manual_hypothesis_conflicts.py`
  - **Change:** Race create/update/delete from two tabs.
  - **File-level acceptance:** Revision rules preserve one authoritative result.
- [ ] **`I12-S04-T04`**
  - **File:** `tests/security/test_visibility_table_isolation.py`
  - **Change:** Attempt direct cross-module repository/table access.
  - **File-level acceptance:** Architecture and DB grants block it.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I12 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M11 unit/property/contract/component/architecture/security/concurrency suites.
- Run M11↔M09/M10 and manual-hypothesis pairwise tests.
- Run investigation-cluster core with real DB, two tabs, restart, stale revision, and hidden-data differential tests.
- Run cumulative access/catalogue/round regressions and all scans.
- Mutation-test the monotonic grant and authorization checks.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I12 exit criteria

- Visible investigation state is authoritative, monotonic, and provenance-complete.
- Manual hypotheses remain visibly player-owned and editable without becoming facts.
- Selections cannot name hidden, incompatible, cross-round, or cross-owner objects.
- Pre-reveal behavior passes noninterference tests.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I13 — Workspace list, document inspection, and read-model projection

**Objective:** Implement M12 list and document projections from M11 without adding independent gameplay state.

**Principal modules:** M12, M11, M02, M03, M04

**Principal interactions:** I08

**Prerequisites:**

- I12 is closed.

**Iteration outputs:**

- `I13-S01` — Projection contracts: M12 projects one revealed state into bounded list/document views.
- `I13-S02` — List workspace UI: The precision workspace is fully keyboard and screen-reader operable.
- `I13-S03` — Workspace composition: The investigate route becomes a usable list-first screen.
- `I13-S04` — Projection parity and safety: Projection cannot reveal more than M11.

### I13-S01 — Projection contracts

**Stage outcome:** M12 projects one revealed state into bounded list/document views.

**Tasks:**

- [ ] **`I13-S01-T01`**
  - **File:** `modules/m12-workspace-projection/contracts/workspace.schema.json`
  - **Change:** Define projection revision, records, columns, selection, filters, sort, groups, documents, provenance, and counts.
  - **File-level acceptance:** Schema contains only M11-visible objects.
- [ ] **`I13-S01-T02`**
  - **File:** `modules/m12-workspace-projection/backend/src/fga_workspace/list_projection.py`
  - **Change:** Implement safe columns, stable pagination, five-key sort, nulls-last, filters, and safe-ID ties.
  - **File-level acceptance:** Property tests prove deterministic order.
- [ ] **`I13-S01-T03`**
  - **File:** `modules/m12-workspace-projection/backend/src/fga_workspace/document_projection.py`
  - **Change:** Implement safe document metadata/content/fallback projection.
  - **File-level acceptance:** Active content and external URL fields are absent.
- [ ] **`I13-S01-T04`**
  - **File:** `modules/m12-workspace-projection/backend/src/fga_workspace/query.py`
  - **Change:** Compose projections solely through M11/M10 public queries.
  - **File-level acceptance:** Architecture test blocks direct table access.
- [ ] **`I13-S01-T05`**
  - **File:** `modules/m12-workspace-projection/testkit/src/fga_workspace_testkit/builders.py`
  - **Change:** Provide dense, Unicode, missing, and mixed-type projections.
  - **File-level acceptance:** Frontend tests need no backend.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I13-S02 — List workspace UI

**Stage outcome:** The precision workspace is fully keyboard and screen-reader operable.

**Tasks:**

- [ ] **`I13-S02-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ListWorkspace.tsx`
  - **Change:** Render paginated records, columns, sorting, filtering, grouping, and synchronized selection.
  - **File-level acceptance:** Keyboard and accessible table tests pass.
- [ ] **`I13-S02-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ColumnManager.tsx`
  - **Change:** Implement add/remove/reorder/reset approved columns.
  - **File-level acceptance:** No hidden column can be requested.
- [ ] **`I13-S02-T03`**
  - **File:** `modules/m12-workspace-projection/frontend/src/SelectionSummary.tsx`
  - **Change:** Render selected IDs/types and clear/save subset actions.
  - **File-level acceptance:** Selection state maps to M11 safe IDs.
- [ ] **`I13-S02-T04`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ProvenancePanel.tsx`
  - **Change:** Render textual source/reveal/generator provenance and warnings.
  - **File-level acceptance:** No guilt or hidden-purpose inference appears.
- [ ] **`I13-S02-T05`**
  - **File:** `modules/m12-workspace-projection/frontend/src/DocumentInspector.tsx`
  - **Change:** Render safe document, transcript, unavailable, and failure states.
  - **File-level acceptance:** Sandbox and accessibility tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I13-S03 — Workspace composition

**Stage outcome:** The investigate route becomes a usable list-first screen.

**Tasks:**

- [ ] **`I13-S03-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/InvestigationWorkspace.tsx`
  - **Change:** Compose header, credits placeholder, list, document, action placeholders, case-file placeholder, legend, and status.
  - **File-level acceptance:** Layout reflows at 320 CSS px.
- [ ] **`I13-S03-T02`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/router.tsx`
  - **Change:** Load M12 workspace on active investigation route.
  - **File-level acceptance:** Closed/recovery states route safely.
- [ ] **`I13-S03-T03`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add workspace, list, document, provenance, sorting, filtering, and empty-state messages.
  - **File-level acceptance:** Catalogue checks pass.
- [ ] **`I13-S03-T04`**
  - **File:** `tests/e2e/t01-list-investigation.spec.ts`
  - **Change:** Inspect T1 records, sort/filter/select, open document, refresh, and create hypothesis.
  - **File-level acceptance:** State remains consistent.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I13-S04 — Projection parity and safety

**Stage outcome:** Projection cannot reveal more than M11.

**Tasks:**

- [ ] **`I13-S04-T01`**
  - **File:** `tests/integration/pairs/I08-workspace-investigation.py`
  - **Change:** Run real M12 backend with M11 visible-state changes.
  - **File-level acceptance:** Every projection object is authorized by M11.
- [ ] **`I13-S04-T02`**
  - **File:** `tests/property/test_list_sorting.py`
  - **Change:** Generate mixed Unicode/null/date/decimal records and verify stable sort/pagination.
  - **File-level acceptance:** No duplicate/missing row across pages.
- [ ] **`I13-S04-T03`**
  - **File:** `tests/security/test_document_sandbox.py`
  - **Change:** Load malicious PDF/HTML/URL fixtures through inspector.
  - **File-level acceptance:** No script, external fetch, or credential access occurs.
- [ ] **`I13-S04-T04`**
  - **File:** `tests/accessibility/list-workspace.spec.ts`
  - **Change:** Run table navigation, filter announcements, reflow, zoom, contrast, and document alternatives.
  - **File-level acceptance:** All critical tasks complete without graph.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I13 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete M12 list/document independent suites and M11 regressions.
- Run M12↔M11/M10/M03/M04 pairwise tests.
- Run list sorting/filtering property tests, document security sandbox, accessibility, and browser E2E.
- Run investigation cluster with real DB and production-like WEB.
- Run all cumulative gates and leakage scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I13 exit criteria

- The list workspace supports all implemented investigation tasks accessibly.
- Projection is deterministic, bounded, and contains only authorized visible objects.
- Documents fail safely and have accessible alternatives.
- M12 remains a read-model/UI module with no gameplay authority.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I14 — Graph visualization, semantic navigation, and list/graph parity

**Objective:** Complete M12 with graph, legend, overview, semantic navigator, and exact equivalence to the list projection.

**Principal modules:** M12, M11, M02, M04

**Principal interactions:** I08

**Prerequisites:**

- I13 is closed.

**Iteration outputs:**

- `I14-S01` — Graph projection: Nodes and edges derive deterministically from visible state.
- `I14-S02` — Visual graph and legend: The graph communicates type and relationship without color-only meaning.
- `I14-S03` — Semantic graph navigator: Every graph-critical task has a noncanvas path.
- `I14-S04` — Parity, performance, and accessibility: List, graph, documents, and semantic navigation expose the same investigation.

### I14-S01 — Graph projection

**Stage outcome:** Nodes and edges derive deterministically from visible state.

**Tasks:**

- [ ] **`I14-S01-T01`**
  - **File:** `modules/m12-workspace-projection/contracts/graph.schema.json`
  - **Change:** Define node, edge, family, direction, style token, label, counts, and bounded layout hints.
  - **File-level acceptance:** Schema forbids guilt/culpability visual fields.
- [ ] **`I14-S01-T02`**
  - **File:** `modules/m12-workspace-projection/backend/src/fga_workspace/graph_projection.py`
  - **Change:** Implement bounded graph projection and stable IDs from M11 state.
  - **File-level acceptance:** Node/edge set equals list-visible relationship state.
- [ ] **`I14-S01-T03`**
  - **File:** `modules/m12-workspace-projection/backend/src/fga_workspace/graph_limits.py`
  - **Change:** Implement case/profile caps, truncation-safe subset rules, and player-safe notices.
  - **File-level acceptance:** Cap behavior cannot reveal hidden total cardinality.
- [ ] **`I14-S01-T04`**
  - **File:** `modules/m12-workspace-projection/testkit/src/fga_workspace_testkit/graphFixtures.ts`
  - **Change:** Provide cycles, disconnected components, dense hubs, bidi labels, and missing icons.
  - **File-level acceptance:** Graph UI tests are deterministic.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I14-S02 — Visual graph and legend

**Stage outcome:** The graph communicates type and relationship without color-only meaning.

**Tasks:**

- [ ] **`I14-S02-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/GraphWorkspace.tsx`
  - **Change:** Implement Cytoscape adapter, pan/zoom/fit/reset, selection, details, and bounded layouts.
  - **File-level acceptance:** Listener cleanup and memory tests pass.
- [ ] **`I14-S02-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/RelationshipLegend.tsx`
  - **Change:** Render textual family labels, line patterns, counts, and provenance help.
  - **File-level acceptance:** All styles remain distinguishable in forced colors.
- [ ] **`I14-S02-T03`**
  - **File:** `modules/m12-workspace-projection/frontend/src/GraphOverview.tsx`
  - **Change:** Implement project-owned overview/minimap with accessible status.
  - **File-level acceptance:** No abandoned plugin dependency is introduced.
- [ ] **`I14-S02-T04`**
  - **File:** `modules/m12-workspace-projection/frontend/src/NodeIcon.tsx`
  - **Change:** Resolve type icon/shape/text fallback through M04.
  - **File-level acceptance:** Missing icon preserves semantics.
- [ ] **`I14-S02-T05`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ViewSwitcher.tsx`
  - **Change:** Switch list/graph without cost, reveal, or selection loss.
  - **File-level acceptance:** State parity tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I14-S03 — Semantic graph navigator

**Stage outcome:** Every graph-critical task has a noncanvas path.

**Tasks:**

- [ ] **`I14-S03-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/SemanticGraphNavigator.tsx`
  - **Change:** Implement node sequence, neighbors, edge meaning, selection, and available actions.
  - **File-level acceptance:** Screen-reader-oriented journeys pass.
- [ ] **`I14-S03-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ExplainCurrentView.tsx`
  - **Change:** Summarize filters, hidden-by-filter counts, selection, visible types, and provenance.
  - **File-level acceptance:** Announcement is concise and complete.
- [ ] **`I14-S03-T03`**
  - **File:** `modules/m12-workspace-projection/frontend/src/GraphDetails.tsx`
  - **Change:** Render node/edge textual details and direction without relying on hover.
  - **File-level acceptance:** Keyboard-only use passes.
- [ ] **`I14-S03-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add graph, relationship, navigator, overview, and parity messages.
  - **File-level acceptance:** Catalogue checks pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I14-S04 — Parity, performance, and accessibility

**Stage outcome:** List, graph, documents, and semantic navigation expose the same investigation.

**Tasks:**

- [ ] **`I14-S04-T01`**
  - **File:** `tests/property/test_list_graph_parity.py`
  - **Change:** Generate visible states and compare list IDs, graph nodes/edges, selection, and provenance.
  - **File-level acceptance:** All generated cases match.
- [ ] **`I14-S04-T02`**
  - **File:** `tests/accessibility/semantic-graph.spec.ts`
  - **Change:** Complete inspect/select/navigate relationship tasks without canvas manipulation.
  - **File-level acceptance:** All critical tasks pass.
- [ ] **`I14-S04-T03`**
  - **File:** `tests/performance/graph-budget.spec.ts`
  - **Change:** Measure bounded Academy and dense-fixture render/update/memory budgets.
  - **File-level acceptance:** Budgets meet configured thresholds.
- [ ] **`I14-S04-T04`**
  - **File:** `tests/e2e/t01-view-parity.spec.ts`
  - **Change:** Switch repeatedly among list, graph, semantic navigator, and documents through refresh.
  - **File-level acceptance:** No state or reveal drift occurs.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I14 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M12 graph/semantic module tests, list regressions, property parity, memory/leak, and performance suites.
- Run M12↔M11/M04 pairwise tests with missing assets, dense graphs, cycles, and disconnected components.
- Run accessibility across keyboard, screen reader-oriented tree, zoom, reflow, contrast, reduced motion, and touch.
- Run investigation/media cluster cumulative tests and browser E2E.
- Run all previous gates and scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I14 exit criteria

- List, graph, documents, and semantic navigation are equivalent projections.
- Graph styling never silently encodes guilt and is not color-only.
- Dense bounded graphs meet performance and memory budgets.
- All graph-critical tasks are completable without direct canvas use.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I15 — Investigation economy and append-only credit ledger

**Objective:** Implement M14 exact fictional-credit accounting independently from real provider cost.

**Principal modules:** M14, M10, M20

**Principal interactions:** I09 participant, I12 participant

**Prerequisites:**

- I14 is closed.

**Iteration outputs:**

- `I15-S01` — Economy contracts and aggregate: Credits use exact append-only semantics.
- `I15-S02` — Policy and read model: Case rules determine budgets without client authority.
- `I15-S03` — Transaction participant: M14 participates atomically without exposing tables.
- `I15-S04` — Economy qualification: Credits are correct under failures and restarts.

### I15-S01 — Economy contracts and aggregate

**Stage outcome:** Credits use exact append-only semantics.

**Tasks:**

- [ ] **`I15-S01-T01`**
  - **File:** `modules/m14-economy-credit/contracts/economy.schema.json`
  - **Change:** Define budget, balance, quote cost, debit, refund, reason, command reference, and exact integer units.
  - **File-level acceptance:** Schema forbids currency fields and floating point.
- [ ] **`I15-S01-T02`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/domain/ledger.py`
  - **Change:** Implement append-only ledger entries and derived/materialized balance invariants.
  - **File-level acceptance:** Property tests prove conservation and nonnegative balance.
- [ ] **`I15-S01-T03`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/domain/settlement.py`
  - **Change:** Implement reserve/debit/refund uniqueness and command linkage.
  - **File-level acceptance:** Double debit/refund model tests fail.
- [ ] **`I15-S01-T04`**
  - **File:** `modules/m14-economy-credit/backend/migrations/0001_economy.sql`
  - **Change:** Create budgets, ledger, materialized balance, and reconciliation constraints.
  - **File-level acceptance:** Database constraints reject negative or duplicate settlement.
- [ ] **`I15-S01-T05`**
  - **File:** `modules/m14-economy-credit/testkit/src/fga_economy_testkit/builders.py`
  - **Change:** Provide balances, entries, failure points, and participant fake.
  - **File-level acceptance:** M13/M16 can test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I15-S02 — Policy and read model

**Stage outcome:** Case rules determine budgets without client authority.

**Tasks:**

- [ ] **`I15-S02-T01`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/policy.py`
  - **Change:** Resolve starting budget and action cost only from signed M10/M20 policy.
  - **File-level acceptance:** Client price field is ignored/rejected.
- [ ] **`I15-S02-T02`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/queries.py`
  - **Change:** Expose balance and player-safe ledger projection.
  - **File-level acceptance:** No provider currency/cost appears.
- [ ] **`I15-S02-T03`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/reconciliation.py`
  - **Change:** Compare ledger, balance, command references, and orphan states.
  - **File-level acceptance:** Deliberate corruption is detected.
- [ ] **`I15-S02-T04`**
  - **File:** `modules/m12-workspace-projection/frontend/src/CreditStatus.tsx`
  - **Change:** Replace credit placeholder with M14 balance and history access.
  - **File-level acceptance:** Zero balance remains operable.
- [ ] **`I15-S02-T05`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add fictional credit, ledger, debit/refund, and zero-credit messages.
  - **File-level acceptance:** No monetary symbol or exchange language is used.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I15-S03 — Transaction participant

**Stage outcome:** M14 participates atomically without exposing tables.

**Tasks:**

- [ ] **`I15-S03-T01`**
  - **File:** `modules/m14-economy-credit/backend/src/fga_economy/participant.py`
  - **Change:** Implement public debit/refund/snapshot participant ports under M20 UnitOfWork.
  - **File-level acceptance:** Rollback tests leave no ledger entry.
- [ ] **`I15-S03-T02`**
  - **File:** `tests/integration/pairs/I09-economy-command-fake.py`
  - **Change:** Run M14 real participant with synthetic M13 orchestrator.
  - **File-level acceptance:** Acceptance and settlement atomicity pass.
- [ ] **`I15-S03-T03`**
  - **File:** `tests/integration/pairs/I12-economy-submission-fake.py`
  - **Change:** Expose immutable economy snapshot for submission eligibility.
  - **File-level acceptance:** Snapshot is revision/digest bound.
- [ ] **`I15-S03-T04`**
  - **File:** `tests/concurrency/test_credit_ledger.py`
  - **Change:** Race debits, refunds, duplicate keys, and serialization retries.
  - **File-level acceptance:** Balance never goes negative or diverges.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I15-S04 — Economy qualification

**Stage outcome:** Credits are correct under failures and restarts.

**Tasks:**

- [ ] **`I15-S04-T01`**
  - **File:** `tests/property/test_ledger_model.py`
  - **Change:** Compare generated command/settlement sequences to a pure reference model.
  - **File-level acceptance:** All sequences conserve balance.
- [ ] **`I15-S04-T02`**
  - **File:** `tests/resilience/test_economy_crash_points.py`
  - **Change:** Crash before/after debit/refund commits and replay requests.
  - **File-level acceptance:** Exactly one economic outcome remains.
- [ ] **`I15-S04-T03`**
  - **File:** `tests/security/test_credit_tampering.py`
  - **Change:** Tamper client cost/balance/revision and attempt cross-owner ledger reads.
  - **File-level acceptance:** All attempts fail safely.
- [ ] **`I15-S04-T04`**
  - **File:** `tests/e2e/t01-zero-credit-shell.spec.ts`
  - **Change:** Use fixture to reach zero credits and verify reading/editing/submission placeholders remain enabled.
  - **File-level acceptance:** No negative balance or forced failure.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I15 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M14 unit/property/model/contract/component/architecture/security/concurrency suites.
- Run participant pairwise tests, ledger reconciliation, crash points, and DB constraint negatives.
- Run workspace credit display, zero-credit, owner isolation, and accessibility tests.
- Run investigation cluster cumulative regression and all earlier gates.
- Mutation-test exact arithmetic, nonnegative balance, and duplicate-settlement checks.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I15 exit criteria

- Investigation credits are exact, append-only, nonnegative, and command-linked.
- Real provider cost is absent from player economy contracts and UI.
- M14 participates atomically through public ports only.
- Crash, retry, concurrency, and tampering cannot duplicate or recover credits.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I16 — Quote, command, outbox, settlement, and reconciliation core

**Objective:** Implement M13 command lifecycle and its atomic collaborations with M14 and M11 before external retrieval is added.

**Principal modules:** M13, M14, M11, M09, M20

**Principal interactions:** I09, I10

**Prerequisites:**

- I15 is closed.

**Iteration outputs:**

- `I16-S01` — Quote and command domain: Every paid action follows one authoritative protocol.
- `I16-S02` — Atomic acceptance: Debit, command, idempotency, and outbox intent commit together.
- `I16-S03` — Durable dispatch and reconciliation: No accepted command depends on a web request remaining alive.
- `I16-S04` — Settlement and pre-reveal safety: Terminal status, economy, and visibility change atomically.

### I16-S01 — Quote and command domain

**Stage outcome:** Every paid action follows one authoritative protocol.

**Tasks:**

- [ ] **`I16-S01-T01`**
  - **File:** `modules/m13-action-command/contracts/quote.schema.json`
  - **Change:** Define normalized scope, cost, expiry, caps, warnings, versions, and hash.
  - **File-level acceptance:** Expired/mismatched quote fixtures fail.
- [ ] **`I16-S01-T02`**
  - **File:** `modules/m13-action-command/contracts/command.schema.json`
  - **Change:** Define command family, lifecycle, idempotency, fingerprint, economic state, provider state reference, and safe result.
  - **File-level acceptance:** Schema covers all terminal/recovery states.
- [ ] **`I16-S01-T03`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/domain/quote.py`
  - **Change:** Implement quote creation/validation/expiry and canonical hash.
  - **File-level acceptance:** Fake-clock and tampering tests pass.
- [ ] **`I16-S01-T04`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/domain/command.py`
  - **Change:** Implement state machine for accepted, dispatch, pending, success, no-result, refundable, refunded, cancelled, and manual reconciliation.
  - **File-level acceptance:** Model tests cover every transition.
- [ ] **`I16-S01-T05`**
  - **File:** `modules/m13-action-command/testkit/src/fga_commands_testkit/builders.py`
  - **Change:** Provide quote/command/outbox/result/failure builders.
  - **File-level acceptance:** Consumers and providers can test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I16-S02 — Atomic acceptance

**Stage outcome:** Debit, command, idempotency, and outbox intent commit together.

**Tasks:**

- [ ] **`I16-S02-T01`**
  - **File:** `modules/m13-action-command/backend/migrations/0001_commands.sql`
  - **Change:** Create quote, command, idempotency, outbox, provider state, cache, and reconciliation tables.
  - **File-level acceptance:** Constraints and migration tests pass.
- [ ] **`I16-S02-T02`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/acceptance.py`
  - **Change:** Implement validation, exact replay, UnitOfWork participants, and outbox creation.
  - **File-level acceptance:** Failure at each participant rolls back all.
- [ ] **`I16-S02-T03`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/idempotency.py`
  - **Change:** Implement key/request hash storage, owner scope, retention, and replay authorization.
  - **File-level acceptance:** Conflicting reuse returns typed 409.
- [ ] **`I16-S02-T04`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/http.py`
  - **Change:** Expose quote, execute, status, reconcile, and cancellation contracts.
  - **File-level acceptance:** OpenAPI/Problem Details tests pass.
- [ ] **`I16-S02-T05`**
  - **File:** `tests/integration/pairs/I09-command-acceptance.py`
  - **Change:** Run real M13/M14/M09/M11 with M19 fake.
  - **File-level acceptance:** Duplicate click and lost response debit once.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I16-S03 — Durable dispatch and reconciliation

**Stage outcome:** No accepted command depends on a web request remaining alive.

**Tasks:**

- [ ] **`I16-S03-T01`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/dispatch.py`
  - **Change:** Create durable workflow payload with stable hash, deadline, and provider idempotency key.
  - **File-level acceptance:** Payload is stored before external I/O.
- [ ] **`I16-S03-T02`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/reconciliation.py`
  - **Change:** Implement known/not-submitted/unknown/correlation-known decision matrix.
  - **File-level acceptance:** Unknown is never blindly retried.
- [ ] **`I16-S03-T03`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/cancellation.py`
  - **Change:** Implement cancellation only at safe lifecycle boundaries.
  - **File-level acceptance:** Races with terminal settlement produce one valid result.
- [ ] **`I16-S03-T04`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/scheduler.py`
  - **Change:** Add work-class fairness, deadlines, capacity, and starvation prevention hooks.
  - **File-level acceptance:** Poison work cannot starve interactive commands.
- [ ] **`I16-S03-T05`**
  - **File:** `tests/resilience/test_command_crash_matrix.py`
  - **Change:** Crash at every local transition and before/after fake external call.
  - **File-level acceptance:** Recovery yields one economic/visibility outcome.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I16-S04 — Settlement and pre-reveal safety

**Stage outcome:** Terminal status, economy, and visibility change atomically.

**Tasks:**

- [ ] **`I16-S04-T01`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/settlement.py`
  - **Change:** Implement success/no-result/refund/recovery terminal participant orchestration.
  - **File-level acceptance:** Partial settlement rolls back.
- [ ] **`I16-S04-T02`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/settlement_participant.py`
  - **Change:** Grant authorized records/relationships once from a validated M13 result.
  - **File-level acceptance:** Duplicate result creates no duplicate reveal.
- [ ] **`I16-S04-T03`**
  - **File:** `modules/m12-workspace-projection/frontend/src/CommandStatus.tsx`
  - **Change:** Render quote, confirmation, pending, no-result, refund, cancellation, and recovery states.
  - **File-level acceptance:** UI never infers failure from timeout.
- [ ] **`I16-S04-T04`**
  - **File:** `tests/security/test_pre_reveal_command_side_channels.py`
  - **Change:** Compare quote/status/error/size/timing-class behavior across hidden result cardinalities.
  - **File-level acceptance:** No hidden match fact is distinguishable.
- [ ] **`I16-S04-T05`**
  - **File:** `tests/integration/clusters/investigation/test_command_core.py`
  - **Change:** Run real M09/M11/M13/M14/M20 with deterministic resolver fake.
  - **File-level acceptance:** Atomic acceptance/settlement/reconciliation pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I16 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M13 suites, M14/M11 affected regressions, model checking, idempotency, and state-machine mutation tests.
- Run real pairwise command acceptance/settlement/workflow tests with timeout, duplicate, stale revision, malformed result, crash, cancellation, and poison work.
- Run investigation cluster and browser quote/status flows.
- Run pre-reveal noninterference and log/redaction tests.
- Run all cumulative gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I16 exit criteria

- Every paid command is quote-driven, idempotent, durable, and atomically settled.
- Unknown external outcomes cannot cause blind retry or duplicate charge.
- Pre-reveal statuses and errors do not leak hidden result facts.
- Accepted work progresses through durable M20 workflows.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I17 — Deterministic materialized retrieval resolver

**Objective:** Implement M19 canonical intent planning and publication-bound deterministic result resolution as the ranked baseline.

**Principal modules:** M19, M10, M13, M20

**Principal interactions:** I10, I16

**Prerequisites:**

- I16 is closed.

**Iteration outputs:**

- `I17-S01` — Retrieval contracts: Questions map to safe canonical plans before any charge.
- `I17-S02` — Deterministic answer resolver: Ranked records come only from immutable publications.
- `I17-S03` — Free interpretation and quote integration: The player sees and edits the plan before acceptance.
- `I17-S04` — Ranked determinism assurance: Provider-independent fairness is executable.

### I17-S01 — Retrieval contracts

**Stage outcome:** Questions map to safe canonical plans before any charge.

**Tasks:**

- [ ] **`I17-S01-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/contracts/retrieval-plan.schema.json`
  - **Change:** Define object types, filters, time range, sort, row cap, ambiguity class, interpretation text, and plan digest.
  - **File-level acceptance:** Schema rejects hidden fields and unsupported operators.
- [ ] **`I17-S01-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/contracts/retrieval-result.schema.json`
  - **Change:** Define publication-bound rows, order, provenance, no-result, and validation metadata.
  - **File-level acceptance:** Generated SQL/reasoning/rich content fields are absent.
- [ ] **`I17-S01-T03`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/domain/plan.py`
  - **Change:** Implement canonical plan model and safe operator/type validation.
  - **File-level acceptance:** Property tests prove deterministic canonicalization.
- [ ] **`I17-S01-T04`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/planner.py`
  - **Change:** Implement deterministic rule/parser baseline with clarification and abstention.
  - **File-level acceptance:** Ambiguous/unsupported/hidden-truth fixtures do not query data.
- [ ] **`I17-S01-T05`**
  - **File:** `modules/m19-retrieval-provider-gateway/testkit/src/fga_retrieval_testkit/builders.py`
  - **Change:** Provide plan/result/capability/provider failure fixtures.
  - **File-level acceptance:** M13 can test without a live provider.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I17-S02 — Deterministic answer resolver

**Stage outcome:** Ranked records come only from immutable publications.

**Tasks:**

- [ ] **`I17-S02-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/materialized_resolver.py`
  - **Change:** Resolve canonical plans against signed immutable safe data with deterministic row order.
  - **File-level acceptance:** Two players/plans receive byte-identical rows.
- [ ] **`I17-S02-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/result_firewall.py`
  - **Change:** Validate case/profile/publication, row/byte caps, safe columns, IDs, order, and intent consistency.
  - **File-level acceptance:** Malformed/cross-case/hidden-column fixtures fail closed.
- [ ] **`I17-S02-T03`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/migrations/0001_retrieval.sql`
  - **Change:** Create plan, parity manifest, resolver publication, and safe result metadata tables.
  - **File-level acceptance:** Migration and ownership tests pass.
- [ ] **`I17-S02-T04`**
  - **File:** `cases/academy/T01/retrieval.json`
  - **Change:** Publish supported T1 plans and deterministic expected rows.
  - **File-level acceptance:** Identifiability and parity validation pass.
- [ ] **`I17-S02-T05`**
  - **File:** `tests/property/test_materialized_retrieval.py`
  - **Change:** Generate supported filters/sorts and compare to reference resolver.
  - **File-level acceptance:** Results are stable and bounded.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I17-S03 — Free interpretation and quote integration

**Stage outcome:** The player sees and edits the plan before acceptance.

**Tasks:**

- [ ] **`I17-S03-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/frontend/src/RetrievalQuestion.tsx`
  - **Change:** Implement question entry, interpretation, clarification, edit, and abstention UI.
  - **File-level acceptance:** No debit occurs before plan acceptance.
- [ ] **`I17-S03-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/frontend/src/PlanPreview.tsx`
  - **Change:** Render exact safe interpretation, scope, sort, row cap, mode, and provider disclosure.
  - **File-level acceptance:** Accessibility and localization tests pass.
- [ ] **`I17-S03-T03`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/quote_factory.py`
  - **Change:** Add natural-language retrieval quote bound to canonical plan digest and resolver mode.
  - **File-level acceptance:** Changed plan invalidates quote.
- [ ] **`I17-S03-T04`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/dispatch.py`
  - **Change:** Route accepted retrieval commands to M19 durable resolver handler.
  - **File-level acceptance:** No WEB request performs data resolution.
- [ ] **`I17-S03-T05`**
  - **File:** `tests/integration/pairs/I10-command-retrieval.py`
  - **Change:** Run real M13/M19/M20 with T1 publication.
  - **File-level acceptance:** Plan, quote, dispatch, result, no-result, replay, and refund paths pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I17-S04 — Ranked determinism assurance

**Stage outcome:** Provider-independent fairness is executable.

**Tasks:**

- [ ] **`I17-S04-T01`**
  - **File:** `tests/benchmark/retrieval/answerable.json`
  - **Change:** Create answerable, ambiguous, overbroad, Unicode, no-result, and hidden-truth benchmark intents.
  - **File-level acceptance:** Every item has deterministic expected plan/outcome.
- [ ] **`I17-S04-T02`**
  - **File:** `tests/benchmark/retrieval/test_ranked_parity.py`
  - **Change:** Run repeated planner/resolver executions across players, seeds, and process restarts.
  - **File-level acceptance:** Authoritative rows/order never vary.
- [ ] **`I17-S04-T03`**
  - **File:** `tests/security/test_retrieval_injection.py`
  - **Change:** Inject prompt/data content, cross-case requests, hidden fields, oversized values, and active content.
  - **File-level acceptance:** Planner/firewall reject or safely abstain.
- [ ] **`I17-S04-T04`**
  - **File:** `tests/e2e/t01-materialized-retrieval.spec.ts`
  - **Change:** Ask, clarify, preview, quote, accept, receive result, repeat free, and submit placeholder evidence.
  - **File-level acceptance:** End-to-end result is deterministic.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I17 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete M19 unit/property/contract/component/architecture/security/performance suites.
- Run real M13↔M19↔M20 pairwise and investigation cluster using T1.
- Run repeated ranked parity, identifiability, clarification, no-result, injection, and side-channel tests.
- Run provider-independent clean route regression with external services disabled.
- Run all cumulative tests and scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I17 exit criteria

- Canonical plans are free, safe, deterministic, and player-editable.
- Authoritative ranked rows/order are publication-bound and repeatable.
- Unsupported or unsafe questions abstain before debit.
- M19 and M13 integrate without a live provider.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I18 — Live provider interpretation, capacity, privacy, and cost accounting

**Objective:** Add optional qualified live interpretation while preserving deterministic ranked row resolution and strict provider boundaries.

**Principal modules:** M19, M13, M20

**Principal interactions:** I10, I19

**Prerequisites:**

- I17 is closed; a development provider sandbox or deterministic API simulator is available.

**Iteration outputs:**

- `I18-S01` — Provider capability and conversation records: Every live call is bound to dated capability and isolated context.
- `I18-S02` — Provider adapter and result stripping: The provider may interpret, never choose ranked evidence.
- `I18-S03` — Real provider cost ledger: Operational cost remains private and separate from game credits.
- `I18-S04` — Qualification and disclosure: Live mode is optional, transparent, and segment-safe.

### I18-S01 — Provider capability and conversation records

**Stage outcome:** Every live call is bound to dated capability and isolated context.

**Tasks:**

- [ ] **`I18-S01-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/contracts/provider-capability.schema.json`
  - **Change:** Define product/SKU, API operation, maturity, region, limits, retention, pricing window, and approved features.
  - **File-level acceptance:** Capability values are effective-window facts, not constants.
- [ ] **`I18-S01-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/capabilities.py`
  - **Change:** Implement discovery/import, signed snapshot, admission headroom, and compatibility decision.
  - **File-level acceptance:** Expired/unknown capability closes admission.
- [ ] **`I18-S01-T03`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/migrations/0002_provider_state.sql`
  - **Change:** Create capability, conversation, deletion, capacity, price catalogue, reservation, usage, and cost ledger tables.
  - **File-level acceptance:** Migration and grants pass.
- [ ] **`I18-S01-T04`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/conversations.py`
  - **Change:** Create one fresh conversation per accepted command and track deletion receipt/deadline.
  - **File-level acceptance:** Cross-command context reuse test fails.
- [ ] **`I18-S01-T05`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/capacity.py`
  - **Change:** Implement table/instruction/conversation/message/rate/workspace headroom admission.
  - **File-level acceptance:** Deletion lag and incident reserve are included.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I18-S02 — Provider adapter and result stripping

**Stage outcome:** The provider may interpret, never choose ranked evidence.

**Tasks:**

- [ ] **`I18-S02-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/provider_adapter.py`
  - **Change:** Submit one bounded text question, poll by durable correlation, and normalize only plan interpretation.
  - **File-level acceptance:** Files, tools, sharing, follow-ups, and history are disabled.
- [ ] **`I18-S02-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/provider_firewall.py`
  - **Change:** Strip/reject SQL, reasoning, visualizations, comments, feedback, rich content, and unexpected fields.
  - **File-level acceptance:** Security audit event is emitted without raw payload.
- [ ] **`I18-S02-T03`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/parity.py`
  - **Change:** Compare provider-proposed plan to allowed canonical plan set; resolve rows only through materialized resolver.
  - **File-level acceptance:** Provider-selected row attempts are ignored/rejected.
- [ ] **`I18-S02-T04`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/quote_factory.py`
  - **Change:** Include mode, capability snapshot, external-context disclosure, and bounded provider envelope in quote.
  - **File-level acceptance:** Mode/capability change invalidates quote.
- [ ] **`I18-S02-T05`**
  - **File:** `tests/integration/pairs/provider-interpretation.py`
  - **Change:** Run real M19 adapter against simulator with context leakage and rich-output attacks.
  - **File-level acceptance:** Only safe plan survives.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I18-S03 — Real provider cost ledger

**Stage outcome:** Operational cost remains private and separate from game credits.

**Tasks:**

- [ ] **`I18-S03-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/src/fga_retrieval/cost_accounting.py`
  - **Change:** Implement price catalogue, budget reservation, actual usage reconciliation, anomaly detection, and currency amount handling.
  - **File-level acceptance:** No shared table or conversion with M14 exists.
- [ ] **`I18-S03-T02`**
  - **File:** `modules/m19-retrieval-provider-gateway/contracts/provider-cost.schema.json`
  - **Change:** Define private usage/cost records, effective price, currency, SKU, reservation, actual, and anomaly.
  - **File-level acceptance:** Contract is not exposed to player APIs.
- [ ] **`I18-S03-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/admission.py`
  - **Change:** Add provider budget/capacity/cleanup health to ranked admission.
  - **File-level acceptance:** Unhealthy provider does not affect materialized mode.
- [ ] **`I18-S03-T04`**
  - **File:** `tests/architecture/test_cost_ledger_separation.py`
  - **Change:** Verify M14 cannot import/query provider cost and player APIs cannot serialize it.
  - **File-level acceptance:** Deliberate coupling fixture fails.
- [ ] **`I18-S03-T05`**
  - **File:** `tests/property/test_provider_cost_reconciliation.py`
  - **Change:** Generate reservations, partial usage, price windows, promotions, and corrections.
  - **File-level acceptance:** Actual ledger balances exactly.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I18-S04 — Qualification and disclosure

**Stage outcome:** Live mode is optional, transparent, and segment-safe.

**Tasks:**

- [ ] **`I18-S04-T01`**
  - **File:** `modules/m19-retrieval-provider-gateway/frontend/src/ProviderDisclosure.tsx`
  - **Change:** Explain mode, external provider context, limitations, row cap, and that records are not conclusions.
  - **File-level acceptance:** Materialized mode is not called a live AI run.
- [ ] **`I18-S04-T02`**
  - **File:** `tests/benchmark/retrieval/test_provider_variance.py`
  - **Change:** Repeat provider interpretation and prove all accepted plans resolve to identical authoritative rows/order.
  - **File-level acceptance:** Variation may affect clarification only, not evidence.
- [ ] **`I18-S04-T03`**
  - **File:** `tests/security/test_provider_privacy.py`
  - **Change:** Verify account, recovery, private notes, accusations, truth, and unrelated history are never sent/logged.
  - **File-level acceptance:** Captured outbound payload is minimal.
- [ ] **`I18-S04-T04`**
  - **File:** `tests/resilience/test_provider_capacity_cleanup.py`
  - **Change:** Exercise cap exhaustion, deletion lag, timeout, outage, budget exhaustion, and conversation cleanup.
  - **File-level acceptance:** Admission closes safely; existing durable work reconciles.
- [ ] **`I18-S04-T05`**
  - **File:** `tests/e2e/t01-live-interpretation.spec.ts`
  - **Change:** Run disclosure → interpretation → quote → deterministic result with provider simulator.
  - **File-level acceptance:** Player provenance states actual mode.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I18 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M19 live adapter, capability, conversation, cost, privacy, contract, and resilience suites.
- Run repeated provider variance/parity benchmarks and cross-command memory contamination tests.
- Run M13/M19/M20 pairwise and operational-resilience cluster with timeout, outage, capacity, deletion lag, budget, and malformed output.
- Run cost-ledger separation architecture/security tests and player API leakage scans.
- Run full materialized-mode and cumulative regressions.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I18 exit criteria

- Live interpretation cannot alter authoritative ranked evidence.
- Every ranked command uses isolated provider context and tracked deletion.
- Capacity, retention, pricing, and budget facts govern admission.
- Real provider cost is private and structurally separate from investigation credits.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I19 — Complete four-action investigation loop

**Objective:** Integrate manual hypotheses, Zingg candidates, exact shared-field reveals, and bounded natural-language retrieval into one coherent quoted investigation experience.

**Principal modules:** M11, M12, M13, M14, M19, M10

**Principal interactions:** I09, I10

**Prerequisites:**

- I18 is closed.

**Iteration outputs:**

- `I19-S01` — Analytical relationship publications: Zingg and exact-field results are immutable, bounded, and truthfully sourced.
- `I19-S02` — Action family handlers: All four families use the same command/economy protocol.
- `I19-S03` — Investigation action UI: Players can quote, confirm, observe, and reuse results accessibly.
- `I19-S04` — Investigation cluster completion: The core gameplay loop is usable before saving/submission.

### I19-S01 — Analytical relationship publications

**Stage outcome:** Zingg and exact-field results are immutable, bounded, and truthfully sourced.

**Tasks:**

- [ ] **`I19-S01-T01`**
  - **File:** `modules/m10-case-content-rules/contracts/analytical-relationship.schema.json`
  - **Change:** Define endpoints, family, subtype, matched fields, confidence/criterion, generation mode, actual-engine flag, and publication versions.
  - **File-level acceptance:** Curated rows cannot claim engine metrics.
- [ ] **`I19-S01-T02`**
  - **File:** `cases/academy/T01/zingg.json`
  - **Change:** Add deterministic candidate-identity rows including an explicit valid no-result selection.
  - **File-level acceptance:** Publication validation passes.
- [ ] **`I19-S01-T03`**
  - **File:** `cases/academy/T01/exact-field.json`
  - **Change:** Add deterministic shared-field links and benign ambiguity warning.
  - **File-level acceptance:** Endpoints exist in the safe snapshot.
- [ ] **`I19-S01-T04`**
  - **File:** `tools/case_compiler/validators.py`
  - **Change:** Validate analytical endpoint visibility rules, provenance, caps, and profile compatibility.
  - **File-level acceptance:** Cross-profile/hidden endpoint fixtures fail.
- [ ] **`I19-S01-T05`**
  - **File:** `tests/cases/test_t01_analytical_publication.py`
  - **Change:** Compile and verify Zingg/exact rows, exclusions, and digests.
  - **File-level acceptance:** Results are deterministic.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I19-S02 — Action family handlers

**Stage outcome:** All four families use the same command/economy protocol.

**Tasks:**

- [ ] **`I19-S02-T01`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/actions/manual.py`
  - **Change:** Register free manual-hypothesis command semantics without ledger use.
  - **File-level acceptance:** No quote/debit is created.
- [ ] **`I19-S02-T02`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/actions/zingg.py`
  - **Change:** Implement selection validation, quote, deterministic reveal lookup, cap, and no-result.
  - **File-level acceptance:** Repeat returns persisted result at zero cost.
- [ ] **`I19-S02-T03`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/actions/exact_field.py`
  - **Change:** Implement field/options/time-window/min-count quote and deterministic reveal.
  - **File-level acceptance:** Ambiguity warning is always included.
- [ ] **`I19-S02-T04`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/actions/retrieval.py`
  - **Change:** Finalize natural-language action integration with M19 plan/result.
  - **File-level acceptance:** Only canonical plan and safe result enter command state.
- [ ] **`I19-S02-T05`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/action_registry.py`
  - **Change:** Expose exactly four action families and reject unregistered actions.
  - **File-level acceptance:** Constitution test detects a fifth or missing family.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I19-S03 — Investigation action UI

**Stage outcome:** Players can quote, confirm, observe, and reuse results accessibly.

**Tasks:**

- [ ] **`I19-S03-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ActionPanel.tsx`
  - **Change:** Compose exactly four action entries with selection-aware availability.
  - **File-level acceptance:** Actions have textual names and keyboard access.
- [ ] **`I19-S03-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ZinggAction.tsx`
  - **Change:** Implement scope, quote, model/provenance, cap, warning, confirmation, and result status.
  - **File-level acceptance:** No-result disclosure precedes debit.
- [ ] **`I19-S03-T03`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ExactFieldAction.tsx`
  - **Change:** Implement fields, any/all, window, minimum matches, quote, warning, and result status.
  - **File-level acceptance:** Unsupported fields are unavailable before quote.
- [ ] **`I19-S03-T04`**
  - **File:** `modules/m12-workspace-projection/frontend/src/RetrievalAction.tsx`
  - **Change:** Integrate M19 question/plan/disclosure/quote/status/result components.
  - **File-level acceptance:** Timeout is shown as pending/unknown, not failed.
- [ ] **`I19-S03-T05`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add all action, quote, confirmation, no-result, provider, refund, and recovery messages.
  - **File-level acceptance:** Catalogue checks pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I19-S04 — Investigation cluster completion

**Stage outcome:** The core gameplay loop is usable before saving/submission.

**Tasks:**

- [ ] **`I19-S04-T01`**
  - **File:** `tests/integration/clusters/investigation/test_four_actions.py`
  - **Change:** Run real M09–M14/M19/M20 with T1 and real DB.
  - **File-level acceptance:** All four action families and settlement outcomes pass.
- [ ] **`I19-S04-T02`**
  - **File:** `tests/e2e/t01-four-actions.spec.ts`
  - **Change:** Exercise manual, Zingg success/no-result, exact link, materialized retrieval, repeat cache, zero credits, and refresh.
  - **File-level acceptance:** No duplicate charge/reveal occurs.
- [ ] **`I19-S04-T03`**
  - **File:** `tests/concurrency/test_action_two_tabs.py`
  - **Change:** Race quotes, accepts, status, cancel, and repeat from two tabs.
  - **File-level acceptance:** Exactly one command/debit/result exists per idempotency intent.
- [ ] **`I19-S04-T04`**
  - **File:** `tests/security/test_action_leakage_matrix.py`
  - **Change:** Run selection, quote, error, no-result, hidden-cardinality, provider injection, and cross-case attacks.
  - **File-level acceptance:** All boundaries pass.
- [ ] **`I19-S04-T05`**
  - **File:** `tests/accessibility/four-actions.spec.ts`
  - **Change:** Complete every action with keyboard and semantic/list paths.
  - **File-level acceptance:** No direct graph manipulation is required.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I19 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete affected M10–M14/M19 module suites and contract compatibility.
- Run all action pairwise integrations and full investigation cluster with real DB/provider simulator.
- Run duplicate, crash, timeout, cancellation, no-result, zero-credit, replay-cache, and side-channel matrices.
- Run keyboard/screen-reader/reflow/zoom/contrast action journeys.
- Run all cumulative gates, scans, and production-like WEB/MAINTENANCE composition.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I19 exit criteria

- Exactly four action families are registered and playable.
- Every paid action is quoted, confirmed, durable, idempotent, and provenance-complete.
- Repeated deterministic requests do not charge twice.
- The investigation loop passes functional, concurrency, security, accessibility, and resilience tests.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I20 — Autosave, checkpoints, draft history, and recovery

**Objective:** Implement M15 and client coordination so reversible work survives navigation and restart without rolling back monotonic ranked state.

**Principal modules:** M15, M06, M09, M11, M16 draft contract, M20

**Principal interactions:** I11

**Prerequisites:**

- I19 is closed.

**Iteration outputs:**

- `I20-S01` — Save contracts and persistence: Checkpoints contain only reversible player-authored/UI state.
- `I20-S02` — Autosave and conflict handling: Client and server coordinate explicit revisions.
- `I20-S03` — Restore and practice fork: Full-state branching is unranked and original history remains intact.
- `I20-S04` — Recovery qualification: Refresh, logout/login, restart, and two tabs preserve exact authoritative state.

### I20-S01 — Save contracts and persistence

**Stage outcome:** Checkpoints contain only reversible player-authored/UI state.

**Tasks:**

- [ ] **`I20-S01-T01`**
  - **File:** `modules/m15-save-recovery/contracts/save.schema.json`
  - **Change:** Define autosave, checkpoint, draft revision, bookmarks, subsets, filters, panels, viewport, and restore receipt.
  - **File-level acceptance:** Schema cannot contain ledger, commands, reveals, bindings, submission, verdict, or progression.
- [ ] **`I20-S01-T02`**
  - **File:** `modules/m15-save-recovery/backend/src/fga_saves/domain/checkpoint.py`
  - **Change:** Implement reversible projection, revision, naming, and restore rules.
  - **File-level acceptance:** Property tests prove monotonic state is never part of restore.
- [ ] **`I20-S01-T03`**
  - **File:** `modules/m15-save-recovery/backend/migrations/0001_saves.sql`
  - **Change:** Create autosave, checkpoint, revision history, practice fork, and retention tables.
  - **File-level acceptance:** Migration and ownership tests pass.
- [ ] **`I20-S01-T04`**
  - **File:** `modules/m15-save-recovery/backend/src/fga_saves/repository.py`
  - **Change:** Implement owner/round-scoped save persistence and bounded history.
  - **File-level acceptance:** IDOR and retention tests pass.
- [ ] **`I20-S01-T05`**
  - **File:** `modules/m15-save-recovery/testkit/src/fga_saves_testkit/builders.py`
  - **Change:** Provide save, conflict, offline, stale-reference, and fork fixtures.
  - **File-level acceptance:** Consumers test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I20-S02 — Autosave and conflict handling

**Stage outcome:** Client and server coordinate explicit revisions.

**Tasks:**

- [ ] **`I20-S02-T01`**
  - **File:** `modules/m15-save-recovery/backend/src/fga_saves/autosave.py`
  - **Change:** Implement expected revision, idempotency, bounded history, and safe stale response.
  - **File-level acceptance:** Concurrent writes never silently overwrite.
- [ ] **`I20-S02-T02`**
  - **File:** `modules/m06-client-state-synchronization/frontend/src/autosave.ts`
  - **Change:** Implement bounded debounce, pending receipt, retry, conflict, and page-exit warning.
  - **File-level acceptance:** Fake network tests pass.
- [ ] **`I20-S02-T03`**
  - **File:** `modules/m15-save-recovery/frontend/src/SaveStatus.tsx`
  - **Change:** Render saving/saved/offline/conflict/recovery states through M02/M03.
  - **File-level acceptance:** Announcements are deduplicated.
- [ ] **`I20-S02-T04`**
  - **File:** `modules/m15-save-recovery/frontend/src/CheckpointManager.tsx`
  - **Change:** Create/update/restore named checkpoints with scope explanation.
  - **File-level acceptance:** Confirmation states what will not be rolled back.
- [ ] **`I20-S02-T05`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add save, checkpoint, conflict, offline, and practice-fork messages.
  - **File-level acceptance:** Catalogue passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I20-S03 — Restore and practice fork

**Stage outcome:** Full-state branching is unranked and original history remains intact.

**Tasks:**

- [ ] **`I20-S03-T01`**
  - **File:** `modules/m15-save-recovery/backend/src/fga_saves/restore.py`
  - **Change:** Restore only M15/M16 reversible projections through public participant ports.
  - **File-level acceptance:** Attempted monotonic-field restore is rejected.
- [ ] **`I20-S03-T02`**
  - **File:** `modules/m15-save-recovery/backend/src/fga_saves/practice_fork.py`
  - **Change:** Create a new unranked round from an approved checkpoint/template.
  - **File-level acceptance:** Source ranked round remains unchanged.
- [ ] **`I20-S03-T03`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/practice.py`
  - **Change:** Add explicit unranked fork mode and ranking-ineligible binding.
  - **File-level acceptance:** Practice cannot advance progression.
- [ ] **`I20-S03-T04`**
  - **File:** `tests/integration/pairs/I11-save-round-casefile.py`
  - **Change:** Run real M15 with M09/M11 and M16 draft fake.
  - **File-level acceptance:** Restore preserves later reveals/ledger/commands.
- [ ] **`I20-S03-T05`**
  - **File:** `tests/security/test_checkpoint_tampering.py`
  - **Change:** Inject credits, hidden evidence, command state, or ranking eligibility into checkpoint payload.
  - **File-level acceptance:** All are rejected.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I20-S04 — Recovery qualification

**Stage outcome:** Refresh, logout/login, restart, and two tabs preserve exact authoritative state.

**Tasks:**

- [ ] **`I20-S04-T01`**
  - **File:** `tests/integration/clusters/save_submission/test_save_cluster.py`
  - **Change:** Run M06/M09/M11/M15/M16-fake with real DB.
  - **File-level acceptance:** Autosave, checkpoint, restore, fork, and conflicts pass.
- [ ] **`I20-S04-T02`**
  - **File:** `tests/e2e/t01-save-resume.spec.ts`
  - **Change:** Investigate, edit draft placeholder, save, refresh, logout/login, restart WEB, and resume.
  - **File-level acceptance:** Reveals/credits/commands remain monotonic.
- [ ] **`I20-S04-T03`**
  - **File:** `tests/concurrency/test_autosave_two_tabs.py`
  - **Change:** Race autosaves and checkpoint restores.
  - **File-level acceptance:** Typed conflict and merge/reload path preserve data.
- [ ] **`I20-S04-T04`**
  - **File:** `tests/resilience/test_save_database_wake.py`
  - **Change:** Lose DB response before/after commit and retry with same key.
  - **File-level acceptance:** No duplicate revision or lost acknowledged save.
- [ ] **`I20-S04-T05`**
  - **File:** `tests/architecture/test_checkpoint_scope.py`
  - **Change:** Statically forbid M15 restore from importing M11/M13/M14 repositories.
  - **File-level acceptance:** Forbidden fixture fails.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I20 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M15 and affected M06 suites, property tests, contract tests, DB tests, and architecture scope tests.
- Run M15↔M09/M11/M16 pairwise and save/submission cluster.
- Run browser refresh, logout/login, process restart, DB wake, offline, stale revision, and two-tab journeys.
- Run tampering tests proving credits/evidence/commands/bindings cannot be restored.
- Run full cumulative gate.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I20 exit criteria

- Autosave and checkpoints are durable, revision-aware, and recoverable.
- Ranked restore changes only reversible draft/UI state.
- Practice forks are new unranked rounds with no progression/ranking effect.
- All save/recovery scenarios pass after restarts and conflicting tabs.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I21 — Structured case file, claims, classifications, and evidence mapping

**Objective:** Implement the editable M16 case-file argument model before immutable submission and evaluation.

**Principal modules:** M16, M11, M15, M02/M03

**Principal interactions:** I11

**Prerequisites:**

- I20 is closed.

**Iteration outputs:**

- `I21-S01` — Case-file domain: Identity, role, culpability, harm, accusation, and uncertainty remain separate.
- `I21-S02` — Validation and warnings: Warnings assist without revealing truth.
- `I21-S03` — Case-file editor: The full argument is editable accessibly and save-integrated.
- `I21-S04` — Save/case-file integration: M15 checkpoints and M16 drafts cooperate without ownership leakage.

### I21-S01 — Case-file domain

**Stage outcome:** Identity, role, culpability, harm, accusation, and uncertainty remain separate.

**Tasks:**

- [ ] **`I21-S01-T01`**
  - **File:** `modules/m16-case-file-submission/contracts/case-file.schema.json`
  - **Change:** Define principals, context actors, identity conclusions, roles, culpability, harm, mechanism, flow, tactics, claims, evidence links, uncertainty, alternatives, and contradictions.
  - **File-level acceptance:** Schema prevents one generic suspect flag.
- [ ] **`I21-S01-T02`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/domain/case_file.py`
  - **Change:** Implement structured draft aggregate and revisions.
  - **File-level acceptance:** Property tests cover add/update/remove/canonical order.
- [ ] **`I21-S01-T03`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/domain/claim.py`
  - **Change:** Implement explicit claims, evidence links, status, and contradiction references.
  - **File-level acceptance:** Circular/self-evidence fixtures are flagged.
- [ ] **`I21-S01-T04`**
  - **File:** `modules/m16-case-file-submission/backend/migrations/0001_casefile.sql`
  - **Change:** Create drafts, classifications, claims, evidence links, notes, and revision history.
  - **File-level acceptance:** Migration/ownership tests pass.
- [ ] **`I21-S01-T05`**
  - **File:** `modules/m16-case-file-submission/testkit/src/fga_casefile_testkit/builders.py`
  - **Change:** Provide clean, partial, wrong, overbroad, uncertain, and contradictory drafts.
  - **File-level acceptance:** M15/M17 can test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I21-S02 — Validation and warnings

**Stage outcome:** Warnings assist without revealing truth.

**Tasks:**

- [ ] **`I21-S02-T01`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/validation.py`
  - **Change:** Validate visible evidence ownership, required structure, duplicate families, unsupported claims, circularity, contradictions, and victim-risk heuristics.
  - **File-level acceptance:** Warnings depend only on player-visible state/rules.
- [ ] **`I21-S02-T02`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/evidence.py`
  - **Change:** Resolve M11 evidence/provenance through public port and canonicalize references.
  - **File-level acceptance:** Hidden/unrevealed/cross-round references fail.
- [ ] **`I21-S02-T03`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/http.py`
  - **Change:** Expose get/update/revisions/restore/review contracts with optimistic concurrency.
  - **File-level acceptance:** OpenAPI and IDOR tests pass.
- [ ] **`I21-S02-T04`**
  - **File:** `tests/security/test_casefile_warning_noninterference.py`
  - **Change:** Compare warnings across protected truths for identical visible draft/input.
  - **File-level acceptance:** Warnings are identical.
- [ ] **`I21-S02-T05`**
  - **File:** `tests/property/test_casefile_canonicalization.py`
  - **Change:** Generate equivalent ordering/formatting and compare canonical draft digest.
  - **File-level acceptance:** Equivalent drafts match.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I21-S03 — Case-file editor

**Stage outcome:** The full argument is editable accessibly and save-integrated.

**Tasks:**

- [ ] **`I21-S03-T01`**
  - **File:** `modules/m16-case-file-submission/frontend/src/CaseFileEditor.tsx`
  - **Change:** Compose structured sections, validation summary, save status, and revision controls.
  - **File-level acceptance:** Keyboard order and reflow pass.
- [ ] **`I21-S03-T02`**
  - **File:** `modules/m16-case-file-submission/frontend/src/ActorClassifications.tsx`
  - **Change:** Edit accusation, role, culpability, harm, and context separately.
  - **File-level acceptance:** Labels avoid guilt-by-identity wording.
- [ ] **`I21-S03-T03`**
  - **File:** `modules/m16-case-file-submission/frontend/src/ClaimsEditor.tsx`
  - **Change:** Create claims, attach evidence, record uncertainty/alternatives, and inspect provenance.
  - **File-level acceptance:** Evidence picker contains only visible records.
- [ ] **`I21-S03-T04`**
  - **File:** `modules/m16-case-file-submission/frontend/src/FlowEditor.tsx`
  - **Change:** Build chronology/money-event flow with exact order and direction.
  - **File-level acceptance:** No graph-only dependency exists.
- [ ] **`I21-S03-T05`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add case-file, classification, claim, evidence, uncertainty, warning, and revision messages.
  - **File-level acceptance:** Catalogue passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I21-S04 — Save/case-file integration

**Stage outcome:** M15 checkpoints and M16 drafts cooperate without ownership leakage.

**Tasks:**

- [ ] **`I21-S04-T01`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/checkpoint_participant.py`
  - **Change:** Expose reversible case-file projection to M15 restore.
  - **File-level acceptance:** Participant mutates only M16 tables.
- [ ] **`I21-S04-T02`**
  - **File:** `tests/integration/pairs/I11-casefile-save.py`
  - **Change:** Run real M15/M16/M11 with edits, checkpoints, later evidence, and restore.
  - **File-level acceptance:** Draft restores; later evidence remains visible.
- [ ] **`I21-S04-T03`**
  - **File:** `tests/integration/clusters/save_submission/test_casefile_cluster.py`
  - **Change:** Run real M06/M09/M11/M15/M16 with browser harness.
  - **File-level acceptance:** Autosave, revisions, warnings, conflicts, and restore pass.
- [ ] **`I21-S04-T04`**
  - **File:** `tests/accessibility/case-file-editor.spec.ts`
  - **Change:** Complete classification, claim, evidence, uncertainty, and revision tasks by keyboard/screen reader path.
  - **File-level acceptance:** All critical tasks pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I21 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M16 draft unit/property/contract/component/architecture/security/accessibility suites.
- Run warning noninterference and canonicalization tests.
- Run real M15↔M16↔M11 pairwise and save/submission cluster with conflicts/restart.
- Run case-file browser E2E on T1 and cumulative investigation regressions.
- Run all earlier gates and leakage scans.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I21 exit criteria

- The case file is structured, canonical, revisioned, and truth-independent before submission.
- Claims map explicitly to visible evidence and uncertainty.
- Warnings do not leak the answer key.
- Editor and save integration pass accessible end-to-end workflows.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I22 — Immutable submission and evaluation-pending workflow

**Objective:** Freeze one canonical submission exactly once, block mutable gameplay, and deliver it durably to the private evaluator boundary.

**Principal modules:** M16, M09, M13, M14, M20, M17 contract

**Principal interactions:** I12

**Prerequisites:**

- I21 is closed.

**Iteration outputs:**

- `I22-S01` — Submission contracts and canonical snapshot: Submission identity commits to all evidence and version lineage.
- `I22-S02` — Atomic submission transition: One confirmation creates one immutable submission and lifecycle transition.
- `I22-S03` — Private delivery protocol: The evaluator receives only an immutable request reference and verified bindings.
- `I22-S04` — Submission UX and recovery: Players understand irreversibility and pending state.

### I22-S01 — Submission contracts and canonical snapshot

**Stage outcome:** Submission identity commits to all evidence and version lineage.

**Tasks:**

- [ ] **`I22-S01-T01`**
  - **File:** `modules/m16-case-file-submission/contracts/submission.schema.json`
  - **Change:** Define canonical case file, command/credit snapshots, round bindings, evidence object digests, evidence Merkle root, and submission digest.
  - **File-level acceptance:** Schema requires immutable lineage.
- [ ] **`I22-S01-T02`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/submission.py`
  - **Change:** Build canonical submission snapshot and digest from public participant snapshots.
  - **File-level acceptance:** Equivalent drafts yield identical snapshot.
- [ ] **`I22-S01-T03`**
  - **File:** `modules/m16-case-file-submission/backend/migrations/0002_submissions.sql`
  - **Change:** Create immutable submissions, payloads, digest lineage, and delivery state.
  - **File-level acceptance:** Database constraints prevent update/delete.
- [ ] **`I22-S01-T04`**
  - **File:** `modules/m11-investigation-visibility/backend/src/fga_investigation/evidence_bundle.py`
  - **Change:** Produce ordered visible evidence object digests and Merkle root.
  - **File-level acceptance:** Root changes for any content/order change.
- [ ] **`I22-S01-T05`**
  - **File:** `modules/m13-action-command/backend/src/fga_commands/submission_snapshot.py`
  - **Change:** Expose terminal command and economic-determinacy snapshot.
  - **File-level acceptance:** Pending/unknown command blocks submission.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I22-S02 — Atomic submission transition

**Stage outcome:** One confirmation creates one immutable submission and lifecycle transition.

**Tasks:**

- [ ] **`I22-S02-T01`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/submit.py`
  - **Change:** Validate ownership, active round, required fields, terminal commands, economy snapshot, evidence lineage, and idempotency.
  - **File-level acceptance:** Every validation failure occurs before commit.
- [ ] **`I22-S02-T02`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/submission_participant.py`
  - **Change:** Transition ACTIVE→SUBMISSION_PENDING→EVALUATION_PENDING under shared UnitOfWork.
  - **File-level acceptance:** Concurrent submissions produce one winner.
- [ ] **`I22-S02-T03`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/http.py`
  - **Change:** Add review and submit endpoints with irreversible confirmation receipt.
  - **File-level acceptance:** Lost response replays exact submission.
- [ ] **`I22-S02-T04`**
  - **File:** `tests/integration/pairs/I12-submission-uow.py`
  - **Change:** Run real M16/M09/M11/M13/M14/M20.
  - **File-level acceptance:** Any participant failure rolls back entire submission.
- [ ] **`I22-S02-T05`**
  - **File:** `tests/concurrency/test_submission_two_tabs.py`
  - **Change:** Race confirmation, refresh, and duplicate keys.
  - **File-level acceptance:** Exactly one immutable submission exists.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I22-S03 — Private delivery protocol

**Stage outcome:** The evaluator receives only an immutable request reference and verified bindings.

**Tasks:**

- [ ] **`I22-S03-T01`**
  - **File:** `modules/m17-evaluation-scoring-ending/contracts/evaluation-request.schema.json`
  - **Change:** Define submission ID/digest, round bindings, evaluator bundle digest, evidence root, and request nonce.
  - **File-level acceptance:** No browser/private player session fields are included.
- [ ] **`I22-S03-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/evaluation-job.schema.json`
  - **Change:** Define private delivery, retries, lease, key version, and safe terminal states.
  - **File-level acceptance:** Public API cannot serialize protected job details.
- [ ] **`I22-S03-T03`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/evaluation_delivery.py`
  - **Change:** Register durable private evaluation job after submission commit.
  - **File-level acceptance:** Crash after commit is recoverable.
- [ ] **`I22-S03-T04`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/private_jobs.py`
  - **Change:** Route evaluation jobs only to EVALUATOR capability/identity.
  - **File-level acceptance:** WEB/MAINTENANCE generic worker cannot claim truth-reading step.
- [ ] **`I22-S03-T05`**
  - **File:** `tests/security/test_evaluation_delivery_isolation.py`
  - **Change:** Attempt to claim/read evaluation job from WEB identity.
  - **File-level acceptance:** Database grants and runtime policy deny access.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I22-S04 — Submission UX and recovery

**Stage outcome:** Players understand irreversibility and pending state.

**Tasks:**

- [ ] **`I22-S04-T01`**
  - **File:** `modules/m16-case-file-submission/frontend/src/SubmissionReview.tsx`
  - **Change:** Show structured summary, unresolved fields, pending-work warning, evidence count/root reference, and irreversible notice.
  - **File-level acceptance:** No answer hints appear.
- [ ] **`I22-S04-T02`**
  - **File:** `modules/m16-case-file-submission/frontend/src/SubmitConfirmation.tsx`
  - **Change:** Require explicit confirmation and show committed/pending/recovery states.
  - **File-level acceptance:** Double click uses one idempotency key.
- [ ] **`I22-S04-T03`**
  - **File:** `modules/m09-round-game-state/frontend/src/EvaluationPending.tsx`
  - **Change:** Render durable pending and safe recovery status.
  - **File-level acceptance:** Browser polling is optional, not correctness-critical.
- [ ] **`I22-S04-T04`**
  - **File:** `tests/e2e/t01-submit-pending.spec.ts`
  - **Change:** Investigate, build case file, review, submit, lose response, refresh, and see same pending submission.
  - **File-level acceptance:** Mutable actions remain blocked.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I22 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M16 submission and M09 lifecycle suites, evidence digest/Merkle property tests, DB immutability, and idempotency.
- Run real cross-module submission UnitOfWork tests with injected failure at every participant.
- Run private job routing/identity/grant tests and WEB truth-import scans.
- Run browser irreversible confirmation, lost response, duplicate tab, pending/recovery journeys.
- Run all cumulative gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I22 exit criteria

- One canonical immutable submission is created exactly once.
- Submission binds evidence Merkle root, round versions, commands, and economy snapshots.
- Mutable gameplay is blocked after confirmation.
- Only the private evaluator runtime can claim the truth-reading evaluation step.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I23 — Private evaluator, deterministic scoring, endings, and safe verdict

**Objective:** Implement M17 Truth Broker, deterministic evaluator, six endings, safe declassification, and exactly-once finalization.

**Principal modules:** M17, M10, M16, M20, M09

**Principal interactions:** I13, I14

**Prerequisites:**

- I22 is closed.

**Iteration outputs:**

- `I23-S01` — Truth Broker and private persistence: Protected truth is reachable only through M17 private adapters.
- `I23-S02` — Canonical deterministic evaluator: Equivalent submissions score identically.
- `I23-S03` — Noninterference, declassification, and signing: Verdicts do not become adaptive truth oracles.
- `I23-S04` — Exactly-once finalization and verdict UI: Safe verdict closes the round without exposing truth services.

### I23-S01 — Truth Broker and private persistence

**Stage outcome:** Protected truth is reachable only through M17 private adapters.

**Tasks:**

- [ ] **`I23-S01-T01`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/truth_broker.py`
  - **Change:** Verify evaluation request, submission digest, bindings, evaluator bundle, evidence root, and nonce before truth access.
  - **File-level acceptance:** Invalid lineage never opens truth repository.
- [ ] **`I23-S01-T02`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/truth_repository.py`
  - **Change:** Implement least-privilege protected truth read adapter.
  - **File-level acceptance:** Only EVALUATOR database role has grants.
- [ ] **`I23-S01-T03`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/migrations/0001_evaluation.sql`
  - **Change:** Create private requests/audit and safe verdict/amendment projection tables with separate grants.
  - **File-level acceptance:** WEB cannot select private schema.
- [ ] **`I23-S01-T04`**
  - **File:** `modules/m17-evaluation-scoring-ending/contracts/verdict.schema.json`
  - **Change:** Define score, components, gates, penalties, ending, coaching codes, versions, signature, and eligibility.
  - **File-level acceptance:** Schema contains only approved safe fields.
- [ ] **`I23-S01-T05`**
  - **File:** `modules/m17-evaluation-scoring-ending/testkit/src/fga_evaluation_testkit/builders.py`
  - **Change:** Provide protected truth, submissions, expected scoring, and oracle-attack fixtures.
  - **File-level acceptance:** Consumers never receive truth builder package.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I23-S02 — Canonical deterministic evaluator

**Stage outcome:** Equivalent submissions score identically.

**Tasks:**

- [ ] **`I23-S02-T01`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/canonicalize.py`
  - **Change:** Normalize order, duplicates, locale, harmless formatting, and structured semantics.
  - **File-level acceptance:** Equivalence golden tests pass.
- [ ] **`I23-S02-T02`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/scoring.py`
  - **Change:** Implement 0–1000 components, solve gates, penalties, caps, and exact integer arithmetic.
  - **File-level acceptance:** Reference fixtures match expected totals.
- [ ] **`I23-S02-T03`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/endings.py`
  - **Change:** Implement deterministic precedence for six canonical endings.
  - **File-level acceptance:** All precedence combinations are golden-tested.
- [ ] **`I23-S02-T04`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/coaching.py`
  - **Change:** Map safe reason codes to bounded templates after score is fixed.
  - **File-level acceptance:** Templates cannot change score or reveal protected facts.
- [ ] **`I23-S02-T05`**
  - **File:** `cases/academy/T01/scoring.yaml`
  - **Change:** Define T1 clean legitimate closure, partial, wrong accusation, overbroad, inefficient, and unresolved expectations.
  - **File-level acceptance:** Compiler/evaluator validation passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I23-S03 — Noninterference, declassification, and signing

**Stage outcome:** Verdicts do not become adaptive truth oracles.

**Tasks:**

- [ ] **`I23-S03-T01`**
  - **File:** `cases/academy/T01/declassification.yaml`
  - **Change:** Declare exact safe closure/debrief facts and abstractions.
  - **File-level acceptance:** Anything not listed is unavailable to verdict projection.
- [ ] **`I23-S03-T02`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/declassification.py`
  - **Change:** Filter gates, reasons, coaching, and debrief references through signed manifest.
  - **File-level acceptance:** Unapproved truth facts are dropped and audited.
- [ ] **`I23-S03-T03`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/signing.py`
  - **Change:** Sign canonical safe verdict envelope with versioned private key port.
  - **File-level acceptance:** Tampering and wrong key fail verification.
- [ ] **`I23-S03-T04`**
  - **File:** `tests/security/test_evaluator_oracle.py`
  - **Change:** Run repeated/adaptive/equivalent submissions and compare output information.
  - **File-level acceptance:** Only approved disclosure varies.
- [ ] **`I23-S03-T05`**
  - **File:** `tests/property/test_evaluator_semantics.py`
  - **Change:** Run equivalence, metamorphic, monotonicity, sensitivity, and replay properties.
  - **File-level acceptance:** All deterministic properties pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I23-S04 — Exactly-once finalization and verdict UI

**Stage outcome:** Safe verdict closes the round without exposing truth services.

**Tasks:**

- [ ] **`I23-S04-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/verdict_finalizer.py`
  - **Change:** Commit safe verdict projection and M09 closure exactly once after signature verification.
  - **File-level acceptance:** Duplicate delivery is idempotent.
- [ ] **`I23-S04-T02`**
  - **File:** `modules/m09-round-game-state/backend/src/fga_rounds/verdict_participant.py`
  - **Change:** Transition EVALUATION_PENDING→CLOSED with verdict reference.
  - **File-level acceptance:** No direct truth access exists.
- [ ] **`I23-S04-T03`**
  - **File:** `modules/m17-evaluation-scoring-ending/frontend/src/VerdictView.tsx`
  - **Change:** Render score, components, gates, penalties, ending, coaching, and safe pending/amended state.
  - **File-level acceptance:** Accessible summary and detail hierarchy pass.
- [ ] **`I23-S04-T04`**
  - **File:** `modules/m17-evaluation-scoring-ending/frontend/src/DebriefView.tsx`
  - **Change:** Render only declassification-approved educational content and closure transcript.
  - **File-level acceptance:** No protected raw truth payload reaches browser.
- [ ] **`I23-S04-T05`**
  - **File:** `tests/e2e/t01-evaluation.spec.ts`
  - **Change:** Submit clean and wrong T1 fixtures, restart evaluator/finalizer, and receive deterministic verdicts.
  - **File-level acceptance:** Scores/endings remain exact.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I23 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M17 unit/property/model/contract/component/architecture/security suites in private EVALUATOR composition.
- Run deterministic replay, equivalence, metamorphic, monotonicity, sensitivity, six-ending, signing, tamper, and oracle-leakage tests.
- Run M17↔M16/M10/M20 and finalization pairwise tests with evaluator/key outage and duplicate delivery.
- Inspect WEB image/dependency/grants/logs/bundle for protected truth or keys.
- Run full cumulative system from registration through verdict.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I23 exit criteria

- Protected truth is isolated to the EVALUATOR identity and private schema.
- Scoring and endings are deterministic, canonical, and exact.
- Safe verdicts are signed, declassification-bound, and oracle-resistant.
- Finalization closes a round exactly once after failures/retries.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I24 — Atomic progression, results, amendments, and leaderboards

**Objective:** Complete the production loop by advancing careers, publishing optional rankings, and preserving historical corrections.

**Principal modules:** M08, M09, M17, M18, M07, M20

**Principal interactions:** I14, I15

**Prerequisites:**

- I23 is closed.

**Iteration outputs:**

- `I24-S01` — Progression finalization: A valid verdict closes one case and unlocks at most the next.
- `I24-S02` — Leaderboard domain: Only compatible eligible results enter opt-in rankings.
- `I24-S03` — Public result and moderation surfaces: Publication is voluntary and privacy-safe.
- `I24-S04` — Amendments and historical integrity: Corrections link to originals and reindex safely.

### I24-S01 — Progression finalization

**Stage outcome:** A valid verdict closes one case and unlocks at most the next.

**Tasks:**

- [ ] **`I24-S01-T01`**
  - **File:** `modules/m08-career-catalogue-progression/backend/src/fga_career/progression.py`
  - **Change:** Implement eligible ranked progression, fixed next case, family transition, and exact-once event handling.
  - **File-level acceptance:** Practice/Academy/revisit/reviewer rounds cannot advance.
- [ ] **`I24-S01-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/verdict_finalizer.py`
  - **Change:** Add M08 progression participant to safe verdict transaction.
  - **File-level acceptance:** Failure rolls back verdict closure/progression together.
- [ ] **`I24-S01-T03`**
  - **File:** `modules/m08-career-catalogue-progression/contracts/progression.schema.json`
  - **Change:** Define completion, next availability, transition, and ineligibility reason.
  - **File-level acceptance:** Contract is version/ranking-segment bound.
- [ ] **`I24-S01-T04`**
  - **File:** `tests/integration/pairs/I14-verdict-progression.py`
  - **Change:** Run real M17 safe verdict/M09/M08/M20.
  - **File-level acceptance:** Duplicate finalization does not skip cases.
- [ ] **`I24-S01-T05`**
  - **File:** `tests/concurrency/test_progression.py`
  - **Change:** Race duplicate verdict delivery and concurrent catalogue reads.
  - **File-level acceptance:** Exactly one next case opens.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I24-S02 — Leaderboard domain

**Stage outcome:** Only compatible eligible results enter opt-in rankings.

**Tasks:**

- [ ] **`I24-S02-T01`**
  - **File:** `modules/m18-leaderboard-results/contracts/leaderboard.schema.json`
  - **Change:** Define alias, entry, segment key, rank key, shared rank, moderation, withdrawal, and dispute states.
  - **File-level acceptance:** Wall-clock/accessibility/provider latency fields are absent.
- [ ] **`I24-S02-T02`**
  - **File:** `modules/m18-leaderboard-results/backend/src/fga_leaderboard/domain/ranking.py`
  - **Change:** Implement score/precision/efficiency ordering and standard competition ranking.
  - **File-level acceptance:** Property tests cover exact ties.
- [ ] **`I24-S02-T03`**
  - **File:** `modules/m18-leaderboard-results/backend/migrations/0001_leaderboard.sql`
  - **Change:** Create aliases, entries, projections, moderation, withdrawal, and disputes.
  - **File-level acceptance:** Ownership/uniqueness constraints pass.
- [ ] **`I24-S02-T04`**
  - **File:** `modules/m18-leaderboard-results/backend/src/fga_leaderboard/eligibility.py`
  - **Change:** Validate first-attempt/mode/version/segment/amendment eligibility.
  - **File-level acceptance:** Mixed provider modes cannot share a segment.
- [ ] **`I24-S02-T05`**
  - **File:** `modules/m18-leaderboard-results/testkit/src/fga_leaderboard_testkit/builders.py`
  - **Change:** Provide eligible/ineligible/tie/amended/moderated fixtures.
  - **File-level acceptance:** Consumers test independently.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I24-S03 — Public result and moderation surfaces

**Stage outcome:** Publication is voluntary and privacy-safe.

**Tasks:**

- [ ] **`I24-S03-T01`**
  - **File:** `modules/m18-leaderboard-results/backend/src/fga_leaderboard/publication.py`
  - **Change:** Implement alias opt-in, publish, withdraw, moderation, and safe event handling.
  - **File-level acceptance:** Login name/private text never enters entry.
- [ ] **`I24-S03-T02`**
  - **File:** `modules/m18-leaderboard-results/frontend/src/LeaderboardView.tsx`
  - **Change:** Render segmented rankings, shared ranks, provenance, and empty/degraded states.
  - **File-level acceptance:** Accessible table and sorting semantics pass.
- [ ] **`I24-S03-T03`**
  - **File:** `modules/m18-leaderboard-results/frontend/src/PublishResult.tsx`
  - **Change:** Implement alias creation/moderation feedback, opt-in, withdrawal, and dispute initiation.
  - **File-level acceptance:** No dark pattern or default opt-in.
- [ ] **`I24-S03-T04`**
  - **File:** `modules/m03-localization-messaging/catalogues/en-GB.json`
  - **Change:** Add progression, result publication, ranking, moderation, withdrawal, and dispute messages.
  - **File-level acceptance:** Catalogue passes.
- [ ] **`I24-S03-T05`**
  - **File:** `tests/integration/pairs/I15-verdict-leaderboard.py`
  - **Change:** Run real M18 with M17 safe events/M07 alias/M09 segment.
  - **File-level acceptance:** Eligibility and privacy pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I24-S04 — Amendments and historical integrity

**Stage outcome:** Corrections link to originals and reindex safely.

**Tasks:**

- [ ] **`I24-S04-T01`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/src/fga_evaluation/amendments.py`
  - **Change:** Implement VALID/UNDER_REVIEW/INVALIDATED/SUPERSEDED lineage and new evaluator version.
  - **File-level acceptance:** Original verdict remains immutable.
- [ ] **`I24-S04-T02`**
  - **File:** `modules/m18-leaderboard-results/backend/src/fga_leaderboard/reindex.py`
  - **Change:** Reindex or withdraw affected entries idempotently after amendment.
  - **File-level acceptance:** Rank projection converges.
- [ ] **`I24-S04-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/amendment-job.schema.json`
  - **Change:** Define review, reproduce, amend, notify, and reindex workflow.
  - **File-level acceptance:** Workflow is audit/version bound.
- [ ] **`I24-S04-T04`**
  - **File:** `tests/integration/clusters/evaluation_progression/test_results_cluster.py`
  - **Change:** Run M08/M09/M16–M18/M20 with clean, wrong, tie, amendment, and withdrawal scenarios.
  - **File-level acceptance:** All historical invariants pass.
- [ ] **`I24-S04-T05`**
  - **File:** `tests/e2e/t01-complete-loop.spec.ts`
  - **Change:** Register → career → investigate → save → submit → verdict → progression → optional ranking → withdrawal.
  - **File-level acceptance:** Complete T1 loop passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I24 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run full M08 progression, M18, and M17 amendment suites plus affected regressions.
- Run verdict/progression and verdict/leaderboard pairwise tests with duplicate events and mixed segments.
- Run evaluation/progression cluster with real DB and browser E2E.
- Run privacy/alias/withdrawal/IDOR and ranking property tests.
- Run full cumulative solution gate through a complete T1 loop.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I24 exit criteria

- Career progression is atomic, exact-once, and fixed-order.
- Leaderboards are opt-in, segmented, tie-correct, private, and withdrawable.
- Amendments never overwrite historical submissions or verdicts.
- The first complete end-to-end game loop passes.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I25 — Detective Academy and Kennel Lab conformance suite

**Objective:** Implement Academy T1–T12 and protected Kennel Lab T13–T15 as executable curriculum and whole-engine conformance fixtures.

**Principal modules:** M01–M20

**Principal interactions:** All principal journeys

**Prerequisites:**

- I24 is closed.

**Iteration outputs:**

- `I25-S01` — Academy package set: Each learning objective has a deterministic package and golden playthrough.
- `I25-S02` — Academy supporting artifacts: Every package includes safe data, truth, retrieval, scoring, assets, and tests.
- `I25-S03` — Protected Kennel Lab: Stress fixtures are server-protected and absent from production player navigation.
- `I25-S04` — Whole-engine conformance: Academy becomes the mandatory regression curriculum.

### I25-S01 — Academy package set

**Stage outcome:** Each learning objective has a deterministic package and golden playthrough.

**Tasks:**

- [ ] **`I25-S01-T01`**
  - **File:** `cases/academy/T02/case.yaml`
  - **Change:** Define the minimal complete happy-path case.
  - **File-level acceptance:** Package compiler and clean-solve fixture pass.
- [ ] **`I25-S01-T02`**
  - **File:** `cases/academy/T03/case.yaml`
  - **Change:** Define fuzzy identity candidates and false-merge traps.
  - **File-level acceptance:** Candidate interpretation fixtures pass.
- [ ] **`I25-S01-T03`**
  - **File:** `cases/academy/T04/case.yaml`
  - **Change:** Define directed cycle and exact-relationship graph.
  - **File-level acceptance:** Graph direction/layout-independent tests pass.
- [ ] **`I25-S01-T04`**
  - **File:** `cases/academy/T05/case.yaml`
  - **Change:** Define disconnected components and progressive reveal.
  - **File-level acceptance:** Visibility/component tests pass.
- [ ] **`I25-S01-T05`**
  - **File:** `cases/academy/T06/case.yaml`
  - **Change:** Define legitimate shared infrastructure and high-degree innocent actor.
  - **File-level acceptance:** False-guilt safeguards pass.
- [ ] **`I25-S01-T06`**
  - **File:** `cases/academy/T07/case.yaml`
  - **Change:** Define chronology, time zones, and deterministic sorting.
  - **File-level acceptance:** Temporal/as_of_time tests pass.
- [ ] **`I25-S01-T07`**
  - **File:** `cases/academy/T08/case.yaml`
  - **Change:** Define conflicting evidence and uncertainty.
  - **File-level acceptance:** Case-file uncertainty scoring passes.
- [ ] **`I25-S01-T08`**
  - **File:** `cases/academy/T09/case.yaml`
  - **Change:** Define missing data and insufficient evidence.
  - **File-level acceptance:** Unresolved ending fixture passes.
- [ ] **`I25-S01-T09`**
  - **File:** `cases/academy/T10/case.yaml`
  - **Change:** Define red herrings and precision requirements.
  - **File-level acceptance:** Overbroad penalties pass.
- [ ] **`I25-S01-T10`**
  - **File:** `cases/academy/T11/case.yaml`
  - **Change:** Define credits, quotes, valid no-result, refunds, and zero-credit completion.
  - **File-level acceptance:** Economy/command fixtures pass.
- [ ] **`I25-S01-T11`**
  - **File:** `cases/academy/T12/case.yaml`
  - **Change:** Define scoring boundaries and all six endings.
  - **File-level acceptance:** Ending matrix passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I25-S02 — Academy supporting artifacts

**Stage outcome:** Every package includes safe data, truth, retrieval, scoring, assets, and tests.

**Tasks:**

- [ ] **`I25-S02-T01`**
  - **File:** `tools/academy/generate_packages.py`
  - **Change:** Generate deterministic player-safe/truth/retrieval/scoring scaffolds from Academy definitions.
  - **File-level acceptance:** Repeated generation is byte-identical.
- [ ] **`I25-S02-T02`**
  - **File:** `tools/academy/validate_curriculum.py`
  - **Change:** Verify T1–T12 cover every constitutional gameplay and learning objective.
  - **File-level acceptance:** Coverage report has no gap.
- [ ] **`I25-S02-T03`**
  - **File:** `assets/manifests/academy.json`
  - **Change:** Register opening/closure media, transcripts, icons, and fallbacks for T1–T12.
  - **File-level acceptance:** Asset and accessibility validation passes.
- [ ] **`I25-S02-T04`**
  - **File:** `tests/academy/golden_playthroughs.json`
  - **Change:** Register clean, partial, wrong, overbroad, inefficient, no-result, and unresolved expected outcomes.
  - **File-level acceptance:** Every Academy package has applicable strategies.
- [ ] **`I25-S02-T05`**
  - **File:** `tests/academy/test_all_cases.py`
  - **Change:** Compile, activate, play, score, and replay T1–T12 deterministically.
  - **File-level acceptance:** All expected scores/endings match.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I25-S03 — Protected Kennel Lab

**Stage outcome:** Stress fixtures are server-protected and absent from production player navigation.

**Tasks:**

- [ ] **`I25-S03-T01`**
  - **File:** `cases/kennel-lab/T13/case.yaml`
  - **Change:** Define extreme names, wrapping, reflow, and responsive stress.
  - **File-level acceptance:** 320px/200% tests pass.
- [ ] **`I25-S03-T02`**
  - **File:** `cases/kennel-lab/T14/case.yaml`
  - **Change:** Define Unicode, normalization, sorting, bidi, and confusable stress.
  - **File-level acceptance:** Cross-language canonicalization passes.
- [ ] **`I25-S03-T03`**
  - **File:** `cases/kennel-lab/T15/case.yaml`
  - **Change:** Define duplicate clicks, stale revisions, transaction races, and diagnostics.
  - **File-level acceptance:** Concurrency matrix passes.
- [ ] **`I25-S03-T04`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/fixture_access.py`
  - **Change:** Require server-side protected capability for Kennel Lab publication/routes.
  - **File-level acceptance:** Client flag alone cannot enable it.
- [ ] **`I25-S03-T05`**
  - **File:** `tests/security/test_kennel_lab_isolation.py`
  - **Change:** Probe routes, catalogue, assets, APIs, and manifests as normal player.
  - **File-level acceptance:** Fixtures remain undiscoverable.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I25-S04 — Whole-engine conformance

**Stage outcome:** Academy becomes the mandatory regression curriculum.

**Tasks:**

- [ ] **`I25-S04-T01`**
  - **File:** `tests/e2e/academy/all-academy.spec.ts`
  - **Change:** Execute T1–T12 core journeys in real browser against exact image.
  - **File-level acceptance:** All journeys pass with deterministic fakes.
- [ ] **`I25-S04-T02`**
  - **File:** `tests/e2e/kennel-lab/all-kennel-lab.spec.ts`
  - **Change:** Execute T13–T15 under protected test identity.
  - **File-level acceptance:** All stress scenarios pass.
- [ ] **`I25-S04-T03`**
  - **File:** `config/testing/mandatory-regressions.yaml`
  - **Change:** Add Academy T1–T12 and protected T13–T15 to integration/release gates.
  - **File-level acceptance:** Impact optimizer cannot omit them.
- [ ] **`I25-S04-T04`**
  - **File:** `reports/academy/COVERAGE.md`
  - **Change:** Map every Academy/Lab objective to modules, requirements, interactions, and tests.
  - **File-level acceptance:** Traceability has no orphan objective.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I25 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Compile every Academy/Lab package twice and compare all digests/Merkle roots.
- Run all module, pairwise, eight cluster, role, browser, accessibility, security, concurrency, and evaluator tests against T1–T15.
- Run every six-ending and economy/no-result/recovery path.
- Verify Kennel Lab is absent from normal player/public artifacts.
- Run complete cumulative system suite from clean checkout and exact production image.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I25 exit criteria

- T1–T12 exercise the real engine and cover all constitutional gameplay rules.
- T13–T15 exercise responsive, Unicode, concurrency, and diagnostic stress safely.
- Academy/Lab regressions are mandatory and deterministic.
- No protected fixture is reachable by an ordinary player.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I26 — Puppy family production packages P1–P3

**Objective:** Build, integrate, and qualify the three Puppy production cases using the frozen modular engine.

**Principal modules:** M10 case packages, All gameplay modules

**Principal interactions:** Production case journeys

**Prerequisites:**

- I25 is closed; core public contracts are frozen for family work.

**Iteration outputs:**

- `I26-S01` — P1 The Maddogg Investment Kennel: Deliver a complete Ponzi/affinity-investment package.
- `I26-S02` — P2 The CEO Who Barked Twice: Deliver an impersonation/mailbox/invoice-diversion package.
- `I26-S03` — P3 The Great Biscuit Relief Fund: Deliver a fake-relief/donation-diversion package.
- `I26-S04` — Puppy family qualification: P1–P3 work as one ranked progression.

### I26-S01 — P1 The Maddogg Investment Kennel

**Stage outcome:** Deliver a complete Ponzi/affinity-investment package.

**Tasks:**

- [ ] **`I26-S01-T01`**
  - **File:** `cases/production/MADDOG/case.yaml`
  - **Change:** Define profiles, rules, economy, warnings, action caps, versions, and debrief references.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I26-S01-T02`**
  - **File:** `cases/production/MADDOG/player-safe.json`
  - **Change:** Publish deterministic records, events, documents, and direct relationships.
  - **File-level acceptance:** Safe, temporal, referential, and leakage gates pass.
- [ ] **`I26-S01-T03`**
  - **File:** `cases/production/MADDOG/analytical.json`
  - **Change:** Publish candidate identity, exact-field, exclusions, provenance, and resolver plans.
  - **File-level acceptance:** Analytical quality and identifiability pass.
- [ ] **`I26-S01-T04`**
  - **File:** `cases/production/MADDOG/truth.json`
  - **Change:** Define principal, mechanism, flow, roles, victim/innocent protections, solve gates, and alternatives.
  - **File-level acceptance:** Private package tests pass.
- [ ] **`I26-S01-T05`**
  - **File:** `cases/production/MADDOG/scoring.yaml`
  - **Change:** Define weights, gates, penalties, six-ending thresholds, and declassification.
  - **File-level acceptance:** Golden evaluator tests pass.
- [ ] **`I26-S01-T06`**
  - **File:** `assets/manifests/MADDOG.json`
  - **Change:** Register opening/closure comics, transcripts, documents, icons, and fallbacks.
  - **File-level acceptance:** Asset/licensing/accessibility checks pass.
- [ ] **`I26-S01-T07`**
  - **File:** `tests/cases/MADDOG/playthroughs.json`
  - **Change:** Define clean, partial, wrong, overbroad, inefficient, unresolved, and no-result strategies.
  - **File-level acceptance:** Expected results validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I26-S02 — P2 The CEO Who Barked Twice

**Stage outcome:** Deliver an impersonation/mailbox/invoice-diversion package.

**Tasks:**

- [ ] **`I26-S02-T01`**
  - **File:** `cases/production/CEO_BARKED_TWICE/case.yaml`
  - **Change:** Define package metadata, profiles, economy, and warnings.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I26-S02-T02`**
  - **File:** `cases/production/CEO_BARKED_TWICE/player-safe.json`
  - **Change:** Publish communications, invoices, mailbox/device events, payments, and innocent comparators.
  - **File-level acceptance:** Schema/temporal/leakage checks pass.
- [ ] **`I26-S02-T03`**
  - **File:** `cases/production/CEO_BARKED_TWICE/analytical.json`
  - **Change:** Publish identity/infrastructure candidates, exact links, and deterministic retrieval plans.
  - **File-level acceptance:** False-merge and ambiguity tests pass.
- [ ] **`I26-S02-T04`**
  - **File:** `cases/production/CEO_BARKED_TWICE/truth.json`
  - **Change:** Define coordinator, technical operator, mule controller, payment flow, and protected parties.
  - **File-level acceptance:** Private truth tests pass.
- [ ] **`I26-S02-T05`**
  - **File:** `cases/production/CEO_BARKED_TWICE/scoring.yaml`
  - **Change:** Define solve gates, penalties, endings, and declassification.
  - **File-level acceptance:** Golden scores pass.
- [ ] **`I26-S02-T06`**
  - **File:** `assets/manifests/CEO_BARKED_TWICE.json`
  - **Change:** Register complete accessible media package.
  - **File-level acceptance:** Asset gates pass.
- [ ] **`I26-S02-T07`**
  - **File:** `tests/cases/CEO_BARKED_TWICE/playthroughs.json`
  - **Change:** Define required strategy fixtures.
  - **File-level acceptance:** All outcomes validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I26-S03 — P3 The Great Biscuit Relief Fund

**Stage outcome:** Deliver a fake-relief/donation-diversion package.

**Tasks:**

- [ ] **`I26-S03-T01`**
  - **File:** `cases/production/BISCUIT_RELIEF/case.yaml`
  - **Change:** Define package metadata, profiles, economy, warnings, and publication versions.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I26-S03-T02`**
  - **File:** `cases/production/BISCUIT_RELIEF/player-safe.json`
  - **Change:** Publish campaign, donation, settlement, provider, impact, and beneficiary records.
  - **File-level acceptance:** Fairness/temporal/schema gates pass.
- [ ] **`I26-S03-T03`**
  - **File:** `cases/production/BISCUIT_RELIEF/analytical.json`
  - **Change:** Publish candidate, exact-field, and retrieval structures with legitimate-provider hard negatives.
  - **File-level acceptance:** Quality gates pass.
- [ ] **`I26-S03-T04`**
  - **File:** `cases/production/BISCUIT_RELIEF/truth.json`
  - **Change:** Define principal, content operator, financial operator, diversion flow, inflated impact, and protected actors.
  - **File-level acceptance:** Private tests pass.
- [ ] **`I26-S03-T05`**
  - **File:** `cases/production/BISCUIT_RELIEF/scoring.yaml`
  - **Change:** Define scoring, gates, penalties, endings, and declassification.
  - **File-level acceptance:** Golden results pass.
- [ ] **`I26-S03-T06`**
  - **File:** `assets/manifests/BISCUIT_RELIEF.json`
  - **Change:** Register complete accessible media package.
  - **File-level acceptance:** Asset gates pass.
- [ ] **`I26-S03-T07`**
  - **File:** `tests/cases/BISCUIT_RELIEF/playthroughs.json`
  - **Change:** Define clean and failure strategies.
  - **File-level acceptance:** All outcomes validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I26-S04 — Puppy family qualification

**Stage outcome:** P1–P3 work as one ranked progression.

**Tasks:**

- [ ] **`I26-S04-T01`**
  - **File:** `config/cases/families/puppy.yaml`
  - **Change:** Register order, profile policy, family transitions, case versions, and eligibility.
  - **File-level acceptance:** Catalogue/progression integration passes.
- [ ] **`I26-S04-T02`**
  - **File:** `tests/integration/families/test_puppy_family.py`
  - **Change:** Run P1→P2→P3 progression with clean and recovery variations.
  - **File-level acceptance:** Exactly correct unlocks occur.
- [ ] **`I26-S04-T03`**
  - **File:** `tests/e2e/families/puppy.spec.ts`
  - **Change:** Play representative complete routes for all three profiles and cases.
  - **File-level acceptance:** Browser/accessibility journeys pass.
- [ ] **`I26-S04-T04`**
  - **File:** `reports/families/puppy/QUALITY_CARD.md`
  - **Change:** Record data, fairness, privacy, solvability, performance, asset, and dual-use evidence.
  - **File-level acceptance:** All approvals and residual risks are explicit.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I26 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run hermetic case compilation, schema, referential, temporal, profile, synthetic privacy/fidelity, leakage, and asset gates for P1–P3.
- Run all golden playthroughs, deterministic resolver parity, scoring/endings, innocent/victim protection, and declassification tests.
- Run Puppy progression, save/recovery, action, provider outage, evaluator restart, and leaderboard segmentation E2E.
- Run accessibility and performance at all three investigation profiles.
- Run the complete Academy/Lab and cumulative system regression.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I26 exit criteria

- P1–P3 are complete signed packages with all required artifacts.
- Every case has multiple solve routes and protects innocent/victim actors.
- Puppy progression and family presentation are exact.
- All family, engine, security, accessibility, and release-quality tests pass.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I27 — Adult family production packages A1–A4

**Objective:** Build, integrate, and qualify the four Adult production cases with denser records, relationships, chronology, and ambiguity.

**Principal modules:** M10 case packages, All gameplay modules

**Principal interactions:** Production case journeys

**Prerequisites:**

- I26 is closed.

**Iteration outputs:**

- `I27-S01` — A1 and A2 package construction: Deliver accounting-manipulation and pyramid/downline cases.
- `I27-S02` — A3 and A4 package construction: Deliver veterinary-claims and procurement/kickback cases.
- `I27-S03` — Adult media and retrieval qualification: Dense cases remain accessible and deterministic.
- `I27-S04` — Adult family qualification: Puppy-to-Adult and Adult-entry paths both work.

### I27-S01 — A1 and A2 package construction

**Stage outcome:** Deliver accounting-manipulation and pyramid/downline cases.

**Tasks:**

- [ ] **`I27-S01-T01`**
  - **File:** `cases/production/BONE_LEDGER/case.yaml`
  - **Change:** Define A1 profiles, economy, dense accounting rules, and warnings.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I27-S01-T02`**
  - **File:** `cases/production/BONE_LEDGER/package-data.json`
  - **Change:** Publish A1 safe data, analytical rows, truth references, and version bindings.
  - **File-level acceptance:** Compiler splits safe/private outputs and all gates pass.
- [ ] **`I27-S01-T03`**
  - **File:** `cases/production/BONE_LEDGER/scoring.yaml`
  - **Change:** Define A1 flow, liability, SPV, journal, role, and innocent-auditor expectations.
  - **File-level acceptance:** Golden strategies pass.
- [ ] **`I27-S01-T04`**
  - **File:** `tests/cases/BONE_LEDGER/playthroughs.json`
  - **Change:** Define A1 clean and failure strategies.
  - **File-level acceptance:** Evaluator results validate.
- [ ] **`I27-S01-T05`**
  - **File:** `cases/production/DOWNLINE/case.yaml`
  - **Change:** Define A2 mixed victim/recruiter/downline package.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I27-S01-T06`**
  - **File:** `cases/production/DOWNLINE/package-data.json`
  - **Change:** Publish A2 safe data, analytical structures, and private generation references.
  - **File-level acceptance:** Fairness and mixed-role gates pass.
- [ ] **`I27-S01-T07`**
  - **File:** `cases/production/DOWNLINE/scoring.yaml`
  - **Change:** Define A2 mechanism, commissions, mixed culpability/harm, and uncertainty.
  - **File-level acceptance:** Golden strategies pass.
- [ ] **`I27-S01-T08`**
  - **File:** `tests/cases/DOWNLINE/playthroughs.json`
  - **Change:** Define A2 clean and failure strategies.
  - **File-level acceptance:** Evaluator results validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I27-S02 — A3 and A4 package construction

**Stage outcome:** Deliver veterinary-claims and procurement/kickback cases.

**Tasks:**

- [ ] **`I27-S02-T01`**
  - **File:** `cases/production/PHANTOM_VET/case.yaml`
  - **Change:** Define A3 claims, license misuse, procedures, and payment-flow package.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I27-S02-T02`**
  - **File:** `cases/production/PHANTOM_VET/package-data.json`
  - **Change:** Publish A3 safe/private source material and analytical relationships.
  - **File-level acceptance:** Schema/privacy/fairness gates pass.
- [ ] **`I27-S02-T03`**
  - **File:** `cases/production/PHANTOM_VET/scoring.yaml`
  - **Change:** Define A3 principal, procedures, claims, role/harm, and protection gates.
  - **File-level acceptance:** Golden strategies pass.
- [ ] **`I27-S02-T04`**
  - **File:** `tests/cases/PHANTOM_VET/playthroughs.json`
  - **Change:** Define A3 strategy fixtures.
  - **File-level acceptance:** Results validate.
- [ ] **`I27-S02-T05`**
  - **File:** `cases/production/GOLDEN_HYDRANT/case.yaml`
  - **Change:** Define A4 procurement, bids, change orders, shells, kickbacks, and emergency comparators.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I27-S02-T06`**
  - **File:** `cases/production/GOLDEN_HYDRANT/package-data.json`
  - **Change:** Publish A4 safe/private data and analytical structures.
  - **File-level acceptance:** Legitimate comparator and chronology gates pass.
- [ ] **`I27-S02-T07`**
  - **File:** `cases/production/GOLDEN_HYDRANT/scoring.yaml`
  - **Change:** Define A4 collusion/kickback flow, roles, evidence diversity, and innocent protection.
  - **File-level acceptance:** Golden strategies pass.
- [ ] **`I27-S02-T08`**
  - **File:** `tests/cases/GOLDEN_HYDRANT/playthroughs.json`
  - **Change:** Define A4 strategy fixtures.
  - **File-level acceptance:** Results validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I27-S03 — Adult media and retrieval qualification

**Stage outcome:** Dense cases remain accessible and deterministic.

**Tasks:**

- [ ] **`I27-S03-T01`**
  - **File:** `assets/manifests/adult-family.json`
  - **Change:** Register opening/closure media, transcripts, documents, icons, and responsive variants for A1–A4.
  - **File-level acceptance:** Asset/licensing/accessibility gates pass.
- [ ] **`I27-S03-T02`**
  - **File:** `tests/benchmark/retrieval/adult.json`
  - **Change:** Register answerable, ambiguous, noisy-schema, Unicode, no-result, and overbroad intents.
  - **File-level acceptance:** Materialized parity passes.
- [ ] **`I27-S03-T03`**
  - **File:** `tests/performance/adult-workspaces.yaml`
  - **Change:** Define list/graph/document/API/evaluator budgets for all profiles.
  - **File-level acceptance:** Performance suite has bounded fixture sizes.
- [ ] **`I27-S03-T04`**
  - **File:** `tests/fairness/adult-slices.yaml`
  - **Change:** Define language/script/shared-service/mixed-role and socioeconomic proxy slices.
  - **File-level acceptance:** Candidate/evaluator slice tests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I27-S04 — Adult family qualification

**Stage outcome:** Puppy-to-Adult and Adult-entry paths both work.

**Tasks:**

- [ ] **`I27-S04-T01`**
  - **File:** `config/cases/families/adult.yaml`
  - **Change:** Register A1–A4 order, transitions, versions, and profile policies.
  - **File-level acceptance:** Catalogue and progression tests pass.
- [ ] **`I27-S04-T02`**
  - **File:** `tests/integration/families/test_adult_family.py`
  - **Change:** Run Puppy→A1 transition and Adult-entry A1→A4 progression.
  - **File-level acceptance:** No skipped/double unlock occurs.
- [ ] **`I27-S04-T03`**
  - **File:** `tests/e2e/families/adult.spec.ts`
  - **Change:** Play representative complete journeys across A1–A4 and profiles.
  - **File-level acceptance:** Dense workspace/accessibility tests pass.
- [ ] **`I27-S04-T04`**
  - **File:** `reports/families/adult/QUALITY_CARD.md`
  - **Change:** Record data, fairness, privacy, solvability, performance, assets, and dual-use evidence.
  - **File-level acceptance:** All approvals are present.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I27 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run complete publication/data/temporal/relational/privacy/fairness/solvability gates for A1–A4.
- Run all golden strategies, scoring/endings, retrieval parity, provider interpretation, save/recovery, and amendments.
- Run dense graph/list/document accessibility and performance tests.
- Run both career entry paths and Puppy→Adult transition.
- Run Academy/Lab, Puppy, and full cumulative regression.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I27 exit criteria

- A1–A4 are complete, deterministic, accessible, and signed.
- Mixed roles, legitimate comparators, and dense graph ambiguity are treated fairly.
- Adult entry and family transitions are exact.
- All cumulative quality gates remain green.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I28 — Senior family production packages V1–V3

**Objective:** Build, integrate, and qualify the three most complex Senior cases with cross-border, cryptocurrency, and beneficial-ownership ambiguity.

**Principal modules:** M10 case packages, All gameplay modules

**Principal interactions:** Production case journeys

**Prerequisites:**

- I27 is closed.

**Iteration outputs:**

- `I28-S01` — V1 Love, Leashes & Offshore Transfers: Deliver relationship manipulation and cross-border transfer layering.
- `I28-S02` — V2 The Long Con at Crypto Kennel: Deliver layered investment/crypto movement with infrastructure ambiguity.
- `I28-S03` — V3 The Panama Pawpers: Deliver offshore beneficial ownership with lawful-versus-abusive ambiguity.
- `I28-S04` — Senior and anthology qualification: All ten cases form one complete fixed anthology.

### I28-S01 — V1 Love, Leashes & Offshore Transfers

**Stage outcome:** Deliver relationship manipulation and cross-border transfer layering.

**Tasks:**

- [ ] **`I28-S01-T01`**
  - **File:** `cases/production/V1/case.yaml`
  - **Change:** Define sensitive-theme warnings, profiles, economy, cross-border chronology, and rules.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I28-S01-T02`**
  - **File:** `cases/production/V1/package-data.json`
  - **Change:** Publish fictional communications, identities, transfers, accounts, intermediaries, and analytical structures.
  - **File-level acceptance:** Privacy/dual-use/temporal gates pass.
- [ ] **`I28-S01-T03`**
  - **File:** `cases/production/V1/scoring.yaml`
  - **Change:** Define manipulation mechanism, flow, victim protection, roles, and uncertainty gates.
  - **File-level acceptance:** Golden results pass.
- [ ] **`I28-S01-T04`**
  - **File:** `assets/manifests/V1.json`
  - **Change:** Register humane accessible opening/closure media and documents.
  - **File-level acceptance:** Content/accessibility review passes.
- [ ] **`I28-S01-T05`**
  - **File:** `tests/cases/V1/playthroughs.json`
  - **Change:** Define clean, partial, victim-blaming, overbroad, inefficient, and unresolved strategies.
  - **File-level acceptance:** Expected penalties/endings pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I28-S02 — V2 The Long Con at Crypto Kennel

**Stage outcome:** Deliver layered investment/crypto movement with infrastructure ambiguity.

**Tasks:**

- [ ] **`I28-S02-T01`**
  - **File:** `cases/production/V2/case.yaml`
  - **Change:** Define crypto/investment profiles, economy, safe abstractions, and dual-use limits.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I28-S02-T02`**
  - **File:** `cases/production/V2/package-data.json`
  - **Change:** Publish fictional wallets, exchanges, transactions, devices, identities, and legitimate shared infrastructure.
  - **File-level acceptance:** No live target or operational evasion detail appears.
- [ ] **`I28-S02-T03`**
  - **File:** `cases/production/V2/scoring.yaml`
  - **Change:** Define long-con mechanism, fund flow, identity uncertainty, infrastructure interpretation, and victim protections.
  - **File-level acceptance:** Golden results pass.
- [ ] **`I28-S02-T04`**
  - **File:** `assets/manifests/V2.json`
  - **Change:** Register accessible media/documents without operational wrongdoing instructions.
  - **File-level acceptance:** Content gates pass.
- [ ] **`I28-S02-T05`**
  - **File:** `tests/cases/V2/playthroughs.json`
  - **Change:** Define clean and failure strategies.
  - **File-level acceptance:** Expected results pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I28-S03 — V3 The Panama Pawpers

**Stage outcome:** Deliver offshore beneficial ownership with lawful-versus-abusive ambiguity.

**Tasks:**

- [ ] **`I28-S03-T01`**
  - **File:** `cases/production/V3/case.yaml`
  - **Change:** Define offshore structure, intermediary, ownership, chronology, and lawful comparator rules.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I28-S03-T02`**
  - **File:** `cases/production/V3/package-data.json`
  - **Change:** Publish fictional entities, filings, interests, intermediaries, payments, and analytical structures.
  - **File-level acceptance:** Source, fairness, and temporal gates pass.
- [ ] **`I28-S03-T03`**
  - **File:** `cases/production/V3/scoring.yaml`
  - **Change:** Define ownership/control, mechanism, evidence, lawful ambiguity, and false-accusation protections.
  - **File-level acceptance:** Golden results pass.
- [ ] **`I28-S03-T04`**
  - **File:** `assets/manifests/V3.json`
  - **Change:** Register accessible media and debrief assets.
  - **File-level acceptance:** Asset/content gates pass.
- [ ] **`I28-S03-T05`**
  - **File:** `tests/cases/V3/playthroughs.json`
  - **Change:** Define clean, lawful, unresolved, overbroad, and wrong-principal strategies.
  - **File-level acceptance:** Expected results pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I28-S04 — Senior and anthology qualification

**Stage outcome:** All ten cases form one complete fixed anthology.

**Tasks:**

- [ ] **`I28-S04-T01`**
  - **File:** `config/cases/families/senior.yaml`
  - **Change:** Register V1–V3 order, transition, profile, and version policy.
  - **File-level acceptance:** Catalogue/progression passes.
- [ ] **`I28-S04-T02`**
  - **File:** `config/cases/anthology.yaml`
  - **Change:** Register immutable P1→V3 order and supported entry tiers.
  - **File-level acceptance:** No branch/reorder is possible.
- [ ] **`I28-S04-T03`**
  - **File:** `tests/integration/families/test_senior_anthology.py`
  - **Change:** Run Puppy, Adult, and Senior entry paths through all applicable cases.
  - **File-level acceptance:** Every transition is exact.
- [ ] **`I28-S04-T04`**
  - **File:** `tests/e2e/families/senior.spec.ts`
  - **Change:** Play representative Senior journeys with tight credits, dense graph, save/recovery, provider outage, and accessibility modes.
  - **File-level acceptance:** All pass.
- [ ] **`I28-S04-T05`**
  - **File:** `reports/families/senior/QUALITY_CARD.md`
  - **Change:** Record sensitive content, dual-use, privacy, fairness, solvability, performance, and residual risks.
  - **File-level acceptance:** Approvals are complete.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I28 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run all publication/data/privacy/relational/temporal/fairness/dual-use/solvability gates for V1–V3.
- Run golden playthroughs including victim protection, lawful ambiguity, crypto infrastructure, and false accusation penalties.
- Run Senior performance/capacity/accessibility, provider-independent solve, provider outage, and evaluator restart tests.
- Run every anthology career entry/path and ranking segmentation.
- Run the complete cumulative Academy and production-case suite.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I28 exit criteria

- V1–V3 are complete signed packages with safe defensive abstraction.
- The fixed ten-case anthology and all three entry tiers are operational.
- Senior complexity remains accessible, bounded, and provider-independent.
- Every cumulative test remains green.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I29 — Privacy lifecycle, export, deletion, erasure, and consent migration

**Objective:** Complete the player-data lifecycle across all module owners, including verifiable export and cryptographic erasure.

**Principal modules:** M07, M15, M16, M18, M20, All data-owning modules

**Principal interactions:** I04, I06

**Prerequisites:**

- I28 is closed.

**Iteration outputs:**

- `I29-S01` — Data inventory and handler registry: Every module declares export, retention, erasure, and tombstone behavior.
- `I29-S02` — Export integrity: A player receives only their data and player-visible context.
- `I29-S03` — Deletion and cryptographic erasure: Deleted private text becomes undecryptable across active and restored storage.
- `I29-S04` — Consent, telemetry, and end-to-end lifecycle: Material policy changes and preferences remain explicit.

### I29-S01 — Data inventory and handler registry

**Stage outcome:** Every module declares export, retention, erasure, and tombstone behavior.

**Tasks:**

- [ ] **`I29-S01-T01`**
  - **File:** `config/privacy/data-inventory.yaml`
  - **Change:** Classify every owned table/field by purpose, sensitivity, retention, exportability, erasure, and backup behavior.
  - **File-level acceptance:** Coverage test finds no unclassified data.
- [ ] **`I29-S01-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/privacy_handlers.py`
  - **Change:** Register module-owned export/erase handlers without generic table access.
  - **File-level acceptance:** Missing handler blocks public-ranked readiness.
- [ ] **`I29-S01-T03`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/privacy-handler.schema.json`
  - **Change:** Define handler capability, version, data classes, limits, and completion receipt.
  - **File-level acceptance:** Schema validation passes.
- [ ] **`I29-S01-T04`**
  - **File:** `tests/privacy/test_data_inventory_coverage.py`
  - **Change:** Compare migrations/schemas/telemetry/log fields to inventory.
  - **File-level acceptance:** Unclassified fixture fails.
- [ ] **`I29-S01-T05`**
  - **File:** `docs/privacy/PRIVACY_THREAT_MODEL.md`
  - **Change:** Document data flows, linkability, inference, exclusion, processors, transfers, and treatments.
  - **File-level acceptance:** Review covers all principal journeys.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I29-S02 — Export integrity

**Stage outcome:** A player receives only their data and player-visible context.

**Tasks:**

- [ ] **`I29-S02-T01`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/export.py`
  - **Change:** Orchestrate authenticated export request status and expiry.
  - **File-level acceptance:** Recent reauthentication is required.
- [ ] **`I29-S02-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/export_workflow.py`
  - **Change:** Collect module projections, stream archive, produce object digests/Merkle root, and expiry receipt.
  - **File-level acceptance:** Partial handler failure is resumable.
- [ ] **`I29-S02-T03`**
  - **File:** `schemas/privacy/export-manifest.schema.json`
  - **Change:** Define files, media types, sizes, digests, Merkle root, omissions, generated time, and expiry.
  - **File-level acceptance:** Manifest validates.
- [ ] **`I29-S02-T04`**
  - **File:** `modules/m16-case-file-submission/backend/src/fga_casefile/export_projection.py`
  - **Change:** Export own drafts/submissions/private text and player-visible evidence references only.
  - **File-level acceptance:** Protected truth/internal source metadata are absent.
- [ ] **`I29-S02-T05`**
  - **File:** `tests/privacy/test_export_integrity.py`
  - **Change:** Verify ownership, completeness, digest/root, expiry, restricted material omission, and no truth.
  - **File-level acceptance:** Tampered archive fails verification.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I29-S03 — Deletion and cryptographic erasure

**Stage outcome:** Deleted private text becomes undecryptable across active and restored storage.

**Tasks:**

- [ ] **`I29-S03-T01`**
  - **File:** `foundation/python/fga_privacy/envelope_encryption.py`
  - **Change:** Implement per-account/per-data-class envelope keys, versioning, rotation, and cryptographic erasure port.
  - **File-level acceptance:** Deleted key makes ciphertext undecryptable.
- [ ] **`I29-S03-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/deletion_workflow.py`
  - **Change:** Orchestrate leaderboard withdrawal, session revocation, handler erasure/pseudonymization, key destruction, tombstones, and backup expiry tracking.
  - **File-level acceptance:** Workflow is idempotent and resumable.
- [ ] **`I29-S03-T03`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/deletion.py`
  - **Change:** Implement confirmation, state transition, account mapping removal, and safe completion status.
  - **File-level acceptance:** Login/recovery cease after finalization.
- [ ] **`I29-S03-T04`**
  - **File:** `modules/m18-leaderboard-results/backend/src/fga_leaderboard/deletion_participant.py`
  - **Change:** Withdraw public entries and sever private ownership mapping.
  - **File-level acceptance:** Public alias no longer links to account.
- [ ] **`I29-S03-T05`**
  - **File:** `tests/privacy/test_backup_erasure.py`
  - **Change:** Restore a pre-deletion backup with destroyed keys/tombstones and prove designated text cannot be decrypted or republished.
  - **File-level acceptance:** Erasure proof passes.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I29-S04 — Consent, telemetry, and end-to-end lifecycle

**Stage outcome:** Material policy changes and preferences remain explicit.

**Tasks:**

- [ ] **`I29-S04-T01`**
  - **File:** `modules/m07-identity-account-security/backend/src/fga_identity/policy_receipts.py`
  - **Change:** Add material-change migration, withdrawal effects, and jurisdiction-specific receipt state.
  - **File-level acceptance:** Existing rounds follow signed compatibility policy.
- [ ] **`I29-S04-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/telemetry_policy.py`
  - **Change:** Enforce coarse consented event schema and Global Privacy Control behavior where applicable.
  - **File-level acceptance:** Raw prompts/notes/evidence/aliases are rejected.
- [ ] **`I29-S04-T03`**
  - **File:** `tests/integration/clusters/privacy/test_privacy_cluster.py`
  - **Change:** Run M07/M15/M16/M18/M20 with export, expiry, withdrawal, deletion, restore, and changed policy.
  - **File-level acceptance:** All module handlers complete.
- [ ] **`I29-S04-T04`**
  - **File:** `tests/e2e/privacy-lifecycle.spec.ts`
  - **Change:** Request export, verify ready/expiry, change preference, withdraw ranking, request/confirm deletion, and verify safe final state.
  - **File-level acceptance:** Journey passes accessibly.
- [ ] **`I29-S04-T05`**
  - **File:** `reports/privacy/DPIA_AND_APPLICABILITY.md`
  - **Change:** Record deployed privacy/legal applicability, processors, transfers, retention, AI notice, and residual risks.
  - **File-level acceptance:** Required approvals are present.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I29 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run privacy inventory, threat-model, handler-contract, export digest, deletion, key destruction, restored-backup, retention, telemetry, and consent migration tests.
- Run privacy cluster with failure injection after each workflow step and duplicate requests.
- Run IDOR and cross-account export/deletion attacks, log/trace/diagnostic redaction, and provider payload privacy scans.
- Run full browser lifecycle and all cumulative game regressions.
- Verify no deletion test uses destructive rewriting of immutable public/historical evidence beyond approved pseudonymization.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I29 exit criteria

- Every player-data class has explicit lifecycle ownership.
- Exports are complete, integrity-verifiable, expiring, and truth-safe.
- Designated private text is cryptographically erasable even after backup restoration.
- Consent, telemetry, withdrawal, and deletion pass end to end.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I30 — Runtime role isolation, deployment epochs, migrations, and container hardening

**Objective:** Compose the exact modular monolith into isolated WEB, MAINTENANCE, EVALUATOR, and MIGRATE roles with reproducible deployment behavior.

**Principal modules:** All modules, Four runtime roles

**Principal interactions:** Role integration

**Prerequisites:**

- I29 is closed.

**Iteration outputs:**

- `I30-S01` — Role entry points and capability registration: Each process loads only allowed modules and capabilities.
- `I30-S02` — Deployment epochs and mixed-version safety: Image, schema, policy, evaluator, provider, and ranking compatibility are bound.
- `I30-S03` — Reproducible hardened image: One lineage produces separate hardened roles.
- `I30-S04` — Migration, rollout, and rollback rehearsal: Deployments preserve historical and active work.

### I30-S01 — Role entry points and capability registration

**Stage outcome:** Each process loads only allowed modules and capabilities.

**Tasks:**

- [ ] **`I30-S01-T01`**
  - **File:** `apps/web/src/fga_web/main.py`
  - **Change:** Finalize WEB composition of player-safe surfaces and role readiness.
  - **File-level acceptance:** Dependency/grant tests prove no truth/migrate privileges.
- [ ] **`I30-S01-T02`**
  - **File:** `apps/maintenance/src/fga_maintenance/main.py`
  - **Change:** Compose durable workflow handlers, provider calls, exports/deletion, safe finalizer, retention, and reindex.
  - **File-level acceptance:** No generic protected-truth repository is available.
- [ ] **`I30-S01-T03`**
  - **File:** `apps/evaluator/src/fga_evaluator/main.py`
  - **Change:** Compose private evaluation claim, Truth Broker, evaluator, signing, and safe verdict output.
  - **File-level acceptance:** No public HTTP ingress is registered.
- [ ] **`I30-S01-T04`**
  - **File:** `apps/migrate/src/fga_migrate/main.py`
  - **Change:** Compose module migrations, publication compiler/activation, verifier policy, and rollback commands.
  - **File-level acceptance:** No player/session functionality is present.
- [ ] **`I30-S01-T05`**
  - **File:** `config/runtime/role-capabilities.yaml`
  - **Change:** Declare modules, commands, DB roles, secrets, network destinations, health dependencies, and denied capabilities per role.
  - **File-level acceptance:** Runtime fitness tests match actual composition.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I30-S02 — Deployment epochs and mixed-version safety

**Stage outcome:** Image, schema, policy, evaluator, provider, and ranking compatibility are bound.

**Tasks:**

- [ ] **`I30-S02-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/contracts/deployment-epoch.schema.json`
  - **Change:** Define image digest, role versions, schema epoch, policy, evaluator, provider capability, publication, and compatibility window.
  - **File-level acceptance:** Schema validation passes.
- [ ] **`I30-S02-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/deployment_epoch.py`
  - **Change:** Implement startup registration, compatibility decision, stale-role fencing, drain, and admission.
  - **File-level acceptance:** N-1/N matrix passes.
- [ ] **`I30-S02-T03`**
  - **File:** `config/runtime/compatibility-matrix.yaml`
  - **Change:** Declare supported role/schema/contract combinations and migration barriers.
  - **File-level acceptance:** Every planned rollout/rollback path is represented.
- [ ] **`I30-S02-T04`**
  - **File:** `tests/integration/roles/test_mixed_versions.py`
  - **Change:** Run N-1/N, stale WEB, stale MAINTENANCE, evaluator replacement, and incompatible schema scenarios.
  - **File-level acceptance:** Unsafe role is fenced before mutation.
- [ ] **`I30-S02-T05`**
  - **File:** `tests/resilience/test_role_drain.py`
  - **Change:** Drain in-flight accepted work before incompatible replacement.
  - **File-level acceptance:** No command/evaluation is lost or double-settled.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I30-S03 — Reproducible hardened image

**Stage outcome:** One lineage produces separate hardened roles.

**Tasks:**

- [ ] **`I30-S03-T01`**
  - **File:** `Dockerfile`
  - **Change:** Build frontend and Python runtime hermetically, copy approved artifacts only, run rootless/read-only, and expose role entrypoints.
  - **File-level acceptance:** Image rebuild digest is reproducible within declared constraints.
- [ ] **`I30-S03-T02`**
  - **File:** `.dockerignore`
  - **Change:** Exclude source secrets, raw authoring truth, reports not intended for runtime, node_modules, caches, and raw media projects.
  - **File-level acceptance:** Image-content scan passes.
- [ ] **`I30-S03-T03`**
  - **File:** `config/runtime/container-hardening.yaml`
  - **Change:** Declare nonroot UID, read-only filesystem, dropped capabilities, no-new-privileges, bounded tmpfs, core-dump disable, and resource limits.
  - **File-level acceptance:** Container inspection verifies settings.
- [ ] **`I30-S03-T04`**
  - **File:** `scripts/image_inspect.py`
  - **Change:** Check contents, permissions, roles, source maps, secrets, truth, raw assets, and dependency manifests.
  - **File-level acceptance:** Deliberate forbidden file fixture fails.
- [ ] **`I30-S03-T05`**
  - **File:** `tests/container/test_role_images.py`
  - **Change:** Start each role from the same image digest with distinct config/grants and verify readiness.
  - **File-level acceptance:** Only WEB exposes public port.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I30-S04 — Migration, rollout, and rollback rehearsal

**Stage outcome:** Deployments preserve historical and active work.

**Tasks:**

- [ ] **`I30-S04-T01`**
  - **File:** `docs/runbooks/DEPLOYMENT.md`
  - **Change:** Define preflight, migrate, role rollout order, epoch verification, smoke, drain, and rollback.
  - **File-level acceptance:** Runbook steps map to automated commands.
- [ ] **`I30-S04-T02`**
  - **File:** `docs/runbooks/DATABASE_RESTORE.md`
  - **Change:** Define PITR/restore, validation, key/tombstone handling, and return-to-service.
  - **File-level acceptance:** Exercise references test evidence.
- [ ] **`I30-S04-T03`**
  - **File:** `tests/deployment/test_expand_contract_rollout.py`
  - **Change:** Run old app/new schema, new app/new schema, backfill, switch, and compatibility window.
  - **File-level acceptance:** No downtime invariant violation occurs.
- [ ] **`I30-S04-T04`**
  - **File:** `tests/deployment/test_rollback.py`
  - **Change:** Rollback image and publication pointer only to compatible trusted state.
  - **File-level acceptance:** Historical rounds remain reproducible.
- [ ] **`I30-S04-T05`**
  - **File:** `reports/iteration-30/role-matrix.json`
  - **Change:** Record exact image digest, role dependencies, grants, network, secrets, and readiness evidence.
  - **File-level acceptance:** Schema and digest validation pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I30 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Build exact image twice, inspect contents, and start all four roles with distinct identities/grants/networks.
- Run all role integration, mixed-version, epoch, stale-client, drain, migration, backfill, rollback, and restore tests.
- Run truth/key/secret/source-map/image-content scans on each role.
- Run complete E2E through WEB/MAINTENANCE/EVALUATOR/MIGRATE composition.
- Run all cumulative module, interaction, cluster, Academy, and production-case suites.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I30 exit criteria

- Four role boundaries are operational and least-privilege.
- Unsafe mixed versions are fenced and accepted work drains safely.
- The image is hardened, reproducible, and free of protected/runtime-forbidden artifacts.
- Migration, deployment, rollback, and restore rehearsals pass.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I31 — Security, browser isolation, LLM assurance, and software supply chain

**Objective:** Complete defense-in-depth controls and release evidence for web, API, provider, dependencies, and signed artifacts.

**Principal modules:** All modules, M19, M20, Runtime roles

**Principal interactions:** Security/privacy/supply chain

**Prerequisites:**

- I30 is closed.

**Iteration outputs:**

- `I31-S01` — Browser and HTTP security profile: All routes use a signed tested header and active-content policy.
- `I31-S02` — Application/API verification: Security controls map to executable requirements.
- `I31-S03` — Supply-chain integrity: Dependencies and build provenance are pinned and verifiable.
- `I31-S04` — Signing, trust rotation, and incident controls: Release trust can rotate, revoke, quarantine, and verify offline.

### I31-S01 — Browser and HTTP security profile

**Stage outcome:** All routes use a signed tested header and active-content policy.

**Tasks:**

- [ ] **`I31-S01-T01`**
  - **File:** `config/security/header-profile.yaml`
  - **Change:** Define CSP, Trusted Types decision, HSTS, Referrer-Policy, Permissions-Policy, framing, COOP/CORP/COEP decision, MIME, Fetch Metadata, and reporting minimization.
  - **File-level acceptance:** Every public/private route has an explicit profile.
- [ ] **`I31-S01-T02`**
  - **File:** `apps/web/src/fga_web/security_headers.py`
  - **Change:** Generate route-aware headers from signed profile and validate Fetch Metadata/origin.
  - **File-level acceptance:** Header tests match policy exactly.
- [ ] **`I31-S01-T03`**
  - **File:** `apps/web-ui/src/trustedTypes.ts`
  - **Change:** Implement approved DOM policy or explicit no-policy enforcement and sink inventory hooks.
  - **File-level acceptance:** Unapproved string-to-DOM sink fails tests.
- [ ] **`I31-S01-T04`**
  - **File:** `config/security/dom-sinks.yaml`
  - **Change:** Inventory all HTML/script/URL/message sinks, owners, sanitizers, and exceptions.
  - **File-level acceptance:** Static scan finds no unregistered sink.
- [ ] **`I31-S01-T05`**
  - **File:** `tests/security/browser_header_profile.spec.ts`
  - **Change:** Exercise framing, cross-origin resources, postMessage origin, Fetch Metadata, CSP, and Trusted Types attacks.
  - **File-level acceptance:** All unauthorized paths are blocked.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I31-S02 — Application/API verification

**Stage outcome:** Security controls map to executable requirements.

**Tasks:**

- [ ] **`I31-S02-T01`**
  - **File:** `config/security/asvs-mapping.yaml`
  - **Change:** Map applicable ASVS controls to modules/tests/evidence.
  - **File-level acceptance:** No applicable control lacks a test or approved exception.
- [ ] **`I31-S02-T02`**
  - **File:** `config/security/llmsvs-mapping.yaml`
  - **Change:** Map live retrieval to LLMSVS/AISVS/AI RMF controls for injection, authorization, lifecycle, output, logging, privacy, and incident response.
  - **File-level acceptance:** Every control has owner/evidence.
- [ ] **`I31-S02-T03`**
  - **File:** `tests/security/api_attack_suite.py`
  - **Change:** Exercise IDOR, mass assignment, injection, SSRF, resource exhaustion, unsafe provider data, CSRF, fixation, and abuse limits.
  - **File-level acceptance:** All attacks fail safely.
- [ ] **`I31-S02-T04`**
  - **File:** `tests/security/truth_noninterference_suite.py`
  - **Change:** Scan imports, grants, APIs, logs, traces, assets, docs, diagnostics, exports, and provider payloads for truth leakage.
  - **File-level acceptance:** Zero leak tolerance passes.
- [ ] **`I31-S02-T05`**
  - **File:** `tests/security/redaction_cardinality_suite.py`
  - **Change:** Verify safe logging fields, redaction, and low-cardinality labels under malicious inputs.
  - **File-level acceptance:** No private/high-cardinality payload enters telemetry.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I31-S03 — Supply-chain integrity

**Stage outcome:** Dependencies and build provenance are pinned and verifiable.

**Tasks:**

- [ ] **`I31-S03-T01`**
  - **File:** `config/supply-chain/registries.yaml`
  - **Change:** Pin approved Python/npm/JVM/container registries, namespaces, packages, hashes, and mirror policy.
  - **File-level acceptance:** Dependency-confusion fixtures fail.
- [ ] **`I31-S03-T02`**
  - **File:** `scripts/generate_sbom.py`
  - **Change:** Generate validated CycloneDX/SPDX SBOMs for source, image, and role composition.
  - **File-level acceptance:** SBOM schema and completeness checks pass.
- [ ] **`I31-S03-T03`**
  - **File:** `scripts/generate_provenance.py`
  - **Change:** Generate signed build provenance, source/ref/workflow, materials, outputs, and reproducibility evidence.
  - **File-level acceptance:** Verifier policy accepts only expected workflow.
- [ ] **`I31-S03-T04`**
  - **File:** `config/supply-chain/vulnerability-policy.yaml`
  - **Change:** Define severity, exploitability, applicability/VEX, SLA, exceptions, and release blocking.
  - **File-level acceptance:** Known vulnerable fixture blocks unless valid nonaffected evidence exists.
- [ ] **`I31-S03-T05`**
  - **File:** `tests/supply_chain/test_dependency_identity.py`
  - **Change:** Probe typosquatting, alternate registry, mutable tag, hash mismatch, and provenance mismatch.
  - **File-level acceptance:** All are rejected.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I31-S04 — Signing, trust rotation, and incident controls

**Stage outcome:** Release trust can rotate, revoke, quarantine, and verify offline.

**Tasks:**

- [ ] **`I31-S04-T01`**
  - **File:** `config/security/verifier-policy.yaml`
  - **Change:** Bind signer/issuer, repository/ref, workflow, artifact type, digest, attestations, freshness, transparency, and revocation.
  - **File-level acceptance:** Unknown signer/workflow fails.
- [ ] **`I31-S04-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/trust_rotation.py`
  - **Change:** Implement staged key rotation, overlap, revocation, offline bundle verification, and emergency quarantine.
  - **File-level acceptance:** Historical valid artifacts remain explainable.
- [ ] **`I31-S04-T03`**
  - **File:** `docs/runbooks/SECURITY_INCIDENT.md`
  - **Change:** Define secret/truth/provider/dependency/publication incidents, containment, evidence, player notice, and recovery.
  - **File-level acceptance:** Runbook links kill switches that only narrow behavior.
- [ ] **`I31-S04-T04`**
  - **File:** `tests/security/test_trust_rotation.py`
  - **Change:** Exercise old/new keys, expired metadata, revocation, offline verification, and anti-downgrade.
  - **File-level acceptance:** All decisions match policy.
- [ ] **`I31-S04-T05`**
  - **File:** `reports/security/SECURITY_CASE.md`
  - **Change:** Assemble control mappings, threat models, scans, penetration results, exceptions, and approvals.
  - **File-level acceptance:** No unresolved severity-1/2 issue remains.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I31 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run browser header/CSP/Trusted Types/Fetch Metadata/cross-origin attack suites on exact image.
- Run complete API, identity, cache, truth, provider injection, data authorization, output firewall, abuse, and redaction tests.
- Generate and validate SBOM/provenance/signatures; run vulnerability/applicability, dependency identity, revocation, rotation, and anti-downgrade tests.
- Run independent penetration test scripts and mutation/fault injection for critical security checks.
- Run all cumulative functional, accessibility, privacy, resilience, and production-case regressions.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I31 exit criteria

- Browser, API, provider, and runtime security profiles are executable and signed.
- Truth, secrets, private content, and rich provider output remain outside public/log surfaces.
- Dependencies, SBOM, provenance, signatures, and verifier policy are complete.
- No unresolved release-blocking security issue remains.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I32 — Full accessibility, localization, and inclusive interaction qualification

**Objective:** Qualify every critical journey, case family, dynamic state, and alternative interaction path against the accessibility target.

**Principal modules:** M01–M06, M12, M16–M18, All cases

**Principal interactions:** Media/accessibility cluster

**Prerequisites:**

- I31 is closed.

**Iteration outputs:**

- `I32-S01` — Dynamic journey traces: Accessibility evidence records complete interactions, not only static scans.
- `I32-S02` — Graph, dense case, and cognitive-load hardening: Senior complexity remains understandable and operable.
- `I32-S03` — Localization robustness: Locale changes cannot change authoritative semantics.
- `I32-S04` — Human conformance review: Automated evidence is supplemented by manual expert review.

### I32-S01 — Dynamic journey traces

**Stage outcome:** Accessibility evidence records complete interactions, not only static scans.

**Tasks:**

- [ ] **`I32-S01-T01`**
  - **File:** `tools/accessibility/trace_recorder.ts`
  - **Change:** Capture keyboard events, focus, accessibility-tree snapshots, live regions, timing, screenshots, and route state.
  - **File-level acceptance:** Trace is deterministic and privacy-redacted.
- [ ] **`I32-S01-T02`**
  - **File:** `schemas/accessibility/dynamic-trace.schema.json`
  - **Change:** Define journey steps, expected focus/announcement/state, artifacts, and human review.
  - **File-level acceptance:** Schema validation passes.
- [ ] **`I32-S01-T03`**
  - **File:** `config/accessibility/critical-journeys.yaml`
  - **Change:** Register authentication, catalogue, investigation, actions, saves, case file, submission, verdict, ranking, export/deletion, and recovery journeys.
  - **File-level acceptance:** Every core function has at least one noncanvas/noaudio path.
- [ ] **`I32-S01-T04`**
  - **File:** `tests/accessibility/dynamic/all-critical.spec.ts`
  - **Change:** Record and validate all critical journey traces.
  - **File-level acceptance:** No focus loss, unlabeled control, missing announcement, or inaccessible recovery remains.
- [ ] **`I32-S01-T05`**
  - **File:** `reports/accessibility/DYNAMIC_TRACE_INDEX.md`
  - **Change:** Index automated traces and human review outcomes.
  - **File-level acceptance:** Every journey has owner and verdict.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I32-S02 — Graph, dense case, and cognitive-load hardening

**Stage outcome:** Senior complexity remains understandable and operable.

**Tasks:**

- [ ] **`I32-S02-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/SemanticGraphNavigator.tsx`
  - **Change:** Refine neighbor grouping, edge-direction announcements, filter summaries, and large-graph chunking based on traces.
  - **File-level acceptance:** Senior tasks complete without canvas.
- [ ] **`I32-S02-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/InvestigationWorkspace.tsx`
  - **Change:** Add cognitive-load controls for panel focus, progressive detail, and current-view summary.
  - **File-level acceptance:** No gameplay information is hidden exclusively.
- [ ] **`I32-S02-T03`**
  - **File:** `modules/m16-case-file-submission/frontend/src/CaseFileEditor.tsx`
  - **Change:** Refine section navigation, error summary, evidence context, and long-form reflow.
  - **File-level acceptance:** Keyboard and screen-reader completion passes.
- [ ] **`I32-S02-T04`**
  - **File:** `tests/accessibility/senior-dense-cases.spec.ts`
  - **Change:** Run V1–V3 at 320px, 200% zoom, forced colors, reduced motion, touch, and screen-reader-oriented mode.
  - **File-level acceptance:** All critical tasks pass.
- [ ] **`I32-S02-T05`**
  - **File:** `tests/performance/accessibility_modes.spec.ts`
  - **Change:** Verify accessibility modes do not exceed interaction budgets or alter results.
  - **File-level acceptance:** No ranking/scoring difference occurs.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I32-S03 — Localization robustness

**Stage outcome:** Locale changes cannot change authoritative semantics.

**Tasks:**

- [ ] **`I32-S03-T01`**
  - **File:** `modules/m03-localization-messaging/catalogues/es-ES.json`
  - **Change:** Add complete Spanish catalogue for all current functional keys.
  - **File-level acceptance:** Completeness and parameter compatibility pass.
- [ ] **`I32-S03-T02`**
  - **File:** `modules/m03-localization-messaging/frontend/src/localeManager.ts`
  - **Change:** Implement locale selection, persistence as non-sensitive preference, and safe fallback.
  - **File-level acceptance:** Locale switch does not mutate game state.
- [ ] **`I32-S03-T03`**
  - **File:** `tests/localization/test_catalogue_equivalence.py`
  - **Change:** Verify key/parameter/plural/date/number coverage and forbidden baked functional text.
  - **File-level acceptance:** All catalogues are compatible.
- [ ] **`I32-S03-T04`**
  - **File:** `tests/e2e/localization-spanish.spec.ts`
  - **Change:** Run core journey in Spanish with Unicode, long labels, and locale formatting.
  - **File-level acceptance:** Scores/digests/selection semantics match English.
- [ ] **`I32-S03-T05`**
  - **File:** `tests/security/test_bidi_confusables_ui.py`
  - **Change:** Exercise bidi controls, confusable labels, alias moderation, and safe visual isolation.
  - **File-level acceptance:** No spoofing or layout escape occurs.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I32-S04 — Human conformance review

**Stage outcome:** Automated evidence is supplemented by manual expert review.

**Tasks:**

- [ ] **`I32-S04-T01`**
  - **File:** `docs/accessibility/HUMAN_REVIEW_PROTOCOL.md`
  - **Change:** Define browser/AT matrix, tasks, severity, evidence, retest, and sign-off.
  - **File-level acceptance:** Protocol covers all critical journeys.
- [ ] **`I32-S04-T02`**
  - **File:** `reports/accessibility/HUMAN_REVIEW_RESULTS.md`
  - **Change:** Record keyboard, screen reader, zoom/reflow, contrast, reduced motion, touch, audio-off, and cognitive review.
  - **File-level acceptance:** All blockers are resolved or release is stopped.
- [ ] **`I32-S04-T03`**
  - **File:** `docs/accessibility/CONFORMANCE_STATEMENT_DRAFT.md`
  - **Change:** Prepare scope, target, limitations, contacts, and known nonblocking issues.
  - **File-level acceptance:** Matches tested release, not aspirational features.
- [ ] **`I32-S04-T04`**
  - **File:** `config/testing/mandatory-regressions.yaml`
  - **Change:** Promote all critical accessibility traces and locale compatibility to release-mandatory.
  - **File-level acceptance:** They cannot be skipped by impact analysis.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I32 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run all automated accessibility scanners plus dynamic traces for every critical journey.
- Run list/graph/document/semantic parity, noaudio, nomotion, keyboard, screen-reader-oriented, touch, zoom, reflow, contrast, and error recovery tests.
- Run English/Spanish catalogue, Unicode, bidi, long-text, date/number, and semantic-equivalence tests.
- Complete human review and retest every identified blocker.
- Run all cumulative security, gameplay, case, and performance gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I32 exit criteria

- Every critical task has an equivalent accessible completion path.
- Dynamic focus, announcements, errors, delayed work, and recovery are verified.
- English and Spanish UI preserve identical authoritative gameplay semantics.
- Human accessibility review has no unresolved blocker.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I33 — Performance, capacity, queue fairness, and long-session resilience

**Objective:** Prove bounded performance and capacity without weakening correctness, privacy, fairness, or accessibility.

**Principal modules:** All modules, M12, M13, M17, M19, M20

**Principal interactions:** Operational resilience cluster

**Prerequisites:**

- I32 is closed.

**Iteration outputs:**

- `I33-S01` — Budgets and workload models: Every critical operation has explicit bounded expectations.
- `I33-S02` — Backend and database optimization: Optimize through owned indexes/queries without cross-module coupling.
- `I33-S03` — Frontend and graph optimization: Dense cases stay responsive and leak-free.
- `I33-S04` — Capacity, fairness, and overload behavior: Overload degrades explicitly and preserves accepted work.

### I33-S01 — Budgets and workload models

**Stage outcome:** Every critical operation has explicit bounded expectations.

**Tasks:**

- [ ] **`I33-S01-T01`**
  - **File:** `config/performance/budgets.yaml`
  - **Change:** Define p50/p95/p99 or bounded budgets for health, auth, catalogue, round, workspace, quote, accept, status, save, submit, verdict, ranking, export, graph, and queues.
  - **File-level acceptance:** Every measured operation has fixture size and environment.
- [ ] **`I33-S01-T02`**
  - **File:** `config/performance/workloads.yaml`
  - **Change:** Define expected/burst concurrency, case/profile data sizes, provider latency, evaluator load, and workflow classes.
  - **File-level acceptance:** Workloads are reproducible.
- [ ] **`I33-S01-T03`**
  - **File:** `tools/performance/runner.py`
  - **Change:** Execute API/DB/workflow/evaluator workloads and emit normalized evidence.
  - **File-level acceptance:** Runner fails on missing sample or budget breach.
- [ ] **`I33-S01-T04`**
  - **File:** `tools/performance/browser.ts`
  - **Change:** Measure startup, interaction, graph render/update, memory, long session, and accessibility modes.
  - **File-level acceptance:** Metrics are stable and privacy-safe.
- [ ] **`I33-S01-T05`**
  - **File:** `reports/performance/BASELINE.md`
  - **Change:** Record hardware/environment, datasets, methods, confidence, and initial results.
  - **File-level acceptance:** No unsupported extrapolation is made.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I33-S02 — Backend and database optimization

**Stage outcome:** Optimize through owned indexes/queries without cross-module coupling.

**Tasks:**

- [ ] **`I33-S02-T01`**
  - **File:** `modules/m12-workspace-projection/backend/migrations/0001_projection_indexes.sql`
  - **Change:** Add owned projection-support indexes or materialized read structures.
  - **File-level acceptance:** Query plans meet list/document budgets.
- [ ] **`I33-S02-T02`**
  - **File:** `modules/m13-action-command/backend/migrations/0002_command_indexes.sql`
  - **Change:** Add pending/due/idempotency/status indexes.
  - **File-level acceptance:** Queue/status plans meet budgets.
- [ ] **`I33-S02-T03`**
  - **File:** `modules/m17-evaluation-scoring-ending/backend/migrations/0002_evaluation_indexes.sql`
  - **Change:** Add safe request/verdict/amendment indexes.
  - **File-level acceptance:** Evaluation lookup/finalization budgets pass.
- [ ] **`I33-S02-T04`**
  - **File:** `modules/m19-retrieval-provider-gateway/backend/migrations/0003_retrieval_indexes.sql`
  - **Change:** Add plan/resolver/conversation/cost/cleanup indexes.
  - **File-level acceptance:** Resolver/capacity cleanup budgets pass.
- [ ] **`I33-S02-T05`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/migrations/0003_workflow_indexes.sql`
  - **Change:** Add due-work, lease, deadline, class, and poison-quarantine indexes.
  - **File-level acceptance:** Claim/fairness budgets pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I33-S03 — Frontend and graph optimization

**Stage outcome:** Dense cases stay responsive and leak-free.

**Tasks:**

- [ ] **`I33-S03-T01`**
  - **File:** `modules/m12-workspace-projection/frontend/src/GraphWorkspace.tsx`
  - **Change:** Optimize incremental updates, layout scheduling, listener disposal, and bounded rendering.
  - **File-level acceptance:** Memory and interaction budgets pass.
- [ ] **`I33-S03-T02`**
  - **File:** `modules/m12-workspace-projection/frontend/src/ListWorkspace.tsx`
  - **Change:** Optimize pagination/virtualization and avoid unnecessary projection recomputation.
  - **File-level acceptance:** Accessibility semantics remain intact.
- [ ] **`I33-S03-T03`**
  - **File:** `modules/m01-application-shell-navigation/frontend/src/bootstrap.ts`
  - **Change:** Optimize route code splitting and preload only required public assets.
  - **File-level acceptance:** Bundle/startup budgets pass.
- [ ] **`I33-S03-T04`**
  - **File:** `modules/m04-asset-resource-management/frontend/src/assetResolver.ts`
  - **Change:** Optimize responsive variant selection and deduplicated loads.
  - **File-level acceptance:** No private cache behavior changes.
- [ ] **`I33-S03-T05`**
  - **File:** `tests/performance/long-session.spec.ts`
  - **Change:** Exercise repeated routes/actions/views/saves for a long deterministic session.
  - **File-level acceptance:** No unbounded memory/listener/cache growth.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I33-S04 — Capacity, fairness, and overload behavior

**Stage outcome:** Overload degrades explicitly and preserves accepted work.

**Tasks:**

- [ ] **`I33-S04-T01`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/scheduler.py`
  - **Change:** Tune weighted fairness, deadlines, per-class concurrency, backpressure, and poison quarantine.
  - **File-level acceptance:** Interactive work is not starved by exports/retention.
- [ ] **`I33-S04-T02`**
  - **File:** `modules/m20-publication-workflow-runtime-control/backend/src/fga_platform/admission.py`
  - **Change:** Enforce DB pool, executor heartbeat, queue age, evaluator backlog, key, provider capacity, and budget health.
  - **File-level acceptance:** Unhealthy admission closes before breach.
- [ ] **`I33-S04-T03`**
  - **File:** `tests/performance/test_queue_fairness.py`
  - **Change:** Load interactive, evaluation, export, deletion, and retention classes with slow/poison jobs.
  - **File-level acceptance:** Deadlines/fairness invariants pass.
- [ ] **`I33-S04-T04`**
  - **File:** `tests/resilience/test_capacity_exhaustion.py`
  - **Change:** Exercise DB pool, disk/tmp, provider conversations, rate limits, evaluator queue, and browser graph caps.
  - **File-level acceptance:** System fails closed with safe status.
- [ ] **`I33-S04-T05`**
  - **File:** `reports/performance/QUALIFICATION.md`
  - **Change:** Record final distributions, capacity ceilings, bottlenecks, and headroom.
  - **File-level acceptance:** All budgets pass or release remains blocked.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I33 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run API/database/browser/graph/evaluator/resolver/workflow p50/p95/p99 suites at expected and burst loads.
- Run long-session, memory, connection, listener, cache, and queue-leak tests.
- Run admission, fairness, deadline, overload, capacity exhaustion, poison work, and recovery tests.
- Repeat accessibility-mode and deterministic-result checks under load.
- Run all cumulative functional, security, privacy, case, and deployment tests.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I33 exit criteria

- All critical operations meet signed budgets at declared workloads.
- Queues preserve fairness/deadlines and accepted work under overload.
- No optimization weakens module boundaries, accessibility, determinism, or privacy.
- Capacity/headroom and safe admission limits are documented and tested.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I34 — Chaos, disaster recovery, key loss, and operational game days

**Objective:** Execute destructive failure scenarios against the exact release topology and prove invariant-preserving recovery.

**Principal modules:** All modules, All runtime roles

**Principal interactions:** Operational resilience cluster, Release lane

**Prerequisites:**

- I33 is closed; backup/restore and staging topology are available.

**Iteration outputs:**

- `I34-S01` — Chaos harness: Failures are injected at controlled, auditable points.
- `I34-S02` — Workflow/provider/evaluator failures: Accepted commands and submissions settle once or remain safely held.
- `I34-S03` — Database, deployment, and publication failures: Historical integrity survives infrastructure incidents.
- `I34-S04` — Full game day: Operators execute the complete incident sequence.

### I34-S01 — Chaos harness

**Stage outcome:** Failures are injected at controlled, auditable points.

**Tasks:**

- [ ] **`I34-S01-T01`**
  - **File:** `tools/chaos/scenario.schema.json`
  - **Change:** Define preconditions, injection, expected invariant, observations, recovery, residual risk, and approval.
  - **File-level acceptance:** Scenario files validate.
- [ ] **`I34-S01-T02`**
  - **File:** `tools/chaos/runner.py`
  - **Change:** Execute role/process/network/DB/key/provider/publication failures and collect evidence.
  - **File-level acceptance:** Runner restores baseline or marks environment unsafe.
- [ ] **`I34-S01-T03`**
  - **File:** `config/chaos/scenarios.yaml`
  - **Change:** Register executor loss, provider timeout/capacity, DB failover, key unavailable, stale client, partial deployment, split brain, and restoration.
  - **File-level acceptance:** Every mandatory scenario is present.
- [ ] **`I34-S01-T04`**
  - **File:** `tests/chaos/test_harness_safety.py`
  - **Change:** Verify guardrails, environment identity, abort, cleanup, and evidence capture.
  - **File-level acceptance:** Production target without explicit authorization is rejected.
- [ ] **`I34-S01-T05`**
  - **File:** `docs/runbooks/CHAOS_GAME_DAY.md`
  - **Change:** Define roles, stop conditions, communication, invariant checklist, and sign-off.
  - **File-level acceptance:** Runbook maps to scenarios.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I34-S02 — Workflow/provider/evaluator failures

**Stage outcome:** Accepted commands and submissions settle once or remain safely held.

**Tasks:**

- [ ] **`I34-S02-T01`**
  - **File:** `tests/chaos/scenarios/maintenance-loss.yaml`
  - **Change:** Kill MAINTENANCE during claim, external call, and settlement.
  - **File-level acceptance:** Lease/fence recovery produces one outcome.
- [ ] **`I34-S02-T02`**
  - **File:** `tests/chaos/scenarios/provider-failure.yaml`
  - **Change:** Inject timeout, unknown submission, malformed result, cap exhaustion, deletion lag, and budget stop.
  - **File-level acceptance:** No blind retry or evidence variation occurs.
- [ ] **`I34-S02-T03`**
  - **File:** `tests/chaos/scenarios/evaluator-key-loss.yaml`
  - **Change:** Remove truth access or signing key before/during/after evaluation.
  - **File-level acceptance:** Submission remains immutable; no unsafe verdict is emitted.
- [ ] **`I34-S02-T04`**
  - **File:** `tests/chaos/scenarios/poison-work.yaml`
  - **Change:** Introduce permanently failing export/provider/evaluation jobs.
  - **File-level acceptance:** Quarantine prevents starvation.
- [ ] **`I34-S02-T05`**
  - **File:** `reports/chaos/WORKFLOW_PROVIDER_EVALUATOR.md`
  - **Change:** Record outcomes, timelines, invariant checks, and repairs.
  - **File-level acceptance:** Every scenario passes or release is blocked.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I34-S03 — Database, deployment, and publication failures

**Stage outcome:** Historical integrity survives infrastructure incidents.

**Tasks:**

- [ ] **`I34-S03-T01`**
  - **File:** `tests/chaos/scenarios/database-failover.yaml`
  - **Change:** Interrupt connections during all constitutional transactions and restore/PITR.
  - **File-level acceptance:** No partial debit/submission/verdict/progression occurs.
- [ ] **`I34-S03-T02`**
  - **File:** `tests/chaos/scenarios/partial-deployment.yaml`
  - **Change:** Deploy mixed role versions and stale workers.
  - **File-level acceptance:** Epoch fencing and drain prevent unsafe mutation.
- [ ] **`I34-S03-T03`**
  - **File:** `tests/chaos/scenarios/publication-revocation.yaml`
  - **Change:** Revoke/quarantine active case/asset/evaluator bundle during new and existing rounds.
  - **File-level acceptance:** New admission closes; incident policy preserves/pauses history.
- [ ] **`I34-S03-T04`**
  - **File:** `tests/chaos/scenarios/backup-restore.yaml`
  - **Change:** Restore backup with deletion tombstones, key state, pending workflows, and publications.
  - **File-level acceptance:** Erasure and exactly-once recovery hold.
- [ ] **`I34-S03-T05`**
  - **File:** `reports/chaos/DATABASE_DEPLOYMENT_PUBLICATION.md`
  - **Change:** Record restoration, RPO/RTO observations, and invariant evidence.
  - **File-level acceptance:** Targets are met.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I34-S04 — Full game day

**Stage outcome:** Operators execute the complete incident sequence.

**Tasks:**

- [ ] **`I34-S04-T01`**
  - **File:** `docs/runbooks/INCIDENT_INDEX.md`
  - **Change:** Index authentication, database, provider, evaluator, publication, secret, truth, asset, leaderboard, and privacy runbooks.
  - **File-level acceptance:** Every alert maps to a runbook.
- [ ] **`I34-S04-T02`**
  - **File:** `config/operations/alert-routing.yaml`
  - **Change:** Map safe alerts to severity, owner, escalation, and runbook without private payload.
  - **File-level acceptance:** Coverage test passes.
- [ ] **`I34-S04-T03`**
  - **File:** `tests/operations/test_runbook_commands.py`
  - **Change:** Verify every documented diagnostic/recovery command exists and is least-privilege.
  - **File-level acceptance:** Stale command references fail.
- [ ] **`I34-S04-T04`**
  - **File:** `reports/chaos/CHAOS_QUALIFICATION_REPORT.md`
  - **Change:** Consolidate signed scenarios, expected/observed behavior, recovery, residual risks, and approvals.
  - **File-level acceptance:** All mandatory scenarios are successful.
- [ ] **`I34-S04-T05`**
  - **File:** `reports/chaos/evidence.json`
  - **Change:** Create digest-bound machine-readable game-day evidence.
  - **File-level acceptance:** Evidence schema and digests pass.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I34 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run every registered chaos scenario against the exact signed candidate topology and database/provider simulators or approved staging services.
- Verify zero duplicate debit/refund/reveal/submission/verdict/progression and zero truth/privacy/accessibility invariant breach.
- Measure restore and recovery objectives; validate pending-work convergence and tombstone/key behavior.
- Retest the complete system after chaos cleanup from a clean environment.
- Run all cumulative release gates.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I34 exit criteria

- All mandatory chaos/game-day scenarios have signed passing evidence.
- Database restore, key loss, provider/evaluator failure, partial deployment, and publication incidents preserve invariants.
- Runbooks, alerts, commands, and owners are complete.
- The environment returns to a fully passing clean state after game day.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I35 — Release candidate convergence, freeze, and immutable evidence

**Objective:** Freeze one exact artifact and prove that all requirements, modules, interactions, cases, roles, migrations, and quality gates are satisfied.

**Principal modules:** All modules, All cases, All roles

**Principal interactions:** Complete solution

**Prerequisites:**

- I34 is closed; no unresolved release-blocking defect exists.

**Iteration outputs:**

- `I35-S01` — Requirement and contract freeze: The current release graph is complete and internally consistent.
- `I35-S02` — Full clean qualification: All test layers run from a clean checkout against exact candidate.
- `I35-S03` — Artifact creation and verification: The artifact deployed is exactly the artifact tested.
- `I35-S04` — Freeze control: No code or publication changes after evidence without invalidating the candidate.

### I35-S01 — Requirement and contract freeze

**Stage outcome:** The current release graph is complete and internally consistent.

**Tasks:**

- [ ] **`I35-S01-T01`**
  - **File:** `config/governance/release-candidate.json`
  - **Change:** Bind normative pair, modular pack, module/contract versions, case/asset/evaluator publications, policy, provider capability, schema, and deployment epoch.
  - **File-level acceptance:** All IDs/digests resolve.
- [ ] **`I35-S01-T02`**
  - **File:** `docs/release/RELEASE_NOTES.md`
  - **Change:** Document player-visible features, modes, limitations, privacy, accessibility, provider behavior, and compatibility.
  - **File-level acceptance:** No unverified claim appears.
- [ ] **`I35-S01-T03`**
  - **File:** `docs/release/KNOWN_ISSUES.md`
  - **Change:** List only approved nonblocking issues with owner, impact, workaround, and expiry.
  - **File-level acceptance:** No severity-1/2 or constitutional issue is listed as nonblocking.
- [ ] **`I35-S01-T04`**
  - **File:** `reports/traceability/CONFORMANCE_GRAPH.json`
  - **Change:** Generate complete requirement→module→contract→task→test→evidence→artifact graph.
  - **File-level acceptance:** No orphan, stale version, duplicate, or contradictory predicate remains.
- [ ] **`I35-S01-T05`**
  - **File:** `tests/governance/test_release_graph.py`
  - **Change:** Verify release graph, current normative layer, document links, migrations, diagrams, and manifests.
  - **File-level acceptance:** Any stale ID blocks freeze.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I35-S02 — Full clean qualification

**Stage outcome:** All test layers run from a clean checkout against exact candidate.

**Tasks:**

- [ ] **`I35-S02-T01`**
  - **File:** `config/testing/release-suite.yaml`
  - **Change:** Pin complete module, contract, pairwise, cluster, role, E2E, accessibility, security, privacy, performance, chaos, migration, and case suites.
  - **File-level acceptance:** No test target is dynamically omitted.
- [ ] **`I35-S02-T02`**
  - **File:** `scripts/release_qualify`
  - **Change:** Build clean, run complete suite, collect reports, and fail on retry-only green, missing, skipped-critical, or quarantined-critical results.
  - **File-level acceptance:** Dry run with deliberate failure blocks.
- [ ] **`I35-S02-T03`**
  - **File:** `reports/release-candidate/test-results.json`
  - **Change:** Record normalized results, seeds, environments, durations, and artifacts.
  - **File-level acceptance:** All statuses are passing.
- [ ] **`I35-S02-T04`**
  - **File:** `reports/release-candidate/coverage.json`
  - **Change:** Record requirement, branch/rule, mutation, interaction, case strategy, and accessibility journey coverage.
  - **File-level acceptance:** Required thresholds and mappings pass.
- [ ] **`I35-S02-T05`**
  - **File:** `reports/release-candidate/qualification.md`
  - **Change:** Summarize exact commands and outcomes without replacing machine evidence.
  - **File-level acceptance:** Every claim links to result.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I35-S03 — Artifact creation and verification

**Stage outcome:** The artifact deployed is exactly the artifact tested.

**Tasks:**

- [ ] **`I35-S03-T01`**
  - **File:** `scripts/release_build.py`
  - **Change:** Build image, static assets, case/evaluator bundles, SBOM, provenance, signatures, and offline verification package.
  - **File-level acceptance:** Outputs are content-addressed.
- [ ] **`I35-S03-T02`**
  - **File:** `reports/release-candidate/artifact-manifest.json`
  - **Change:** List every artifact, digest, signer, source, workflow, verifier policy, and publication status.
  - **File-level acceptance:** Manifest verifies offline.
- [ ] **`I35-S03-T03`**
  - **File:** `reports/release-candidate/image-inspection.json`
  - **Change:** Record role contents, packages, permissions, source/truth/secret scans, and hardening.
  - **File-level acceptance:** No forbidden content exists.
- [ ] **`I35-S03-T04`**
  - **File:** `reports/release-candidate/migration-restore-rollback.json`
  - **Change:** Record final migration, backup/restore, deployment epoch, drain, and rollback rehearsal.
  - **File-level acceptance:** Every supported path passes.
- [ ] **`I35-S03-T05`**
  - **File:** `reports/release-candidate/approvals.yaml`
  - **Change:** Collect product, architecture, QA, security, privacy, accessibility, legal/content, data, SRE, and release approvals.
  - **File-level acceptance:** All required independent approvals are present.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I35-S04 — Freeze control

**Stage outcome:** No code or publication changes after evidence without invalidating the candidate.

**Tasks:**

- [ ] **`I35-S04-T01`**
  - **File:** `config/governance/freeze-policy.yaml`
  - **Change:** Define frozen paths, allowed evidence-only updates, invalidation triggers, and emergency unfreeze procedure.
  - **File-level acceptance:** CI rejects prohibited post-freeze change.
- [ ] **`I35-S04-T02`**
  - **File:** `.github/workflows/release-freeze.yml`
  - **Change:** Verify candidate digest, branch/tag, signatures, evidence, approvals, and unchanged frozen inputs.
  - **File-level acceptance:** Changed input invalidates release.
- [ ] **`I35-S04-T03`**
  - **File:** `docs/release/DEPLOYMENT_CHECKLIST.md`
  - **Change:** Create exact predeploy/deploy/verify/rollback checklist referencing artifact digests.
  - **File-level acceptance:** Checklist contains no rebuild step.
- [ ] **`I35-S04-T04`**
  - **File:** `reports/release-candidate/FINAL_DECISION.md`
  - **Change:** Record approve/reject decision and exact frozen digests.
  - **File-level acceptance:** Approval is impossible if any gate is not passing.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I35 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Run the complete release suite twice from independent clean environments using the same frozen inputs.
- Compare all deterministic outputs and explain only declared nondeterminism.
- Verify every module independently, all interaction edges pairwise, all eight clusters, all roles, all Academy/Lab and production cases, and all whole-solution journeys.
- Run complete security/privacy/accessibility/performance/chaos/migration/restore/rollback/supply-chain evidence.
- Invalidate the candidate on any code, dependency, policy, case, asset, evaluator, schema, or configuration change.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I35 exit criteria

- All current requirements and interactions have passing executable evidence.
- Two independent clean qualifications pass for the exact frozen inputs.
- Artifact, publications, SBOM, provenance, signatures, approvals, and rollback evidence are complete.
- The candidate is frozen by digest and ready for deployment without rebuild.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## I36 — Production deployment, verification, and operational handover

**Objective:** Deploy the exact frozen candidate, verify production behavior, retain rollback readiness, and hand over supported operations.

**Principal modules:** All roles, All modules, Operations

**Principal interactions:** Deployment and live verification

**Prerequisites:**

- I35 is closed and an approved production environment exists.

**Iteration outputs:**

- `I36-S01` — Predeployment checks: Production dependencies and legal/operational records match the frozen candidate.
- `I36-S02` — Exact artifact deployment: No production rebuild or mutable package generation occurs.
- `I36-S03` — Production verification: Safe smoke and synthetic journeys prove the deployed system.
- `I36-S04` — Handover and closure: Ownership, support, and future iteration entry are explicit.

### I36-S01 — Predeployment checks

**Stage outcome:** Production dependencies and legal/operational records match the frozen candidate.

**Tasks:**

- [ ] **`I36-S01-T01`**
  - **File:** `config/environments/production.yaml`
  - **Change:** Bind approved domains, regions, DB, provider mode, capabilities, budgets, retention, policy, keys, alerts, and deployment epoch without secrets.
  - **File-level acceptance:** Configuration validates against candidate compatibility.
- [ ] **`I36-S01-T02`**
  - **File:** `reports/deployment/preflight.json`
  - **Change:** Record DNS/TLS, DB backup/PITR, provider capacity/budget, key availability, policy/evaluator/publication signatures, and rollback target.
  - **File-level acceptance:** All checks pass.
- [ ] **`I36-S01-T03`**
  - **File:** `docs/release/DEPLOYMENT_CHECKLIST.md`
  - **Change:** Record the approved operator sequence and named decision points for this deployment.
  - **File-level acceptance:** Every step has evidence destination.
- [ ] **`I36-S01-T04`**
  - **File:** `reports/deployment/go-no-go.md`
  - **Change:** Record final deployment authorization against exact artifact digest.
  - **File-level acceptance:** Digest matches I35.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I36-S02 — Exact artifact deployment

**Stage outcome:** No production rebuild or mutable package generation occurs.

**Tasks:**

- [ ] **`I36-S02-T01`**
  - **File:** `reports/deployment/deployment-record.json`
  - **Change:** Record image digest, role revisions, schema migration, publication pointers, deployment epoch, timestamps, and operators.
  - **File-level acceptance:** Record is signed and schema-valid.
- [ ] **`I36-S02-T02`**
  - **File:** `reports/deployment/migration-output.txt`
  - **Change:** Capture sanitized release-only MIGRATE execution and compatibility result.
  - **File-level acceptance:** No destructive/unapproved migration occurs.
- [ ] **`I36-S02-T03`**
  - **File:** `reports/deployment/role-readiness.json`
  - **Change:** Capture WEB/MAINTENANCE/EVALUATOR readiness, grants, network, epoch, and executor heartbeat.
  - **File-level acceptance:** All roles are compatible and healthy.
- [ ] **`I36-S02-T04`**
  - **File:** `reports/deployment/publication-pointers.json`
  - **Change:** Capture active trusted case/asset/evaluator/policy pointers and anti-downgrade state.
  - **File-level acceptance:** Pointers match candidate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I36-S03 — Production verification

**Stage outcome:** Safe smoke and synthetic journeys prove the deployed system.

**Tasks:**

- [ ] **`I36-S03-T01`**
  - **File:** `config/testing/production-smoke.yaml`
  - **Change:** Define non-destructive health, auth test account, Academy, materialized retrieval, save, submit/evaluate, export initiation, and operator checks.
  - **File-level acceptance:** No real player data or destructive deletion is used.
- [ ] **`I36-S03-T02`**
  - **File:** `reports/deployment/smoke-results.json`
  - **Change:** Record exact production smoke outcomes and correlation IDs.
  - **File-level acceptance:** All tests pass.
- [ ] **`I36-S03-T03`**
  - **File:** `reports/deployment/security-verification.json`
  - **Change:** Record TLS/headers/cookies/origin/cache/role exposure/signature/build digest checks.
  - **File-level acceptance:** All match frozen evidence.
- [ ] **`I36-S03-T04`**
  - **File:** `reports/deployment/observability-verification.json`
  - **Change:** Record safe metrics, logs, traces, alerts, queue, DB, provider, evaluator, and redaction checks.
  - **File-level acceptance:** No private/truth data appears.
- [ ] **`I36-S03-T05`**
  - **File:** `reports/deployment/rollback-readiness.json`
  - **Change:** Verify prior compatible artifact/publication pointer and database restore path remain available.
  - **File-level acceptance:** Rollback can be executed without rebuild.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I36-S04 — Handover and closure

**Stage outcome:** Ownership, support, and future iteration entry are explicit.

**Tasks:**

- [ ] **`I36-S04-T01`**
  - **File:** `docs/operations/SERVICE_HANDBOOK.md`
  - **Change:** Consolidate architecture, roles, SLO targets, dashboards, alerts, runbooks, privacy/security boundaries, and escalation.
  - **File-level acceptance:** All links and commands validate.
- [ ] **`I36-S04-T02`**
  - **File:** `docs/operations/RELEASE_HANDOVER.md`
  - **Change:** Record artifact versions, active publications, known issues, owners, maintenance duties, and next review triggers.
  - **File-level acceptance:** No hidden operational assumption remains.
- [ ] **`I36-S04-T03`**
  - **File:** `reports/deployment/final-acceptance.md`
  - **Change:** Record production acceptance only after all smoke/security/observability/rollback checks pass.
  - **File-level acceptance:** Acceptance is signed by required owners.
- [ ] **`I36-S04-T04`**
  - **File:** `config/governance/current-release.json`
  - **Change:** Set the current release digest, deployment epoch, policy, schema, and publication versions.
  - **File-level acceptance:** Read-only public version endpoint matches.
- [ ] **`I36-S04-T05`**
  - **File:** `reports/iteration-36/evidence.json`
  - **Change:** Create final iteration evidence linking I00–I36 and production deployment.
  - **File-level acceptance:** All digests and test results validate.

**Stage closure:** all tasks above are complete; their file-level checks pass; affected contracts and tests are updated; no stage defect is deferred.

### I36 comprehensive test gate

Run the complete universal gate `G01–G15` for every implemented capability, including all prior iteration regressions. The iteration-specific emphasis is:

- Verify production uses the exact I35 image and publication digests; do not rebuild.
- Run approved production smoke, security header/cache/TLS, role readiness, executor/provider/evaluator/DB, and observability/redaction checks.
- Confirm backup/PITR, rollback target, trust metadata, provider capacity/budget, and incident paging.
- Run the complete non-destructive mandatory production verification suite; any failure triggers stop/rollback according to runbook.
- Close only after final evidence, handover, and current-release record are signed.

**Failure handling:** any failure creates one or more new file-atomic corrective tasks in this iteration. After correction, rerun the failed layer, all affected pairwise/cluster suites, and then the complete clean iteration gate.

### I36 exit criteria

- The exact frozen artifact is deployed with matching epoch and trusted publications.
- All production smoke, security, observability, dependency, and rollback-readiness checks pass.
- Operational ownership and runbooks are complete.
- The project is released only after final evidence is signed; otherwise deployment is rolled back and I36 remains open.
- The evidence bundle validates against `schemas/testing/iteration-evidence.schema.json` and records a passing status.
- The iteration branch is not marked complete and the next iteration does not begin until every criterion is true.

---

## 9. Module-to-iteration implementation map

| Module | Primary implementation and hardening iterations |
|---|---|
| `M01` — Application Shell and Navigation | I08; enhanced I10–I14, I30–I32 |
| `M02` — Presentation System and Accessibility | I05; enhanced I06–I08, I13–I14, I19–I24, I32 |
| `M03` — Localization and Messaging | I05; expanded continuously through I32 |
| `M04` — Asset and Resource Management | I06; case assets I09, I25–I28; hardening I31 |
| `M05` — Audio and Radio | I06; shell integration I08; qualification I32 |
| `M06` — Client State and Synchronization | I08; save integration I20; resilience I30–I34 |
| `M07` — Identity, Account, Policy Receipt, and Privacy Requests | I07; shell I08; privacy lifecycle I29; hardening I31 |
| `M08` — Career, Catalogue, and Progression | I10; round integration I11; progression I24; family paths I26–I28 |
| `M09` — Round and Game-State Engine | I11; submission I22; closure/progression I23–I24 |
| `M10` — Case Content and Rules | I09; analytics I19; Academy/production packages I25–I28 |
| `M11` — Investigation and Visibility Engine | I11–I12; projections I13–I14; action settlement I16–I19 |
| `M12` — Workspace Projection: List, Graph, Documents, and Semantic Navigation | I13–I14; action UI I19; case/performance/accessibility hardening I25–I33 |
| `M13` — Action, Quote, Command, and Settlement Orchestration | I16; retrieval/actions I17–I19; operational hardening I30–I34 |
| `M14` — Investigation Economy and Credit Ledger | I15; command/submission integration I16–I22 |
| `M15` — Save, Checkpoint, Draft History, and Recovery | I20; case-file/privacy integration I21/I29 |
| `M16` — Case File, Claims, Evidence Mapping, and Submission | I21–I22; evaluation integration I23; privacy I29 |
| `M17` — Evaluation, Scoring, Endings, Verdicts, and Amendments | I23; amendments/results I24; cases I25–I28; role/security/chaos I30–I34 |
| `M18` — Leaderboard, Public Results, Moderation, and Disputes | I24; case/ranking I25–I28; privacy I29 |
| `M19` — Retrieval, Deterministic Resolver, and Provider Gateway | I17–I18; four-action integration I19; hardening I31–I34 |
| `M20` — Publication Trust, Durable Workflow, and Runtime Control | I03; CI I04; publication I09; workflows across I16–I24; privacy/runtime/security/chaos I29–I34 |

## 10. Per-module independent qualification checklist

Each module must satisfy its module-pair specification in addition to the iteration tasks. The following cards summarize the independently testable boundary.

### M01 — Application Shell and Navigation

**Architectural intent:** Own the application bootstrap, route lifecycle, global navigation policy, shell-level error recovery, and composition of independently implemented UI modules.

**Owned state/data:**

- route intent and browser-history projection
- shell bootstrap state
- global overlay and announcement state
- safe public build/capability projection
- composition-root registrations

**Required independent tests:**

- route-table unit tests
- guard decision-table tests
- component tests with fake session/capability ports
- browser-history and deep-link tests
- keyboard/focus journey tests
- stale-client and global-error E2E tests
- architecture test forbidding domain repositories in the shell

**Cross-module integration obligations:**

1. Shell + Identity: sign-in redirect and expired-session recovery.
2. Shell + Career/Round: deep-link guards for open, review, and unavailable rounds.
3. Shell + Client Sync: stale revision and incompatible-client recovery.
4. Shell + Radio: route transitions do not restart audio.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M02 — Presentation System and Accessibility

**Architectural intent:** Provide reusable semantic UI primitives and enforce accessibility, interaction, responsive, and visual-consistency contracts independently of game-domain rules.

**Owned state/data:**

- design tokens and semantic component contracts
- focus-management policy
- live-region and status-announcement primitives
- accessible modal and disclosure stack
- responsive layout primitives
- accessibility preference projection

**Required independent tests:**

- isolated story/component tests
- keyboard interaction tests
- automated accessibility scans
- accessibility-tree snapshot tests
- screen-reader-oriented dynamic-flow tests
- forced-colors and reduced-motion tests
- 320px reflow and 200% zoom tests
- DOM sink and CSP tests
- visual-regression tests for semantic states

**Cross-module integration obligations:**

1. Presentation + Workspace: list and semantic graph offer equivalent core tasks.
2. Presentation + Shell: route and modal focus lifecycle.
3. Presentation + Case File: accessible validation summary and evidence mapping.
4. Presentation + Localization: pseudo-localization and bidirectional text.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M03 — Localization and Messaging

**Architectural intent:** Own locale negotiation, versioned message catalogues, safe error-code translation, formatting, Unicode/bidirectional behavior, and deterministic fallback.

**Owned state/data:**

- message keys and catalogue versions
- locale and fallback policy
- formatting profiles
- public error-code mappings
- pseudo-locales and missing-key reports
- case-content translation bundle metadata

**Required independent tests:**

- catalogue schema tests
- missing-key and duplicate-key tests
- plural/date/number golden tests
- Unicode normalization and bidi tests
- pseudo-localization layout tests
- problem-code mapping contract tests
- cross-language snapshot tests
- security tests for interpolation and markup injection

**Cross-module integration obligations:**

1. Localization + every UI module: key completeness contract.
2. Localization + Case: case bundle activation and fallback.
3. Localization + Identity: policy receipt records exact locale/version shown.
4. Localization + Workspace: deterministic Unicode sorting uses domain keys, not translated labels.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M04 — Asset and Resource Management

**Architectural intent:** Own signed asset manifests, content-addressed resolution, variants, transcripts/alternatives, loading policy, integrity verification, caching eligibility, and safe fallback.

**Owned state/data:**

- asset identifiers and manifest schema
- asset variant metadata
- digests, media types, dimensions, purposes, and approval state
- alt text/transcript linkage
- public immutable cache manifest
- asset creation/provenance records

**Required independent tests:**

- manifest schema and checksum tests
- variant-selection tests
- missing/corrupt asset component tests
- service-worker cache-policy tests
- active-content and path-traversal tests
- alt/transcript equivalence tests
- responsive crop tests
- publication activation/rollback integration tests

**Cross-module integration obligations:**

1. Assets + Shell: bootstrap and route assets.
2. Assets + Workspace: evidence document rendition and transcript.
3. Assets + Radio: approved audio manifest.
4. Assets + Publication: atomic activation, rollback, and quarantine.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M05 — Audio and Radio

**Architectural intent:** Provide optional persistent noir-radio playback with deterministic policy, browser-safe activation, multi-tab coordination, and complete gameplay independence.

**Owned state/data:**

- radio preference
- playlist traversal state
- playback-leader state
- current approved track reference
- safe audio availability state

**Required independent tests:**

- state-machine unit tests
- seeded shuffle/no-repeat property tests
- browser user-gesture tests
- route persistence tests
- multi-tab leadership tests
- all-track failure tests
- audio-disabled E2E test
- memory/resource cleanup tests

**Cross-module integration obligations:**

1. Radio + Shell: persistence across navigation.
2. Radio + Assets: digest-approved MP3 loading.
3. Radio + multi-tab browser harness: leader election and recovery.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M06 — Client State and Synchronization

**Architectural intent:** Coordinate server-authoritative state, revisions, request lifecycle, local convenience drafts, conflicts, stale clients, and degraded connectivity without becoming an authority for ranked state.

**Owned state/data:**

- client query cache metadata
- pending UI mutation state
- server revision projections
- local convenience draft envelope
- conflict and retry state
- request cancellation handles

**Required independent tests:**

- cache and reducer unit tests
- revision-conflict component tests
- lost-response integration tests
- two-tab concurrency tests
- offline/uncommitted browser tests
- service-worker bypass tests
- stale-contract tests
- security tests for cache content
- long-session memory tests

**Cross-module integration obligations:**

1. Client Sync + Save: autosave, conflict, and restore.
2. Client Sync + Command: lost response and idempotent replay.
3. Client Sync + Submission: single-winner concurrent submit.
4. Client Sync + Shell: stale-client blocking.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M07 — Identity, Account, Policy Receipt, and Privacy Requests

**Architectural intent:** Own authentication identity, credentials, sessions, recovery, policy receipts, account status, privacy preferences, and authenticated requests for export/deletion.

**Owned state/data:**

- accounts and normalized login identifiers
- password and passkey credentials
- sessions and device projections
- recovery-code sets and verifiers
- account security state
- policy receipts and feature consent state
- privacy preferences and GPC observation
- export/deletion request ownership

**Required independent tests:**

- password/recovery/passkey unit tests
- enumeration and rate-limit security tests
- session rotation and revocation tests
- policy receipt contract tests
- GPC/telemetry preference tests
- IDOR and ownership tests
- export/deletion request integration tests
- RECOVERY_LIMITED E2E tests
- cryptographic erasure acceptance tests with M20

**Cross-module integration obligations:**

1. Identity + Shell/Client Sync: register, login, expiry, logout.
2. Identity + Policy Platform: version change, re-consent, withdrawal.
3. Identity + Workflow: export/deletion completion and cryptographic erasure.
4. Identity + Leaderboard: alias separation and withdrawal.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M08 — Career, Catalogue, and Progression

**Architectural intent:** Own named careers, fixed entry tiers and paths, catalogue state derivation, practice/revisit eligibility, atomic progression, and default-resume preference.

**Owned state/data:**

- careers
- career path and current unlocked position
- career case progress
- career events
- default-resume pointer
- derived case-card state and availability reason

**Required independent tests:**

- path and state-derivation unit tests
- multiple-career property tests
- concurrent unlock integration tests
- publication availability matrix tests
- practice/revisit eligibility tests
- invalidated/amended verdict tests
- owner authorization tests
- full anthology progression E2E

**Cross-module integration obligations:**

1. Career + Case/Publication: catalogue projection.
2. Career + Round: create/resume eligible round.
3. Career + Evaluation: atomic or coordinated verdict/progression finalization.
4. Career + Leaderboard: eligibility remains separate from progression.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M09 — Round and Game-State Engine

**Architectural intent:** Own one immutable-version-bound investigation attempt, its lifecycle, mode, ranking segment, compatibility bindings, and authorization of lifecycle-dependent operations.

**Owned state/data:**

- round aggregate
- immutable version binding set
- round lifecycle and phase detail
- mode and career linkage
- provider mode/capability binding
- ranking segment
- recovery reason
- round revision

**Required independent tests:**

- state-machine unit/model tests
- binding immutability tests
- invalid-transition property tests
- provider-mode continuity tests
- two-tab transition tests
- recovery and restart integration tests
- stale-client contract tests
- round lifecycle E2E across every mode

**Cross-module integration obligations:**

1. Round + Investigation: lifecycle gates all reveals and hypotheses.
2. Round + Command/Economy: submission block and recovery.
3. Round + Save: revisions and monotonic state.
4. Round + Submission/Evaluation: single immutable close path.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M10 — Case Content and Rules

**Architectural intent:** Own the registry-driven definition of cases, investigation profiles, safe fields, starting evidence, action/rule configuration, content suitability, and evaluator/publication references.

**Owned state/data:**

- case registry and stable ordering
- case manifest schema
- investigation profile definitions
- safe record/document/relationship type dictionaries
- starting evidence and reveal prerequisites
- action caps and rule references
- content warnings, fictionalization, debrief metadata
- case-package compatibility declaration

**Required independent tests:**

- manifest/schema tests
- registry order and stable-ID tests
- cumulative-profile property tests
- hidden-field leakage tests
- provider-independent solve fixtures
- Academy/Kennel Lab compatibility tests
- content/licensing gate tests
- publication activation/rollback integration tests

**Cross-module integration obligations:**

1. Case + Career: catalogue availability.
2. Case + Round: immutable binding.
3. Case + Investigation/Workspace: safe schema and rules.
4. Case + Evaluation: protected evaluator bundle reference under separate runtime.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M11 — Investigation and Visibility Engine

**Architectural intent:** Own the authoritative revealed-state model, visibility grants, direct and analytical relationship provenance, manual hypotheses, selections, and ranked monotonicity.

**Owned state/data:**

- revealed records, documents, and relationships
- reveal provenance
- manual hypotheses and audit history
- safe record/relationship references
- visibility revision
- selection validation rules

**Required independent tests:**

- visibility-rule unit tests
- monotonicity property tests
- selection boundary tests
- duplicate reveal tests
- manual hypothesis lifecycle tests
- cross-case/IDOR tests
- atomic settlement integration tests
- list/graph parity contract tests
- temporal/as-of leakage tests

**Cross-module integration obligations:**

1. Investigation + Command/Economy: atomic successful settlement and reveal.
2. Investigation + Workspace: projection parity.
3. Investigation + Save: checkpoints cannot roll back reveals.
4. Investigation + Case File: evidence references must be visible and owned.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M12 — Workspace Projection: List, Graph, Documents, and Semantic Navigation

**Architectural intent:** Convert one authoritative revealed state into equivalent bounded list, graph, document, and semantic-navigation projections without granting new evidence.

**Owned state/data:**

- projection schemas
- column and sort definitions
- safe graph node/edge view models
- document view models
- filter/group/selection projection
- semantic graph navigation model
- view explanation summary

**Required independent tests:**

- projection unit/golden tests
- deterministic sorting and null tests
- Unicode/bidi tests
- list/graph set-equivalence property tests
- graph cap and dense-case performance tests
- document sandbox tests
- keyboard/semantic navigator tests
- 320px/zoom/accessibility flow tests
- missing asset fallback tests

**Cross-module integration obligations:**

1. Workspace + Investigation: projection contract and parity.
2. Workspace + Presentation: keyboard, focus, screen-reader navigation.
3. Workspace + Assets: safe document renditions and fallbacks.
4. Workspace + Client Sync: filters/selection persistence without visibility changes.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M13 — Action, Quote, Command, and Settlement Orchestration

**Architectural intent:** Own the four action-family protocol, authoritative quotes, idempotent acceptance, command lifecycle, durable dispatch intent, reconciliation, cancellation, and pre-reveal noninterference.

**Owned state/data:**

- quotes
- commands
- idempotency records
- outbox intents and provider state references
- command result cache
- reconciliation event history
- work-class and deadline binding

**Required independent tests:**

- quote/rule unit tests
- command state-machine/model tests
- idempotency contract tests
- pre-reveal noninterference tests
- duplicate-click concurrency tests
- outbox crash-point tests
- unknown-outcome reconciliation tests
- valid no-result tests
- cancellation boundary tests
- poison-work and fairness integration tests
- full four-action E2E

**Cross-module integration obligations:**

1. Command + Economy + Investigation: atomic debit/command and terminal settlement/reveal.
2. Command + Retrieval: isolated provider/deterministic resolver protocol.
3. Command + Workflow: leases, fairness, retry, cancellation.
4. Command + Client Sync: duplicate click, timeout, exact replay.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M14 — Investigation Economy and Credit Ledger

**Architectural intent:** Own fictional investigation credits, exact append-only ledger semantics, debit/refund invariants, balance projection, quote-cost validation, and efficiency snapshot inputs.

**Owned state/data:**

- credit ledger entries
- materialized/derived balance
- debit and refund correlation
- economy policy/version reference
- efficiency accounting projection

**Required independent tests:**

- ledger unit tests
- property-based conservation tests
- concurrent debit tests
- duplicate refund tests
- transaction rollback tests
- exact arithmetic/currency-neutral tests
- checkpoint rollback attack tests
- reconciliation/invariant-monitor tests
- performance tests on long ledgers

**Cross-module integration obligations:**

1. Economy + Command: shared transaction for debit and command creation.
2. Economy + Investigation: terminal charge/refund/reveal finalization.
3. Economy + Save: checkpoint cannot restore ledger.
4. Economy + Submission/Evaluation: immutable efficiency snapshot.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M15 — Save, Checkpoint, Draft History, and Recovery

**Architectural intent:** Own autosave acknowledgements, manual ranked checkpoints, draft revision history, reversible restoration, practice forks, restart recovery, and conflict-safe persistence.

**Owned state/data:**

- save slots and checkpoint metadata
- draft revision history references
- practice fork lineage
- autosave status and revision
- retention/expiry metadata
- local-draft reconciliation envelope

**Required independent tests:**

- revision/checkpoint unit tests
- restore allowlist tests
- property tests proving monotonic tables unchanged
- two-tab conflict tests
- lost-response/restart integration tests
- practice fork tests
- retention/expiry tests
- encryption/erasure tests
- full save-resume E2E

**Cross-module integration obligations:**

1. Save + Client Sync: autosave and conflict UX.
2. Save + Round/Investigation/Economy: checkpoint isolation attack tests.
3. Save + Case File: revision restore.
4. Save + Platform: retention, restart, and erasure.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M16 — Case File, Claims, Evidence Mapping, and Submission

**Architectural intent:** Own the structured investigative argument, warnings, evidence-to-claim mapping, immutable canonical submission, evidence-root binding, and submission review lifecycle.

**Owned state/data:**

- case-file draft
- claims and classifications
- identity, role, culpability, harm, and context conclusions
- evidence links
- uncertainty and alternatives
- submission payload and canonical digest
- submission evidence Merkle root
- submission revision/state

**Required independent tests:**

- field/rule unit tests
- warning noninterference tests
- canonicalization golden vectors
- semantic-equivalence/metamorphic tests
- evidence ownership and visibility tests
- pending-command block tests
- duplicate submit concurrency tests
- Merkle/digest tests
- lost-response recovery tests
- immutable historical review E2E

**Cross-module integration obligations:**

1. Case File + Investigation: visible evidence references.
2. Case File + Command/Round: submission block.
3. Case File + Evaluation: immutable canonical contract.
4. Case File + Save: reversible draft history but immutable submission.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M17 — Evaluation, Scoring, Endings, Verdicts, and Amendments

**Architectural intent:** Own protected-truth evaluation, deterministic score/gates/penalties/endings, safe verdict envelope, declassification, amendment lineage, and oracle-resistance.

**Owned state/data:**

- protected evaluator truth access adapter
- evaluator bundle and version
- evaluation request/result
- score component breakdown
- solve gates and penalties
- ending code
- safe coaching/debrief references
- signed verdict envelope
- amendment lineage and validity state

**Required independent tests:**

- golden scoring tests
- property/metamorphic/monotonicity/sensitivity tests
- deterministic replay tests
- all-six-endings fixtures
- truth noninterference and adaptive-oracle tests
- signature/key tests
- mixed-version deployment tests
- amendment lineage tests
- private-runtime authorization tests
- chaos tests for evaluator/key failure

**Cross-module integration obligations:**

1. Evaluation + Submission: digest/version verification.
2. Evaluation + Maintenance/Career: safe verdict finalization and progression.
3. Evaluation + Leaderboard: eligibility/result event.
4. Evaluation + Publication: old bundle replay and amendments.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M18 — Leaderboard, Public Results, Moderation, and Disputes

**Architectural intent:** Own ranking eligibility projections, segment-compatible ranking, shared ties, optional public alias publication, withdrawal, moderation, disputes, and amendment-aware reindexing.

**Owned state/data:**

- ranking segments and keys
- leaderboard entries
- publication/withdrawal state
- public alias projection
- moderation and dispute events
- rank index and season/version scope

**Required independent tests:**

- ranking comparator unit/property tests
- shared-rank tests
- segment isolation tests
- eligibility matrix tests
- alias privacy/moderation tests
- withdrawal/deletion integration tests
- amendment reindex tests
- IDOR tests
- large-board pagination/performance tests
- opt-in E2E

**Cross-module integration obligations:**

1. Leaderboard + Evaluation: eligibility and amendment.
2. Leaderboard + Identity: alias, deletion, and withdrawal.
3. Leaderboard + Client/UI: pagination and exact ties.
4. Leaderboard + Platform: season/version activation and reindex.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M19 — Retrieval, Deterministic Resolver, and Provider Gateway

**Architectural intent:** Own bounded natural-language planning/clarification, deterministic ranked result resolution, provider adapters, conversation isolation, result firewall, parity evidence, capability/capacity, and real provider-cost accounting.

**Owned state/data:**

- canonical retrieval plans
- ambiguity/clarification classes
- ranked retrieval parity manifest references
- provider capability snapshots
- provider conversation records
- provider cost ledger and price catalogue
- safe normalized retrieval results
- provider adapter correlation state

**Required independent tests:**

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

**Cross-module integration obligations:**

1. Retrieval + Command: accepted plan and durable execution.
2. Retrieval + Publication: parity manifests and deterministic resolver.
3. Retrieval + Workflow: timeouts, reconciliation, capacity, deletion.
4. Retrieval + Investigation: safe result IDs only through command settlement.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

### M20 — Publication Trust, Durable Workflow, and Runtime Control

**Architectural intent:** Own signed publication trust, active pointers, policy/configuration bundles, durable work execution, leases/fencing/fairness, deployment epochs, migrations, admission, runtime hardening evidence, exports/deletion workflows, and release qualification.

**Owned state/data:**

- case/asset/evaluator/policy publication metadata
- active pointers, signatures, verifier policy, revocation, quarantine, freshness, and anti-downgrade state
- durable workflow jobs, leases, attempts, deadlines, cancellation, and poison quarantine
- deployment epochs and compatibility matrix
- migration state/barriers
- runtime role health and admission projection
- export artifacts/manifests and deletion/retention tombstones
- release evidence and chaos qualification records

**Required independent tests:**

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

**Cross-module integration obligations:**

1. Platform + Case/Assets: signed activation, rollback, quarantine.
2. Platform + Command/Retrieval: outbox, leases, QoS, capacity admission.
3. Platform + Evaluation/Career: safe finalization across roles.
4. Platform + Identity: policy, export, deletion, erasure.
5. Platform + all roles: deployment epoch, migration, readiness, chaos.

**Independent completion rule:** build, unit, property/model, contract, component, architecture, security/privacy, and performance-smoke suites pass using only this module, its owned persistence, and fake outbound ports.

## 11. Test design standards

### 11.1 Unit and property/model tests

- Domain tests use no database, network, browser, filesystem, or framework bootstrap.
- State machines are compared to reference models where practical.
- Critical invariants use property tests and mutation or equivalent fault injection.
- Clocks, identifiers, randomness, locales, provider states, and failure points are injected.

### 11.2 Contract tests

- The producer publishes schemas, valid/invalid golden fixtures, canonicalization vectors, and a verifier.
- Every consumer runs against the producer testkit and publishes its assumptions.
- N-1/N compatibility, retirement, stored-event replay, and historical payloads are tested.
- A contract change cannot merge while any known consumer fails.

### 11.3 Pairwise tests

- Use the real producer and real consumer.
- Replace all unrelated modules with deterministic fakes.
- Test success, validation failure, authorization failure, timeout, duplicate, stale revision, malformed payload, crash-after-commit, cancellation, and dependency-unavailable behavior where applicable.
- Every critical interaction I01–I20 has at least one passing pairwise suite before release.

### 11.4 Cluster tests

- Use real module implementations, real module migrations, real PostgreSQL, and deterministic external/browser fakes.
- Assert cross-module invariants, not internal implementation details.
- Run all clusters cumulatively after they first become available.

### 11.5 Whole-solution tests

- Use a real browser against the exact production image.
- Compose the actual WEB, MAINTENANCE, EVALUATOR, and MIGRATE roles with their real grants and network boundaries.
- Use deterministic provider simulators for ordinary CI and separate live-provider qualification evidence.
- Exercise Academy T1–T12, Kennel Lab T13–T15, all production golden strategies, restart, two tabs, provider/evaluator/key outage, database restore, stale client, publication rollback, privacy lifecycle, accessibility, and security scans.

### 11.6 Test failure rules

- Do not weaken an assertion to make a failing implementation pass unless the normative requirement changes through approved change control.
- Do not mock the behavior under test.
- Do not accept flaky critical tests. Fix the race, clock, fixture, resource leak, or nondeterminism.
- Do not delete historical regression tests when a bug is fixed.
- Every production incident or escaped defect adds a regression test in the owning module and, when cross-module, a pairwise/cluster or E2E test.

## 12. Branch, review, and evidence workflow

1. Create or resume branch `Iteration-XX` from the last closed iteration.
2. Implement tasks in dependency order within each stage.
3. Commit small coherent changes; a commit may include several already completed file-atomic tasks, but task traceability must remain explicit.
4. Run task-local checks after each task and the stage gate after each stage.
5. Run the complete clean iteration gate after all stages.
6. Fix failures inside the same branch and iteration.
7. Generate `reports/iteration-XX/evidence.json` and human summary.
8. Review code, migrations, contracts, tests, security/privacy/accessibility impact, and evidence.
9. Mark the iteration closed only when the evidence status is passing.
10. Tag or record the iteration baseline before beginning the next iteration.

## 13. Critical path and parallel work

### 13.1 Critical path

`I00 → I01 → I02 → I03 → I04 → I07 → I08 → I09 → I10 → I11 → I12 → I13 → I14 → I15 → I16 → I17 → I19 → I20 → I21 → I22 → I23 → I24 → I25 → I26 → I27 → I28 → I29 → I30 → I31 → I32 → I33 → I34 → I35 → I36`

I05 and I06 are foundations needed before the first full browser experience. I18 may proceed after I17 and before I19. Family package authoring can begin in isolated worktrees after the public Core Contract is frozen, but integration qualification remains ordered by I26–I28.

### 13.2 Safe parallelization

- M02/M03 and M04/M05 may be developed in parallel after I04, provided their contracts are merged before I08.
- Case authors may prepare data/assets in separate family worktrees after I25's engine conformance freeze.
- Security, privacy, accessibility, and performance specialists review every iteration and may prepare future fixtures in parallel; their release gates remain cumulative.
- Provider live-qualification work may proceed separately from the deterministic materialized resolver and cannot block provider-independent gameplay.

### 13.3 Unsafe parallelization

- Do not implement M13 command settlement before M14 ledger and M20 unit-of-work semantics exist.
- Do not implement submission finalization before M16 canonical snapshots and M09 lifecycle participants exist.
- Do not expose evaluation until M17 private runtime/grants and declassification are tested.
- Do not start production case integration before Academy/Lab freezes the core contracts.
- Do not deploy before migration, rollback, restore, security, accessibility, performance, and chaos evidence is complete.

## 14. Risk register

| Risk | Earliest affected iterations | Prevention and detection |
|---|---|---|
| Module boundaries become nominal only | I01 onward | Public contract packages, import rules, owned migrations/grants, no cross-table access, architecture tests in every gate. |
| Shared transaction creates internal coupling | I03, I15–I24 | Public transaction participants, global lock order, no generic callbacks, fault-injected atomicity tests. |
| Provider nondeterminism creates ranking unfairness | I17–I19 | Deterministic materialized resolver is authoritative; provider only interprets plans; repeated parity benchmarks. |
| Credits duplicate or become recoverable | I15–I20 | Append-only exact ledger, idempotency, DB constraints, save-scope rules, model/concurrency/crash tests. |
| Hidden truth leaks through code, data, logs, verdicts, or providers | I09 onward | Separate schemas/roles/packages, scans, noninterference/oracle tests, declassification manifest, image inspection. |
| Contracts freeze too early and force forks | I02–I25 | Candidate contracts evolve with N-1/N tests; freeze only after Academy/Lab conformance. |
| Test suite becomes slow or flaky and is bypassed | I04 onward | Impact optimization plus mandatory regressions; deterministic testkits; no critical quarantine; failure policy and evidence. |
| Accessibility is treated as final polish | I05 onward | Accessible primitives first, per-iteration journeys, dedicated I32 qualification, human review. |
| Case data is solvable only through one provider or one path | I17, I25–I28 | Query-identifiability records, provider-independent clean routes, multiple golden strategies and parity tests. |
| Migration or mixed-version deployment corrupts work | I03, I30–I36 | Expand/contract, epoch compatibility, stale-role fencing, drain, rollback/restore rehearsals. |
| Privacy deletion is superficial | I29 | Module handler registry, envelope keys, tombstones, restored-backup nondecryptability tests. |
| Release artifact differs from tested artifact | I30–I36 | Content-addressed frozen image/publications, no production rebuild, digest checks and signed deployment record. |

## 15. Final project completion criteria

The project is complete only when:

1. all 723 file-atomic tasks in this plan are complete or have been superseded by an approved traceable change;
2. all 37 iterations have passing evidence bundles;
3. all twenty modules build and test independently;
4. every interaction I01–I20 passes producer, consumer, and pairwise verification;
5. all eight capability clusters pass with real module implementations and PostgreSQL;
6. all four runtime roles pass identity, grant, network, readiness, mixed-version, and failure tests;
7. Academy T1–T12, Kennel Lab T13–T15, and all ten production cases pass all golden playthroughs;
8. the full browser, accessibility, localization, security, privacy, concurrency, resilience, performance, chaos, migration, restore, and rollback suites pass;
9. SBOM, provenance, signatures, verifier policy, vulnerability decisions, image inspection, traceability, and approvals are complete;
10. the exact frozen artifact is deployed without rebuild and production verification passes;
11. no unresolved release-blocking defect, failed test, critical skip, stale contract, missing migration, or evidence gap remains.

---

**End of document**
