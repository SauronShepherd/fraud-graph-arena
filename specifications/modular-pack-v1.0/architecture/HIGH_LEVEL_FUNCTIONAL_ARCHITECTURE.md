# Fraud Graph Arena

## High-Level Functional Modular Architecture and Interaction Specification

**Document version:** 1.0  
**Architecture pair ID:** `FGA-MODULAR-ARCHITECTURE-1.0-20260726`  
**Specification pack:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Status:** Normative modular decomposition companion  
**Date:** 26 July 2026

---

## 1. Purpose

This document divides Fraud Graph Arena into **20 independently testable logical modules** while preserving one coherent product. The modules form a **modular monolith**: they can be built, versioned, tested, and reasoned about independently, but they are composed into four isolated production runtime roles rather than deployed as twenty network services.

The companion high-level technical document defines code layout, dependency enforcement, runtime composition, data ownership, CI, integration testing, end-to-end testing, and release evidence.

## 2. Product-wide constitutional boundaries

1. The player has exactly four investigation action families.
2. The browser and public web runtime never receive protected truth.
3. Ranked evidence retrieval is deterministic and publication-bound; a live provider cannot select authoritative ranked rows.
4. Credits, evidence, commands, submissions, verdicts, and progression are server-authoritative and monotonic where specified.
5. Historical rounds bind immutable case, data, policy, provider, rules, scoring, asset, and contract versions.
6. Submission and evaluation are deterministic, immutable, and amendment-safe.
7. List, graph, document, and semantic navigation provide equivalent access to core investigation tasks.
8. One signed image may serve several runtime roles, but identities, secrets, networks, and permissions remain separate.
9. Correctness never depends on browser polling, player traffic, process memory, local disk, or one executor.
10. Every module and every integration edge has executable acceptance evidence.

## 3. Module catalogue

| ID | Module | Kind | Runtime | Allowed contract dependencies |
|---|---|---|---|---|
| `M01` | Application Shell and Navigation | Frontend orchestration | WEB browser bundle | M02 Presentation and Accessibility, M03 Localization and Messaging, M04 Asset and Resource Management, M05 Audio and Radio, M06 Client State Synchronization, public client contracts of M07 and M20 |
| `M02` | Presentation System and Accessibility | Frontend foundation | WEB browser bundle | M03 Localization and Messaging, M04 Asset and Resource Management |
| `M03` | Localization and Messaging | Cross-stack content foundation | WEB plus server-side safe message catalogues | M20 signed publication and policy bundles |
| `M04` | Asset and Resource Management | Frontend plus publication adapter | WEB and MIGRATE/publication tooling | M03 Localization and Messaging, M20 Publication/Workflow/Runtime Control |
| `M05` | Audio and Radio | Frontend feature | WEB browser bundle | M04 Asset and Resource Management, M06 Client State Synchronization |
| `M06` | Client State and Synchronization | Frontend data coordination | WEB browser bundle | public contracts of M07–M19, M01 Application Shell, M20 client compatibility and policy |
| `M07` | Identity, Account, Policy Receipt, and Privacy Requests | Backend domain plus frontend surfaces | WEB and MAINTENANCE for long-running privacy workflows | M03 Localization for notices, M20 policy bundles, workflows, and runtime admission, M18 for optional public alias linkage |
| `M08` | Career, Catalogue, and Progression | Backend domain plus frontend surfaces | WEB and MAINTENANCE finalization | M07 Identity, M10 Case Content and Rules, M20 Publication/Runtime Control, event contract from M17 |
| `M09` | Round and Game-State Engine | Backend domain | WEB plus MAINTENANCE recovery/finalization | M08 Career, M10 Case Content and Rules, M20 policy/publication/runtime |
| `M10` | Case Content and Rules | Backend domain plus authoring contracts | WEB reads; MIGRATE/publication compiles | M03 Localization, M04 Assets, M20 Publication/Trust |
| `M11` | Investigation and Visibility Engine | Backend domain | WEB plus MAINTENANCE settlement | M09 Round, M10 Case Content and Rules, settlement contract from M13 |
| `M12` | Workspace Projection: List, Graph, Documents, and Semantic Navigation | Read-model and frontend feature | WEB server projection plus browser bundle | M03 Localization, M04 Assets, M10 Case safe schema, M11 Investigation |
| `M13` | Action, Quote, Command, and Settlement Orchestration | Backend domain | WEB acceptance plus MAINTENANCE execution/reconciliation | M09 Round, M11 Investigation, M14 Economy, M19 Retrieval, M20 Workflow/Runtime |
| `M14` | Investigation Economy and Credit Ledger | Backend domain | WEB and MAINTENANCE settlement | M10/M20 economy policy only; M13 uses public settlement port |
| `M15` | Save, Checkpoint, Draft History, and Recovery | Backend domain plus frontend collaboration | WEB and MAINTENANCE retention/recovery | M06 Client Sync, M09 Round, M11 Investigation references, M16 Case File, M20 Retention/Workflow |
| `M16` | Case File, Claims, Evidence Mapping, and Submission | Backend domain plus frontend feature | WEB plus MAINTENANCE finalization | M09 Round, M11 Investigation, M13 Command, M14 Economy, M20 Integrity/Workflow |
| `M17` | Evaluation, Scoring, Endings, Verdicts, and Amendments | Private backend domain | EVALUATOR plus MAINTENANCE safe finalization | M16 Submission contract, M10 protected evaluator bundle contract, M20 private runtime/trust/workflow |
| `M18` | Leaderboard, Public Results, Moderation, and Disputes | Backend domain plus frontend surfaces | WEB plus MAINTENANCE reindex/moderation | M07 Identity public alias, M09 ranking segment, M17 safe verdict events, M20 workflows/policy |
| `M19` | Retrieval, Deterministic Resolver, and Provider Gateway | Backend integration domain | MAINTENANCE primarily; WEB for free deterministic planning only | M10 Case safe interface, M13 Command, M20 Publication/Workflow/Capability |
| `M20` | Publication Trust, Durable Workflow, and Runtime Control | Platform bounded context | WEB safe queries, MAINTENANCE, EVALUATOR support, and MIGRATE | foundation only; all modules consume its public platform contracts or register workflow handlers |

## 4. Functional composition principles

### 4.1 Independent capability ownership

Each module owns one cohesive capability, its vocabulary, state transitions, error codes, and acceptance tests. Another module may ask it to perform work through a public contract but cannot reinterpret or mutate its state directly.

### 4.2 Contract-first collaboration

Every interaction is one of:

- synchronous command or query through an in-process port;
- immutable versioned domain event;
- durable workflow/job with idempotency, lease, and fencing;
- signed immutable artifact/publication;
- explicit cross-module transaction participant under a shared unit of work.

A database table, filesystem path, browser cache, internal class, or framework callback is never a functional integration contract.

### 4.3 Strong and eventual consistency

Strong atomic consistency is reserved for constitutional invariants:

- quote acceptance + investigation-credit debit + command + outbox intent;
- terminal command settlement + refund/charge + visibility grant;
- submission + round transition to evaluation pending;
- safe verdict finalization + round closure + career progression;
- publication pointer activation + trust/freshness checks.

Other projections—leaderboard reindex, public notifications, telemetry aggregation, export generation—use durable idempotent workflows and are visibly pending until complete.

## 5. Interaction catalogue

| ID | Producer/orchestrator | Consumer/participant | Interaction style | Purpose |
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

## 6. Principal end-to-end functional journeys

### 6.1 Registration and first entry

`M01 → M07 → M20 policy → M03 messages → M08 dashboard/catalogue`

The player explicitly registers, receives recovery codes, records the exact policy receipt, enters the dashboard, and sees no case or identity information before authorization.

### 6.2 Career and round creation

`M08 → M10/M20 availability → M09 immutable round binding → M11 starting evidence → M12 workspace`

The career module determines eligibility; the round module binds immutable versions; the investigation module grants starting evidence; the workspace projects it without revealing more.

### 6.3 Paid analytical action

`M12 selection → M13 quote → M14 debit + M13 command/outbox → M20 workflow → M19 resolver/provider → M13 settlement + M14 ledger + M11 reveal → M12 projection`

Pre-reveal behavior depends only on player-visible input and signed policy. A crash at any point is idempotently recoverable and cannot duplicate charge or evidence.

### 6.4 Save and resume

`M06 client sync → M15 save → M16 case-file draft → M09/M11 revision references`

Only reversible draft/UI state is restored. Evidence, commands, credits, bindings, submission, verdict, and progression are never rolled back.

### 6.5 Submission, evaluation, and progression

`M16 immutable submission → M20 private workflow → M17 evaluator → M20 finalizer → M09 close + M08 progress → M18 optional ranking`

The evaluator sees protected truth under a private identity and emits only a signed safe verdict. Finalization is exactly-once and amendment-safe.

### 6.6 Account export and deletion

`M07 authenticated request → M20 isolated workflow → module-owned export projections → integrity manifest/expiry → erasure/tombstones → M18 public withdrawal`

Each module exports or erases only its owned player data through a registered handler. Protected truth, other players, secrets, and restricted source metadata are excluded.

## 7. Functional integration contracts

Every module pair MUST define:

1. producer and consumer contract versions;
2. authorization principal and owner scope;
3. request/event schema and canonicalization;
4. idempotency and duplicate behavior;
5. timeout, retry, cancellation, and unknown-outcome behavior;
6. revision or immutable-version requirements;
7. safe error/status vocabulary;
8. security/privacy classification;
9. producer and consumer contract tests;
10. at least one pairwise integration test when the edge affects gameplay, money-like credits, evidence, submission, evaluation, progression, privacy, or trust.

## 8. Functional testing model

### 8.1 Module qualification

Each module passes its functional scenarios and acceptance criteria using its own test kit and deterministic fake collaborators.

### 8.2 Pairwise integration

Every interaction in section 5 has a test suite with the real producer and consumer and fakes for unrelated modules.

### 8.3 Capability-cluster integration

Required clusters are:

- **Access cluster:** M01, M03, M06, M07, M20.
- **Catalogue cluster:** M01, M08, M09, M10, M20.
- **Investigation cluster:** M09–M14, M19, M20.
- **Save/submission cluster:** M06, M09, M11, M15, M16.
- **Evaluation/progression cluster:** M08, M09, M16–M18, M20.
- **Media/accessibility cluster:** M01–M05, M12.
- **Privacy lifecycle cluster:** M07, M15, M16, M18, M20.
- **Operational resilience cluster:** M13, M17, M19, M20 plus real database and failure injection.

### 8.4 Whole-solution acceptance

The complete signed image and all runtime roles execute Academy T1–T12, Kennel Lab T13–T15, golden production-case playthroughs, restart and two-tab scenarios, provider outage, database restore, evaluator/key outage, stale client, publication rollback, export/deletion, accessibility journeys, and security/leakage scans.

## 9. Module-pair document index

Each directory under `modules/` contains:

- `FUNCTIONAL_SPECIFICATION.md`
- `TECHNICAL_AND_TEST_SPECIFICATION.md`

The module pair shares one module pair ID and is subordinate to this architecture pair and the parent v9.0 normative pair.

## 10. Functional definition of done

1. All twenty module functional specifications are approved.
2. All public commands, queries, events, artifacts, and status vocabularies are versioned.
3. Every interaction edge has a named owner and executable contract tests.
4. Constitutional atomic workflows pass transaction and crash-point tests.
5. Every module can be functionally tested without the entire application.
6. All required pairwise, cluster, and complete-solution journeys pass.
7. Security, privacy, accessibility, fairness, determinism, and historical integrity release blockers pass.
8. The generated conformance graph contains no missing, duplicate, stale, or contradictory module requirements.
