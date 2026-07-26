# Fraud Graph Arena

## Complete Functional Specification

**Document version:** 10.0  
**Normative pair ID:** `FGA-NORMATIVE-PAIR-10.0-20260726`  
**Project baseline:** Version 9.0 consolidated functional specification plus Iteration 20 provider-fact/credential, cryptographic-lifecycle, audit-integrity, active-content, regional-recovery, automation-fairness, privacy-measurement, contract/time-evolution, vulnerability, source, and 26 July 2026 research/platform audit; Definitive Game Specification v5.3; Master Development Plan v8.3; Image Asset Production Bible v3.3; and signed shared-core contracts through Iteration 11  
**Language:** English  
**Status:** Normative consolidated product specification — Iteration 20 credential, audit, content-safety, recovery, and contract-evolution convergence  
**Audience:** Product owners, game designers, fraud specialists, data engineers, frontend/backend engineers, QA, accessibility reviewers, security reviewers, legal/licensing reviewers, privacy reviewers, operations/SRE, and release reviewers  
**Research and platform verification date:** 26 July 2026  

---

## 0. Iteration 20 / version 10.0 change register

Version 10.0 supersedes the paired version 9.0 specifications and is joined to the technical specification by `FGA-NORMATIVE-PAIR-10.0-20260726`. It preserves the fixed anthology, four-action constitution, deterministic scoring, private evaluator, monotonic ranked state, deterministic ranked retrieval, pre-reveal noninterference, explicit policy lifecycle, signed publications, secure exports, role-isolated runtime, queue fairness, and supply-chain evidence. Iteration 20 turns the remaining security and operability assumptions into explicit product guarantees around provider facts and credentials, cryptographic lifecycle, tamper-evident audit, active-content safety, regional recovery, automation resistance, privacy-preserving measurement, and contract/time evolution.

All sections labelled as inherited version 5.0 through 9.0 history are informative traceability only. They cannot override the version 10.0 constitutional layer, acceptance criteria, generated contract graph, current policy bundle, current provider-fact ledger, or current release-effective windows.

### 0.1 Defects and gaps corrected

| Area | Version 9.0 residual risk | Version 10.0 decision |
|---|---|---|
| Provider-fact contradictions | Provider limits, maturity, prices, corrections, and future entitlement changes were recorded in prose, but official notices can supersede or contradict one another | Add an immutable `PROVIDER_FACT_LEDGER` with source time, effective interval, scope, precedence, supersession, observed evidence, contradiction state, and qualification decision. A conflict blocks new affected ranked admission rather than selecting the most convenient notice [S177]–[S181] |
| Service credentials and entitlements | OAuth M2M was preferred, but token acquisition, secret overlap, privilege migration, expiry, and entitlement drift were not one player-safety contract | Add a `CREDENTIAL_LIFECYCLE_PROFILE`: nonhuman provider access uses dedicated service principals, short-lived access tokens, dual-secret rotation, explicit entitlements, expiry alerts, least privilege, and rehearsed revocation. The July/September 2026 entitlement migration is a release event, not a background platform detail [S177][S178][S182] |
| Key lifecycle and cryptographic agility | Signing, envelope encryption, TLS, database, backup, and provider secrets existed without one inventory, rotation/compromise state machine, or algorithm migration plan | Add a complete cryptographic-asset inventory, purpose-bound keys, key IDs/algorithms in signed envelopes, rotation/revocation/destruction evidence, break-glass controls, and crypto-agility/PQC migration planning without silently changing ranked bytes or trust roots [S183][S184] |
| Audit integrity | Structured logs were redacted but ordinary logs could still be deleted, reordered, truncated, or forged after compromise | Add append-only audit segments, canonical event digests, sequence/gap detection, chained or Merkle commitments, independent anchoring where available, clock/source identity, retention classes, and verification drills. Provider audit/query tables are supplementary because their availability and maturity are provider-scoped [S180][S181][S185][S186] |
| Incident and player redress | Chaos evidence existed, but incident declaration, scope, preservation, player notice, and result-validity decisions were not one lifecycle | Add signed incident records, severity and evidence-preservation rules, affected-round determination, no-speculation player notices, amendment/invalidation linkage, recovery criteria, and post-incident learning aligned to current incident-response guidance [S185] |
| Active content and document safety | Export integrity protected bytes but did not fully prevent spreadsheet formulas, macros, embedded scripts, unsafe SVG/PDF/Office content, decompression bombs, or path traversal | Treat every authoring input and generated download as untrusted active content. Use allowlisted formats, signature/magic-byte checks, sandboxed conversion, size/decompression limits, macro/script stripping, CSV formula neutralization, safe filenames, malware/CDR policy where applicable, and final-byte digesting [S187][S188] |
| Regional recovery and split brain | PITR and restore were qualified, but promotion, stale-writer fencing, immutable-backup recovery, key availability, provider reconciliation, and recovery-epoch semantics were incomplete | Add a `RECOVERY_EPOCH`, authoritative-writer lease/fence, promotion barrier, stale-writer rejection, restored-security-state proof, immutable backup copy, provider-command reconciliation, and game-day evidence for regional loss [S196] |
| Automation and abuse fairness | Rate limits existed without a complete accessible anti-automation policy; a CAPTCHA or opaque device score could disadvantage legitimate players | Add a signed `AUTOMATION_ABUSE_POLICY` using risk-based throttling and server-authoritative invariants. Challenges are accessible and provide alternatives; no accessibility tool, slow interaction, language, device class, or network quality can affect score, rank, evidence, or guilt-like labels [S193][S194] |
| Privacy-preserving measurement | Optional telemetry and differential privacy guidance existed, but experiment assignment, contribution bounds, cohort suppression, privacy-budget accounting, and publication rules were underspecified | Add a `PRIVACY_MEASUREMENT_PROFILE`: no raw free text, purpose-scoped events, minimum cohorts, contribution bounding, delayed aggregation, deterministic experiment assignment, and a privacy-budget ledger whenever formal differential privacy is claimed [S176] |
| API/schema/time evolution | N-1/N deployment compatibility did not fully define API deprecation, cursor integrity, idempotency-fingerprint evolution, timezone-database changes, Unicode direction metadata, or deterministic collation | Add signed compatibility windows, additive-change rules, principal/query-bound opaque cursors, explicit fingerprint versions, pinned tzdb/locale/collation, UTC-plus-source-zone storage, language/direction metadata, and testable client retirement [S195][S196] |
| Database ownership isolation | Owner checks were backend-authoritative, but critical private tables still allowed row-level security to remain optional defense in depth | In `PUBLIC_RANKED`, owner-scoped private tables use composite ownership constraints plus forced row-level policies under non-bypass application roles, with separately authorized maintenance/evaluator paths and migration/IDOR tests |
| Vulnerability prioritization | SBOM and VEX existed, but remediation could still be driven by raw severity alone | Combine CVSS v4, EPSS, CISA KEV, reachability, privilege, data exposure, compensating controls, and artifact provenance. Known exploitation and reachable truth/credential paths receive priority regardless of a single score [S189]–[S191] |
| Additional governed sources | Banking structure, unauthorized-investment warnings, international alerts, and director-disqualification chronology were incomplete | Add FDIC BankFind, FCA Warning List, IOSCO I-SCAN, and Companies House disqualified-director data as authoring inputs only, with effective dates, context, source caveats, fictionalization, and no-guilt controls [S197]–[S200] |
| Research refresh | The benchmark portfolio lacked very large realistic schema corpora, annotation-free synthetic-data selection, novel-pattern explanation, and capacity-aware human/AI deferral fixtures | Add SQaLe-style schema scaling, SynQuE-style dataset-selection evidence, FRAUDGUESS-style novelty/explanation tests, and FiFAR-style capacity-aware deferral simulations as nonproduction research inputs [S201]–[S204] |
| Structural cleanup | The technical prose still stated that it translated version 8.0 rules and retained stale Iteration-17/18 deployment wording | Correct current authority, delivery, and release language; generated checks reject any current-layer statement naming an obsolete normative pair or deployment gate |

### 0.2 Version 10.0 constitutional additions

1. A volatile provider fact is never trusted merely because it is the newest sentence encountered; source, scope, effective time, supersession, and observed billing/capability evidence are reconciled.
2. Every nonhuman external integration has a dedicated least-privilege identity and a tested credential rotation and revocation path.
3. Every cryptographic asset has an owner, purpose, algorithm, key identifier, state, rotation window, compromise action, and destruction/retention rule.
4. Emergency access is time-bounded, strongly authenticated, independently reviewed, and cannot become an ordinary truth-export path.
5. Security/audit history is verifiable for deletion, reordering, truncation, and source gaps; ordinary application logs are not the sole audit authority.
6. A player-facing file is safe by format and content policy as well as by digest.
7. Disaster recovery cannot produce two authoritative writers or resurrect revoked, deleted, quarantined, or superseded state.
8. Anti-automation controls cannot penalize accessibility, language, slow reading, or ordinary network/device differences and cannot alter ranked semantics.
9. Telemetry and experiments are incapable of changing evidence, price, score, progression, or ranking segment inside an accepted round.
10. API, schema, Unicode, locale, and timezone evolution is versioned and reproducible rather than inherited from host defaults.
11. Vulnerability response uses exploitation and reachability evidence in addition to nominal severity.
12. Adverse-status or warning sources inform fictional design only and never become direct suspect lists.
13. A guessed object identifier cannot cross account ownership even if an application-layer check is omitted or regresses.

### 0.3 Canonical vocabulary additions

| Term | Meaning |
|---|---|
| `PROVIDER_FACT_LEDGER` | Append-only, precedence-aware record of provider capabilities, prices, limits, maturity, corrections, effective windows, and qualification decisions |
| `CREDENTIAL_LIFECYCLE_PROFILE` | Signed identity, scope, token, secret, rotation, revocation, alerting, and entitlement rules for a service integration |
| `CRYPTOGRAPHIC_ASSET_INVENTORY` | Complete inventory of keys, certificates, secrets, algorithms, purposes, owners, states, and dependencies |
| `BREAK_GLASS_RECORD` | Immutable evidence for an exceptional privileged session, approvals, scope, duration, actions, and review |
| `AUDIT_INTEGRITY_CHAIN` | Verifiable ordered commitment to security/audit events with gap and tamper detection |
| `CONTENT_SAFETY_PROFILE` | Allowed file/media types and required scanning, conversion, stripping, size, naming, isolation, and export rules |
| `RECOVERY_EPOCH` | Monotonic disaster-recovery generation that fences stale writers and binds restored state, keys, publications, and workflows |
| `AUTOMATION_ABUSE_POLICY` | Signed rate, risk, challenge, accessibility, appeal, and false-positive handling rules |
| `PRIVACY_MEASUREMENT_PROFILE` | Purpose, fields, cohorts, contribution limits, retention, experiment, aggregation, and privacy-budget rules |
| `CONTRACT_COMPATIBILITY_WINDOW` | Signed interval and matrix in which client/API/schema/idempotency versions may safely interoperate |
| `TIME_SEMANTICS_PROFILE` | Bound timezone database, locale, collation, normalization, instant/zone representation, and clock-authority rules |


## 0A. Inherited Iteration 19 / version 9.0 change register

Version 9.0 supersedes the paired version 8.0 specifications. It preserves the fixed anthology, four-action constitution, deterministic scoring, private evaluator, monotonic ranked state, provider-independent solve route, signed publications, cryptographic erasure, accessible list/graph equivalence, continuous workflow liveness, provider-conversation isolation, real-cost separation, browser trust profile, evidence Merkle lineage, and chaos qualification. It closes the remaining gaps between *provider-assisted interpretation* and *competitive evidence parity*, and between documented controls and deployable protocol/runtime contracts.

Sections explicitly labelled as inherited version 5.0, 6.0, 7.0, or 8.0 change history are **informative traceability records**. They cannot authorize current behavior or override the version 9.0 constitutional layer, acceptance criteria, generated contract graph, signed policy bundle, or current source-effective windows.

### 0.1 Defects and gaps corrected

| Area | Version 8.0 residual risk | Version 9.0 decision |
|---|---|---|
| Ranked live-provider variance | A qualified live provider could still choose the final row set, allowing identical canonical questions to reveal different evidence inside one ranking segment | In `PUBLIC_RANKED`, the provider may assist interpretation, clarification, or plan validation, but the authoritative record set and order are produced by a deterministic publication-bound resolver. Direct provider-selected rows are unranked/experimental only [S154][S155][S165][S167] |
| Evidence parity proof | Segment equivalence tested configurations but did not prove that every supported canonical intent yields one stable answer set for every player | Add `RANKED_RETRIEVAL_PARITY_MANIFEST`, canonical intent corpus, deterministic answer-set digests, null/no-result fixtures, and per-segment parity gates |
| Quote/status side channels | Cost, status vocabulary, retry timing, queue position, response size, or error detail could reveal facts about unrevealed data before a paid reveal | Quotes and pre-settlement status are functions of player-visible inputs and signed policy only. Hidden cardinality, protected truth, provider internals, and unrevealed matches cannot influence price or distinguishable pre-reveal behavior |
| Clarification quality | A safe planner could still trap players in repeated or inconsistent clarification loops | Clarification is bounded, versioned, accessibility-tested, and evaluated for expected regret. Equivalent ambiguity receives equivalent options; unanswered ambiguity abstains without debit [S165] |
| Policy and consent lifecycle | Registration stored consent, but material terms, privacy, processor, AI-disclosure, or telemetry changes lacked a complete version-migration contract | Add immutable policy bundles, notice receipts, effective windows, change classification, re-consent/acknowledgement gates, withdrawal, and round-safe migration. No retroactive acceptance or silent expansion of data use |
| Browser privacy signal | Optional telemetry did not define treatment of browser-level opt-out signals | Where legally/applicably recognized, Global Privacy Control disables optional third-party sale/share and optional telemetry/export-to-third-party behavior without reducing gameplay [S157] |
| Idempotency authority | The project used `Idempotency-Key` as if its wire semantics were settled, while the IETF document remains work in progress | FGA defines and versions its own exact key scope, request fingerprint, retention, concurrent-request, replay, authorization, and error semantics; external drafts are informative only [S158] |
| Download/export integrity | Export expiry and privacy were defined, but player-verifiable representation integrity was not | Exports and downloadable evidence packages include a canonical manifest and digest; HTTP `Content-Digest` is used where supported, with optional message signatures for server-to-server or high-assurance delivery [S159][S160] |
| Runtime hardening | Image contents and role isolation were strong, but filesystem, Linux capability, process-dump, temporary-file, and shell/tooling behavior were not one release profile | Add a signed rootless/read-only runtime profile, minimal writable paths, no core dumps, dropped capabilities, noninteractive shell posture, bounded temp storage, and secret-safe crash handling [S169] |
| Mixed-version deployment | Expand/contract migration existed, but simultaneous old/new `web`, `maintenance`, and `evaluator` roles lacked a complete compatibility and rollout order | Add `N-1/N` role compatibility, deployment epochs, role-specific readiness, migration barriers, drain/rollback rules, and no mixed evaluator/policy lineage for one submission |
| Queue quality of service | Basic fairness existed but lacked a machine-verifiable service-class and cancellation contract | Add per-account/case/segment/provider concurrency, weighted fairness, aging, deadline budgets, poison-work quarantine, cancellation cutoffs, and starvation evidence |
| Supply-chain operational baseline | SBOM/provenance existed without a current project-security baseline and explicit SBOM schema/profile choice | Pin CycloneDX 1.7 or SPDX 3.0-compatible release evidence, map OpenSSF OSPS Baseline v2026.02.19, and require vulnerability applicability/VEX workflow; Dependency-Track 5.0 is an optional implementation, never the authority [S168][S172]–[S175] |
| New governed sources | U.S. sanctions delivery, EU payment/e-money authorization, and UK overseas-entity structures were incomplete | Add OFAC Sanctions List Service, EBA payment/e-money register, and Companies House Register of Overseas Entities as defensive schema/effective-date inputs only [S162]–[S164] |
| New research implications | Clarification regret, noisy data-lake grounding, multimodal temporal fraud benchmarks, and synthetic temporal-graph generation were absent | Add bounded clarification evaluation, dirty-schema/value-discovery fixtures, multimodal/temporal graph fidelity tests, and provenance-constrained evidence review [S165]–[S171] |
| Structural cleanup | Strategic decision tables still referenced Iteration 16 gates and the live-provider flow remained semantically ambiguous | Update gates to Iteration 19, make provider/result authority explicit, and require generated checks to reject “live provider chooses ranked evidence” semantics |

### 0.2 Version 9.0 constitutional additions

1. Every supported ranked canonical retrieval intent produces one publication-bound deterministic record set and order for the ranking segment.
2. A live provider may help interpret a question but cannot be the authoritative selector of ranked evidence.
3. Pre-reveal quote, status, latency class, and error behavior cannot become an oracle for hidden or unrevealed facts.
4. Clarification is bounded, consistent, accessible, and free; unresolved ambiguity abstains before debit.
5. Material policy, privacy, processor, telemetry, or AI-disclosure changes have immutable versioned notices and cannot be accepted retroactively.
6. Applicable browser privacy signals narrow optional data processing without reducing core play.
7. FGA owns and versions its idempotency semantics regardless of the status of an external Internet-Draft.
8. Player downloads have verifiable content integrity and remain private, expiring, and noncacheable.
9. Production role containers run under a signed least-privilege runtime-hardening profile.
10. Rolling deployment permits only explicitly compatible role/schema/policy combinations.
11. Queue fairness and cancellation are constitutional for accepted work, not best-effort implementation details.
12. Supply-chain evidence identifies the SBOM schema/profile and the project-security baseline version used for qualification.

### 0.3 Canonical vocabulary additions

| Term | Meaning |
|---|---|
| `RANKED_RETRIEVAL_PARITY_MANIFEST` | Signed mapping from supported canonical intent plus immutable snapshot/profile to deterministic answer-set/order/no-result digests |
| `DETERMINISTIC_RESULT_RESOLVER` | Publication-bound executor that produces the authoritative ranked record set from a canonical safe plan |
| `PRE_REVEAL_NONINTERFERENCE_PROFILE` | Policy proving quote, status, error, timing class, and retry behavior do not depend on hidden/unrevealed facts |
| `POLICY_BUNDLE` | Immutable versioned set of terms, privacy, processor, telemetry, AI-disclosure, content, and jurisdiction notices with effective windows |
| `POLICY_RECEIPT` | Account-scoped record of the exact policy version shown, decision, method, locale, time, and evidence digest |
| `IDEMPOTENCY_CONTRACT` | Project-owned versioned semantics for key scope, fingerprint, retention, in-progress handling, replay, and authorization |
| `EXPORT_INTEGRITY_MANIFEST` | Canonical manifest of export files, sizes, media types, digests, generation time, expiry, and optional signature |
| `RUNTIME_HARDENING_PROFILE` | Signed role-specific rootless/filesystem/capability/process/temp/crash-dump security configuration |
| `DEPLOYMENT_EPOCH` | Monotonic release-orchestration identifier binding role versions, schema compatibility, policy bundle, and migration state |
| `WORK_CLASS_POLICY` | Signed queue fairness, concurrency, priority, aging, deadline, retry, cancellation, and poison-work rules |

## 0B. Inherited Iteration 18 / version 8.0 change register

Version 8.0 supersedes the paired version 7.0 specifications. It preserves the complete fixed anthology, four-action constitution, private evaluator, deterministic score and endings, provider-independent solve route, monotonic ranked state, accessible list/graph equivalence, signed publications, privacy lifecycle, and all version 7.0 transparency and assurance controls. It converts the final operational assumptions into explicit player and release guarantees.

Sections explicitly labelled as inherited version 5.0, 6.0, or 7.0 change history were **informative traceability records** in version 8.0. In this document they remain historical provenance and do not override the version 9.0 rules, invariants, acceptance criteria, or signed generated contract graph.

### 0.1 Defects and gaps corrected

| Area | Version 7.0 residual risk | Version 8.0 decision |
|---|---|---|
| Workflow hosting | “Maintenance executor or scheduler” could still be read as permission to rely only on periodic cron | Accepted ranked work is progressed by an always-on private maintenance executor. Cron is a coarse backstop and housekeeping mechanism, not the sole interactive liveness path [S137]–[S139] |
| Provider conversation context | Provider conversations could retain prior questions and unintentionally affect accuracy, privacy, or fairness | Each accepted ranked retrieval command uses a fresh isolated conversation; follow-ups and cross-command memory are disabled in the baseline. Provider memory is not a gameplay feature [S05][S147] |
| Conversation capacity and deletion | The 10,000-conversation ceiling was recorded but not tied to cleanup and admission | The service tracks capacity headroom, deletion lag, retention, and safe shutdown of new live-provider admission before limits are approached [S125] |
| Product pricing identity | Genie Code and Genie One/Agents notices could be conflated | Product/SKU, currency, unit, promotion, contract, and effective window are separate facts. Cost tests for one product never qualify another [S126] |
| Real cost versus game credits | The fictional economy and provider operating cost had no explicit anti-confusion rule | Real provider spend is private operational accounting; investigation credits remain fictional game units and cannot be converted, refunded, ranked, or displayed as money |
| Provider rich outputs | Generated SQL, reasoning traces, visualizations, comments, and long-lived history could be retained unintentionally | They are outside the player contract, stripped by the adapter, excluded from ordinary logs, and available only through separately approved diagnostics where lawful [S05] |
| Account recovery assurance | An operator reset could be interpreted as restoring full trust immediately | Exceptional reset places the account in `RECOVERY_LIMITED`, revokes sessions/authenticators as required, applies cooldown/step-up, and never claims civil-identity proof. Operators use phishing-resistant MFA [S140] |
| LLM-specific verification | AISVS/AI RMF coverage did not explicitly incorporate the current LLM verification standard | The live retrieval release gate maps OWASP LLMSVS 2.0 in addition to ASVS/AISVS/AI RMF [S141] |
| Browser trust boundary | CSP and Trusted Types were strong, but cross-origin opener/resource policy, Fetch Metadata, permissions, and `postMessage` controls were not one enforceable product contract | Add a signed route-aware security-header profile and compatibility tests [S142][S143] |
| Economic and progression races | Concurrency rules were documented but database isolation/lock ordering was not player-contract explicit | The implementation must guarantee no duplicate debit/refund/submission/unlock under retries, deadlocks, failover, and two-tab races, with bounded safe retry and clear recovery |
| Evidence package identity | Checksums existed, but a complete ordered evidence-bundle commitment was not first-class | Every snapshot and submission binds canonical object digests and an evidence Merkle root; verdicts and debriefs preserve that lineage [S152] |
| AI Act transitional detail | The 2 August 2026 rule was treated as a single deadline without modelling provider/deployer role and the official marking grace for certain pre-existing systems | The applicability record evaluates interaction notice, marking/labelling, placement date, content type, editorial control, exceptions, and any applicable grace separately [S144] |
| Operational confidence | Resilience tests existed but no single public-ranked game-day evidence bundle was required | Public-ranked release requires executed failure scenarios for executor, provider, database, keys, deployment, cache/client, and restoration |
| New defensive sources | MiCA provider status and public SAR trend structures were absent | Add ESMA MiCA register and FinCEN SAR statistics/trend analyses as fictional-schema and defensive-learning inputs only [S145][S146] |
| New research implications | Multi-turn memory, exploratory text-to-SQL agents, synthetic membership inference, and current accessibility prevalence were not fully reflected | Isolate ranked provider turns, budget exploratory queries, strengthen empirical privacy tests, and retain human accessibility review [S147]–[S150] |
| Normative clarity | The pair still contained many inherited delta sections and one stale compatibility-table label | Mark old deltas informative and require the generated export to identify exactly which requirements are current |

### 0.2 Version 8.0 constitutional additions

1. Accepted ranked workflows have an always-on private liveness path; periodic cron alone is insufficient.
2. Ranked AI-assisted retrieval is single-command and context-isolated by default.
3. Provider conversation capacity, retention, deletion, and headroom are admission inputs.
4. Real provider cost is never represented by investigation credits.
5. Provider reasoning, SQL, comments, visualizations, and cross-user history are not player evidence.
6. Exceptional account recovery reduces privileges until step-up/cooldown succeeds.
7. Privileged operators and release signers use phishing-resistant authentication.
8. Browser security headers and cross-origin policy form a signed tested release artifact.
9. Every immutable evidence package, submission, and verdict has canonical digest lineage.
10. AI transparency applicability is evaluated per obligation and transitional rule, not by one blanket flag.
11. Public-ranked readiness includes executed chaos/game-day evidence, not only unit and integration tests.
12. Historical delta text is informative; only the current normative layer can authorize behavior.

### 0.3 Canonical vocabulary additions

| Term | Meaning |
|---|---|
| `CONTINUOUS_MAINTENANCE_EXECUTOR` | Always-on private service that progresses accepted commands and workflows within signed deadlines |
| `PROVIDER_CONVERSATION_RECORD` | Durable player-safe internal record of one FGA command's provider conversation lifecycle and deletion state |
| `PROVIDER_CAPACITY_HEADROOM` | Reserved provider capacity required before new live commands may be admitted |
| `PROVIDER_COST_LEDGER` | Private append-only operational record of provider usage and currency cost, unrelated to game credits |
| `RECOVERY_LIMITED` | Temporary restricted account state following exceptional recovery or operator reset |
| `SECURITY_HEADER_PROFILE` | Signed browser security and cross-origin policy attached to the release |
| `EVIDENCE_MERKLE_ROOT` | Digest that commits to the ordered immutable evidence objects used by a snapshot/submission |
| `CHAOS_QUALIFICATION_REPORT` | Release evidence showing invariant-preserving behavior under injected operational failures |

## 0C. Inherited Iteration 17 / version 7.0 change register

Version 7.0 supersedes both version 6.0 documents. It preserves every version 6.0 constitutional boundary while converting the specification set from an accumulation of iteration deltas into an explicitly governed, deployable release contract. The principal additions are cross-document authority repair, current Genie capacity/pricing qualification, imminent EU AI transparency readiness, AI-asset provenance, browser injection hardening, privacy threat modelling, dynamic-flow accessibility evidence, statistical provider benchmarking, staged rollout controls, and additional fraud/relational research inputs.

### 0A.1 Inherited defects and gaps corrected

| Area | Version 6.0 residual risk | Version 7.0 decision |
|---|---|---|
| Normative authority | The functional authority chain incorrectly named the version 5.0 technical specification | The version 7.0 functional and technical documents are mutually paired and jointly supersede version 6.0; generated semantic-diff evidence is a release artifact |
| Invariant numbering | The technical invariant appendix restarted at item 19 after item 48 | Invariants are uniquely numbered, machine-exported, and checked for duplicate IDs and contradictory predicates |
| Source snapshot date | Appendix metadata stated 25 July while the document header stated 26 July 2026 | All source snapshots use 26 July 2026 and record retrieval date separately from publication/effective date |
| Genie capacity | Provider object limits were recorded abstractly but not converted into a package gate | Every live Genie package proves that its safe table/view and instruction sets fit current provider limits; the current documented ceiling of 30 tables/views per Genie Agent is treated as a volatile capability, not a constant [S125] |
| Genie pricing transition | Pre-August tests could understate cost because Genie One/Agents usage is free only through 31 July 2026 in the current release notes | `PUBLIC_RANKED` qualification reruns cost-envelope tests after the applicable billing effective date and stores currency, unit price, effective time, and workspace budget evidence [S126] |
| AI transparency deadline | Article 50 readiness was described, but the 2 August 2026 applicability date is now imminent | EU public release is blocked until the legal applicability record, player disclosure, and any required machine-readable marking are operational, tested, and included in release evidence [S88][S104] |
| AI-generated assets | Asset manifests did not define a machine-readable AI-assistance/provenance profile | Public media receives an internal signed creation record and, where applicable and technically viable, a C2PA 2.4 AI disclosure assertion. C2PA is a supplementary signal, never the sole authority [S129]–[S131] |
| Browser DOM injection | CSP existed, but a project-wide DOM sink policy and migration gate were not explicit | The frontend avoids string-to-DOM/script sinks; `PUBLIC_RANKED` requires CSP enforcement and a Trusted Types adoption/compatibility decision with report-only evidence before enforcement [S127][S128] |
| Privacy engineering | Retention and erasure were strong, but there was no explicit privacy threat model and DPIA trigger matrix | Every public release carries a data-flow inventory, privacy threat model, risk treatment, processor map, and jurisdictional DPIA/applicability decision [S134] |
| Accessibility assurance | Static scanners and manual review were required, but interaction-flow evidence was not a first-class artifact | Critical journeys produce ordered keyboard/focus/accessibility-tree traces; automated flow analysis is evidence support, not a replacement for human conformance review [S132] |
| Provider benchmarks | Repetition was required but minimum runs, variance, cost confidence, and flaky classification were underspecified | Benchmark manifests define seeds/snapshots, minimum repetitions, exact outcome scoring, variance, confidence bounds, drift thresholds, cost distribution, and fail/abstain taxonomy |
| Feature rollout | Capability snapshots existed, but a mutable operational flag could still alter new-round behavior without release discipline | Ranked-affecting flags are signed configuration, segment-bound, audited, and immutable for existing rounds; emergency kill switches may only narrow/disable behavior |
| Dependency registry attacks | SBOM and provenance existed, but package-source namespace/registry pinning was not explicit | Builds pin approved registries, package names, hashes, provenance, and lockfiles; dependency-confusion and typosquatting tests are release blockers |
| Current fraud inputs | Stablecoin/P2P wallet and EU payment-fraud adaptation evidence was not separately governed | FATF 2026 stablecoin/unhosted-wallet guidance and the latest EBA/ECB payment-fraud analysis are added as defensive authoring inputs only [S135][S136] |
| Research refresh | Relational and temporal gates lacked schema-topology reasoning and dynamic accessibility research | Add DW-Bench schema-topology reasoning and Flow-A11y-style runtime evidence as research-informed test design, never as sole release authority [S132][S133] |

### 0A.2 Inherited version 7.0 constitutional additions

1. At the version 7.0 release, the paired version 7.0 functional and technical specifications were the then-current normative prose authorities.
2. Every normative invariant and acceptance criterion has a unique stable identifier or a generated unique export key.
3. A provider capacity, price, maturity, retention, or regional limit is a dated capability fact and cannot be hard-coded as a timeless product rule.
4. Tests run under a free or promotional billing window do not qualify a paid production cost envelope.
5. EU AI transparency applicability is decided before release, not deferred until an incident or complaint.
6. AI-assisted public media provenance is recorded, but no provenance metadata format is treated as proof of truth or authorship by itself.
7. Ranked-affecting feature flags can only be changed through signed release/configuration governance and cannot mutate existing round semantics.
8. Browser-side active-content sinks are deny-by-design; deviations are isolated, reviewed, and policy-enforced.
9. Privacy risk is modelled from data flows and individual harms, not only from database tables and retention periods.
10. Accessibility evidence covers interaction sequences, focus, announcements, modal state, delayed updates, and recovery—not only static pages.
11. Provider qualification reports outcome variance, abstention, cost variance, and drift, not one headline accuracy number.
12. Dependency identity includes registry, namespace, package, version, hash, signer/provenance, and lockfile position.

### 0A.3 Inherited canonical vocabulary additions

| Term | Meaning |
|---|---|
| `NORMATIVE_PAIR_ID` | Digest-bound identifier joining the functional specification, technical specification, schemas, diagrams, and conformance export for one release |
| `CAPABILITY_EFFECTIVE_WINDOW` | Start/end interval during which a provider maturity, price, quota, or behavior statement was verified |
| `ASSET_CREATION_RECORD` | Signed internal record of source assets, tools/models, prompts where retained lawfully, human edits, licenses, approvals, and output digests |
| `AI_DISCLOSURE_PROFILE` | Human- and machine-readable disclosure rules for AI-assisted interaction or generated media in a release/jurisdiction |
| `PRIVACY_THREAT_MODEL` | Data-flow-based analysis of privacy harms, actors, linkability, detectability, disclosure, exclusion, and remediation |
| `DYNAMIC_ACCESSIBILITY_TRACE` | Ordered runtime evidence for focus, keyboard, accessibility-tree, announcement, modal, error, and state transitions in a user journey |
| `RANKED_FEATURE_POLICY` | Signed allow/deny/kill-switch policy whose digest contributes to new-round bindings and ranking compatibility |
| `BENCHMARK_VARIANCE_REPORT` | Repeated-run exact outcome, abstention, latency, cost, tool-use, and drift statistics for one frozen provider benchmark |
| `DEPENDENCY_IDENTITY` | Approved registry, namespace, package, version, integrity hash, provenance/signature, and lockfile entry |

## 0D. Inherited Iteration 16 / version 6.0 change register

Version 6.0 is a complete replacement for version 5.0. It retains the fixed ten-case anthology, four-action investigation constitution, immutable publications, deterministic evaluation, provider-independent solvability, monotonic ranked state, exact economic semantics, private evaluator, cryptographic erasure, accessible graph equivalence, publication freshness, and legal/content governance. It closes the implementation contradictions and newly verified platform risks found during the Iteration 16 audit.

### 0B.1 Inherited defects and gaps corrected

| Area | Version 5.0 residual risk | Version 6.0 decision |
|---|---|---|
| Runtime topology | Some diagrams and acceptance text still implied one deployed container even though evaluator and maintenance isolation require separate runtime identities | One signed release image is executed as separately isolated `web`, `maintenance`, `evaluator`, and release-only `migrate` roles. “One image” never means one process, one credential set, or one network trust zone |
| Workflow liveness | Reconciliation remained described in places as request-driven or optionally scheduled | A qualified nonpublic executor/scheduler is mandatory for `PUBLIC_RANKED`; browser polling and web requests are accelerators only. Admission closes when executor heartbeat, queue capacity, or deadline compliance is unhealthy |
| Genie maturity | Version 5.0 stated that Agent mode itself remained beta | Genie Agent mode became GA on 2 July 2026, while the programmatic Agent mode APIs and some result surfaces remain Beta. Maturity is recorded per exact product/API operation, not per marketing label [S110][S111] |
| Agentic cost and determinism | Agent mode can run multiple iterative queries and now uses pay-as-you-go billing, which can violate a fixed quote without explicit controls | Public-ranked `LIVE_GENIE` defaults to the GA Conversation API with one bounded question/result contract. Agent mode is disabled unless query-count, DBU, wall-time, row, byte, tool, and cancellation budgets are enforceable and prequalified. Workspace budgets and hard admission caps are required [S110] |
| Provider feature sprawl | File upload, unstructured-volume access, conversation sharing, thinking traces, visualizations, and long-lived history could expand the data boundary | These features are disabled or unreachable for FGA player sessions unless a new signed capability profile explicitly approves them. The player path accepts only text questions and schema-validated player-safe tabular records [S110][S111] |
| Evaluator oracle leakage | A safe verdict schema could still leak protected truth through repeated, adaptive, or overly granular responses | Add evaluator noninterference/oracle-resistance tests, fixed safe reason vocabularies, minimum aggregation, replay equivalence, and a signed `DECLASSIFICATION_MANIFEST` for every closure/debrief disclosure |
| Publication signatures | Signature presence alone did not define who/what/where may sign or how identity is verified | Add a signed `VERIFIER_POLICY` binding signer identity/issuer, source repository/ref, build workflow, artifact type, digest, freshness, revocation, and required attestations. Transparency inclusion is verified where used [S113][S114][S115] |
| Supply-chain transparency | TUF-style freshness did not require transparency-log evidence or offline-verifiable bundles | Release artifacts SHOULD carry offline-verifiable Sigstore-style bundles or an equivalent transparency proof. Verification clients consume rotated trust material through TUF-compatible metadata and never hard-code a transparency-log shard [S113][S114] |
| JVM database client | The database floor covered PostgreSQL server versions but not JDBC publication tooling | Any JVM/Spark/GraphFrames publication path using pgJDBC MUST use 42.7.12 or later and pass channel-binding/TLS regression tests after the July 2026 downgrade vulnerability [S112] |
| Cryptographic erasure strength | Envelope encryption of designated private text was still a `SHOULD` in one normative section | It is a `MUST` for `PUBLIC_RANKED` designated private text. Key scope, deletion proof, restored-backup nondecryptability, replica/index purge, and safe completion receipts are release blockers |
| Query completeness | Safe provider views could be structurally incapable of answering a required question even with more data or a larger model | Every benchmarked retrieval intent has a `QUERY_IDENTIFIABILITY_RECORD`; required solve-route queries must be determined by the exposed safe interface, otherwise the interface or solve route changes [S123] |
| Synthetic relational fidelity | Existing tests emphasized rows, graphs, and behavior but not schema/connectivity diversity at relational-database scale | Add schema graph, primary/foreign-key topology, entity-history, and relational-interface generation tests inspired by PluRel and current temporal-fidelity research [S120][S122] |
| Agent benchmark quality | Provider tests could overuse LLM-as-judge or one-shot accuracy | Add deterministic sandboxed fixtures, normalized exact/structured scoring, repeated execution over frozen snapshots, schema-grounding error classification, and explicit cost budgets [S121][S124] |
| Open-data portfolio | Current APP-scam performance, regulated-firm status, disclosure chronology, and 2026 FATF typology inputs were absent | Add FATF cyber-enabled-fraud guidance, UK PSR APP-scam performance/reimbursement data, FCA Financial Services Register, and FCA National Storage Mechanism as governed authoring inputs only [S116]–[S119] |
| Specification duplication | Overlapping backlog sections and stale topology language weakened normative clarity | Consolidate terminology, distinguish strategic decisions from implementation decisions, add v6 traceability, and require cross-document semantic-diff tests |

### 0B.2 Version 6.0 constitutional additions

1. One signed image never collapses public ingress, maintenance, evaluation, and migration into one runtime identity.
2. `PUBLIC_RANKED` cannot accept work without a healthy qualified executor/scheduler and private evaluator path.
3. Provider maturity is recorded per exact API operation; GA of Agent mode does not make its Beta programmatic APIs production-qualified.
4. An agentic provider cannot consume an open-ended quote. Query count, provider cost, time, rows, bytes, tools, and cancellation behavior are bounded before acceptance.
5. Player provider sessions cannot upload files, attach arbitrary volumes, share conversations, expose thinking traces, or return active/rich content under the baseline capability profile.
6. Safe verdicts and debriefs are tested for protected-truth noninterference and adaptive oracle leakage.
7. Every intentional post-verdict disclosure is governed by a signed declassification manifest.
8. Trust decisions evaluate signer identity, source, workflow, artifact type, digest, freshness, transparency evidence, and revocation—not a signature bit alone.
9. Required retrieval questions must be identifiable from the provider-safe interface.
10. Designated private text in `PUBLIC_RANKED` is envelope-encrypted and cryptographically erasable as a mandatory control.
11. JVM publication tooling is part of the security patch floor.
12. Relational synthetic-data quality includes schema topology, foreign-key connectivity, trajectories, and time-varying relationships.

### 0B.3 Normative product boundary

Fraud Graph Arena is an educational strategy game using fictional, synthetically generated evidence. It is **not** an AML, KYC, sanctions-screening, credit, employment, insurance, law-enforcement, compliance-adjudication, or real-world accusation system. Open data and fraud research may inform fictional schemas, distributions, mechanisms, controls, and debriefs; named real people or organizations MUST NOT become playable suspects.

The product teaches detection, evidence discipline, uncertainty, and protection of innocent actors. It MUST NOT provide operational instructions that materially facilitate fraud, laundering, account takeover, evasion, credential abuse, exploitation of a live service, or circumvention of investigative controls.

### 0B.4 Inherited canonical vocabulary additions

| Term | Meaning |
|---|---|
| `RUNTIME_ROLE` | One of `WEB`, `MAINTENANCE`, `EVALUATOR`, or `MIGRATE`, each with separate identity, secrets, network policy, and executable permissions |
| `EXECUTOR_HEALTH_STATE` | `HEALTHY`, `DEGRADED`, `STALE`, `CAPACITY_EXHAUSTED`, or `UNAVAILABLE`; used by admission control |
| `PROVIDER_FEATURE_PROFILE` | Signed allowlist of exact provider APIs and features permitted for a case/environment/segment |
| `PROVIDER_COST_ENVELOPE` | Maximum provider queries, DBUs/cost units, elapsed execution time, rows, bytes, and tool invocations accepted by one quote |
| `QUERY_IDENTIFIABILITY_RECORD` | Proof or test evidence that a required intent is determined by the exposed provider-safe interface |
| `DECLASSIFICATION_MANIFEST` | Signed list of protected facts or abstractions intentionally releasable in verdict, closure, debrief, support, or appeal surfaces |
| `ORACLE_LEAKAGE_TEST` | Test family checking whether safe outputs, repeated submissions, amendments, or appeals reveal protected truth beyond approved disclosure |
| `VERIFIER_POLICY` | Signed policy for acceptable signer identity, issuer, source/ref, workflow, artifact type, digest, attestations, freshness, and revocation |
| `TRANSPARENCY_BUNDLE` | Offline-verifiable signature/attestation material containing identity, timestamp, and transparency inclusion proof where applicable |
| `RELATIONAL_FIDELITY_PROFILE` | Required schema, key-connectivity, trajectory, temporal, graph, and behavioral properties for synthetic case data |

## 1. Purpose and authority

This document defines the complete functional behavior of **Fraud Graph Arena**. It describes player journeys, game rules, progression, evidence semantics, scoring, accessibility, privacy, content governance, provider behavior, and release acceptance.

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. Bracketed references such as `[S05]` point to Appendix C. Platform facts are dated release inputs and MUST be revalidated at release freeze.

When artifacts conflict, precedence is:

1. This version 10.0 consolidated functional specification for product behavior.
2. The version 10.0 Complete Technical Architecture and Design Specification for implementation constraints.
3. Signed, versioned machine-readable Core Contract schemas and manifests, which govern exact values only when they conform to items 1 and 2.
4. Approved automated conformance tests and release evidence.
5. Definitive Game Specification v5.3, Master Development Plan v8.3, and Image Asset Production Bible v3.3 for nonconflicting historical intent.
6. Earlier plans, prototypes, comments, screenshots, and reduced-scope artifacts.

A manifest cannot silently override a constitutional rule. A change to the four action families, hidden-truth boundary, ranked-save monotonicity, deterministic evaluation, career order, player-safety boundary, provider-fact authority, cryptographic trust, recovery fencing, or ranked contract compatibility requires an explicit new specification version and migration policy.

## 2. Product vision

Fraud Graph Arena is a noir investigative strategy game in which a Spanish Water Dog detective examines synthetic records, entities, events, documents, transactions, and relationships to reconstruct fictional fraud schemes inspired by documented real-world mechanisms.

The game turns fraud analysis into a disciplined investigation rather than a hidden-object clicking exercise. The player must distinguish:

- identity from association;
- association from culpability;
- a suspicious signal from proof;
- a central graph node from a guilty actor;
- an analytical candidate from an established fact;
- absence of evidence from evidence of absence;
- a victim, innocent employee, or shared-service provider from a facilitator.

The core fantasy is: **find the fraud network, explain how it worked, identify who did what, protect innocent or victimized actors, and support every important conclusion with evidence.**

### 2.1 Educational goals

The game MUST teach that:

- fuzzy identity matches can be false;
- exact shared fields can be benign;
- graph prominence does not imply guilt;
- chronology, control, authorization, benefit, intent, and corroboration matter;
- automated analytics are investigative signals, not verdicts;
- defensible accusations require explicit claims and diverse evidence;
- the correct conclusion may be that a case is legitimate or unresolved;
- selecting everything cannot produce a top result.

### 2.2 Fictionalization statement

Every playable production case MUST display a clear notice equivalent to:

> This case is inspired by documented fraud mechanisms. All playable characters, organizations, communications, transactions, evidence, and events are fictional and synthetically generated.

No real person is a playable suspect. No real account, credential, private address, telephone number, or nonreserved domain may appear in playable data.

### 2.3 Humor and tone

The tone is hard-boiled urban noir with humane, dry humor. Humor MAY target:

- fraudsters’ excuses;
- corporate euphemisms;
- absurd shell structures;
- fake expertise;
- greed;
- bureaucracy;
- overcomplicated spreadsheets;
- the detective’s habits.

Humor MUST NOT target victims, poverty, loneliness, age, disability, ethnicity, nationality, religion, gender, education, whistleblowers, journalists, or trauma.

---

## 3. Product scope

The complete product contains:

- application-owned username/password sign-in and explicit account creation presented through one accessible authentication surface;
- no email collection, plus player-held one-time recovery codes and no email-based recovery;
- an authenticated dashboard;
- a two-screen section and case selector;
- three ranked career entry tiers and three evidence-complexity investigation profiles;
- one fixed ten-case anthology plus a governed future-case backlog;
- a public Detective Academy with twelve deterministic microcases;
- a protected Kennel Lab with three QA-only fixtures;
- a generic registry-driven case engine;
- list, graph, document, and case-file views;
- exactly four investigation action families;
- an investigation-credit economy;
- autosave, manual save slots, resume, recovery, Practice, replay, and closed-case revisit;
- immutable submission;
- deterministic scoring from 0 to 1,000;
- six mutually exclusive endings;
- atomic career progression;
- Hall of Fame and opt-in Hall of Shame;
- opening and closure comics;
- a persistent noir jazz radio with on/off-only control;
- accessible alternatives to graph, audio, animation, and visual-only information;
- historical and educational debriefs;
- public deployment as one web application using a qualified `PUBLIC_RANKED` environment profile.
- explicit provider execution modes and ranking-segment compatibility.
- player-data export, deletion, retention, and evaluation-amendment workflows.
- content suitability, content-warning, and dual-use publication controls.

### 3.1 Explicit non-goals

The player MUST NOT be able to:

- run arbitrary SQL;
- start a live Spark, Zingg, or GraphFrames pipeline;
- permanently merge source records;
- alter costs or scoring rules;
- access protected truth;
- treat manual hypotheses as system facts;
- force Genie to read unapproved datasets;
- receive automatic culpability decisions;
- use a development/free-tier provider environment for public ranked play;
- restore a ranked save to recover spent credits, erase command history, or unreveal evidence;
- use free sorting or filtering to reveal unretrieved records;
- submit while paid work is nonterminal;
- obtain ranked credit from a replay or revisit of a disclosed completed case.

---

## 4. Users and operating roles

### 4.1 Player

A player authenticates, creates or resumes a career, investigates cases, saves work, submits a case file, receives a verdict, and optionally appears on eligible leaderboards under a public alias.

### 4.2 Reviewer or demo player

A reviewer uses the same player-facing login flow and has no hidden-truth privilege. Reviewer rounds MAY be marked ineligible for rankings. Reviewer status MUST NOT change case evidence, costs, scoring, or unlock behavior unless the round is explicitly labeled as an unranked demo.

### 4.3 Operator

An operator performs protected account resets, case publication, rollback, diagnostics, and release operations. Operator functions are not exposed as public player controls.

### 4.4 Content author and evaluator maintainer

Content authors build synthetic case packages. Evaluator maintainers define protected truth, solve gates, scoring, penalties, endings, and coaching. Authoring and evaluator information MUST remain outside the player data path.

---

## 5. Modes

### 5.1 Ranked Career

Ranked Career is the canonical progression mode.

- A career has one immutable entry tier.
- A production round belongs to exactly one career.
- Cases progress in a fixed order from the selected entry point.
- A valid completed submission closes the current case and unlocks only the next published case.
- Original results remain immutable.
- Eligible first attempts may appear in rankings.

### 5.2 Detective Academy

Detective Academy is public, unranked, and separate from production careers.

It MUST:

- use the real generic case loader and real game engine;
- teach the actual four-action model;
- provide instructor guidance, progress, reset/retry, hints, transcripts, and graduation;
- exclude its rounds from career progression and normal leaderboards;
- support replay without affecting any production result.

### 5.3 Kennel Lab

Kennel Lab is a protected validation mode for automated and authorized QA. It MUST NOT be discoverable or activatable by ordinary players in production.

### 5.4 Practice

Practice is unranked play against an approved case snapshot. It may be started independently of career progression when the case is published and Practice is enabled.

### 5.5 Closed-case Revisit

A `CLOSED` case can be revisited through a new independent round labeled:

> Practice — no score or progression impact

A revisit MUST NOT modify the original submission, score, ending, leaderboard eligibility, completion timestamp, or career progression.

### 5.6 Review

Review is read-only inspection of a completed result, including the submitted case file, score breakdown, ending, coaching, closure content, and debrief.

---

## 6. Career model and case progression

### 6.1 Screen 1: section selection

After login and dashboard navigation, the player chooses one of four equal-status sections:

1. `DETECTIVE_ACADEMY`
2. `PUPPY`
3. `ADULT_DOG`
4. `SENIOR_DOG`

The four choices use consistent Spanish Water Dog representations. Selection MUST support pointer, keyboard, touch, screen reader, visible focus, and a normal-cursor fallback if the decorative magnifying-glass cursor is unavailable.

Choosing Academy does not create a career. Choosing Puppy, Adult Dog, or Senior Dog can lead to New Game or an existing career.

### 6.2 Screen 2: case catalogue

The second screen shows every case card in the selected section from the beginning.

Each card MUST show:

- case code;
- title;
- family;
- spoiler-safe teaser;
- primary state;
- state-specific action;
- publication or availability message when necessary.

Every card has exactly one primary career state:

| State | Meaning | Player action |
|---|---|---|
| `OPEN` | Available as the current playable case | Start or Resume |
| `CLOSED` | Completed in the current career | Review or Revisit |
| `LOCKED` | Not yet available in this career | Spoiler-safe preview only |

State MUST be conveyed through text, icon/shape, and interaction behavior, not color alone.

Primary state is separate from availability. A card can therefore remain `LOCKED` while explaining *why* it is unavailable.

| Availability reason | Meaning | Required behavior |
|---|---|---|
| `CURRENT_OPEN` | The next ranked case is available | Start or resume |
| `ACTIVE_ROUND` | An unfinished round already exists | Resume is primary; duplicate ranked starts are blocked |
| `UNPUBLISHED` | The package is planned but not released | Show a spoiler-safe “coming later” message; do not imply a date |
| `NOT_IN_PATH` | The case precedes this career’s entry tier | Do not mark complete; Practice may be offered separately |
| `PRACTICE_AVAILABLE` | Published for unranked play but not currently ranked-open | Start a clearly labeled Practice round |
| `VERSION_UNAVAILABLE` | The required immutable package is missing or quarantined | Fail closed and show a support correlation ID |
| `RETIRED` | No new ranked rounds are created | Historical review remains; Practice follows retirement policy |
| `SECURITY_HOLD` | Publication was disabled for a security or leakage incident | Existing affected rounds follow the incident policy; no new round starts |

A case card MUST display one primary state and zero or more noncontradictory status badges/reason messages. API clients MUST receive stable reason codes rather than infer availability from prose.


### 6.3 Ranked entry tiers

| Entry tier | Stable ID | First ranked case | Initial presentation | Career path |
|---|---|---|---|---|
| Puppy | `PUPPY` | P1 | Young Spanish Water Dog | P1 → P2 → P3 → A1 → A2 → A3 → A4 → V1 → V2 → V3 |
| Adult Dog | `ADULT_DOG` | A1 | Adult Spanish Water Dog | A1 → A2 → A3 → A4 → V1 → V2 → V3 |
| Senior Dog | `SENIOR_DOG` | V1 | Senior Spanish Water Dog | V1 → V2 → V3 |

The entry tier is a starting point, not permission to reorder or branch the anthology. Earlier cases skipped by a later entry tier are not marked complete.

### 6.4 Family transitions

A Puppy career changes to Adult presentation at A1 and Senior presentation at V1. An Adult career changes to Senior presentation at V1. Presentation changes are milestones; they MUST NOT change protected truth or retroactively alter prior rounds.

### 6.5 New Game

New Game MUST:

1. explain that a new career is being created;
2. ask for the entry tier;
3. show the first case and complete fixed path;
4. require explicit confirmation;
5. create a new career identifier;
6. preserve completed history, existing saves, scores, and submissions;
7. avoid destructive replacement.

Multiple named careers are REQUIRED and multiple incomplete careers MAY coexist. A player may mark one incomplete career as the default resume target, but this pointer is only a dashboard convenience. Every career has an independent identity, entry tier, progression, rounds, saves, and history. Creating another career never archives, deletes, locks, or overwrites an earlier career.

### 6.6 Atomic progression

After an eligible production submission is finalized:

- the current `OPEN` case becomes `CLOSED`;
- exactly the next published case in the path may change from `LOCKED` to `OPEN`;
- progression and verdict persistence occur atomically;
- retries or concurrent tabs MUST NOT unlock twice or skip a case;
- Practice, Academy, replay, debug, migrated test, and Kennel Lab rounds MUST NOT advance progression.

---

## 7. Production case catalogue

The canonical order is fixed:

| Order | Case ID | Title | Family | Core mechanism | Baseline status |
|---:|---|---|---|---|---|
| 1 | P1 / `MADDOG` | The Maddogg Investment Kennel | Puppy | Ponzi/affinity investment fraud, fabricated statements, later deposits funding earlier payouts | Accepted deterministic data baseline |
| 2 | P2 / `CEO_BARKED_TWICE` | The CEO Who Barked Twice | Puppy | CEO impersonation, mailbox compromise, invoice substitution, payment diversion | Accepted deterministic data baseline |
| 3 | P3 / `BISCUIT_RELIEF` | The Great Biscuit Relief Fund | Puppy | Fake relief campaign, inflated impact, donation diversion | Accepted deterministic data baseline |
| 4 | A1 / `BONE_LEDGER` | The Bone Ledger | Adult Dog | Manipulated accounting, hidden liabilities, SPVs, false journals, polished statements | Accepted deterministic data baseline |
| 5 | A2 / `DOWNLINE` | Every Dog Gets a Downline | Adult Dog | Pyramid/downline recruitment, product cover, commissions, mixed victim/recruiter roles | Accepted deterministic data baseline |
| 6 | A3 / `PHANTOM_VET` | The Phantom Veterinary Clinic | Adult Dog | Veterinary/insurance claims fraud, misrepresented procedures, license misuse, payment flows | Accepted deterministic data baseline |
| 7 | A4 / `GOLDEN_HYDRANT` | The Golden Fire Hydrant Contract | Adult Dog | Procurement fraud, bids, change orders, shells, kickbacks, legitimate emergency comparators | Accepted deterministic data baseline |
| 8 | V1 | Love, Leashes & Offshore Transfers | Senior Dog | Romance/relationship manipulation and cross-border transfer laundering | Planned production package |
| 9 | V2 | The Long Con at Crypto Kennel | Senior Dog | Long-con investment and cryptocurrency movement with layered identities and infrastructure | Planned production package |
| 10 | V3 | The Panama Pawpers | Senior Dog | Offshore structures, beneficial ownership, intermediaries, and lawful-versus-abusive ambiguity | Planned production package |

A data baseline being accepted does not mean the case is automatically published. A case becomes playable only after runtime integration, evaluator validation, assets, accessibility, security, rollback, and publication gates pass.

### 7.1 Case-specific fairness requirements

Every production case MUST include:

- at least one plausible but innocent or victimized high-connectivity actor;
- exculpatory and contradictory evidence where appropriate;
- more than one meaningful solve route;
- a protected answer key that distinguishes identity, role, culpability, harm, and context;
- a defensible clean solve;
- deterministic partial, overbroad, wrong-principal, budget-waste, and unresolved outcomes;
- an educational debrief that explains warning signs without suggesting that a single graph pattern proves fraud.

### 7.2 Known clean-solve expectations for the Puppy family

P1 must support identification of the principal, Ponzi/affinity mechanism, later-deposit-to-earlier-payout flow, fabricated statements, knowing operator, culpable recruiter, protected victim/unwitting connector, protected innocent employee, and at least two independent evidence categories.

P2 must support the impersonation/mailbox/invoice/payment-diversion mechanism, the principal/coordinator, technical mailbox operator, mule-stage controller, beneficiary substitution, first diverted payment and downstream dispersal, protection of innocent parties, and at least two independent evidence categories.

P3 must support the fake-relief and donation-diversion mechanism, principal/controller, campaign/content operator, financial operator, settlement and onward diversion, materially inflated claimed impact, protection of legitimate beneficiaries/providers, and at least two independent evidence categories.

---

## 8. Detective Academy catalogue

Academy uses twelve public deterministic microcases:

| ID | Title | Learning objective |
|---|---|---|
| T1 | The Empty Bowl | Close a legitimate case without a false accusation |
| T2 | The Obvious Biscuit Thief | Exercise the smallest complete happy path |
| T3 | Two Collars, One Dog | Interpret fuzzy candidates and reject false merges |
| T4 | The Circular Bone | Understand directed cycles, exact relationships, and graph layout |
| T5 | The Lonely Shell | Handle disconnected components and progressive reveal |
| T6 | The Shared Kennel | Distinguish hubs and legitimate shared infrastructure |
| T7 | The Time-Traveling Invoice | Resolve chronology, time zones, and deterministic sorting |
| T8 | The Contradictory Witnesses | Record uncertainty when evidence conflicts |
| T9 | The Missing Pawprint | Recognize missingness and insufficient evidence |
| T10 | The Red Herring | Ignore distractors and preserve precision |
| T11 | The Last Biscuit | Manage quotes, credits, no-result outcomes, and zero-credit completion |
| T12 | The Six Doors | Exercise scoring, immutable submission, and all six endings |

Protected Kennel Lab fixtures are:

- T13 — The Very Long Company Name: wrapping, reflow, and responsive stress.
- T14 — Señor Ñu’s Café: Unicode, normalization, sorting, and display safety.
- T15 — Double Click Dog: duplicate actions, idempotency, concurrency, and stale-version behavior.

---

## 9. End-to-end player journey

The canonical journey is:

1. Open the application.
2. Log in or create an account through the same form.
3. Enter the authenticated dashboard.
4. Resume an existing career/round or choose New Game.
5. Select Academy, Puppy, Adult Dog, or Senior Dog.
6. Browse all case cards in that section.
7. Confirm a ranked career entry tier when creating a new career.
8. Start/resume an `OPEN` case, review/revisit a `CLOSED` case, or inspect a `LOCKED` preview.
9. View the opening comic or accessible transcript.
10. Read the briefing and fictionalization notice.
11. Enter the investigation workspace.
12. Inspect initial revealed records and direct source relationships.
13. Sort, filter, group, select, and switch list/graph views for free.
14. Create manual hypotheses for free.
15. Request and accept quotes for Zingg candidate, Exact shared-field, or Genie Agent actions.
16. Inspect results, provenance, no-result outcomes, failures, or refunds.
17. Review documents and build the case file.
18. Save automatically or manually.
19. Review warnings and submit one immutable case snapshot.
20. Receive a deterministic score, ending, breakdown, and coaching.
21. Read the closure comic and educational debrief.
22. Opt into eligible leaderboard publication.
23. Return to the catalogue, where progression states are updated atomically.

---

## 10. Authentication and account lifecycle

### 10.1 One authentication surface, two explicit actions

The login screen MAY use the same username/password fields for sign-in and registration, but it MUST present two explicit actions:

- **Sign in** authenticates only and never creates an account.
- **Create account** performs registration only after validation, password confirmation, acceptance of the current terms/privacy notice, and acknowledgement of recovery-code responsibility.

A nonexistent username submitted to **Sign in** receives the same generic failure class as a wrong password. A username collision submitted to **Create account** receives a generic unavailable/invalid response that does not provide a reliable enumeration oracle. A typo can never silently create an account.

### 10.2 Identifiers, aliases, and validation

Login usernames:

- are 3–32 characters;
- are normalized to lowercase;
- use the conservative ASCII set `a-z`, `0-9`, `.`, `_`, and `-`;
- cannot begin or end with punctuation or contain reserved/operator-like names;
- are never displayed publicly.

Public leaderboard aliases are separate, optional, Unicode-capable, moderated, and revocable. Confusable, impersonating, abusive, or personal-data aliases can be rejected without affecting the login identifier.

Password-only authentication requires 15–256 Unicode characters. At least 64 characters MUST be accepted. The interface supports paste, password managers, a visibility toggle, and accessible validation. The service rejects commonly used, expected, context-specific, and known-compromised passwords; it MUST NOT require arbitrary character-class composition or periodic rotation without evidence of compromise [S01].

### 10.3 Sessions and security events

The system MUST support secure server-managed sessions, rotation after authentication and password reset, idle and absolute expiry, logout, revocation, rate limiting, credential-stuffing resistance, and generic authentication failures. Security-sensitive events are recorded without logging passwords, recovery codes, or private case content.

### 10.4 Recovery codes

There is no email collection or email-based recovery. Registration generates a set of one-time recovery codes with sufficient cryptographic entropy. Codes are shown in full only at generation, can be downloaded or printed accessibly, are stored only as one-way protected verifiers, and are individually single-use.

A valid unused code plus username can reset the password through a rate-limited, enumeration-resistant flow. Regeneration requires recent reauthentication and invalidates every previous code. A separate, protected, audited operator reset remains a last resort and cannot reveal the existing password.

### 10.5 Ownership and account status

Every career, round, save, command, submission, export, deletion request, and private case-file object is owner-scoped. Guessing an identifier MUST NOT reveal whether another player’s object exists. Accounts support active, locked, recovery-limited, deletion-pending, and deleted/pseudonymized states with clear player-safe messaging.

### 10.6 Age suitability and consent

The public ranked service is not directed to children under 13. The deployment uses a jurisdiction-approved age-suitability rule without collecting an exact date of birth unless legally required. The first-run flow includes content suitability, privacy choices, fictionalization, and recovery-code acknowledgement. An underage or mistaken-registration support path is available without public disclosure.

## 11. Round lifecycle

A round is one immutable-version-bound investigation attempt. At creation it binds owner, mode, career where applicable, case/publication versions, investigation profile, `as_of_time`, analytical publication versions, provider execution mode and semantic configuration, rules/economy/scoring/ending versions, asset/core-contract versions, and ranking segment. These bindings never change inside the round.

### 11.1 Canonical observable lifecycle

| State | Meaning |
|---|---|
| `CREATED` | The round exists and initialization/opening has not completed |
| `ACTIVE` | Investigation and case-file editing are allowed |
| `SUBMISSION_PENDING` | The player confirmed submission; mutable gameplay is blocked while the immutable snapshot is committed |
| `EVALUATION_PENDING` | The immutable submission exists and evaluation is incomplete |
| `CLOSED` | A final or amended-safe verdict is reviewable |
| `ABANDONED` | The player intentionally stopped an unfinished round |
| `EXPIRED` | Retention policy closed an inactive round |
| `RECOVERY_REQUIRED` | Infrastructure/provider uncertainty prevents normal progress and requires safe reconciliation or operator action |

Internal substates MAY refine initialization, provider, or evaluation work, but public APIs and UI map them to this canonical lifecycle.

A round may reach zero credits and remain `ACTIVE`. Zero credits prevents further paid actions only; it does not prevent reading, free filtering, hypotheses, case-file work, saving, or submission.

### 11.2 Pending-action submission block

Submission is blocked while an accepted paid action remains nonterminal, economically indeterminate, or under reconciliation. The player may wait, request status/reconciliation, or cancel only when the command contract supports safe cancellation. A browser timeout never proves that an action failed.

### 11.3 Provider-mode continuity

A live-provider outage does not silently switch an existing ranked round to a different execution mode. The round either resumes the bound mode, uses a predeclared equivalent fallback whose equivalence was qualified before publication, pauses in `RECOVERY_REQUIRED`, or is invalidated/amended according to the incident policy. New rounds may bind a new mode only in a new ranking segment.

## 12. Revealed-state model

The player sees one coherent revealed investigation state.

The state includes:

- revealed records/entities/events/documents;
- direct source relationships whose prerequisites are visible;
- revealed Zingg candidate relationships;
- revealed exact shared-field relationships, with generator provenance;
- player-created manual hypotheses;
- selection and saved subsets;
- reveal provenance and command history;
- case-file draft;
- credit and quote history.

List and graph views MUST represent the same revealed records, edges, filters, selection, and history. Switching views is free and MUST NOT reveal new data.

### 12.1 Relationship families

| Family | Player meaning | Source | Visual grammar |
|---|---|---|---|
| Direct source | Recorded relationship in source data | Published source evidence | Neutral solid |
| Manual | Player hypothesis | Player | Red dashed |
| Zingg | Possible same identity | Precomputed candidate publication | Purple dotted |
| Exact shared-field | Shared normalized exact field | Precomputed exact-link publication; may be generated with GraphFrames | Blue patterned/solid |

Color MUST NOT be the only differentiator. Every edge must expose a textual family label and safe provenance.

### 12.2 Identity conclusions

A Zingg candidate is not an identity conclusion. The player may classify candidate pairs as likely same identity, likely different, unresolved, or case-defined alternatives. The system MUST preserve the difference between source records and canonical protected identities.

### 12.3 Culpability separation

Identity, operational role, culpability, harm/victim status, accusation, and contextual relevance are separate dimensions. The user interface and evaluator MUST NOT collapse them into a single suspect flag.

---

## 13. Investigation workspace

### 13.1 Shared shell

The workspace includes:

- case/investigation-profile/mode context;
- credit balance;
- save/recovery status;
- list/graph switch;
- relationship legend;
- selection summary;
- four action entry points;
- document/evidence inspector;
- case-file panel;
- radio on/off control;
- accessible help and glossary.

### 13.2 List view

List view is the precision workspace and SHOULD be the default initial investigation view.

It MUST support:

- safe default columns per entity type;
- add/remove/reorder approved columns;
- reset columns;
- deterministic pagination;
- single-column ascending/descending/unsorted cycling;
- multi-column sorting using up to five ordered criteria;
- visible sort priority and direction;
- deterministic safe-ID tie-breaking;
- nulls-last by default;
- free filters over already revealed data;
- free grouping and saved subsets;
- synchronized selection with the graph;
- keyboard and screen-reader operation.

Sorting, filtering, grouping, column changes, and view switching MUST NOT consume credits when they operate only on revealed data.

### 13.3 Graph view

The graph MUST support:

- bounded node/edge rendering;
- pan and zoom;
- fit/reset view;
- selection and multi-selection;
- focus and keyboard navigation where practicable;
- node and edge tooltips/details;
- entity-specific icons and labels;
- relationship-specific styles;
- a minimap/overview where supported;
- a legend showing visible entity types and counts;
- stable node and edge identifiers;
- an accessible list equivalent;
- optional drag only when it does not destabilize testing or accessibility.

Node size, color, location, degree, breed, or lighting MUST NOT silently encode guilt. Layout coordinates are not normative and automated tests MUST NOT depend on exact positions.

### 13.4 Documents and evidence inspection

The player can inspect revealed documents, communications, statements, invoices, claims, transactions, and other evidence. Unavailable or failed documents need explicit states and accessible fallback text. Documents must expose source category, record identifier, reveal provenance, and any safe metadata required for a claim.

---

## 14. The four investigation action families

The player has exactly four action families.

### 14.1 Manual relationship hypothesis

The player may create, edit, and delete a relationship hypothesis between compatible revealed records or nodes.

Requirements:

- free and immediate;
- controlled relationship vocabulary;
- optional note and uncertainty;
- persisted and auditable;
- visibly labeled as player-created;
- never treated as source or analytical fact;
- eligible for case-file inclusion and evaluation as a hypothesis;
- deletion removes the active hypothesis but preserves appropriate audit history.

### 14.2 Zingg candidate reveal

The player selects a bounded compatible set of already revealed records and asks to reveal precomputed candidate-identity relationships among those visible endpoints. A case MAY support discovery of additional records only through an explicit manifest capability with a separate quote, cap, provenance rule, and accessibility path; discovery is never implied by ordinary candidate reveal.

Flow:

1. Validate the selection for free.
2. Generate a backend-authored quote.
3. Show cost, selection scope, model/profile label, result cap, and no-result warning.
4. Require confirmation before debit.
5. Execute a persisted idempotent reveal against immutable published rows.
6. Return zero or more candidate pairs with safe provenance.
7. Persist result and settlement state.

Initial releases MAY use reviewed `CURATED_APPROXIMATION` rows. Such rows MUST state that they are curated approximations and MUST NOT claim actual Zingg execution, precision, recall, runtime, or model metrics.

### 14.3 Exact shared-field reveal

The player selects a bounded set of already revealed records and asks to reveal precomputed exact shared-field relationships among those visible endpoints. Any optional endpoint discovery is an explicit case capability and not the default behavior.

The quote and result must describe:

- approved fields;
- match-any or match-all behavior;
- optional time window;
- minimum match count;
- result cap;
- ambiguity warning;
- no-result possibility.

Player-facing exact-link rows represent exact matches over normalized case-approved fields. The publication provenance states `GRAPHFRAMES`, another approved generator, or `CURATED_APPROXIMATION`; `GRAPHFRAMES` is used only after an actual qualified run. These rows are not runtime traversal, centrality, connected components, communities, or guilt scores.

### 14.4 Bounded natural-language retrieval through the AI-assisted retrieval adapter

The fourth action family is bounded natural-language record retrieval. The player-facing label MUST disclose AI assistance whenever a live generative/provider system participates. Its bound `PROVIDER_EXECUTION_MODE` is one of:

- `LIVE_GENIE`: a qualified commercial Databricks Genie environment;
- `MATERIALIZED_RETRIEVAL`: a deterministic, publication-bound intent/result implementation with the same safe domain contract;
- `DISABLED`: available only where the mode/case explicitly permits a zero-cost unavailable explanation; ranked publication normally requires a completable equivalent.

The player-facing action family and game semantics remain stable across modes, but provenance MUST state the actual mode. A ranking segment never mixes materially different modes.

Flow:

1. The player asks a question.
2. A free, bounded, nonrevealing intent planner proposes safe object types, filters, date scope, sort, and row cap.
3. Unsupported, ambiguous, hidden-truth-seeking, or overbroad intent returns clarification or abstention before debit.
4. The player edits or accepts the interpretation.
5. The backend issues an authoritative quote bound to the normalized intent plan and provider mode.
6. Only after confirmation may the command debit and access the bound player-safe publication/provider.
7. In `PUBLIC_RANKED`, the accepted canonical plan is executed by the deterministic publication-bound resolver; the live provider may contribute interpretation/validation but cannot choose the authoritative record set or order.
8. Result rows pass schema, ownership, case/profile, row/byte, content, intent-consistency, and answer-set-digest validation before reveal.

A direct provider-selected row set is permitted only in a clearly labelled unranked experimental mode with no shared competitive leaderboard. The action MUST never create relationships, infer culpability, expose generated SQL, access protected truth, use private notes as hidden prompt context, or send account/recovery data to a provider. Free Edition is not permitted for public player prompts or ranked evidence [S09][S44].

### 14.5 Valid no-result outcomes

An accepted valid paid action may return no new relationships or no records and still consume the quote. This must be explained before confirmation. Failures attributable to the platform or a nonexecuted request follow refund/retry policy instead.

---

## 15. Investigation economy

### 15.1 Credits

Each round starts with a versioned credit budget defined by its case/family/profile rules. Puppy is generous, Adult moderate, and Senior tight. Exact values are configuration, not hard-coded product constants.

Credits MUST be backed by an append-only ledger. The system MUST prevent:

- negative balances;
- duplicate debits;
- double refunds;
- mutation of historical ledger entries;
- client-side price authority.

### 15.2 Free actions

The following are free when limited to revealed data:

- reading and inspection;
- list/graph switching;
- sorting, filtering, grouping, and column configuration;
- selection and saved subsets;
- manual hypotheses;
- case-file editing;
- saving and loading;
- accessibility controls;
- reviewing provenance;
- submission itself.

### 15.3 Quotes

Every paid action requires a backend-authored quote containing:

- quote ID;
- action family;
- cost;
- round and selection binding;
- expiry;
- result and size limits;
- rule/version references;
- no-result disclosure;
- any relevant warnings.

Expired or mismatched quotes cannot be accepted.

### 15.4 Settlement outcomes

Paid actions must settle as one of:

- charged and completed;
- charged with valid no-result;
- cancelled before execution without charge or with defined refund;
- provider/system failure with refund or reconciliation state;
- indeterminate/recovery-required with no duplicate re-execution.

### 15.5 Efficiency

Efficiency contributes a limited part of the final score. It must reward disciplined use of credits without punishing accessibility needs, reading speed, provider latency, or thoughtful investigation.

---

## 16. Case-file construction

The case file is the player’s structured argument.

It MUST support:

- selection of accused principals and other accused entities;
- nonaccusatory context classifications;
- operational roles;
- culpability classifications;
- victim/harm classifications;
- identity conclusions;
- important relationship conclusions;
- fraud mechanism;
- chronology and money/event flow;
- manipulation tactics;
- explicit claims;
- evidence attached to claims;
- uncertainty and alternative explanations;
- exculpatory or contradictory evidence;
- notes and draft text where enabled;
- undo/redo for current-session edits;
- bounded server-side draft revision history and checkpoint restore;
- record pinning/bookmarks that do not change visibility or score.

### 16.1 Evidence-to-claim mapping

Evidence must be attached to explicit claims. Merely collecting evidence is insufficient.

The system SHOULD warn about:

- unsupported accusations;
- circular evidence;
- duplicate evidence families;
- overreliance on one analytical relationship;
- identity conclusions without support;
- victim or innocent-actor risk;
- contradictions;
- missing mandatory fields;
- broad select-all behavior.

Warnings assist the player but do not reveal the answer key.

### 16.2 Evidence diversity

Independent evidence categories matter. Repeating the same category or derivative copies must not create artificial diversity.

Examples of categories include:

- financial transactions;
- communications;
- contracts or invoices;
- identity/source records;
- direct operational relationships;
- chronology;
- system/device/infrastructure evidence;
- witness or document evidence;
- analytical candidate relationships.

---

## 17. Submission

Submission is free, explicit, and irreversible.

Before submission, the system MUST:

- show a review summary;
- identify unresolved required fields;
- warn about pending paid actions;
- warn that the result is immutable;
- require confirmation.

On confirmation:

- the complete case-file snapshot is frozen;
- all bound rule and content versions are recorded;
- mutable investigation commands are blocked;
- evaluation begins or is queued;
- retries are idempotent;
- the player cannot replace the submission.

The submission includes the selected entities, classifications, mechanism, claims, evidence mappings, uncertainty, relevant relationship conclusions, credit/command snapshot, and version bindings.

---

## 18. Evaluation and scoring

### 18.1 Score scale

Every eligible production submission receives an integer score from `0` to `1000`.

| Component | Points |
|---|---:|
| Principal and mechanism | 250 |
| Roles, culpability, and harm | 180 |
| Money-flow/event reconstruction | 180 |
| Identity conclusions | 100 |
| Relationship interpretation | 90 |
| Evidence quality and diversity | 120 |
| Manipulation tactics | 40 |
| Efficiency | 40 |
| **Total** | **1000** |

A case may refine internal subweights through a signed versioned scoring manifest, but public component meaning and total remain stable unless a new scoring version is explicitly published.

### 18.2 Solve gates

A high numeric score cannot bypass mandatory solve gates. Gates may require correct principal/mechanism, essential flow reconstruction, protection of specified victim/innocent roles, minimum independent evidence categories, and explicit uncertainty where truth is genuinely unresolved.

### 18.3 Penalties

Penalties include false accusations, false identity merges, severe misclassification of victims or innocent actors, unsupported bulk accusations, treating analytical signals as proof, contradictions, duplicated evidence families, missing solve gates, overbroad select-all behavior, and waste that leaves the case materially under-supported.

### 18.4 Canonicalization and semantic equivalence

Scoring operates on a canonical structured submission, not prose style. Equivalent ordering, harmless formatting, locale, spelling, or explanatory verbosity MUST NOT change the authoritative score. Free text may enrich coaching but cannot create or remove authoritative points unless the case manifest defines a safely parsed, testable structured field.

The evaluator MUST pass:

- equivalence tests for semantically identical submissions;
- metamorphic tests for harmless reordering and duplicate references;
- monotonicity tests showing that adding correct supported evidence cannot lower score except where it creates a genuine contradiction or overbreadth;
- sensitivity tests showing that material wrong-principal, false-merge, and innocent-accusation changes affect score;
- determinism and replay tests across the frozen evaluator environment.

A nondeterministic generative model MUST NOT decide score, solve gates, penalties, ending, progression, or ranking eligibility.

### 18.5 Historical reproducibility and amendments

Identical immutable submissions against identical bound versions produce identical verdicts. Historical scores are never silently recomputed. A defect is corrected through a linked versioned amendment as defined in section 33.

### 18.6 Explainability

The verdict provides a safe component breakdown, gate outcomes, penalties, and coaching. It explains strengths, weaknesses, unsupported claims, overbreadth, or missing categories without disclosing protected truth beyond approved closure/debrief content.

## 19. Endings

Every closed evaluated round receives exactly one ending according to deterministic precedence.

| Ending code | Meaning |
|---|---|
| `CLEAN_COLLAR` | Essential gates met, high precision, strong evidence, correct treatment of innocent/victim actors |
| `CASE_CLOSED_KENNEL_WRECKED` | Principal/mechanism substantially correct, but evidence or secondary roles materially incomplete |
| `THE_SCENT_WENT_COLD` | Investigation unresolved or essential claims/evidence missing |
| `BISCUIT_BUDGET_BLOWN` | Poor credit use contributed to an under-supported submission; zero credits alone is insufficient |
| `CHASED_EVERY_SQUIRREL` | Overbroad suspicion, unsupported links, or select-all behavior dominates |
| `BARKING_UP_THE_WRONG_TREE` | Principal/mechanism materially wrong or severe false accusations dominate |

Ending thresholds and precedence are versioned and tested with golden fixtures.

---

## 20. Leaderboards

### 20.1 Hall of Fame

Hall of Fame is opt-in and segmented by `RANKING_SEGMENT`: case, case version, snapshot, investigation profile, provider execution mode/capabilities, relationship publication, rules/economy, scoring/ending versions, and season.

Ranking order is:

1. score descending;
2. accuracy/precision tie-breakers defined in the scoring manifest;
3. efficiency tie-breakers defined in the economy manifest.

Wall-clock elapsed time, reading speed, provider latency, keyboard versus pointer use, accessibility settings, screen-reader use, animation preferences, or audio state MUST NOT affect rank. Players with identical ranking keys share the same rank; the next rank follows the selected standard competition-ranking rule documented in the segment.

Only eligible attempts appear. Academy, Kennel Lab, Practice, replay, revisit, debug, migrated test, invalidated, provider-incompatible, and reviewer-excluded rounds are omitted or shown only in clearly separate noncompetitive views.

### 20.2 Casebook Bloopers / Hall of Shame compatibility label

The humorous failure board is voluntary. The player-facing name SHOULD be “Casebook Bloopers”; the stable internal compatibility code MAY remain `HALL_OF_SHAME`. It MUST require explicit opt-in, use a moderated public alias, expose no login name/private text/prompts, avoid humiliation or protected characteristics, and focus only on fictional investigative mistakes.

### 20.3 Privacy, withdrawal, and disputes

Entries contain only alias, score, approved ending/summary, segment scope, and allowed tie-break fields. A player may withdraw an entry without deleting the underlying private result. Disqualification or moderation uses reason codes, audit records, and a dispute path; detection signals are not automatic proof of cheating.

## 21. Save, load, recovery, and concurrency

### 21.1 Autosave

Autosave uses bounded debounce, optimistic concurrency, and server acknowledgement. The player sees `saving`, `saved`, `offline/retrying`, `conflict`, or `recovery required`. A local browser copy is a convenience draft only and never proves that a ranked write committed.

### 21.2 Ranked checkpoint semantics

Ranked manual save slots checkpoint only reversible player-authored state:

- case-file draft and structured claims;
- private notes;
- bookmarks/pins and saved subsets;
- column layout, filters, panel layout, and graph viewport;
- accessibility and presentation preferences that belong to the round.

Restoring a ranked checkpoint MUST NOT roll back or erase:

- revealed records/documents/relationships;
- command history or provider state;
- credit ledger, debit, refund, or balance;
- quote history;
- round bindings, `as_of_time`, chronology, or ranking segment;
- submission state, verdict, or progression.

If a checkpoint references evidence that has since become visible, it remains valid. If it omits later evidence, the authoritative revealed state still contains that evidence.

### 21.3 Practice and Academy forks

A full-state reset or branch is allowed only by creating a new unranked Practice/Academy round or through an explicitly unranked fixture. It cannot modify or inherit ranking eligibility from the source round.

### 21.4 Resume and provider-state recovery

A retained active round resumes after navigation, refresh, logout/login, application replacement, or database wake. Pending provider and settlement state survives restart. Recovery never duplicates submission, provider work, ledger entries, visibility grants, refunds, or verdicts.

### 21.5 Multi-tab and offline behavior

Two tabs may inspect a round; writes carry explicit revisions and idempotency keys. Stale writes receive a conflict/recovery path instead of overwriting newer work. Ranked state changes require a live server acknowledgement. Service workers and browser caches may cache only approved public static assets, never authenticated API responses, private evidence, case-file drafts, commands, or verdicts.

### 21.6 Completed results

Closed submissions are immutable and read-only. Revisit creates a new noncompetitive round. A score amendment links to the original result and does not reopen the original submission.

## 22. Visual, narrative, and audio experience

### 22.1 Visual direction

The visual language is urban hard-boiled noir, not Western.

Use:

- rain-darkened city streets;
- private offices and police archives;
- typewriters, case files, evidence boards, venetian-blind shadows;
- restrained ink wash, paper grain, halftone, and cinematic lighting;
- believable Spanish Water Dog anatomy and consistent character continuity.

Do not use cowboy hats, sheriff badges, saloons, desert/frontier motifs, wanted-poster composition, or Western typography.

### 22.2 Live functional text

Functional labels, scores, case facts, credentials, dialogue, and player data MUST be live HTML/CSS/SVG text, never baked into raster assets.

### 22.3 Investigation-board composition

The target workspace evokes a noir evidence desk:

- a wide, relatively shallow typewriter/paper case-file area;
- a large graph/evidence area;
- compact Exact-link and Zingg action keys using their approved logos where licensing and project assets permit;
- Databricks/Genie action access;
- clear relationship legend;
- node-type legend and counts;
- minimap where supported;
- no decorative clutter that steals investigation space.

### 22.4 Comics

Every production case requires an opening and closure comic package with:

- final rendered panels;
- responsive crops/variants;
- alt text;
- transcript;
- skip control;
- no baked hidden answers;
- safe fallback when an asset is unavailable.

### 22.5 Radio

The persistent transistor radio:

- plays approved local noir jazz MP3 assets;
- begins only after a valid browser user gesture;
- uses a randomized nonrepeating sequence;
- persists across SPA routes;
- has on/off-only player control;
- contains no gameplay information;
- is excluded from scoring, timing, hints, and evaluator input;
- handles missing tracks without blocking play;
- coordinates multiple tabs so uncontrolled simultaneous playback is avoided;
- remains fully optional.

---

## 23. Accessibility

The complete game MUST target **WCAG 2.2 Level AA** conformance and remain operable without audio and without direct graph manipulation [S03]. Automated checks are necessary but not sufficient; release evidence includes keyboard, zoom/reflow, screen-reader-oriented, touch, reduced-motion, and high-contrast review.

Requirements include:

- keyboard access to all core actions;
- visible focus;
- screen-reader labels and announcements;
- accessible list equivalent for graph information;
- state and relationship semantics not conveyed by color alone;
- high-contrast support;
- reduced-motion support;
- reflow at 320 CSS pixels;
- usability at 200% zoom;
- touch support;
- captions/transcripts for relevant media;
- comic transcripts and skip controls;
- radio-off operation;
- no continuously ticking countdown as a primary failure mechanic;
- deterministic content independent of reading speed or assistive technology;
- a semantic graph navigator that announces current node, neighbors, edge meaning, selection, filters, and available actions;
- an “explain current view” summary for active filters, hidden-by-filter counts, selection, and result provenance;
- plain-language error recovery and cognitive-load controls for dense Senior cases.

Elapsed wall-clock time MAY be retained privately for coarse operational diagnostics only when privacy-approved; it MUST NOT be a competitive tie-breaker or scoring input.

---

## 24. Failure and degradation behavior

### 24.1 General principle

Failure is explicit, bounded, recoverable where possible, and never leaks hidden data or silently changes price, evidence source, provider mode, score rules, or ranking eligibility.

### 24.2 Provider and Databricks degradation

The UI distinguishes application, database, Databricks SQL, Genie Agent, publication, and asset failures. Existing ranked rounds remain bound to their provider execution mode. A live-provider outage may produce retry, bounded reconciliation, pause, declared qualified fallback, or incident invalidation; it cannot silently switch to a materially different answer source.

Databricks Free Edition is development-only and cannot process player prompts, private player data, public ranked evidence, or commercial production traffic [S09][S44].

### 24.3 Repeated deterministic actions

An action whose normalized fingerprint, round bindings, selected visible records, options, intent plan, and publication versions match a settled deterministic command reopens the persisted result without a debit. This includes prior valid no-result outcomes. The UI labels it as history/cache, not a fresh engine run.

### 24.4 Database unavailable or waking

The application shows a safe temporary state and retries idempotently. A browser timeout or failed response never proves that a write did not commit. The player can retrieve the authoritative command/save/submission state after recovery.

### 24.5 Asset and evidence failures

Decorative assets use accessible fallbacks and cannot block play. Missing essential evidence is an explicit publication/incident state. A ranked round with materially unavailable required evidence is paused, invalidated, or amended according to policy; the system never pretends the evidence was available.

### 24.6 Version, signature, or downgrade failure

New round creation fails closed when a publication is incomplete, incompatible, unsigned, signature-invalid, revoked, quarantined, or older than the active anti-downgrade floor. Historical rounds continue only when their exact immutable package remains safe and available.

### 24.7 Unsupported or unsafe actions

Invalid selections, unsupported fields, malformed questions, overbroad intent, cross-case requests, hidden-truth requests, and disallowed discovery are rejected before charge whenever possible with a player-safe explanation and correlation ID.

## 25. Privacy, security, and data handling requirements

### 25.1 Player data

Player usernames, session data, private notes, prompts, drafts, saves, and case files are private. They are not shared with other players or placed on leaderboards.

### 25.2 Hidden truth

Protected truth MUST NOT appear in:

- browser bundles;
- source maps;
- public static files;
- player-safe tables/views;
- Genie datasets;
- logs;
- screenshots/traces intended for players;
- error details;
- client-side scoring logic.

### 25.3 Synthetic data

Playable evidence is synthetic. Reserved domains and nonreal identifiers are required. Real secrets, accounts, private contact details, live exploit paths, or copied real-person accusations are prohibited. Synthetic rows undergo memorization, rare-combination, membership-inference, narrative, and dual-use review.

### 25.4 Security behaviors visible to users

- generic authentication errors;
- secure logout;
- expired-session handling;
- CSRF/origin/host protection without exposing internal details;
- ownership enforcement;
- input and output encoding;
- rate-limit feedback;
- signed publication verification and anti-downgrade enforcement;
- no authenticated-response caching in a service worker;
- safe error correlation IDs where useful.

### 25.5 Export

A player export, if provided, contains only player-visible synthetic evidence and the player’s own case material. It excludes hidden truth and protected internal identifiers.

---

## 26. Case-package functional contract

A production case cannot be published without a complete versioned manifest containing at least:

- stable case ID, title, family, order, and version;
- publication state;
- fictionalization and historical-debrief content;
- three cumulative investigation-profile snapshots;
- starting records and reveal rules;
- object, event, document, and relationship types;
- player-safe fields and Genie-safe fields;
- direct relationships;
- Zingg candidates and exclusions;
- exact shared-field matches, generator provenance, and ambiguity warnings;
- economy, quote, and limit rules;
- valid roles, culpability, harm, identity, and relationship conclusions;
- claims and evidence categories;
- protected truth;
- scoring weights and solve gates;
- penalties and ending thresholds;
- opening and closure assets, transcripts, and fallbacks;
- accessibility requirements;
- deterministic strategy/playthrough fixtures;
- leaderboard eligibility;
- checksums and rollback metadata.

Publication is atomic. An incomplete case remains disabled rather than partially playable.

---


## 27. First-run onboarding, consent, and account recovery

The first authenticated experience is short, recoverable, and explicit. It contains:

1. fictionalization, educational purpose, and “not real-world decision support” boundary;
2. age/content suitability acknowledgement required by the deployment jurisdiction, without exact birth-date collection unless legally required;
3. spoiler-safe explanation of Career, Academy, Practice, and Review;
4. recovery-code generation and confirmation that the player stored at least one code;
5. privacy and optional telemetry choices with no dark patterns;
6. accessibility shortcuts and the ability to start without audio, animation, custom cursors, or graph manipulation;
7. a brief glossary covering record, entity, direct relationship, candidate identity, exact shared field, hypothesis, claim, evidence, role, culpability, and harm;
8. content warnings that can be reviewed again before sensitive cases.

The player can revisit onboarding, regenerate recovery codes after recent reauthentication, change telemetry preference, and download or print an accessible recovery-code sheet. Recovery codes are secrets: they are sufficiently random, one-way protected at rest, shown in full only when generated, individually single-use, rate-limited, and excluded from logs/analytics.

## 28. Data-source, content, and licensing governance

### 28.1 Source-use principles

External public information is an authoring input, not runtime truth. Approved sources may inform schemas, field distributions, legitimate comparators, procurement structures, beneficial-ownership patterns, corporate filings, exclusion-list provenance, and aggregate fraud trends. They MUST NOT copy a named real person into a playable accusation.

Each source receives a machine-readable record covering owner/jurisdiction, official landing page, access method, snapshot date, exact license/terms, attribution/database rights, permitted and prohibited uses, personal/sensitive-data class, disclaimers, integrity/staleness, transformation lineage, checksums, synthetic-generation relationship, retention, and legal/privacy/security approvals.

“Publicly accessible” never means free of license, privacy, fairness, security, reputational, fair-access, database-right, or trademark constraints. A changed term, source-integrity incident, revoked license, or missing approval blocks new publication.

### 28.2 Candidate sources for synthetic case design

| Source family | Useful schema or learning value | Required caution |
|---|---|---|
| GLEIF Global LEI Index [S22] | Legal entities, names, addresses, parent relationships, mappings | Respect terms/update cadence; no guilt implication |
| Open Ownership / BODS [S23] | Beneficial-ownership statements, interests, provenance | Jurisdictional completeness varies; transform to fiction |
| ICIJ Offshore Leaks [S24] | Offshore entity/intermediary/address motifs | Apply license/attribution and explicit “presence does not imply wrongdoing” disclaimer |
| TED Open Data and OCDS [S25][S36] | Procurement notices, lots, awards, buyers, suppliers, amendments | Normalize schema versions; contracts are legitimate by default |
| USAspending [S26] | Award, recipient, agency, and transaction structures | API/data-quality caveats; synthetic transformation only |
| SEC EDGAR APIs [S27] | Filings, submissions, company facts, accounting concepts | Follow fair-access policy; filings are not fraud labels |
| Companies House API [S28] | Company/officer/filing schema and chronology | Track availability/integrity incidents; identity is not culpability |
| Official EU/UK sanctions sources [S29][S30] | Provenance, identifiers, aliases, effective dates | High-risk personal data; research-only unless specially approved and fictionalized |
| OpenSanctions [S31] | Integrated provenance and entity-matching research | Review license/commercial use and source-level attribution; no direct playable persons |
| World Bank ineligible firms and procurement [S48][S49] | Exclusion/procurement schema, decision dates, grounds, supplier structure | Decisions need context; never copy named parties into play |
| SAM.gov public exclusions/entity data [S50] | Exclusion and federal entity registration schemas | Use only approved public extracts/APIs; sensitive/nonpublic interfaces are prohibited |
| UK Find a Tender OCDS and Contracts Finder archive [S51][S77] | Current and historical UK notice/award structures | Use Find a Tender as current; mark Contracts Finder `ARCHIVE_ONLY`; synthetic comparators only |
| EU Financial Transparency System [S52] | EU funding recipient, programme, amount, and year schema | Publication threshold/scope varies; no wrongdoing inference |
| FTC, IC3, Europol, and ACFE reports [S32–S35] | Aggregate trends, mechanisms, educational debrief references | Complaint/report statistics are not adjudicated truth |
| EU Arachne [S57] | Restricted risk-scoring concepts and governance lessons | Not open data; reference-only unless a separate lawful access basis exists |

### 28.3 Content and data cards

Every case package includes a public content card and a protected authoring data card. The public card states fictionalization, themes, content warnings, profile, provider mode, accessibility alternatives, and known nonspoiler limitations. The protected card records sources, synthetic method, temporal boundary, quality/fairness/privacy tests, dual-use review, exclusions, residual risks, and approvals.

### 28.4 Brand, dependency, and asset rights

Databricks, Zingg, GraphFrames, and other names/logos are used only under current license/trademark/brand rules. A logo is never required to understand a control. Zingg’s exact AGPL/community or commercial artifact obligations are release-reviewed; no assumption is made from product marketing alone [S20][S21]. Missing approval fails the asset/dependency gate.

## 29. Current fraud landscape and future training backlog

The fixed ten-case anthology remains the ranked target. Current public reporting informs Academy refreshes, debriefs, and a governed post-release backlog rather than becoming direct playable evidence.

The FBI’s 2025 IC3 report recorded 1,008,597 complaints and approximately USD 20.877 billion in reported losses; investment-related losses were approximately USD 8.649 billion and business-email-compromise losses approximately USD 3.047 billion [S33]. FTC reporting for 2025 described approximately USD 16 billion in reported fraud losses, including approximately USD 3.5 billion from imposter scams and USD 2.1 billion associated with fraud that began on social media [S32][S58]. Europol’s IOCTA 2026 describes increasingly industrialized and AI-assisted abuse, malicious advertising, SIM-box infrastructure, crypto/neo-bank misuse, and more autonomous criminal workflows [S34]. ACFE’s 2026 Report to the Nations supplies cross-jurisdiction occupational-fraud case patterns [S35]. These are reports, complaints, and study samples—not adjudicated truth for any individual.

Candidate future Academy or anthology material includes:

- AI-assisted executive impersonation and synthetic-media escalation;
- malicious-ad-to-investment-funnel attribution;
- SIM-farm/SIM-box infrastructure shared by legitimate and malicious traffic;
- crypto-drainer and recovery-scam re-victimization;
- remote-worker identity and payroll diversion;
- cross-platform mule recruitment with mixed victim/recruiter roles;
- procurement integrity with beneficial-ownership opacity;
- sanctions/entity matching across scripts, transliteration, and aliases;
- exclusion-list false positives and effective-date reasoning;
- supplier collusion indicators with legitimate emergency-procurement comparators.

Adding a case requires the complete case-package, fairness, accessibility, evaluation, source, legal, dual-use, security, and publication gates. News alone never becomes playable evidence.

## 30. Research-informed analytical quality and fairness

### 30.1 Entity resolution

Pairwise candidate quality is insufficient. Publications MUST be evaluated at pair, cluster, and entity-centric levels. Tests cover false merges/splits, transitivity, oversized components, hard negatives, common names, household/shared-service data, transliteration, Unicode normalization, cross-script aliases, missingness, and uncertainty calibration.

OpenSanctions Pairs contains a large multilingual, multi-source labeled pair corpus and reinforces the importance of blocking, cross-script matching, and source-aware evaluation [S37]. In-context clustering research reinforces that production entity resolution must reason beyond isolated pairs [S38]. No learned entity-resolution score is presented as guilt.

### 30.2 Natural-language retrieval and schema selection

Enterprise text-to-SQL remains difficult on realistic schemas [S39]. The retrieval action is therefore a bounded intent-and-record service, not an oracle. Each case/profile/provider-mode combination has answerable, ambiguous, adversarial, cross-case, hidden-truth-seeking, Unicode, overbroad, and no-result benchmarks. New schema-retrieval research is tracked because selecting the wrong tables/columns can fail before SQL generation [S59].

### 30.3 Synthetic-data fidelity and privacy

Synthetic validation covers schema/referential integrity, important marginals/joints, chronology, time zones, intervals/bursts/reversals, multi-account/device behavior, graph motifs, legitimate shared infrastructure, solve routes, nearest-neighbor and rare-combination similarity, memorization, membership inference, sensitive-attribute leakage, and manual narrative review.

Recent financial synthetic-data research emphasizes explicit privacy/utility measurement [S41], including multi-table membership-inference risk [S53] and relation-aware attacks against tabular diffusion models [S67]. Graph-oriented generators and AML benchmarks such as Tide and TransXion illustrate the need to preserve temporal and network structure rather than only row distributions [S54][S55]. SynthEval and realistic synthetic transaction research inform reproducible evaluation frameworks [S56][S60]. These papers are research inputs, not automatic production dependencies.

### 30.4 Temporal integrity

Every case snapshot has an `as_of_time`, timezone policy, and narrative phase. Starting evidence, direct relationships, analytical signals, benchmarks, and evaluator expectations may use only information available at or before the applicable boundary unless the story explicitly advances time. Future information cannot leak into an earlier decision point. Leakage-safe graph-feature principles apply to offline research models [S42].

### 30.5 Fairness and accessibility-sensitive testing

Protected or sensitive attributes MUST NOT drive suspicion, price, score, culpability, or graphical salience. Tests compare candidate quality, false-merge risk, evidence availability, and evaluator behavior across synthetic language, script, name pattern, age role, disability-relevant, and socioeconomic variations where relevant. Accessibility tools and slower interaction cannot be treated as suspicious behavior or competitive disadvantage. Current counterfactual AML research further supports testing direct and indirect sensitive-feature effects rather than relying only on aggregate parity metrics [S66].

## 31. Privacy, telemetry, export, and deletion

### 31.1 Data minimization

The service collects only data required for authentication, security, game state, optional ranking, and explicitly approved analytics. Raw retrieval questions, private notes, recovery codes, passwords, case-file prose, and evidence annotations do not enter general telemetry or ordinary application logs.

### 31.2 Optional telemetry

Telemetry is consent-based or otherwise uses an approved lawful basis for the deployment. Events use coarse identifiers and may include route, action family, outcome class, latency/result-count bucket, accessibility mode, and version. They contain no synthetic record content, hidden truth, free text, public alias, or account credential. The player can change preference without losing game functionality.

### 31.3 Export

An authenticated player may request an export containing account metadata, careers/rounds, ledger, saves, submissions, verdicts/amendments, and their private text, plus only player-visible synthetic evidence required for context. It excludes secrets, other players, protected truth, provider credentials, internal source metadata, and restricted licensed material.

### 31.4 Deletion

A player can request deletion after recent reauthentication or recovery-code verification. The service explains deletion, pseudonymization, security/audit retention, leaderboard withdrawal, and backup expiry. No result remains publicly linked to the player after withdrawal/deletion.

### 31.5 Baseline retention schedule

The release policy defines machine-testable defaults, adjustable only through approved legal/privacy configuration:

| Data class | Baseline maximum |
|---|---:|
| Unused recovery-code verifier | Until used, regenerated, or account deletion |
| Active session | 30 days idle and 90 days absolute, unless stricter deployment policy applies |
| Security/audit events | 90 days online; longer only when documented and access-restricted |
| Generated export archive | 7 days after ready, then deleted |
| Raw optional telemetry | 30 days before aggregation/deletion |
| Abandoned unsubmitted round private text | 180 days after inactivity, with prior notice where practical |
| Deleted-account remnants in ordinary backups | Expire within 35 days unless an incident/legal hold applies |

The public privacy notice states the deployed values. Legal holds and incident preservation are exceptional, documented, access-controlled, and never used for product analytics.

## 32. Leaderboard integrity, moderation, and disputes

Leaderboards are optional and privacy-preserving by default. Integrity controls include:

- one eligible ranking result per configured attempt policy;
- detection of impossible client sequences, duplicate-account abuse, replayed idempotency keys, automated command bursts, and modified clients;
- server-authoritative timing and event order;
- alias profanity, impersonation, and personal-data moderation;
- transparent disqualification reason codes and an operator audit trail;
- a player-visible withdrawal and dispute path;
- season/version segmentation so materially changed cases do not share one ranking pool.

Detection signals do not automatically prove cheating. Ambiguous cases receive review, and private security details are not exposed. Accessibility tools, slow reading, keyboard-only play, assistive technology, and provider latency MUST NOT be treated as suspicious behavior.

## 33. Evaluation amendments, appeals, and historical integrity

A verdict is immutable as the result of a specific submission and evaluator version, but software can contain defects. The correction model is:

1. preserve the original submission and verdict;
2. mark the verdict `VALID`, `UNDER_REVIEW`, `INVALIDATED`, or `SUPERSEDED` with a reason and timestamp;
3. reproduce the issue against the original immutable inputs;
4. publish a new evaluator/scoring version;
5. create an amendment linked to—not overwriting—the original;
6. update career progression only when policy and fairness require it;
7. transparently remove, restore, or reindex leaderboard entries;
8. notify the affected player in-product without revealing protected truth.

A player can report a suspected technical error using a safe correlation ID. Appeals concern system behavior, scoring defects, or moderation; they do not provide unrestricted access to the answer key.

## 34. Product service, recovery, and degradation commitments

Service objectives are release-profile targets, not unconditional external guarantees.

| Measure | `DEVELOPMENT` / `DEMO` | `PUBLIC_RANKED` target |
|---|---:|---:|
| Core application availability | Best effort / documented | 99.5% monthly, excluding announced maintenance and separately measured provider degradation |
| Warm p95 authenticated read | Measured | ≤ 500 ms server time |
| Warm p95 quote creation | Measured | ≤ 750 ms server time |
| Warm p95 autosave acknowledgement | Measured | ≤ 1 second server time |
| Database RPO | May be ≤ 24 hours if explicitly labeled | ≤ 15 minutes with qualified PITR/continuous backup |
| Database RTO | ≤ 8 hours target | ≤ 4 hours for declared disaster |
| Duplicate debit/refund tolerance | Zero | Zero |
| Hidden-truth leakage tolerance | Zero | Zero |
| Accessible completion path | Required | Required for every release-blocking journey |

Provider-dependent actions expose independent state and do not make the rest of the game unavailable. A public ranked launch is blocked until the database, provider mode, backup/restore, incident, and ranking-segment controls meet the `PUBLIC_RANKED` profile. A demo cannot be mislabeled as production-grade.

## 35. Strategic product decisions and long-term backlog

| Decision | Required resolution point | Default until resolved |
|---|---|---|
| Production database provider | Iteration 20 release freeze | PostgreSQL-compatible managed database; portable PostgreSQL 16 schema; no local-volume durability assumption |
| Lakebase versus independent PostgreSQL | Integration qualification | Adapter-neutral migrations; qualify one primary and one recovery path |
| Public provider mode | Before ranked publication | `MATERIALIZED_RETRIEVAL` unless a commercial `LIVE_GENIE` environment passes capability/privacy/fairness qualification |
| Zingg artifact and AGPL/commercial obligations | Before distribution or hosted use | Treat direct dependency use as legally blocked; curated/independently generated candidates remain truthfully labeled |
| Logo/trademark use | Asset freeze | Text labels plus project-owned icons; third-party logos omitted without approval |
| Object storage/CDN | Performance gate | Approved content-addressed assets in immutable image |
| Passkeys/WebAuthn | Public-ranked security gate or signed risk acceptance | Password + recovery codes remain the compatibility baseline; add optional passkeys and session-device controls [S68] |
| Real-time collaboration | Future product decision | Out of scope |
| Additional anthology cases | After ten-case release | Governed backlog only; no schedule promise |
| Public age rating and regional availability | Legal/content release gate | Not directed to under-13s; jurisdiction-configured suitability and warning policy |

## 36. Functional acceptance criteria

The product is functionally acceptable only when all applicable criteria pass:

1. Sign-in and account creation are explicit separate actions on one accessible surface; a typo cannot create an account.
2. Authentication is enumeration-resistant, usernames are spoof-resistant login identifiers, recovery codes are one-time protected secrets, and sessions meet policy.
3. Multiple incomplete named careers coexist without destructive replacement; one default-resume pointer has no lifecycle authority.
4. The two-screen selector works with mouse, keyboard, touch, switch-like navigation, and screen-reader paths.
5. All case cards show correct primary state plus independent availability reason.
6. Career paths and family transitions follow the fixed order and unlock atomically.
7. List, graph, and semantic graph navigator expose one synchronized revealed state.
8. All four action families implement validation, free intent preview where applicable, quote, confirmation, provenance, persistence, and failure policy.
9. Analytical reveals default to visible endpoints; any discovery capability is explicit, capped, and tested.
10. Zingg/GraphFrames never run live in a player round and provenance never invents engine execution or metrics.
11. Every round binds provider execution mode, semantic configuration, publication versions, `as_of_time`, and ranking segment.
12. Free Edition or other noncommercial/no-SLA environments cannot process public ranked play, private player prompts, or commercial traffic.
13. Credits cannot become negative, duplicate debit/refund, or be recovered through save restore.
14. Ranked saves restore only reversible draft/UI state; evidence, commands, ledger, chronology, and submissions remain monotonic.
15. Autosave, restart recovery, browser timeouts, and multi-tab conflicts are safe and idempotent.
16. Service workers/browser caches never cache authenticated API responses or become ranked-state authority.
17. The case file keeps identity, role, culpability, harm, accusation, claims, evidence, and uncertainty separate.
18. Submission is immutable and blocked by nonterminal or economically indeterminate paid work.
19. Evaluation is deterministic, canonicalized, semantically equivalent, version-bound, and generative-model-independent.
20. One score and one ending are produced, with safe explanation and tested amendment lineage.
21. Wall-clock time and accessibility behavior never affect score or rank; exact ties share rank.
22. Progression is atomic and Practice/revisit is score-neutral.
23. Leaderboards are opt-in, mode/version segmented, moderated, withdrawable, and dispute-capable.
24. Academy T1–T12 and protected T13–T15 exercise the same core contracts.
25. The complete game works without audio, animation, custom cursor, or direct graph manipulation.
26. Hidden truth is absent from browser, normal API routes, logs, telemetry, static assets, provider views, and downloadable exports.
27. The evaluator reaches protected truth only through the narrow Truth Broker boundary.
28. Every snapshot enforces `as_of_time` and passes temporal-leakage validation.
29. Every source/dependency/media artifact has current license, terms, attribution, provenance, checksum, and approval state.
30. Synthetic data passes schema, behavior, graph, temporal, fairness, memorization, rare-combination, and membership-inference tests.
31. Content passes fictionalization, age/content-warning, victim-respect, stereotype, and dual-use review.
32. Account export, deletion, telemetry preference, leaderboard withdrawal, and recovery flows pass end to end.
33. Signed image and case manifests pass provenance, signature, revocation, quarantine, and anti-downgrade tests.
34. Public ranked profile meets PITR, RPO/RTO, restore, incident, and publication-quarantine exercises.
35. Provider modes are completable and competitively fair; a provider change creates a new ranking segment unless equivalence is proven before publication.
36. The exact signed release image behaves the same in local qualification and deployment, while each runtime role retains its qualified identity, secrets, network policy, and entrypoint.

## 37. Player quick rules

1. Connections are clues, not convictions.
2. Manual links are your hypotheses and are free.
3. Zingg links are possible shared identities, not proven merges.
4. Exact shared-field links may be generated with GraphFrames and may be legitimate.
5. AI-assisted retrieval returns bounded records; it does not solve the case or decide guilt.
6. Paid actions always show a price before execution.
7. A valid paid action can return no result.
8. Zero credits does not prevent submission.
9. Protect victims and innocent actors from unsupported accusations.
10. Use more than one independent evidence category.
11. Submitting is irreversible.
12. Selecting everything cannot win.

---


## 38. Release profiles, provider capability, and competitive compatibility

### 38.1 Environment profiles

| Profile | Intended use | Player/private data | Durability | Ranking |
|---|---|---|---|---|
| `DEVELOPMENT` | Local engineering and automated tests | Synthetic test identities only | Best effort | Never eligible |
| `DEMO` | Reviewer/demo deployment | Limited test/demo accounts under explicit notice | Documented backup/recovery limitations | Never mixed with public ranked pools |
| `PUBLIC_RANKED` | Public competitive release | Approved production handling | Qualified managed durability, PITR, restore, incident controls | Eligible |

The UI and release metadata state the active profile. A demo or Free Edition environment cannot present itself as `PUBLIC_RANKED`.

### 38.2 Provider execution modes

A case/profile publication declares the supported retrieval mode, capabilities, row limits, benchmark version, privacy posture, and fallback policy. `LIVE_GENIE` requires a commercial qualified environment, current capability detection, leakage/adversarial benchmarks, retention review, and result firewall. `MATERIALIZED_RETRIEVAL` uses deterministic signed publications and is the safe default. `DISABLED` cannot make a ranked case unsolvable.

### 38.3 Ranking compatibility

A ranking segment key includes every factor that can materially affect evidence availability or cost. At minimum: case/snapshot/profile, provider mode and semantic configuration, direct/analytical publication versions, economy, scoring, endings, progression rules, and season. A materially changed provider model, table set, instruction set, fallback, or row cap creates a new segment unless a prepublication equivalence study proves no competitive effect.

## 39. Content suitability and dual-use safety

Every case and debrief receives:

- an age/content suitability classification;
- spoiler-safe warnings for coercion, financial loss, relationship manipulation, impersonation, exploitation, or other sensitive themes;
- humane treatment of victims and mixed victim/recruiter roles;
- review for stereotypes and protected-attribute proxies;
- a dual-use assessment distinguishing detection education from operational criminal enablement.

The product may explain indicators, evidence reasoning, controls, and defensive lessons. It MUST NOT publish live credentials, current exploitable targets, copy-ready social-engineering scripts, money-laundering optimization, sanctions-evasion playbooks, anti-forensic instructions, or procedural detail unnecessary for the learning objective. Sensitive debrief detail uses the minimum sufficient defensive abstraction.

## 40. Consolidated inherited product invariants

1. Sign-in failure never creates an account.
2. A public alias is never an authentication identifier.
3. Creating a career never archives another career.
4. A ranked checkpoint never restores credits or unreveals evidence.
5. Browser offline state never outranks the server ledger or submission.
6. A round never changes provider execution mode after creation.
7. Materially different provider modes never share a ranking segment.
8. Free Edition never handles public player prompts or ranked production traffic.
9. Wall-clock time never affects score or rank.
10. Equivalent structured conclusions receive equivalent authoritative scoring.
11. Normal web routes never read protected truth directly.
12. Unsigned, revoked, quarantined, or downgraded publications cannot start new rounds.
13. A public ranked release has qualified PITR, restore, incident, and provider-degradation behavior.
14. Fraud education never becomes an operational wrongdoing guide.

15. A ranked case has a tested provider-independent clean solve.
16. A preview provider capability is never the sole ranked completion path.
17. AI-assisted retrieval provenance and disclosure match actual execution.
18. A stale/incompatible client cannot mutate ranked state.
19. Database session loss cannot violate game, economic, or publication correctness.
20. Public player free text is not published under the baseline product.
21. Every public release has current jurisdiction, AI, accessibility, processor, and residency applicability records.
22. Incident, appeal, moderation, and amendment outcomes are auditable and player-visible at a safe level.

## 41. AI-assisted retrieval transparency and provider maturity

### 41.1 Player disclosure

The natural-language action is labeled **AI-assisted retrieval** when a live generative/provider system participates. Before the player confirms a paid action, the interface MUST state:

- the actual execution mode (`MATERIALIZED_RETRIEVAL`, qualified `LIVE_GENIE`, or unavailable);
- whether an external provider receives the question;
- the exact player-safe context categories sent;
- the maximum result rows and cost;
- that the system may misunderstand, abstain, or return incomplete results;
- that results are records, not guilt, identity, or fraud conclusions;
- the provider/configuration version and whether the capability is preview-qualified.

A materialized deterministic implementation is not described as a live AI run. A live AI response is never represented as deterministic beyond the persisted result returned to that round.

### 41.2 Maturity and change policy

Provider maturity is a release-gated input at the individual API/capability level. The Genie Conversation API is generally available. Genie Agent mode became generally available on 2 July 2026, while its programmatic Agent mode APIs and selected result/benchmark surfaces remain Beta; neither a product-level GA label nor GA of one operation approves another [S05][S74][S85][S86][S110][S111]. `LIVE_GENIE` may be enabled for public ranked play only when the exact API, region, commercial terms, privacy/retention configuration, limits, benchmark, incident process, and deprecation risk are approved. A preview/beta capability requires a signed `PREVIEW_EXCEPTION` with an owner, expiry, fallback, rollback trigger, and explicit statement that it is not the sole completion path.

A provider model, instruction set, table set, API version, row cap, or safety behavior change creates a new capability snapshot and normally a new ranking segment. The player receives a concise disclosure when a new round binds a materially changed provider.

### 41.3 EU AI transparency readiness

Before an EU public release, the project records whether Article 50 or other AI Act transparency obligations apply and implements the required notice. The Commission published Article 50 guidance on 20 July 2026 and the transparency obligations apply from 2 August 2026 [S69][S88][S104]. The game does not rely on a “video game” characterization to avoid disclosure: AI-assisted interaction is identified plainly whenever it occurs.

## 42. Account hardening, passkeys, and session/device control

### 42.1 Passkeys as an additional authenticator

The password-and-recovery-code baseline remains supported. The product SHOULD add WebAuthn/passkeys as an optional phishing-resistant authenticator before `PUBLIC_RANKED` scale. Passkeys:

- are registered only after recent authentication;
- use the production origin/RP ID and secure contexts;
- support accessible platform and roaming authenticators;
- never make a single device the only recovery route;
- can be named, reviewed, and individually revoked;
- are not silently downgraded to a weaker flow;
- follow current WebAuthn Level 3 and NIST guidance [S01][S68].

### 42.2 Session/device management

The account area lists active sessions using safe approximate metadata: creation time, last activity, broad browser/device class, and approximate region only when privacy-approved. The player can revoke one session or **log out all other sessions**. Password reset, recovery-code regeneration, passkey changes, and operator reset revoke or rotate affected sessions according to policy.

Security events are communicated in-product because email is not collected. Notices cannot reveal enough detail to aid an attacker. The product never claims that browser fingerprints uniquely identify a person.

### 42.3 Recovery-loss boundary

The product clearly warns that losing the password, all recovery codes, and all registered passkeys may require a protected operator process and may still result in account loss. An operator reset requires documented identity/support evidence appropriate to the deployment and cannot reveal credentials, truth, or private case content.

## 43. Provider-independent solvability and competitive continuity

Every published ranked case MUST have at least one tested `PROVIDER_INDEPENDENT_SOLVE` route. The route may use initial evidence, direct relationships, deterministic analytical publications, and `MATERIALIZED_RETRIEVAL`; it cannot require a live external model or provider conversation.

For each case/profile, release evidence includes:

- a clean provider-independent golden playthrough;
- a zero-live-provider partial and clean solve test;
- proof that provider outage cannot strand a paid command without reconciliation;
- a comparison of evidence availability and cost across supported provider modes;
- a declared fallback and ranking-segment rule;
- a deprecation plan if a provider API, region, model, or product is withdrawn.

A live provider MAY enrich convenience or offer an equivalent retrieval implementation, but it cannot make the game solvable only for players who received one provider behavior. Mid-round provider substitution remains prohibited unless the fallback was prequalified as equivalent and bound in the round contract.

## 44. Legal, regional, accessibility, and public-content governance

### 44.1 Release applicability record

Every public release records target jurisdictions and an approved applicability decision covering privacy/data protection, consumer terms, age suitability, AI transparency, accessibility, public rankings/user-generated content, processor/subprocessor use, international transfers, and local retention requirements. “Not applicable” requires a rationale and reviewer.

### 44.2 Accessibility-law readiness

WCAG 2.2 Level AA remains the product baseline. For EU distribution, procurement, or covered services, the project additionally maps applicable requirements from the European Accessibility Act and the current published EN 301 549 baseline, while monitoring the next standard revision [S03][S71][S72]. An accessibility statement, known-limitations process, and contact/redress route are release artifacts.

### 44.3 Public-content minimization

The ordinary public surface contains only moderated aliases and approved derived score fields. Player notes, prompts, case-file prose, screenshots, and free-text explanations are never public. Before enabling comments, sharing, profiles, or other user-generated content, the product requires a new moderation, safety, privacy, and Digital Services Act/platform-law review [S70].

### 44.4 Data processors and residency

The privacy notice and internal register identify hosting, database, observability, provider, support, and other processors/subprocessors, their regions, transfer mechanism, retention, training/use posture, and incident obligations. A provider whose terms permit broad access or training on submitted content cannot receive player or proprietary data without an explicit lawful and product-approved basis.

## 45. Player support, status, incidents, and redress

The product provides a player-safe support and incident model:

- a status/degradation surface for core application, database, retrieval provider, publication, evaluation, and assets;
- correlation IDs and safe diagnostic summaries;
- explicit incident categories: service, economic settlement, scoring/evaluation, publication/evidence, security/privacy, moderation, and account access;
- in-product notices for materially affected rounds or results;
- a ticket/reference state visible to the player where support is offered;
- appeal/dispute status for scoring amendments and moderation;
- no request for passwords, recovery codes, provider tokens, or hidden truth.

A diagnostic bundle is generated only after the player previews and explicitly approves the safe fields. It excludes raw prompts, private notes, case-file prose, evidence content, credentials, and protected identifiers by default.

## 46. Browser, device, localization, and client compatibility

### 46.1 Supported clients

Each release publishes a browser/device support matrix based on current stable Chromium, Firefox, and Safari families plus touch/mobile coverage. Core play MUST work with keyboard, touch, zoom, reduced motion, high contrast, and the accessible noncanvas graph path. Unsupported clients receive a clear explanation without exposing security details.

### 46.2 Client compatibility state

The server classifies the SPA as `SUPPORTED`, `REFRESH_REQUIRED`, or `BLOCKED` based on build digest and API/Core Contract compatibility. A stale client may read safe immutable history when compatible but cannot create ranked commands, accept quotes, save authoritative drafts, or submit after its write contract is blocked. Forced refresh preserves server-acknowledged state.

### 46.3 Localization invariants

Functional copy is externalized and versioned. Locale affects display only; identifiers, sorting tie-breakers, money representation, timestamps, canonical submissions, scoring, costs, and ranking keys remain locale-independent. Translations receive spoiler, accessibility, content-safety, and terminology review. Case currency is explicit and is never inferred from the player locale.

## 47. Open-data portfolio refresh

The following sources are added or reclassified as governed authoring inputs. None is directly playable and none supplies a guilt label.

| Source | Useful fictional schema/design value | Version 6.0 constraint |
|---|---|---|
| Find a Tender OCDS [S51] | Current UK procurement notices, awards, procedures, amendments, identifiers | Primary current UK procurement source; pin API/schema and OGL terms |
| Contracts Finder [S77] | Historical lower-value notices and legacy structures | `ARCHIVE_ONLY`; do not treat as the current canonical UK procurement feed |
| Companies House PSC snapshot [S78] | Beneficial ownership/control statements, effective dates, company-person links | Public-person identifiers require strict fictionalization and privacy review |
| IRS EO BMF and Form 990 XML [S79] | Charity entities, filings, officers, grants, expenses, related organizations | U.S. tax-exempt status is not a fraud indicator; schema/aggregate research only |
| CMS NPPES [S80] | Provider identifiers, organization/person distinctions, taxonomy, practice locations | Public professional data; no direct playable person and no medical inference |
| CMS Open Payments [S81] | Payment categories, manufacturers, providers, dates, dispute/publication status | Payment disclosure is not wrongdoing; preserve reporting context in synthetic design |
| HHS OIG LEIE [S82] | Exclusion effective dates, reinstatement, entity/person identifier patterns | High-risk adverse data; named entries never become playable actors |
| Charity Commission register [S83] | Charity purposes, trustees, accounts, status, regulatory chronology | Terms/OGL and personal-data review; legitimate charities are the default comparator |
| Open Ownership BODS 0.4 [S23][S84] | Structured beneficial-ownership statements and provenance | Pin BODS 0.4 transform; record standards-development pause and source snapshot |

Source approval requires a machine-readable terms snapshot, exact extraction method, data-class classification, allowed transformations, quality caveats, synthetic relationship, and deletion/quarantine plan.

## 48. Research and threat-landscape refresh

Version 6.0 retains and extends the 2025–2026 research watchlist as concrete product tests:

- **Entity resolution:** evaluate pair, cluster, and entity-centric quality; include cross-script names, source-aware blocking, false transitive closure, common service addresses, and oversized components [S37][S38].
- **Schema retrieval/text-to-SQL:** benchmark table/column selection separately from query execution; require clarification and abstention rather than confident wrong-schema retrieval [S39][S59].
- **Synthetic privacy:** run single-table, multi-table, relational, rare-combination, and nearest-neighbor attacks; document utility/privacy tradeoffs rather than declaring data “anonymous” [S41][S53][S56][S67].
- **Temporal/graph fidelity:** preserve causal ordering, burst/reversal behavior, graph motifs, and leakage-safe feature boundaries [S42][S54][S55][S60].
- **Fairness:** use counterfactual and slice tests for direct and indirect sensitive-feature effects; do not rely on one aggregate parity metric [S66].
- **Accessible graph interaction:** continue semantic navigation and list equivalence rather than assuming a visual canvas is accessible [S43].

Current fraud reports continue to inform fictional typologies and debriefs, not accusations. Reported complaints/losses are not adjudicated truth [S32]–[S35][S58].

## 49. Workflow liveness and player-visible completion guarantees

### 49.1 Liveness classes

Every asynchronous or externally dependent operation declares a `WORKFLOW_LIVENESS_CLASS`:

| Class | Typical use | Product guarantee |
|---|---|---|
| `INTERACTIVE` | Fast local write completed during a request | The request either commits or returns a recoverable authoritative state |
| `SCHEDULED` | Export, deletion, retention, notice fan-out | A guaranteed scheduler claims due work without player traffic |
| `ALWAYS_ON` | Ranked command reconciliation, evaluation dispatch, critical incident actions | A fenced executor is continuously available or admission closes |
| `MANUAL_REVIEW` | Provider outcome cannot be proven, integrity dispute, exceptional account recovery | A named queue, owner, service target, and player-visible status exist |

Persisting a row is not completion. A public-ranked release MUST prove that every accepted workflow can progress after browser closure, application restart, database wake, and absence of further player requests.

### 49.2 Deadlines and escalation

Each workflow type defines:

- acceptance deadline and terminal target;
- maximum attempts and backoff;
- safe cancellation point;
- economic state while pending;
- escalation reason codes;
- operator ownership;
- player notice threshold;
- compensation, refund, amendment, or invalidation policy.

A missed internal deadline never causes a duplicate debit, duplicate provider submission, duplicate verdict, or hidden retry. It moves the workflow to a visible degraded or manual-review state.

### 49.3 Admission control

New ranked commands, submissions, exports, or deletion requests MUST be rejected before acceptance when the required executor, queue capacity, key material, trusted publication, or database writer cannot meet the declared liveness contract. Read-only review may remain available.

## 50. Private evaluator and verdict-envelope requirements

### 50.1 Separation visible in product behavior

The player-facing service may accept a submission and show `EVALUATION_PENDING`, but it cannot read or infer protected truth. Evaluation occurs in a private runtime with a separate identity, network path, secrets, and audit stream.

The public runtime sends only:

- immutable submission reference and digest;
- immutable round bindings;
- canonical evaluator request digest;
- player-safe command/economy summary required by the scoring contract.

The private evaluator returns a signed safe verdict envelope containing score, components, gates, penalties, one ending, coaching references, evaluator versions, and ranking eligibility. It never returns raw truth.

### 50.2 Failure behavior

If the evaluator is unavailable:

- the immutable submission remains committed;
- the round remains `EVALUATION_PENDING` or enters `RECOVERY_REQUIRED`;
- no score, ending, progression, or ranking entry is guessed;
- the player sees a status and incident reference when thresholds are exceeded;
- replay uses the same canonical request and evaluator bundle, never a mutable draft.

### 50.3 Reviewer separation

Public-ranked content requires distinct accountable identities for:

1. synthetic case/evidence author;
2. protected truth and evaluator reviewer;
3. release/publication approver.

A two-person exception must explain combined duties, compensating automated checks, independent sign-off, scope, and expiry.

## 51. Publication freshness, threshold approval, and evidence integrity

### 51.1 Freshness

A publication is eligible for new ranked rounds only when its signed metadata is current and mutually consistent. The trust model separates long-lived root trust, delegated targets, repository snapshot, and short-lived timestamp/freshness metadata. Clients and servers detect expired metadata, rollback, freeze, and mix-and-match conditions [S89].

A clock anomaly cannot silently extend trust. Trusted-time policy, allowed skew, emergency expiry extension, and offline recovery require explicit release evidence and two-person approval.

### 51.2 Canonical signed artifacts

Machine-readable manifests, evaluator requests, verdict envelopes, and release metadata:

- validate against a pinned JSON Schema 2020-12 dialect;
- reject duplicate keys, non-I-JSON values, and unbounded numbers;
- canonicalize using RFC 8785;
- state digest and signature algorithms plus key identifiers;
- include cross-language golden vectors;
- sign the canonical bytes, not parser-specific serialization [S92][S93].

Eligible immutable downloads MAY expose RFC 9530 digest fields as an additional transport-integrity signal; authorization, signatures, and content-addressed identity remain authoritative [S94].

### 51.3 Evidence chain of custody

Every runtime evidence item and rendition exposes a player-safe integrity/provenance projection and has a protected full record containing:

- object digest and media type;
- source/parent digests;
- transform/tool/version;
- authoring and review identities;
- creation/publication times;
- accessibility-equivalent linkage;
- correction/supersession lineage;
- signature/publication set.

A transcript, crop, redaction, thumbnail, rendered PDF page, normalized record, or relationship row is a separate rendition with explicit derivation. A correction never overwrites an old object.

## 52. Exact amounts, temporal order, and deterministic arithmetic

### 52.1 Money and assets

Authoritative money values use:

- integer minor units when the currency has a stable minor unit;
- otherwise bounded exact decimal strings/decimal database types with declared scale;
- explicit ISO currency or governed asset identifier;
- immutable FX rate source/snapshot/time where conversion is part of a case;
- explicit rounding mode and conversion sequence.

Binary floating point is prohibited for credits, debits, refunds, ledger balances, score components, thresholds, penalties, ranking keys, and case money-flow truth. Display localization never changes canonical values.

### 52.2 Event order

Ordering is determined by domain sequence, aggregate revision, ledger sequence, workflow sequence, and fencing epoch. UTC timestamps remain authoritative for expiry and historical time but ties and clock skew are resolved by stable sequences, not sub-millisecond assumptions.

Cases involving ambiguous chronology MUST distinguish:

- occurred time;
- recorded/received time;
- effective time;
- source timezone and offset;
- uncertainty interval;
- later correction.

## 53. Cryptographic erasure, restore safety, and privacy completion

In `PUBLIC_RANKED`, sensitive private text—such as notes, retrieval questions, case-file prose, support narratives, and generated export payloads—MUST be envelope-encrypted under narrowly scoped data-class/account keys. `DEVELOPMENT` and `DEMO` may use documented substitutes only with synthetic test identities and no production migration path. A deletion workflow:

1. verifies authorization and scope;
2. withdraws aliases and public projections;
3. destroys or disables wrapping material for in-scope keys;
4. writes durable deletion tombstones outside the deleted key scope;
5. removes searchable indexes and caches;
6. schedules physical expiry according to provider capability;
7. tests that a restored backup cannot decrypt or republish deleted content;
8. records safe completion evidence.

Cryptographic erasure does not excuse unnecessary retention, weak key isolation, shared keys across unrelated accounts, plaintext logs, or uncontrolled replicas [S90].

## 54. Fair-play integrity, review, and accessibility-safe enforcement

### 54.1 Signals

The service may record bounded server-side integrity events such as impossible command order, forged/stale client contracts, repeated conflicting idempotency reuse, automation beyond declared limits, impossible evidence references, or multi-account collusion indicators.

The service MUST NOT treat assistive technology, keyboard-only use, copy/paste for accessibility, screen-reader behavior, slow reading, network instability, locale, device class, or provider latency as proof of cheating.

### 54.2 Decisions

Disqualification requires:

- an integrity case with multiple corroborating signals or one cryptographically conclusive event;
- documented rule and evidence threshold;
- human review for ambiguous cases;
- reason code and safe explanation;
- retained evidence with expiry;
- appeal and amendment path;
- false-positive and slice monitoring.

Raw detection logic and secrets need not be disclosed, but the player receives enough information to understand the category and challenge an error.

## 55. Unicode, bidirectional text, and safe-content compilation

All authored and localized content passes a deterministic `CONTENT_COMPILER`.

The compiler MUST:

- normalize only according to field-specific rules; preserve original display text where required;
- reject or visibly escape disallowed control/invisible characters;
- isolate bidirectional text and prevent directionality spillover;
- detect confusable identifiers, deceptive whitespace, mixed-script login/public aliases, and filename spoofing;
- sanitize Markdown/HTML to an inert allowlist;
- prohibit scripts, event handlers, remote embeds, active SVG, macros, and unapproved external URLs;
- produce stable semantic HTML, plain-text transcript, and checksum-linked renditions;
- validate links, reserved domains, alt text, and spoiler equivalence;
- run localization pseudotests, long-string tests, and right-to-left layouts.

Security normalization must not silently change case evidence semantics. Player-visible raw/source text and normalized matching values remain distinct.

## 56. Updated open-data authoring portfolio

The following sources are added as governed authoring inputs, never guilt labels or direct playable actors:

| Source | Design value | Required caution |
|---|---|---|
| CFPB Consumer Complaint Database [S95] | Product, issue, company-response, channel, chronology, and consumer-harm schema | Complaints are allegations, narrative text may contain personal data, and current legal/availability status must be revalidated |
| EBA/ECB payment-fraud reporting [S96] | Payment instrument, channel, authentication, loss-allocation, geography, and trend schema | Aggregate/regulatory reporting is not individual adjudication |
| FinCEN SAR Stats [S97] | Aggregated suspicious-activity categories, filing-sector trends, and reporting taxonomy | SAR counts are reports, not proof; underlying SARs are not public authoring data |
| OFAC Sanctions List Service [S98] | Current list-delivery formats, identifiers, aliases, effective dates, deltas, and provenance | High-risk adverse personal data; research-only and strictly fictionalized |

The source registry stores exact landing page/API, snapshot, terms/license, data class, freshness, transform, checksums, approvals, permitted use, and quarantine/deletion plan. Narrative complaint text is excluded by default unless a separate privacy/legal/content approval exists.

## 57. Updated research implications

Version 6.0 adds the following tests:

- **Enterprise semantic grounding:** EntSQL shows that long-context business knowledge remains difficult; benchmark the intent plan and semantic layer separately from execution [S99].
- **Temporal distribution shift:** forward-in-time fraud evaluation must measure degradation and avoid relying on static graph advantage [S100].
- **Behavioral fidelity:** synthetic datasets can preserve tables while failing downstream fraud behavior; require sequence, business-rule, and detector-relative fidelity tests [S101].
- **Privacy auditing:** use challenge-style black/white-box membership-inference suites across single and relational tables, not one anonymity metric [S102].
- **Multi-turn retrieval:** conversation memory can introduce omissions, stale assumptions, and model regressions; every turn remains bound to visible evidence, canonical intent, and result firewall [S103].

Research results inform tests and risk decisions. They are not automatic production dependencies or claims that one model is suitable.

## 58. Version 5.0 inherited release-delta acceptance criteria

The inherited version 5.0 controls remain mandatory:

1. Every accepted workflow has a declared liveness class, deadline, executor, retry/escalation policy, and no-player-traffic test.
2. The public web runtime starts and operates without any protected-truth credential or importable truth repository.
3. Private evaluator dispatch, canonical request digest, signed safe verdict envelope, replay, and outage recovery pass end to end.
4. Author, truth/evaluator reviewer, and release approver separation is evidenced for every ranked package.
5. Publication metadata passes expiry, rollback, freeze, mix-and-match, revocation, threshold, trusted-time, and emergency-recovery tests.
6. Signed JSON and verdict artifacts pass JSON Schema 2020-12, RFC 8785, duplicate-key, number-bound, and cross-language golden-vector tests.
7. Every evidence object/rendition has digest, derivation, reviewer, accessibility linkage, and correction lineage.
8. Money, credits, scores, thresholds, and ranking keys contain no binary floats and pass rounding/FX/property tests.
9. Sequence and fencing tests prove timestamps alone cannot create double settlement, double progression, or ambiguous winner selection.
10. Deletion destroys the correct scoped keys, removes projections/indexes, and survives backup restore without decrypting or republishing deleted data.
11. Fair-play rules pass accessibility, locale, network, assistive-technology, false-positive, human-review, appeal, and retention tests.
12. The content compiler passes bidi, invisible-character, confusable, mixed-script, active-content, URI, Markdown, transcript, and RTL tests.
13. Genie Conversation API GA, Agent mode product GA, and Beta programmatic Agent mode/result APIs are represented as distinct capability snapshots; no Beta feature is the sole ranked path.
14. Lakebase scale-to-zero tests prove session loss cannot violate safety or workflow deadlines; admission closes when liveness cannot be met.
15. PostgreSQL, React, Vite, Python, FastAPI/Pydantic, WebAuthn, and provider versions are exact, patched, pinned, and revalidated at freeze.
16. CFPB, EBA/ECB, FinCEN, and OFAC additions have exact terms/data-class records and cannot introduce named real actors.
17. EntSQL, temporal-shift, behavioral-fidelity, privacy-audit, and multi-turn retrieval suites have signed thresholds and reproducible reports.
18. Cross-document schemas, vocabulary, states, role topology, and acceptance criteria are diff-tested and consistent.

## 59. Iteration 16 implementation decisions and post-v6 backlog

| Decision | Resolution gate | Default |
|---|---|---|
| Maintenance executor topology | Before `PUBLIC_RANKED` | Guaranteed nonpublic scheduled/always-on role from the same signed image |
| Private evaluator transport | Security/operations qualification | Durable database-backed queue or private authenticated invocation; no public endpoint |
| Key-management provider | Privacy/security release gate | Envelope encryption with scoped DEKs and auditable destroy/disable operation |
| Publication metadata framework | Release engineering gate | TUF-inspired role separation and expiry; use a mature implementation where compatible |
| Signature algorithm and key custody | Cryptography/release review | Modern approved algorithm, offline/restricted root, online short-lived metadata keys, rotation/revocation |
| Public passkeys | Security scale gate | Optional passkeys plus password/recovery compatibility; no single-device lock-in |
| Live Genie use | Provider/privacy/fairness gate | `MATERIALIZED_RETRIEVAL` default; GA Conversation API only after qualification |
| Agent mode APIs | Future capability review | Product mode is GA, but programmatic Agent mode APIs remain Beta; disabled for ranked play unless separately qualified with enforceable cost/tool/query bounds and never the sole solve route [S110][S111] |
| Complaint narrative use | Privacy/legal/content review | Excluded; use schema and aggregate categories only |
| Multi-region writes | Disaster-recovery review | Single authoritative writer with fencing; no active-active ranked writes |

## 60. Final product principles

Every feature must support at least one of these activities:

- observe evidence;
- form a hypothesis;
- retrieve relevant records;
- reveal a precomputed relationship;
- test an interpretation;
- build a defensible case;
- explain uncertainty.

A feature should be removed or redesigned if it automates culpability, rewards uncontrolled clicking, leaks hidden truth, bypasses the economy, conflates identity with association, conflates association with guilt, produces irreproducible ranked evidence, lacks a liveness path, cannot survive deletion/restore requirements, uses inexact authoritative arithmetic, or cannot be audited.

**Relationships help the player investigate. Evidence helps the player argue. Context, chronology, uncertainty, integrity, and protection of innocent actors make a conclusion defensible. Provider output is never a verdict.**



## 61. Runtime-role and player-visible liveness convergence

### 61.1 One image, multiple runtime roles

The public product may be built once, but it is not operated as one trust domain. The release manifest identifies the same immutable image digest for:

- `WEB`: public HTTPS ingress, authenticated reads/writes, quotes, command acceptance, and safe status;
- `MAINTENANCE`: nonpublic workflow execution, provider dispatch/poll/reconciliation, exports, deletion, retention, notices, integrity scans, and amendments;
- `EVALUATOR`: private truth access, deterministic evaluation, verdict signing, and evaluator-only audit;
- `MIGRATE`: release-only schema migration and verification.

Only `WEB` receives player traffic. Each role has a separate service identity, secret set, database role, network policy, startup checks, health state, and allowed commands. The same image digest is a reproducibility property, not a privilege-sharing shortcut.

### 61.2 Admission and status

`PUBLIC_RANKED` admission checks at least:

- maintenance heartbeat freshness and fencing epoch;
- oldest due workflow age and backlog capacity;
- evaluator availability and verdict-signing readiness;
- publication freshness and trusted-time state;
- database writer/readiness and migration compatibility;
- provider capability and cost-budget availability for the requested action;
- key-management ability to encrypt newly accepted private text.

When admission is closed, the system rejects the operation before accepting money, commands, submissions, exports, or deletion work. Safe read-only review MAY remain available. The player sees a stable reason code, safe status, and incident reference rather than a false “pending” state.

## 62. Provider feature profile, cost envelope, and conversation safety

### 62.1 Baseline live-provider profile

The baseline `LIVE_GENIE` profile permits only:

- one player text question after deterministic intent planning;
- one approved Genie Agent/Space bound to allowlisted player-safe views;
- the GA Conversation API operations required to create/send/read a conversation result;
- bounded tabular result rows normalized through the FGA result firewall;
- provider correlation/status metadata necessary for reconciliation and deletion.

The baseline profile denies file upload, arbitrary Unity Catalog volume documents, conversation sharing, external embedding, MCP access, scheduled provider tasks, thinking traces, generated SQL exposure, provider visualizations, downloadable full results, and provider-side active links/content. A provider UI capability does not become an FGA capability automatically [S110][S111].

### 62.2 Agent mode

Genie Agent mode is GA as a product feature, but its programmatic APIs remain Beta and it may execute multiple iterative SQL queries [S110][S111]. It is therefore disabled for public-ranked play unless all of the following are true:

1. the exact APIs and region are approved;
2. maximum query/tool count is enforceable before and during execution;
3. a provider cost/DBU ceiling and workspace budget alert are active;
4. wall-time, warehouse-time, result-row, result-byte, and conversation-history bounds are enforceable;
5. cancellation and unknown-outcome reconciliation are proven;
6. intermediate SQL, traces, files, visualizations, and hidden provider context cannot cross the result firewall;
7. every benchmark intent has deterministic expected records and a signed cost envelope;
8. the capability receives a separate ranking segment unless equivalence is proven.

A quote cannot promise a fixed investigation-credit price while allowing unbounded provider work. Provider billing introduced on 8 July 2026 is an operational input, not a player-visible surprise [S110].

### 62.3 Provider conversation lifecycle

Provider conversations are round-scoped, private, nonshareable, and minimized. The system records provider retention/deletion capability and performs deletion or expiry according to the approved processor record. Provider history is never the source of authoritative game state; the persisted normalized command result is.

## 63. Evaluator noninterference, declassification, and oracle resistance

### 63.1 Safe-output boundary

The evaluator may use protected truth internally but returns only fields approved by the safe verdict schema and declassification manifest. Safe outputs use bounded enumerations, capped component scores, fixed gate/penalty identifiers, and reviewed coaching templates. Arbitrary truth-derived text is prohibited.

### 63.2 Oracle-resistance tests

Release tests MUST attempt to infer protected truth through:

- semantically equivalent and near-boundary submissions;
- repeated Practice/Academy interactions;
- score-component deltas and ending thresholds;
- amendment, appeal, moderation, support, and incident messages;
- locale, accessibility, and ordering variants;
- malformed or partial submissions;
- timing, error-class, payload-size, and status differences.

The tests verify that outputs reveal no more than the approved player-safe contract. Ranked one-submission rules do not replace these tests because retries, test modes, defects, and support paths can still create an oracle.

### 63.3 Declassification manifest

Each case/version defines a signed `DECLASSIFICATION_MANIFEST` for:

- verdict component explanations;
- ending-specific coaching;
- closure comic and transcript;
- educational debrief;
- post-case review and Academy hints;
- support and appeal reason codes.

A debrief fact is released because it was explicitly reviewed, not because the evaluator happened to know it. A corrected declassification creates a new package and lineage; it does not mutate historical artifacts.

## 64. Verifier policy and release transparency

A signature is accepted only under a signed verifier policy. The policy defines permitted signer identity/issuer, source repository and protected branch/tag, build workflow, artifact type, expected digest subject, SLSA/in-toto predicate requirements, transparency inclusion, signed timestamp, trust-root version, freshness, and revocation behavior [S113]–[S115].

For public releases, the project SHOULD use an offline-verifiable bundle format containing signature, certificate/key identity, timestamp, and transparency proof. A transparency-log URL or shard MUST NOT be hard-coded; rotated signing/trust configuration is obtained from trusted metadata [S113][S114].

Verification distinguishes:

- **authenticity:** the artifact was signed by an allowed identity;
- **provenance:** it came from the allowed source and build workflow;
- **integrity:** the digest matches the exact artifact;
- **freshness:** metadata and trust roots are current;
- **transparency:** inclusion evidence is valid where required;
- **authorization:** the artifact type/version is permitted for this environment.

## 65. Query identifiability and safe-interface completeness

Every required natural-language retrieval intent maps to a structured query contract and a `QUERY_IDENTIFIABILITY_RECORD`. The record demonstrates, through formal schema constraints, exhaustive fixture worlds, or equivalent tests, that the answer is determined by the provider-safe interface. More rows or a stronger model cannot repair an interface that omits decisive attributes or relationships [S123].

A required clean-solve query fails publication when:

- two legal protected worlds produce the same provider-safe view but different expected answers;
- the query requires a hidden field, unexposed join, future event, or ambiguous normalization;
- the same safe plan can validly map to materially different record sets;
- the result depends on provider memory or unstated semantic context.

The remedy is to change the safe interface, make the question clarifying/abstaining, or remove it from the required solve route.

## 66. Relational and temporal synthetic-data quality extension

The `RELATIONAL_FIDELITY_PROFILE` adds:

- schema graph and table-role diversity;
- primary/foreign-key connectivity, cardinality, optionality, and orphan policy;
- entity-history length and cross-table trajectory consistency;
- aligned-time cross-sectional structure;
- within-entity dynamics and temporal autocorrelation;
- time-varying relationship structure;
- valid timestamp ordering, duplicate-time policy, and impossible-transition detection;
- safe-interface identifiability and downstream case solvability.

PluRel motivates explicit schema/connectivity generation rather than isolated table synthesis [S120]. Current temporal-fidelity research shows that correct marginals and foreign keys can coexist with backwards timestamps or impossible trajectories, so trajectory-aware tests are mandatory [S122].

## 67. Additional governed open-data and typology inputs

| Source | Authoring value | Mandatory constraint |
|---|---|---|
| FATF, *Cyber-Enabled Fraud — Digitalisation and ML/TF/PF Risks* (24 February 2026) [S116] | Scam-centre, deepfake, payment-transparency, asset-recovery, virtual-asset, beneficial-ownership, and cross-border coordination typologies | Typology/debrief input only; no operational evasion detail and no named actor becomes playable |
| UK Payment Systems Regulator APP-scam performance and reimbursement data [S117] | Sending/receiving PSP, prevention, reimbursement, victim outcome, reporting-period, and policy-transition schemas | Firm-level figures require context and dates; performance data is not a guilt label; use synthetic comparators |
| FCA Financial Services Register [S118] | Authorisation status, firm/person role, appointed representative, historical status, clone/unauthorised warning patterns | Public-person/adverse data is high risk; API is Beta and extract access/terms differ; no direct playable actor |
| FCA National Storage Mechanism [S119] | Regulated-announcement chronology, issuer disclosures, iXBRL/JSON/CSV rendition structure, correction/supersession | Disclosures are not fraud findings; preserve filing/effective time and transform only to fiction |

## 68. New research implications and benchmark changes

- **AI-native SQL remains error-prone:** Spider 2.0-AIFunc reports leading-model execution accuracy around 67–70%, with predicate, schema-grounding, and AI-function parameter errors. FGA continues to prohibit AI-native SQL functions and separately scores intent, schema grounding, and records [S121].
- **Deterministic agent evaluation is practical:** Telco-GAIA uses a frozen sandbox and normalized exact scoring without LLM-as-judge; FGA adopts this pattern for provider benchmarks and multilingual fixtures [S124].
- **Relational interfaces can be structurally ambiguous:** identifiability tests are required before a provider-safe view is declared sufficient [S123].
- **Synthetic sequences need trajectory tests:** aligned-time, within-entity, and time-varying relationship fidelity supplement static distribution checks [S122].
- **Relational generation needs schema/connectivity diversity:** synthetic case tooling records schema graph and key-topology coverage, not only row counts [S120].

## 69. Version 6.0 release-delta acceptance criteria

Version 6.0 is not accepted until:

1. All single-container and optional-scheduler contradictions are removed from text, diagrams, schemas, and deployment tests.
2. `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE` role identities, secrets, network policies, entrypoints, and health checks are independently verified.
3. Zero-player-traffic tests prove command reconciliation, evaluation, export, deletion, retention, notices, and amendments reach terminal/manual-review outcomes.
4. Admission closes before acceptance when executor heartbeat, evaluator, key management, publication freshness, queue capacity, or provider budget is unhealthy.
5. Genie capability snapshots distinguish Conversation API GA, Agent mode GA, and Beta Agent mode/result APIs.
6. Baseline player sessions cannot upload/share/attach files, expose traces/SQL/visualizations, schedule tasks, or retain unbounded provider history.
7. Any enabled Agent mode command has enforceable query/DBU/time/tool/row/byte/cancellation bounds and a separate/equivalent ranking decision.
8. Workspace/provider cost alarms and hard admission ceilings are tested after the July 2026 pricing change.
9. Evaluator noninterference and adaptive oracle tests pass across verdict, debrief, appeal, support, amendment, error, timing, and locale surfaces.
10. Every case/version has a signed declassification manifest and spoiler-equivalence review.
11. Artifact verification rejects correct signatures from wrong identities, issuers, repositories, refs, workflows, artifact types, digests, or stale/revoked trust roots.
12. Transparency/offline bundle verification and trust-material rotation are rehearsed where enabled.
13. JVM publication jobs use pgJDBC 42.7.12+ and pass channel-binding/TLS tests.
14. Designated private text encryption is mandatory in `PUBLIC_RANKED`; deletion and restored-backup nondecryptability pass.
15. Every required retrieval benchmark has an identifiability record and no hidden/future/interface-ambiguous dependency.
16. Relational schema/key/trajectory/time-varying fidelity gates pass with reproducible reports.
17. New FATF, PSR, FCA Register, and FCA NSM inputs have exact terms, dates, data-class, fictionalization, and approval records.
18. Functional, technical, OpenAPI, JSON Schema, diagrams, state machines, and acceptance criteria pass semantic-diff consistency checks.

## 70. Version 6.0 retained and extended invariants

1. One image never means one runtime trust identity.
2. Public ingress never advances workflows as the only liveness mechanism.
3. A provider product GA label never overrides exact API maturity.
4. A quote never authorizes unbounded provider work or cost.
5. Provider file upload, sharing, traces, and active result content are denied by default.
6. The evaluator cannot reveal protected truth outside a signed declassification manifest.
7. Appeals and support cannot become answer-key side channels.
8. A signature without verifier-policy authorization is insufficient.
9. Transparency endpoints are rotated through trusted metadata, not hard-coded.
10. Required retrieval questions are identifiable from the safe interface.
11. Static fidelity cannot substitute for relational and temporal trajectory fidelity.
12. Designated private text remains unreadable after approved deletion and backup restore.


## 71. Version 7.0 normative-pair and consistency contract

### 71.1 Authority

The authoritative prose set is:

1. **Fraud Graph Arena Complete Functional Specification v7.0** for product behavior.
2. **Fraud Graph Arena Complete Technical Architecture and Design Specification v7.0** for implementation constraints.
3. Signed machine-readable contracts, only where consistent with 1 and 2.

The two documents share one `NORMATIVE_PAIR_ID`. A release cannot combine one v7 document with a v6 counterpart. Historical change-register sections remain evidence of evolution but do not override later v7 requirements.

### 71.2 Machine-checkable consistency

The release produces a generated conformance export containing requirement ID, source document/section, normative verb, subject, object, state/value vocabulary, related API/schema/table/test, and status. CI fails on:

- duplicate or missing requirement/invariant IDs;
- a referenced state or enum absent from the current Core Contract;
- stale version authority or source-date statements;
- contradictory `MUST`/`MUST NOT` predicates;
- diagrams that contain obsolete runtime roles or forbidden trust paths;
- API/schema fields that expose protected truth or omit immutable bindings;
- acceptance criteria without at least one test/evidence owner.

## 72. Provider capacity, price, and post-promotion qualification

### 72.1 Volatile capability facts

Current provider documentation limits Genie Agents to a finite table/view and instruction set; as of this audit, the documented table/view ceiling is 30 per agent [S125]. This value is not a product constant. Every `LIVE_GENIE` publication records the exact limits observed, the verification time, workspace class, region, API operation, and failure behavior.

A case/profile cannot be published when its provider-safe semantic interface exceeds the verified limit. The preferred design is a compact per-case or per-case-family interface with explicit views, not one cross-anthology agent with broad schema access.

### 72.2 Pricing-effective-window rule

Current Databricks release notes state that Genie One and Genie Agents usage is free through **31 July 2026** [S126]. Therefore:

- cost tests conducted only during that promotional window are provisional;
- before paid `PUBLIC_RANKED` use, the project reruns a representative benchmark after the applicable billing date or obtains a contractually reliable price schedule;
- every quote cost model records provider currency, billable unit, unit price, taxes/fees treatment where relevant, effective time, budget source, and conversion policy;
- a price or billing-model change creates a new capability snapshot and normally a new ranking segment;
- admission closes before accepting a paid provider action when its worst-case provider envelope cannot be funded.

## 73. AI transparency and public-media provenance

### 73.1 Player interaction disclosure

For an EU public release on or after **2 August 2026**, the project completes and signs the Article 50 applicability record before deployment [S88][S104]. Whenever a player interacts with a live AI-assisted retrieval system, the UI identifies that fact plainly before the question is sent and before a paid quote is accepted. The disclosure states the external-provider status, categories of data sent, limits, fallibility, retention posture, and the fact that the output is not a fraud or guilt decision.

### 73.2 Generated or AI-assisted media

Each public image, comic, audio item, text asset, or promotional rendition has an `ASSET_CREATION_RECORD` covering:

- original source/ingredient digests and licenses;
- human authors/editors and approval roles;
- tools/models and versions used where known and lawfully retainable;
- material generation/edit steps;
- accessibility renditions and spoiler review;
- final public digest and signature.

Where law/applicability and format support make it appropriate, the release also carries machine-readable Content Credentials using C2PA 2.4, including the AI disclosure assertion [S129]. The player-facing credits/about surface provides an understandable disclosure without forcing users to inspect metadata.

C2PA is a provenance signal, not proof that content is true, harmless, lawfully licensed, or entirely human/AI generated. Metadata may be removed, and valid signals may conflict; FGA therefore relies on its signed internal asset record and cross-layer validation [S130][S131].

## 74. Privacy threat modelling and data-protection assurance

Every `PUBLIC_RANKED` release includes:

- a current data-flow inventory from browser through web, database, maintenance, evaluator, provider, telemetry, export, support, backup, and deletion systems;
- a privacy threat model covering linkability, detectability, identification, disclosure, inference, manipulation, exclusion, and inability to exercise rights;
- a NIST Privacy Framework-aligned treatment map [S134];
- a jurisdictional DPIA/impact-assessment trigger decision and, when triggered, the completed assessment;
- data-minimization and purpose-limitation tests for every outbound provider/telemetry/support payload;
- proof that designated private text cryptographic erasure also removes searchable indexes, replicas, caches, exports, and reprocessing queues;
- a player-safe explanation of residual retention, legal holds, and backup expiry.

Privacy defects affecting an individual are treated as product correctness defects, not merely security incidents.

## 75. Ranked feature policy, staged rollout, and emergency controls

### 75.1 Signed ranked feature policy

A ranked-affecting feature flag is part of a signed `RANKED_FEATURE_POLICY`. Its digest is bound to each newly created ranked round and included in ranking compatibility. It controls provider mode, API operation, data categories, result caps, cost envelope, fallback, asset package, and optional experimental functionality.

An operator dashboard cannot silently change those semantics. Existing rounds retain their bound policy. A changed policy creates a new segment unless equivalence is proven before activation.

### 75.2 Rollout stages

New provider, evaluator, publication, or frontend security behavior advances through:

1. local/contract tests;
2. deterministic shadow or replay tests with no player effect;
3. protected internal/demo canary;
4. small unranked cohort;
5. new ranked segment with admission ceilings;
6. general availability after evidence review.

A kill switch may stop new actions/rounds, pause evaluation, quarantine a publication, or disable a provider. It MUST NOT broaden access, change a settled charge, replace evidence, alter score, or move an existing round to another provider mode.

## 76. Dynamic accessibility and conformance evidence

Static page scans do not prove accessibility for a stateful investigation application. Release-critical journeys produce `DYNAMIC_ACCESSIBILITY_TRACE` evidence for authentication, career creation, case selection, quote confirmation, provider pending/recovery, graph/list selection, document inspection, case-file errors, submission confirmation, verdict, export, deletion, and session revocation.

Each trace records focus transitions, keyboard/pointer/touch actions, accessibility-tree snapshots, live-region output, modal containment, error association, delayed updates, route changes, and recovery. Flow-aware research supports this evidence approach, but its current accuracy limitations mean it cannot replace expert/manual review [S132].

The release publishes an accessibility statement and a versioned Accessibility Conformance Report or equivalent internal/external evidence package. Draft EN 301 549 V4.1.0 status is tracked, but the product does not claim conformance to an unapproved or nonapplicable version.

## 77. Provider benchmark variance, drift, and schema reasoning

Every provider benchmark suite specifies:

- immutable dataset, schema, semantic instructions, provider capability digest, and expected record sets;
- exact/structured scorer and abstention/clarification classification;
- minimum repeated-run count and separated execution windows;
- complete inclusion of timeouts, malformed outputs, policy rejections, and cost outliers;
- latency, query/tool count, rows/bytes, provider cost, and result-set variance;
- confidence intervals or clearly stated descriptive uncertainty where sample size is too small;
- drift thresholds that block new rounds or force a new segment;
- multilingual, Unicode, adversarial, hidden-truth, and no-result cases.

DW-Bench reinforces that schema graph and lineage reasoning is a separate capability from producing syntactically valid SQL [S133]. FGA therefore scores intent selection, table/view selection, join/lineage path, predicate/time semantics, and final safe record set separately.

## 78. Dependency identity and registry integrity

For every Python, npm, JVM, container, action, and release tool dependency, the build records a `DEPENDENCY_IDENTITY`: approved registry, namespace, package, version, integrity hash, provenance/signature where available, and lockfile location. Public release builds:

- reject mutable tags and unapproved alternate registries;
- verify lockfiles are in sync with manifests;
- test namespace/package-confusion and typosquatting scenarios for critical dependencies;
- isolate package-manager credentials and use least-privilege read access;
- record the exact build action/container digest, not only its human-readable tag;
- fail closed when a package identity cannot be reconciled with the SBOM/provenance policy.

## 79. Additional governed fraud and payment inputs

| Source | Authoring value | Mandatory constraint |
|---|---|---|
| FATF 2026 targeted report on stablecoins and unhosted wallets [S135] | Stablecoin issuer, chain, wallet, P2P, cross-chain, intermediary, and control-point schemas for V2/V3 research | Defensive typology only; no evasion optimisation, operational laundering recipe, named actor, or live wallet |
| EBA/ECB payment-fraud analysis [S136] | Strong-customer-authentication, payment instrument, payer/payee initiation, geography, loss allocation, and adaptation patterns | Aggregate/regulatory context only; authentication failure or cross-border status is never a guilt label |

## 80. Inherited version 7.0 release-delta acceptance criteria

Version 7.0 is accepted only when:

1. The functional and technical files share one `NORMATIVE_PAIR_ID` and all authority references point to version 7.0.
2. Generated consistency checks find no duplicate invariant IDs, stale state names, contradictory predicates, or obsolete topology diagrams.
3. The current Genie table/view/instruction/rate limits fit every live provider package and are stored with an effective window.
4. Provider cost qualification is rerun under the applicable paid billing regime; promotional/free-window results are not the sole cost evidence.
5. EU AI interaction disclosure and media-marking applicability are approved before any release subject to 2 August 2026 obligations.
6. Every public media asset has a signed creation record; any C2PA credential is verified but not treated as sole authority.
7. CSP and DOM sink tests pass; the Trusted Types compatibility/enforcement decision is documented with zero unreviewed violations.
8. A current privacy threat model, data-flow inventory, processor map, and DPIA/applicability decision are signed.
9. Dynamic accessibility traces and expert review pass all release-critical journeys.
10. Provider benchmark reports include every run, exact outcomes, variance, cost, drift, and schema-grounding classification.
11. Ranked feature flags are signed, policy-bound, immutable for existing rounds, and kill-switch tested.
12. Critical dependency identities are registry/hash/provenance pinned and dependency-confusion tests pass.
13. FATF stablecoin/unhosted-wallet and EBA/ECB source cards include exact terms, snapshot, data class, fictionalization, and dual-use approval.
14. Version 7.0 documents, schemas, tests, deployment manifests, source bibliography, and release evidence have zero unresolved semantic-diff findings.

## 81. Inherited version 7.0 retained and extended invariants

1. A provider quota or price is never assumed timeless.
2. A free/promotional test window never proves paid production affordability.
3. AI interaction is disclosed whenever a live AI system participates.
4. AI provenance metadata never substitutes for source, license, safety, or factual review.
5. An existing ranked round never changes feature-policy digest.
6. An emergency switch can only narrow, pause, quarantine, or disable behavior.
7. A browser string cannot reach an active DOM/script sink outside an approved reviewed policy.
8. Privacy harms are release-blocking even when no credential or hidden truth leaked.
9. Accessibility conformance is not inferred from a static scanner or autonomous agent alone.
10. Provider qualification includes failed runs and cost outliers.
11. A package name without approved registry/hash/provenance identity is not a dependency.
12. At the version 7.0 release, every then-current normative requirement belonged to one consistent version 7.0 pair.


## 82. Operational liveness and hosting guarantees

### 82.1 Player-visible guarantee

Once a paid ranked action or submission is accepted, a private always-on maintenance path progresses or safely reconciles it. Player traffic, an open browser tab, repeated polling, or a periodic cron invocation is not required for correctness. Railway cron jobs may run coarse sweeps and housekeeping, but the interactive command deadline belongs to the continuous maintenance executor [S137]–[S139].

### 82.2 Admission behavior

Before charging, the service checks executor heartbeat, queue age, provider and conversation headroom, budget, database/key readiness, evaluator backlog, and expected deadline. When unhealthy, the quote/action is unavailable before debit with a clear safe reason. Existing accepted work remains visible and recoverable.

### 82.3 Fair completion

Work scheduling prevents one player, case, or failing provider request from starving others. Poison or indeterminate work enters an explicit reconciliation state. A maintenance deployment or restart cannot duplicate provider submission, debit, refund, evidence reveal, submission, evaluation, or progression.

## 83. Provider conversation privacy, capacity, and single-turn semantics

### 83.1 Fresh provider context

Each accepted ranked AI-assisted retrieval command uses a fresh provider conversation. The player may ask another question, but it becomes a new quoted command and new conversation. The baseline does not provide provider-memory follow-ups. Revealed FGA evidence remains in the game state; it is not silently copied into provider history [S05][S147].

### 83.2 Capacity and cleanup

The service records conversation/message identifiers, terminal state, retention deadline, deletion request/receipt, and capacity headroom. New live commands close before the current provider ceiling can be reached, including cleanup lag and incident reserve [S125]. Failure to delete an old provider conversation does not erase the FGA result, but it affects privacy/capacity admission and triggers reconciliation.

### 83.3 Excluded outputs

Generated SQL, reasoning traces, suggested follow-ups, visualizations, comments, sharing links, and provider-wide history are not player evidence. They are not shown in the UI or ordinary diagnostics and cannot affect score, refund, or support outcomes.

## 84. Real provider cost and investigation-credit boundary

Investigation credits are fictional game units. They are never displayed as euros, dollars, DBUs, tokens, or provider charges and cannot be purchased, converted, invoiced, or refunded as money under the baseline product.

Real provider usage and cost are private operational data governed by product/SKU, currency, unit, contract, promotion, and effective window. Genie Code pricing facts do not qualify Genie One or Genie Agents, and a free/promotional period does not establish paid affordability [S126]. Budget exhaustion disables new live-provider acceptance without taking credits or changing existing round semantics.

## 85. Account recovery and privileged-access safeguards

### 85.1 Player accounts

The product follows the final NIST SP 800-63-4 suite as a security reference without claiming formal government identity assurance for player accounts [S140]. A username, password, recovery code, or passkey proves control of an authenticator/account path, not a person's legal identity.

### 85.2 Exceptional reset

An operator-assisted reset places the account in `RECOVERY_LIMITED`. Existing sessions and affected authenticators are revoked or rotated. High-risk actions—export, deletion, public alias/leaderboard changes, new passkeys, recovery-code regeneration, and broad session expansion—remain blocked until step-up and a documented cooldown/review complete. The player receives an in-product notice and dispute route.

### 85.3 Privileged users

Operators, evaluator maintainers, database administrators, and release signers use separate privileged accounts with phishing-resistant MFA and recent step-up. A normal player session can never become an operator session.

## 86. Browser and client trust profile

Every release carries a signed browser security-header profile. It covers HTTPS/HSTS, CSP, Trusted Types where supported, anti-framing, referrer and permissions policy, MIME protection, Fetch Metadata, CORS, COOP/CORP, an explicit COEP decision, sandboxed evidence viewers, safe caching, and privacy-minimized violation reporting [S127][S128][S142][S143].

Cross-window messages verify exact origin, source, schema, and nonce. Unsupported browsers receive a safe compatibility state; the application does not disable security controls silently. Cross-origin isolation is enabled only after audio, PDF, font, browser, and assistive-technology testing.

## 87. Evidence integrity and reproducible case packages

Every immutable record, relationship, document, asset, manifest, submission, verdict, and policy has a canonical content digest. JSON uses RFC 8785-compatible canonicalization plus explicit FGA rules for time, Unicode, decimals, absent/null values, and ordering [S152].

A case snapshot publishes an `EVIDENCE_MERKLE_ROOT`; a submission binds the snapshot root and exact revealed-evidence subset root; the verdict binds the submission and evaluator roots. Historical review can prove which immutable package produced the result without exposing protected truth.

Case publication records pinned toolchains, source commits/digests, seeds, timezone/locale, deterministic ordering, build environment, output roots, and declared nondeterminism. Unexplained logical-root drift blocks publication.

## 88. AI Act Article 50 obligation-by-obligation applicability

The 20 July 2026 Commission guidance and official quick facts are applied per obligation [S144]. The signed release record separately determines:

- whether FGA is provider, deployer, or both for each AI feature;
- whether a player is directly interacting with an AI system and what notice is required;
- whether generated/modified content requires machine-readable marking and/or human-visible labelling;
- system placement date and whether a stated transitional/grace rule applies;
- content type, deepfake/public-interest status, and degree of human editorial control;
- jurisdiction, language, accessibility, persistence, and evidence of notice/marking.

The official material notes a grace period until December 2026 for the marking obligation for certain generative AI systems placed on the market before 2 August 2026. This does not waive applicable interaction disclosure, other obligations, or FGA's own honest provenance policy. Legal approval—not product convenience—decides applicability.

## 89. LLM security and provider-result handling

The live retrieval release gate maps OWASP LLMSVS 2.0 alongside ASVS, AISVS, NIST AI RMF, and the GenAI Profile [S141]. It tests prompt injection from player questions and synthetic evidence, unauthorized tool/data access, cross-case retrieval, hidden-truth requests, output injection, excessive query/tool use, denial of service, privacy, provider changes, and incident recovery.

The provider has read-only access to allowlisted safe views and no arbitrary file, volume, network tool, protected schema, DDL/DML, or active-content path. A model statement never overrides the accepted intent plan, result firewall, quote cap, ownership, visibility, or publication policy.

## 90. Chaos qualification and player-safe incident behavior

Before public-ranked release, executable game days cover maintenance loss, provider timeout and duplicate delivery, conversation-capacity exhaustion, cost-budget exhaustion, database deadlock/failover/restore, evaluator or key outage, partial deployment, stale client/service worker, publication revocation, private-network failure, and deletion cleanup failure.

A test passes only when no duplicate economic/progression result occurs, no protected/private data leaks, ranked semantics do not drift, unsafe admission closes before charge, accessible status/recovery remains usable, and historical state remains explainable. The signed `CHAOS_QUALIFICATION_REPORT` is release evidence, not an optional operations note.

## 91. New governed sources and research implications

### 91.1 Defensive sources

- **ESMA MiCA register:** may inform fictional crypto-provider, authorisation, noncompliance, white-paper, issuer, and effective-date schemas. A registered or noncompliant status is not a guilt verdict, and named entities never become playable suspects [S145].
- **FinCEN SAR Stats and Financial Trend Analyses:** may inform aggregate reporting categories, industries, chronology, and defensive debrief vocabulary. A SAR filing is not adjudicated fraud, and no confidential SAR content is used [S146].

### 91.2 Research changes

EnterpriseMem-Bench supports disabling provider cross-command memory for ranked fairness [S103]. EntSQL adds long-context enterprise-knowledge grounding cases [S147]. VLD-Bench strengthens value-linking tests across lexical and semantic mismatches [S148]. FlexSQL supports separate limits for schema/value exploration, query count, time, and cost even when exploration improves answer quality [S149]. The MIDST challenge strengthens black-box/white-box membership-inference testing for tabular and relational synthetic data [S102]. The 2026 WebAIM Million report supports broad automated scanning but does not replace dynamic-flow and expert review [S150].

## 92. Inherited version 8.0 release-delta acceptance criteria

Version 8.0 is accepted only when:

1. An always-on private maintenance executor—not cron, browser polling, or web traffic alone—progresses accepted ranked workflows.
2. Executor heartbeat, backlog, fairness, graceful shutdown, private networking, and admission fail-closed behavior pass.
3. Every ranked provider command uses a fresh conversation and no provider-memory follow-up path exists in the baseline.
4. Provider conversation capacity, deletion, remote inventory, retention, and headroom are reconciled.
5. Product-specific pricing/effective windows and the real provider-cost ledger pass paid-window/budget qualification.
6. Investigation credits remain entirely separate from money/provider usage.
7. Generated SQL, reasoning traces, comments, visualizations, sharing, and provider history cannot reach players or ordinary logs.
8. Operator/release identities use phishing-resistant MFA and exceptional reset enters `RECOVERY_LIMITED`.
9. The OWASP LLMSVS 2.0 mapping and indirect-prompt-injection suite pass for live retrieval.
10. The signed security-header/cross-origin profile passes supported browser and assistive-technology tests.
11. Concurrency/failover tests prove no duplicate debit, refund, reveal, submission, evaluation, unlock, or leaderboard result.
12. Every snapshot, submission, and verdict has canonical digest and Merkle lineage.
13. Publication reproducibility has no unexplained logical-root drift.
14. The Article 50 record separately resolves interaction disclosure, marking/labelling, provider/deployer role, placement date, editorial control, exception, and grace.
15. Required executable chaos scenarios pass with player-safe status and historical integrity.
16. ESMA MiCA and FinCEN SAR source cards, plus the four new research cards, pass source-use and dual-use review.
17. The generated contract graph marks inherited delta sections informative and reports zero current v8 contradictions.

## 93. Inherited version 8.0 retained and extended invariants

1. Accepted ranked work never depends on an open browser or periodic cron alone.
2. One ranked retrieval command never inherits another command's provider conversation context.
3. Provider capacity cleanup failure closes admission before exceeding the signed ceiling.
4. Investigation credits are not money and never settle provider costs.
5. Provider reasoning and generated SQL are neither evidence nor authority.
6. Recovery of account control does not prove civil identity or instantly restore every privilege.
7. Privileged production actions never originate from a player session.
8. Browser trust policy cannot be weakened by an unsigned route/config change.
9. A retry/deadlock/failover cannot create a second debit, refund, submission, verdict, or unlock.
10. Evidence identity is canonical content/provenance digest, not filename, label, or database row ID alone.
11. Article 50 obligations and transitions are evaluated separately and documented.
12. Synthetic data remains subject to empirical privacy attack testing.
13. Chaos evidence can justify safe operation only when constitutional invariants remain intact.
14. Every current normative requirement belongs to the version 9.0 pair and machine-readable contract graph.


## 94. Ranked retrieval evidence parity

### 94.1 Authoritative ranked result

The natural-language action remains one of the four investigation families. In a `PUBLIC_RANKED` round, its authoritative effect is:

1. normalize the player's question into a versioned canonical safe plan;
2. show and confirm that plan and the investigation-credit quote;
3. optionally use the bound provider to assist interpretation or validate the plan;
4. execute the confirmed plan through the deterministic player-safe resolver;
5. compare the result against the segment's parity contract;
6. grant the stable ordered records or stable valid no-result.

The live provider cannot add, remove, reorder, or substitute ranked evidence. A direct provider-selected result may exist only as a labelled unranked experiment, cannot share ranked leaderboards, and cannot advance a ranked career.

### 94.2 Parity manifest

Every ranked case/profile/semantic configuration publishes a `RANKED_RETRIEVAL_PARITY_MANIFEST` containing:

- supported canonical intent classes;
- allowed fields/operators/value domains;
- canonical filter/date/order semantics;
- result and byte caps;
- stable null/missingness behavior;
- deterministic ordering and safe-ID tie-breaker;
- expected result-set digest or deterministic rule for its derivation;
- valid no-result fixtures;
- unsupported/ambiguous intent behavior;
- publication, rules, economy, and ranking-segment bindings.

A change to any item is a material evidence change and normally creates a new ranking segment.

### 94.3 Fairness guarantee

For the same player-visible prerequisite state, canonical plan, immutable round bindings, and accepted quote, every player in one ranking segment receives the same records, fields, order, and valid no-result behavior. Provider latency, model sampling, hidden conversation state, workspace load, or provider feature rollout cannot alter that evidence.

## 95. Pre-reveal noninterference and clarification

### 95.1 Quote and status noninterference

Before the final reveal commits, observable behavior MUST NOT disclose hidden or unrevealed case facts. In particular:

- quote cost is determined by action family, visible selection/plan class, and signed economy policy—not hidden match count;
- acknowledgement and public status use a fixed safe state vocabulary;
- queue position is not exposed as an exact cross-player value;
- retry and cancellation eligibility depend on command state, not result cardinality;
- error detail does not distinguish “no hidden match exists” from provider/internal failure before settlement;
- latency is monitored operationally but player-visible timing classes are coarse and cannot intentionally encode result size or truth;
- response padding MAY be used when necessary, but cannot create accessibility or performance harm.

The valid terminal outcomes remain charged result, charged valid no-result, refundable failure, cancelled/refunded where supported, or recovery-required. A valid no-result becomes visible only through the same charged/revealed settlement boundary as a nonempty result.

### 95.2 Clarification policy

Clarification is free and uses deterministic ambiguity classes. The system:

- asks only questions answerable from the player's intended scope, not hidden data;
- offers concise, mutually distinguishable options plus an accessible free-text correction where appropriate;
- limits the clarification chain according to signed policy;
- preserves the player's original question and selected interpretation privately;
- abstains without debit when ambiguity remains;
- does not reward or penalize language fluency, verbosity, assistive technology, or slower interaction;
- measures clarification regret, repeated-loop rate, abandonment, and inconsistent-option rate across locales and accessibility modes [S165].

## 96. Policy, consent, notice, and privacy-signal lifecycle

### 96.1 Policy bundles and change classes

Terms, privacy notice, processor/subprocessor disclosure, optional telemetry, AI interaction disclosure, content suitability, leaderboard publication, and jurisdiction-specific notices are versioned as immutable `POLICY_BUNDLE`s. Each bundle has effective time, applicable jurisdiction/profile/features, human-readable copy, accessible format, locale versions, source/legal evidence, and digest.

Changes are classified:

- `EDITORIAL_NONMATERIAL`: no new choice; history remains available.
- `NOTICE_REQUIRED`: show before the affected feature is next used.
- `ACKNOWLEDGEMENT_REQUIRED`: explicit acknowledgement before affected processing.
- `CONSENT_REQUIRED`: freely given specific choice before optional processing.
- `FEATURE_DISABLED`: feature remains unavailable where no valid basis/choice exists.

Continued use, silence, a generic login, or accepting an unrelated policy cannot satisfy a required acknowledgement or consent.

### 96.2 Policy receipts and withdrawal

A `POLICY_RECEIPT` records the exact bundle/digest, locale, presentation method, decision, timestamp, account, and applicable feature. Withdrawal of optional telemetry, leaderboard publication, or other consent-based processing is as easy as enabling it and does not reduce core gameplay. Historical receipts are append-only; a new choice supersedes but does not rewrite the old record.

Material policy changes do not alter immutable historical round evidence, costs, scores, or ranking semantics. They may block new provider actions, exports, public alias publication, or new rounds until the required notice/choice is completed.

### 96.3 Global Privacy Control

Where applicable to the deployment, an observed Global Privacy Control signal is treated as a request not to sell/share personal information and as a default-off signal for optional third-party telemetry or advertising-like processing. FGA does not use the signal to infer protected characteristics, change score/rank, or deny core play [S157]. The deployed legal record specifies exact jurisdictions and effects because GPC remains a developing web standard.

## 97. Idempotency, exports, and download integrity

### 97.1 Project-owned idempotency behavior

FGA's `IDEMPOTENCY_CONTRACT` is normative even while the corresponding IETF header remains a work in progress [S158]. For each protected mutation it defines:

- authenticated-principal and operation scope;
- accepted key syntax and entropy guidance;
- canonical request fingerprint;
- minimum retention;
- behavior for a matching completed request;
- behavior while the first request is in progress;
- rejection of same key with a different fingerprint;
- authorization recheck on replay;
- exact fields replayed versus regenerated;
- privacy-safe error and observability rules.

A replay cannot disclose another account's object, resurrect expired authorization, or bypass a newer security block.

### 97.2 Export integrity

A completed export contains an `EXPORT_INTEGRITY_MANIFEST` listing every file's logical name, media type, byte size, canonical digest, generation time, account/subject scope, export schema version, and expiry. Delivery uses `Content-Digest` where supported [S159]. Optional HTTP Message Signatures may protect controlled server-to-server or high-assurance flows [S160], but the signed FGA manifest and application authorization remain authoritative.

Exports are:

- available only after recent authentication or approved step-up;
- delivered through an unguessable single-purpose capability or authenticated endpoint;
- `Cache-Control: no-store`;
- protected from cross-account enumeration;
- bounded in size and generation time;
- deleted after expiry with a completion record;
- free of provider credentials, protected truth, other-player data, and restricted source material.

## 98. Runtime, deployment, and workflow service guarantees

### 98.1 Hardened runtime

A `PUBLIC_RANKED` release uses role-specific signed runtime hardening. Player-visible behavior is unchanged, but release is blocked if a role requires root, ambient Linux capabilities, privilege escalation, a writable root filesystem, unbounded temporary files, enabled core dumps, or interactive administrative tooling. Writable paths are explicit, bounded, nonpersistent unless approved, and contain no secrets after termination [S169].

### 98.2 Mixed-version safety

Rolling deployment may temporarily run version `N-1` and `N` only when the signed compatibility matrix permits the exact combination of:

- image and role;
- database schema/read-write contract;
- policy bundle;
- provider capability/semantic configuration;
- evaluator bundle;
- cache/client minimum version;
- publication/evidence root format.

An accepted submission cannot be evaluated partly under two evaluator/policy epochs. Incompatible roles fail readiness and are drained before migration or activation. Rollback preserves settled commands, evidence, verdict lineage, withdrawals, revocations, and deletion tombstones.

### 98.3 Work classes and cancellation

Accepted work is scheduled under a signed `WORK_CLASS_POLICY`. It prevents one player, case, benchmark, cleanup task, or provider incident from starving another. The policy defines concurrency, fairness, aging, deadline budgets, retries, poison-work quarantine, and cancellation cutoffs. Investigation credits never buy infrastructure priority.

Cancellation is explicit:

- before provider submission: normally cancel/refund;
- after submission with provable provider cancellation: settle according to observed outcome and policy;
- unknown provider outcome: reconcile before economic finality;
- after deterministic result settlement: cannot erase the command or reveal; historical result remains.

## 99. Supply-chain transparency and maintenance

The release declares its SBOM and security-baseline formats. The preferred baseline is a validated CycloneDX 1.7 or SPDX 3.0-compatible document, with exact schema/profile, tool identity, component hashes, dependency graph, services, build/runtime packages, licenses, cryptographic assets where supported, and provenance [S172][S173]. A preview SPDX 3.1 feature cannot become required release evidence without qualification.

The project maps applicable controls to the OpenSSF OSPS Baseline v2026.02.19 and NIST SSDF/SSDF-AI practices [S156][S174]. Vulnerability findings receive a signed applicability/VEX-style decision with affected artifact, exploitability evidence, owner, due date, and reevaluation trigger. OWASP Dependency-Track 5.0 or another platform MAY automate tracking, but no product database or vendor dashboard overrides signed release evidence [S168].

## 100. Additional governed open-data inputs

The following sources are added to the authoring portfolio:

| Source | Defensive fictional design value | Mandatory constraint |
|---|---|---|
| OFAC Sanctions List Service [S162] | Alias, program, list, identifier, effective-update, and fuzzy-match test structures | High-risk adverse data; official snapshot only; named entries never playable; list presence is not a generalized guilt label |
| EBA payment and electronic-money institutions register [S163] | Authorization, home/host state, service, branch/agent, and status chronology for payment-provider cases | Authorization status is contextual, not culpability; record legal basis, update cadence, schema, and fictional transformation |
| Companies House Register of Overseas Entities [S164] | Overseas entity, beneficial owner/managing officer, property-registration, annual update, and change chronology for Senior cases | Public-person data requires strict fictionalization; registration is not wrongdoing; preserve filing/effective dates and source limitations |

## 101. New research implications

- **Clarification:** RegretBench motivates measuring whether clarification choices reduce expected downstream error rather than merely increasing turn count. FGA keeps a bounded, deterministic, no-debit clarification policy [S165].
- **Noisy enterprise data:** LakeQuest reinforces that discovery and reasoning over weak metadata and noisy data lakes differ from clean-schema benchmarks. FGA adds misleading labels, duplicate fields, stale descriptions, missing lineage, and irrelevant tables to authoring/provider fixtures [S167].
- **Multimodal temporal fraud:** TSAI-MetaFraud adds research evidence for joint behavioral, transaction, graph, temporal-link, and weak-supervision evaluation. FGA uses this only to extend synthetic quality/benchmark dimensions, not to introduce automated culpability models [S166].
- **Temporal graph generation:** SAGA informs tests for semantic richness, temporal ordering, anomaly provenance, and generated-ground-truth consistency [S170].
- **Provenance-constrained evidence:** PREF-Gate-like research reinforces that analytical signals must retain provenance and validation gates before decision use; it does not authorize model scoring in FGA [S171].
- **Agent/data boundary:** Current Databricks documentation explicitly supports stateful follow-ups, generated SQL, visualizations, files, and history, reinforcing FGA's deny-by-default provider feature profile and single-command isolation [S154][S155].

## 102. Inherited version 9.0 release-delta acceptance criteria

Version 9.0 is acceptable only when:

1. Every ranked canonical natural-language intent has a deterministic answer-set/order/no-result contract.
2. Repeated execution across players, hosts, locales, provider availability, and supported database versions produces the same authoritative ranked result.
3. A live provider cannot directly add, remove, or reorder ranked evidence.
4. Direct provider-selected results are clearly unranked and cannot progress or rank.
5. Quote cost and pre-reveal status/error behavior pass hidden-cardinality and truth noninterference tests.
6. Clarification is bounded, consistent, accessible, free, and abstains before debit when unresolved.
7. Policy bundles and receipts pass effective-window, material-change, locale, accessibility, withdrawal, and no-retroactive-acceptance tests.
8. Applicable GPC behavior disables only optional processing and never core play.
9. The project idempotency contract passes key-scope, fingerprint-conflict, concurrent-request, expiry, replay-authorization, and cross-account tests.
10. Exports contain a valid manifest and representation digests, expire, remain no-store, and delete cleanly.
11. Every production runtime role passes the signed rootless/read-only/capability/temp/core-dump hardening profile.
12. Mixed-version deployment passes `N-1/N`, migration barrier, evaluator/policy epoch, drain, rollback, and stale-role tests.
13. Work scheduling passes fairness, starvation, deadline, poison-work, cancellation, and accessibility-neutrality tests.
14. SBOMs validate against the declared schema/profile and include signed vulnerability applicability.
15. OFAC/EBA/ROE source cards pass terms, adverse-data, temporal, fictionalization, and dual-use review.
16. RegretBench/LakeQuest/TSAI-MetaFraud/SAGA/PREF-Gate research cards result in concrete fixtures or documented nonadoption.
17. Strategic/open decision gates no longer reference superseded Iteration 16 release timing.
18. The generated normative graph rejects any contract in which live provider output is ranked evidence authority.

## 103. Inherited version 9.0 retained and extended invariants

1. A ranked canonical retrieval plan has one deterministic publication-bound answer set and order.
2. Provider stochasticity cannot change ranked evidence, cost, score, or progression.
3. Before reveal, hidden result cardinality cannot be inferred from quote, status, error, or intentional timing behavior.
4. Ambiguity cannot create a debit.
5. A material policy choice is never inferred from silence or unrelated continued use.
6. Withdrawal of optional processing does not reduce core game functionality.
7. Idempotency replay is scoped to the same authorized principal, operation, key, and request fingerprint.
8. A private export is verifiably complete, integrity-protected, expiring, and owner-scoped.
9. Production runtime roles do not require root, ambient capabilities, writable root, or core dumps.
10. An incompatible deployment epoch cannot claim readiness or settle accepted work.
11. One principal cannot indefinitely starve another principal's accepted work.
12. Investigation credits cannot purchase infrastructure scheduling priority.
13. An SBOM without a declared validated schema/profile and component identity is not release evidence.
14. Adverse public-register presence is never direct playable guilt.
15. Version 9.0 current requirements, not inherited delta text, are the sole normative product layer.

## 104. Provider facts, service credentials, and entitlement migration

### 104.1 Player-visible continuity guarantee

Provider limits, prices, maturity, billing corrections, workspace entitlements, regional support, and retention are volatile external facts. The game MUST NOT silently change a quote, provider mode, ranking segment, evidence source, or command availability because an external page changed. New affected ranked work is admitted only when the current provider-fact projection is nonconflicting, inside its effective window, and backed by qualification evidence.

A player-safe degradation message may state that an external capability is temporarily unavailable or being requalified. It MUST NOT expose internal invoices, credentials, workspace identifiers, capacity counts, or conflicting-provider details.

### 104.2 Fact precedence and corrections

Every material fact records its source, retrieval time, publication/effective time, product/SKU, cloud/region/workspace class, API operation, currency/unit where relevant, confidence, superseded assertion, and observed evidence. A later correction can negate an earlier billing record without rewriting history. Conflicting current assertions cause `FACT_CONFLICT` and close new affected admission until a signed qualification decision resolves them [S179].

### 104.3 Service identity lifecycle

Nonhuman integrations MUST use dedicated least-privilege service identities. Credentials are not shared among `WEB`, `MAINTENANCE`, `EVALUATOR`, publication, or release roles. Rotation is rehearsed without downtime using a bounded overlap window; the old secret is revoked after the new credential succeeds and audit evidence is complete. Expiry or revocation cannot strand an accepted command without entering the defined recovery/refund path [S177][S182].

### 104.4 Entitlement migration

Provider entitlement changes are treated as controlled releases. The signed capability snapshot stores required and forbidden grants. Before and after a provider migration, tests prove that the service principal can read only approved player-safe objects, cannot access protected truth or authoring data, and cannot inherit broad default-user privileges. Databricks' 27 July and 14 September 2026 entitlement milestones are tracked as explicit requalification dates [S178].

## 105. Cryptographic lifecycle, agility, and emergency access

### 105.1 Inventory and purpose separation

The release maintains a `CRYPTOGRAPHIC_ASSET_INVENTORY` for session protection, password/recovery verifiers, TLS, evidence/publication signatures, evaluator signatures, export encryption, private-text envelope encryption, database/backups, audit anchoring, provider OAuth, and CI/release credentials. Each asset has an owner, purpose, algorithm/suite, key ID, storage boundary, creation/activation/expiry, permitted operations, dependent artifacts, rotation rule, compromise playbook, retention, and destruction evidence [S183].

A key for one purpose MUST NOT be silently reused for another purpose. Player-facing signature or digest verification identifies the applicable algorithm/suite and key ID without exposing secret material.

### 105.2 Rotation, revocation, and historical verification

Rotation creates a new active key while preserving the minimum public verification material required for legitimate historical artifacts. Revocation prevents new trust and triggers impact analysis; it does not rewrite historical bytes. Compromised signing or evaluator keys cause publication/round review and amendment or invalidation where required. Destroyed deletion-scoped encryption keys are not restored from backup.

### 105.3 Cryptographic agility and post-quantum planning

The project inventories every dependency on vulnerable public-key algorithms and maintains a migration plan. New algorithms are introduced only through compatibility, performance, interoperability, canonical-byte, signature-size, browser, provider, and rollback qualification. NIST PQC standards inform the migration backlog, but no experimental or unilateral algorithm switch may change a ranked round or make historical verification impossible [S184].

### 105.4 Break-glass access

Emergency access requires a declared incident, strong phishing-resistant authentication, narrowly scoped just-in-time privilege, a short expiry, reason and ticket, independent approval where the action can affect truth, keys, publications, deletion, or rankings, automatic revocation, and post-use review. The player is notified when an incident materially affects their data, result validity, or service, subject to safety and legal constraints. Break-glass access cannot disable logging or create a general protected-truth export.

## 106. Tamper-evident audit, incidents, and player redress

### 106.1 Audit completeness

Security-relevant events include authentication, recovery, privileged access, key lifecycle, provider facts/credentials, publication, policy, command settlement, evaluator requests/results, export/deletion, abuse controls, deployment/recovery epochs, and incident decisions. Events use canonical fields, source identity, event/ingest time, sequence, correlation, actor class, object class, outcome, and safe reason code. Sensitive payloads remain excluded.

Events are grouped into immutable segments committed by an `AUDIT_INTEGRITY_CHAIN`. Verification detects deletion, insertion, reordering, truncation, duplicate sequence, invalid source, and missing expected source intervals. Provider audit and query-history tables may corroborate activity but cannot replace the FGA ledger because their maturity, region, privileges, and retention are external capabilities [S180][S181][S186].

### 106.2 Incident lifecycle

Incidents move through `SUSPECTED`, `DECLARED`, `CONTAINING`, `ERADICATING`, `RECOVERING`, `MONITORING`, and `CLOSED`, with an optional `REOPENED` transition. The incident record preserves evidence-hold scope, affected components/data/rounds, player impact, legal/privacy assessment, decisions, recovery criteria, and control improvements [S185].

### 106.3 Result validity and notices

An incident affecting evidence, provider parity, evaluator integrity, scoring, keys, or publication trust produces an explicit validity decision for each affected segment/round class: unaffected, under review, paused, invalidated, or superseded by amendment. Player notices are factual, dated, accessible, and avoid speculation or hidden-answer disclosure. A notice links to available recovery, withdrawal, dispute, and amendment paths.

## 107. Safe documents, authoring inputs, and exports

### 107.1 Baseline upload boundary

Ordinary players do not upload arbitrary files in the baseline product. Case authors, release engineers, and support workflows still handle untrusted files and therefore follow the same `CONTENT_SAFETY_PROFILE`. A future player-upload feature requires a new explicit specification version and threat/privacy/accessibility review.

### 107.2 Ingestion and rendering

Allowed formats are enumerated by purpose. Extension, declared MIME, magic bytes, parser result, and expected structure must agree. Archives have file-count, nesting, uncompressed-size, compression-ratio, path, symlink, and duplicate-name limits. Conversion/rendering runs in an isolated, resource-bounded environment without network, credentials, protected mounts, or persistent writable state. Macros, scripts, external references, embedded executables, unsafe fonts, active SVG, and unsupported object types are rejected or removed according to the profile [S188].

### 107.3 Spreadsheet and text export

CSV/TSV cells that could be interpreted as formulas are neutralized according to a documented reversible display/export policy; untrusted values cannot begin an executable formula in common spreadsheet applications [S187]. Exports use safe filenames, explicit UTF-8 encoding, language/direction metadata where applicable, bounded fields, and no hidden sheets/macros. ZIP paths cannot escape the archive root.

### 107.4 Final-byte integrity

Security transformations occur before digesting. The `EXPORT_INTEGRITY_MANIFEST` commits to the exact bytes delivered after sanitization, conversion, compression, and encryption. A clean source digest cannot authorize a transformed artifact whose final bytes were not scanned and committed.

## 108. Regional recovery, immutable backup, and write fencing

### 108.1 Recovery epoch

Every authoritative environment has one current `RECOVERY_EPOCH`. The database primary, web admission, maintenance executor, evaluator delivery, migration role, and publication activation must present the current epoch/fence before committing. A stale site or process can read only where policy permits and cannot settle commands, issue verdicts, activate publications, or mutate player state.

### 108.2 Backup and restore guarantees

Public-ranked backups include database state, immutable publications, policy/verifier metadata, audit-chain material, deletion tombstones, revocations, aliases/withdrawals, key references, and workflow correlations. At least one recovery copy is protected from ordinary application credentials and destructive overwrite. Restore qualification proves RPO/RTO, digest/signature validity, schema compatibility, key availability or intentional erasure, and nonresurrection of deleted/revoked/quarantined state [S196].

### 108.3 Promotion and failback

Promotion is a fenced workflow: stop or isolate the old writer, establish database/provider facts, restore/verify, increment the recovery epoch, validate secrets/keys/publications/policy/evaluator lineage, reconcile pending provider work, then open writes. Failback uses the same process and never assumes that DNS or process restart alone establishes authority.

### 108.4 Player behavior during recovery

The game may become read-only or pause affected commands. It never accepts a mutation that cannot be durably acknowledged. Recovery messages distinguish read-only, pending reconciliation, and unavailable states without leaking topology. Refund, command, evaluation, and amendment rules remain idempotent across the recovery boundary.

## 109. Automation abuse resistance and accessible challenges

### 109.1 Separation from gameplay

Abuse controls protect authentication, account creation, command APIs, exports, and infrastructure. Their signals are not evidence, do not influence score/rank/ending, and cannot alter the records a player may reveal. Accessibility settings, assistive technology, keyboard-only use, slow reading, language, timezone, screen size, network latency, and ordinary device changes are prohibited risk features for competitive decisions.

### 109.2 Progressive controls

The default sequence is bounded server-side rate limiting, idempotency, concurrency limits, cooldown, recent-authentication, and risk-triggered step-up. Challenges must satisfy accessible-authentication requirements, provide a nonvisual/noncognitive alternative, and avoid a CAPTCHA-only gate; automated accessibility evidence may use approved ACT-format rules but never replaces human review [S192]–[S194]. A false-positive path preserves the account and unfinished rounds and offers retry or support without requiring hidden personal data.

### 109.3 Privacy and retention

Risk events use coarse, purpose-limited data, short retention, and protected access. Cross-site fingerprinting and sale/share of device signals are prohibited. Security telemetry is not repurposed for marketing or ranking. Operator actions and policy changes are audited.

## 110. Privacy-preserving telemetry and experimentation

### 110.1 Event minimization

Every event field has a purpose, data class, lawful basis/consent state, retention, aggregation level, and prohibited joins. Raw prompts, notes, case-file prose, evidence content, recovery data, exact IP addresses beyond justified security windows, and protected truth remain excluded from product analytics.

### 110.2 Aggregation and contribution limits

Reports apply minimum cohort sizes, per-account/per-round contribution bounds, category bucketing, and delayed publication. Small cells are suppressed rather than combined in ways that permit subtraction attacks. When formal differential privacy is claimed, the mechanism, adjacency definition, clipping, epsilon/delta, composition, seed/randomness handling, and cumulative privacy budget are recorded in a `PRIVACY_BUDGET_LEDGER` [S176].

### 110.3 Experiments

Experiment assignment is deterministic from a privacy-safe pseudonymous key and experiment version. Ranked-affecting behavior is excluded unless a new ranking segment and signed feature policy are created before round acceptance. Experiments cannot use dark patterns, weaken accessibility/security/privacy, or conceal a material policy/provider change. Players who decline optional telemetry retain core functionality.

## 111. API, schema, client, Unicode, and time evolution

### 111.1 Compatibility window

Every public client/API/schema release declares supported predecessor versions, read/write compatibility, retirement date, migration behavior, and emergency block conditions. Additive fields may appear only when older clients safely ignore them; meaning, authorization, defaults, economic semantics, and enum interpretation cannot change silently. A write from an unsupported client fails before mutation with an accessible upgrade path.

### 111.2 Cursor and replay integrity

Opaque pagination cursors are bound to principal or public scope, endpoint/query hash, immutable snapshot/segment, ordering contract, page size, expiry, and signing key. A cursor cannot be modified to cross owners, cases, snapshots, or filters. Idempotency fingerprints record their canonicalization version; a new version cannot reinterpret an old key.

### 111.3 Time semantics

Database time is authoritative for durable deadlines and ordering; process monotonic clocks measure only local duration. Case events store UTC instant plus source timezone/offset and precision. Every publication binds a timezone-database version, ambiguous/nonexistent local-time resolution rule, and chronology tests. A tzdb update creates new qualification evidence and cannot reorder a historical snapshot [S196].

### 111.4 Unicode, language, and direction

Identifiers use field-specific normalization; evidence text preserves original bytes/text plus safe normalized search projections. Language and direction metadata travel with strings where context is not sufficient, including mixed RTL/LTR content [S195]. Collation and case folding are pinned for canonical sorts. Bidi controls, confusables, invisible characters, and malformed encodings are safely displayed and tested without erasing evidentiary distinctions.

### 111.5 Database ownership isolation

Every private account, career, round, save, command, submission, export, deletion, alias, and security object is protected by ownership in both the domain query and database model. Public-ranked storage uses composite owner/object constraints and enforced row-level policies for owner-scoped private tables. Normal application roles cannot bypass or disable those policies. Maintenance, evaluator, migration, and incident access use distinct roles and explicit audited procedures; a nested URL or guessed opaque ID never establishes ownership.

## 112. Vulnerability prioritization, new sources, and research implications

### 112.1 Vulnerability decision model

Release and patch decisions combine component identity/provenance, reachable call path, privilege, truth/credential exposure, exploit maturity, CISA KEV status, EPSS probability, CVSS v4 vectors, deployment controls, and VEX evidence [S189]–[S191]. A reachable KEV affecting authentication, public ingress, provider credentials, publication verification, evaluator isolation, exports, or database writes blocks release unless removed or covered by a signed time-bounded emergency exception with effective containment.

### 112.2 Additional governed sources

- **FDIC BankFind/Open Data:** useful for fictional insured-institution, branch, merger, failure, and historical-structure schemas; source recency and API-key/availability changes are recorded [S197].
- **FCA Warning List:** useful for clone-firm aliases, domains, warning dates, and authorized-versus-unauthorized comparisons; absence from the list is not proof of legitimacy and presence is never copied into playable accusation [S198].
- **IOSCO I-SCAN:** useful for cross-regulator alert provenance and jurisdiction/date schemas; source context and duplicate alerts are preserved [S199].
- **Companies House disqualified directors:** useful for effective-date and permission/exception reasoning; named persons remain excluded from playable content and public-record caveats are retained [S200].

### 112.3 Research implications

SQaLe adds large, realistic schema-size and ambiguity stress for safe plan generation [S201]. SynQuE motivates selecting synthetic fixture sets by downstream utility evidence rather than one distribution score [S202]. FRAUDGUESS motivates novelty and explanation fixtures but does not authorize an unsupervised fraud verdict [S203]. FiFAR motivates capacity-aware human/AI deferral simulations and queue tests, not automated culpability or replacement of the deterministic evaluator [S204]. All remain research inputs until reproducibility, license, privacy, safety, and publication gates pass.

## 113. Version 10.0 release-delta acceptance criteria

1. Every provider capability, price, correction, entitlement, region, retention, and maturity fact used for admission has a current nonconflicting ledger projection and evidence owner.
2. Databricks or another provider integration uses a dedicated service identity; short-lived-token issuance, secret rotation, revocation, expiry, and least-privilege checks pass.
3. The provider entitlement migration is rehearsed before and after the documented effective milestones; broad inherited grants are absent.
4. The cryptographic inventory covers every production key, certificate, token-secret class, and signed/encrypted artifact dependency.
5. Signing/evaluator/export/private-text key rotation, revocation, compromise, restore, and historical-verification tests pass.
6. Break-glass access requires approved scope, strong authentication, expiry, audit, auto-revocation, and independent review.
7. Audit-chain verification detects deleted, inserted, reordered, truncated, duplicated, and missing-source events.
8. Incident drills produce signed affected-object, player-notice, result-validity, evidence-hold, recovery, and closure records.
9. Authoring inputs and exports pass format allowlist, magic-byte, archive-bomb/path, sandbox, active-content, malware/CDR-policy, and final-byte-digest tests.
10. CSV/spreadsheet exports cannot execute player-controlled formulas under the documented supported-client tests.
11. Regional recovery increments a fencing epoch, rejects stale writers, restores security/policy/publication state, reconciles pending provider work, and meets RPO/RTO evidence.
12. Abuse controls have accessible alternatives, false-positive recovery, privacy limits, and proof that their signals do not affect score/rank/evidence.
13. Telemetry and experiments pass purpose/schema linting, contribution/cohort controls, retention, opt-out, and ranked-semantics isolation.
14. Any differential-privacy claim has a complete mechanism and cumulative privacy-budget record.
15. API/client/schema compatibility, signed cursors, idempotency-fingerprint evolution, and retirement behavior pass N-1/N tests.
16. Timezone-database, locale/collation, Unicode normalization, language/direction, and ambiguous-time fixtures are version-bound and deterministic.
17. Vulnerability triage ingests KEV/EPSS/CVSS v4 plus reachability/VEX and blocks reachable exploited critical paths.
18. New FDIC/FCA/IOSCO/Companies House sources have exact terms, snapshots, context, fictionalization, and no-guilt approvals.
19. SQaLe/SynQuE/FRAUDGUESS/FiFAR-inspired fixtures are documented as research-only and cannot become scoring or truth dependencies.
20. Composite ownership constraints and forced row-level policies block cross-account reads/writes even when an application ownership check is fault-injected.
21. Functional, technical, manifest, schema, OpenAPI, deployment, runtime, policy, provider-fact, cryptographic, audit, DR, and acceptance artifacts share `FGA-NORMATIVE-PAIR-10.0-20260726` and pass semantic-diff checks.

## 114. Version 10.0 retained and extended invariants

1. A contradictory, expired, or unqualified provider fact cannot admit affected new ranked work.
2. A provider billing correction or entitlement migration cannot retroactively mutate a round, debit, quote, evidence set, or ranking segment.
3. Every production service credential belongs to one explicit nonhuman principal, role, scope, owner, and lifecycle.
4. A revoked credential or cryptographic key cannot regain authority through process restart, old configuration, or backup restore.
5. One cryptographic key cannot silently serve incompatible signing, encryption, authentication, and audit purposes.
6. A break-glass session cannot outlive its grant or operate without an immutable reviewable record.
7. Audit deletion, insertion, reordering, truncation, sequence gaps, and invalid source identity are detectable.
8. Provider audit/query history cannot be the sole audit authority.
9. A file is not safe merely because its digest or filename is valid.
10. Final export digests commit to sanitized final bytes, not pre-transform inputs.
11. A stale recovery epoch cannot commit authoritative writes or verdicts.
12. Restore cannot resurrect deleted private text, revoked keys, quarantined publications, withdrawn aliases, or superseded policy.
13. An abuse score cannot influence game evidence, price, score, ending, progression, or leaderboard rank.
14. An accessible challenge alternative exists wherever an anti-automation challenge can block core access.
15. Analytics cannot contain raw private prose, protected truth, credentials, or recovery secrets.
16. An experiment cannot mutate accepted ranked semantics.
17. An old client, cursor, schema, or idempotency fingerprint cannot be reinterpreted under a new contract.
18. Historical ordering and chronology cannot depend on the host's current tzdb, locale, collation, or Unicode defaults.
19. A reachable known-exploited vulnerability on a protected path cannot be accepted by numeric severity alone.
20. New adverse-status sources never become direct playable accusation lists.
21. A private object cannot be read, linked, mutated, exported, or enumerated outside its owner scope even if an application-layer ownership check fails.

## Appendix A — Functional glossary

| Term | Player-safe definition |
|---|---|
| Record | One observable source row, document, event, or account representation |
| Entity | A real-world-like thing that one or more records may describe; canonical identity remains protected |
| Direct relationship | A relationship explicitly recorded by a visible source |
| Candidate identity | A precomputed suggestion that two records may refer to the same entity |
| Exact shared-field link | A precomputed statement that approved normalized fields match exactly |
| Manual hypothesis | A player-created theory, visibly separate from source facts and analytics |
| Claim | A proposition in the case file that must be supported, qualified, or left uncertain |
| Evidence | A visible item attached to a claim with provenance |
| Role | What an actor did operationally |
| Culpability | The player’s supported conclusion about knowing responsibility |
| Harm | Victimization, loss, or other impact, separate from role and culpability |
| Investigation profile | `GUIDED`, `STANDARD`, or `EXPERT` evidence complexity |
| Valid no-result | A correctly executed, disclosed paid action that returns no new records/links |
| Protected truth | Evaluator-only answer material never sent to the browser or provider |
| Environment profile | Deployment assurance level: Development, Demo, or Public Ranked |
| Provider execution mode | Bound retrieval implementation such as Materialized Retrieval or Live Genie |
| Ranking segment | Exact compatibility pool for competitive comparison |
| Ranked checkpoint | Restorable draft/UI snapshot that cannot roll back evidence, commands, credits, or submission |
| Truth Broker | Narrow evaluator-only path that converts protected truth plus a submission into a safe verdict |
| Ranked retrieval parity manifest | Signed deterministic answer-set contract for supported canonical retrieval plans |
| Deterministic result resolver | Publication-bound component that selects and orders ranked records |
| Pre-reveal noninterference | Guarantee that quote/status/error/timing behavior does not reveal hidden evidence |
| Policy bundle | Immutable versioned set of applicable notices, disclosures, and choices |
| Policy receipt | Append-only record of the exact policy version and player decision |
| Idempotency contract | FGA-owned retry/replay semantics for protected mutations |
| Export integrity manifest | Digest index for a private downloadable export |
| Runtime hardening profile | Signed least-privilege process/container requirements |
| Deployment epoch | Compatible image/role/schema/policy/evaluator rollout identity |
| Work class policy | Durable scheduling, fairness, deadline, retry, and cancellation rules |
| Provider fact ledger | Versioned source/effective-time record that resolves volatile provider facts before admission |
| Credential lifecycle profile | Service-identity privilege, token, secret, rotation, revocation, and expiry contract |
| Cryptographic asset inventory | Registry of every production key/certificate/secret, purpose, algorithm, owner, state, and dependency |
| Break-glass record | Reviewable evidence for exceptional, scoped, expiring privileged access |
| Audit integrity chain | Ordered cryptographic commitment that makes audit deletion, reordering, and truncation detectable |
| Content safety profile | Rules for allowed formats, scanning, sanitization, conversion, naming, isolation, and exports |
| Recovery epoch | Monotonic authority generation used to fence stale writers after recovery/failover |
| Automation abuse policy | Accessible, privacy-minimized rate/risk/challenge and false-positive rules |
| Privacy measurement profile | Purpose, contribution, cohort, retention, experiment, aggregation, and privacy-budget rules |
| Contract compatibility window | Signed period and matrix for safe client/API/schema/fingerprint interoperability |
| Time semantics profile | Bound timezone, locale, collation, Unicode, direction, and clock behavior |


| Workflow liveness class | Assurance that an accepted workflow will progress without relying on future player traffic |
| Private evaluator | Nonpublic evaluator identity that alone reads protected truth |
| Publication freshness | Expiry and consistency state used to detect freeze, rollback, or mixed repository metadata |
| Canonical contract bytes | Schema-valid deterministic JSON bytes used for hashing and signing |
| Exact amount | Minor units or exact decimal plus currency/asset, scale, and rounding metadata |
| Fencing epoch | Monotonic ownership token preventing a stale executor from committing |
| Cryptographic erasure | Key-destruction process that makes designated encrypted private data unrecoverable |
| Evidence integrity record | Digest and derivation lineage for an evidence object or rendition |

## Appendix B — Cross-document requirement traceability

| Functional concern | Primary technical specification area |
|---|---|
| Authentication and recovery | Authentication/session service; security architecture; recovery-code storage and endpoints |
| Career/card availability | Career service; catalogue projection; database constraints |
| Four action families | Command/quote engine; provider adapters; durable outbox/reconciliation |
| Credits and repeat actions | Append-only ledger; idempotency; deterministic result cache |
| List/graph equivalence | Shared revealed-state projection; semantic graph navigator |
| Genie Agent safety | Semantic allowlists; benchmark suite; result validator; provider state machine |
| Temporal integrity | Snapshot `as_of_time`; publication validators; leakage-safe offline pipeline |
| Case file and revision history | Draft aggregate; revision log; save/checkpoint service |
| Immutable evaluation and amendments | Submission/evaluation stores; amendment lineage; ranking reindex workflow |
| Open data and licensing | Source registry; data cards; legal gate; checksums |
| Synthetic fidelity/privacy | Data-quality gate; behavioral and privacy test suites |
| Accessibility | WCAG 2.2 AA component and end-to-end qualification |
| Privacy/export/delete | Privacy service; scoped export builder; deletion workflow |
| SLO/DR | Metrics, alerts, backup/restore, incident runbooks |
| Ranked checkpoint monotonicity | Save projections, ledger/visibility immutability, practice fork service |
| Provider fairness | Capability registry, provider-mode binding, benchmark/equivalence gate, ranking segment |
| Protected truth | Separate role/schema plus Truth Broker and route-layer import/authorization tests |
| Build/publication integrity | Signed provenance, signature verification, revocation/quarantine, anti-downgrade floor |
| Age/content/dual-use | Content cards, warning catalogue, policy gate, reviewer evidence |
| AI transparency/provider maturity | Capability disclosure projection; provider inventory; preview exception; model/config change control |
| Passkeys/session devices | WebAuthn credential service; session-device endpoints; recent-auth and revocation tests |
| Provider-independent solve | Case manifest solve-route gate; materialized adapter; outage golden playthroughs |
| Client compatibility | Build handshake; minimum-write-client; service-worker cache revocation |
| Legal/processors/residency | Applicability records; processor inventory; deployment publication gates |
| Formal invariant assurance | State-machine models; property/fault-injection traceability |
| Player incidents/redress | Status projection; incident notices; support bundle and appeal workflows |
| Provider capacity and pricing | Capability effective windows; semantic-interface packing; paid-window cost qualification |
| AI interaction/media provenance | Disclosure profiles; signed asset creation records; optional C2PA validation |
| Privacy threat model | Data-flow inventory; privacy-harm analysis; DPIA/applicability; outbound-schema enforcement |
| Ranked feature governance | Signed feature policy; immutable round binding; staged rollout and narrowing kill switches |
| Dynamic accessibility | Executable journey traces; accessibility-tree/focus/live-region evidence; human conformance review |
| Dependency identity | Registry/namespace/version/hash/provenance pinning; dependency-confusion tests |
| Continuous workflow liveness | Technical §84 always-on maintenance service, private network, heartbeat, queue/deadline admission, and cron backstop |
| Provider conversation isolation | Technical §85 one-command/one-conversation lifecycle, cleanup, retention, remote inventory, and capacity headroom |
| Real provider cost | Technical §86 product/SKU price catalogue, reservation, append-only cost ledger, budget circuit breaker, and invoice reconciliation |
| Recovery and privileged access | Technical §87 phishing-resistant privileged identities, step-up, exceptional recovery, and `RECOVERY_LIMITED` controls |
| Browser/client trust | Technical §88 signed security-header profile, Fetch Metadata, sandboxing, exact-origin messaging, and cross-origin isolation decision |
| Transaction correctness | Technical §89 transaction profiles, global lock order, idempotent retries, failover behavior, and invariant monitor |
| Evidence integrity | Technical §90 canonical serialization, domain-separated digests, Merkle roots, and hermetic/reproducible publication |
| LLM/provider security | Technical §91 LLMSVS mapping, tool/data denial, prompt/output injection, exfiltration, and hard resource budgets |
| Chaos qualification | Technical §92 executable failure scenarios, evidence capture, fail-closed criteria, and signed report |
| New sources and research | Technical §93 source cards, benchmark fixtures, privacy/value-linking tests, and tracked nonproduction research inputs |
| Ranked retrieval evidence parity | Technical §96 provider/plan split, deterministic resolver, answer-set digests, and parity manifest |
| Pre-reveal protocol noninterference | Technical §97 quote/status/error/timing information-flow tests and clarification policy |
| Policy/consent lifecycle | Technical §98 immutable policy bundles, receipts, change assessment, withdrawal, and migration |
| Idempotency and HTTP integrity | Technical §99 project-owned idempotency semantics, RFC 9530 digests, and optional RFC 9421 signatures |
| Secure exports | Technical §100 isolated export builder, integrity manifest, delivery capability, expiry, and deletion |
| Runtime hardening | Technical §101 rootless/read-only/capability/temp/core-dump role profile |
| Mixed-version deployment | Technical §102 deployment epochs, compatibility matrix, migration barriers, drains, and rollback |
| Queue QoS and cancellation | Technical §103 work classes, fairness, aging, deadlines, cancellation, and starvation tests |
| Supply-chain baseline | Technical §104 CycloneDX/SPDX profile, OSPS/SSDF mapping, VEX, and dependency tracking |
| Privacy signals/aggregate telemetry | Technical §105 GPC handling, optional telemetry gating, aggregation thresholds, and privacy review |
| New sources/research | Technical §106 OFAC/EBA/ROE source cards and new benchmark/research fixtures |

| Provider facts and credentials | Technical §109 provider fact assertions/conflicts/qualification, OAuth M2M rotation, entitlement templates, and drift |
| Cryptographic lifecycle and break-glass | Technical §110 key inventory/state machine, compromise/restore behavior, crypto agility, and emergency grants |
| Audit integrity and incidents | Technical §111 canonical audit envelopes, segment roots/anchors, source gaps, incident graph, holds, notices, and validity decisions |
| Safe documents and exports | Technical §112 isolated content pipeline, format rules, archive/formula protections, final-byte manifests, and quarantine |
| Regional recovery | Technical §113 recovery epoch, writer fencing, immutable backup evidence, anti-resurrection, promotion/failback, and reconciliation |
| Automation abuse fairness | Technical §114 privacy-minimized risk/rate controls, accessible challenges, false-positive review, and ranked noninterference |
| Privacy measurement and experiments | Technical §115 schema compiler, contribution/cohort controls, privacy ledger, and experiment isolation |
| API/schema/time evolution | Technical §116 compatibility graph, signed cursors, fingerprint versions, tzdb/Unicode/collation/clock profile |
| Vulnerability and new evidence inputs | Technical §117 KEV/EPSS/CVSS/reachability triage, source cards, and research-only fixtures |

## Appendix C — Current sources and research bibliography

The following sources were reviewed for the consolidated version 9.0 iteration. Platform/version facts are snapshots as of **26 July 2026** and MUST be revalidated at release freeze.

### Standards, security, accessibility, identity, and API design

- **[S01]** NIST, *SP 800-63B-4: Authentication and Authenticator Management*: <https://pages.nist.gov/800-63-4/sp800-63b.html>
- **[S02]** OWASP, *Application Security Verification Standard 5.0*: <https://owasp.org/www-project-application-security-verification-standard/>
- **[S03]** W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*: <https://www.w3.org/TR/WCAG22/>
- **[S04]** IETF, *RFC 9457 — Problem Details for HTTP APIs*: <https://datatracker.ietf.org/doc/html/rfc9457>
- **[S45]** OWASP, *Artificial Intelligence Security Verification Standard (AISVS) 1.0*: <https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/>
- **[S46]** NIST, *Artificial Intelligence Risk Management Framework and Generative AI Profile*: <https://www.nist.gov/itl/ai-risk-management-framework>
- **[S61]** OWASP, *Top 10:2025*: <https://owasp.org/Top10/2025/>
- **[S68]** W3C, *Web Authentication: An API for accessing Public Key Credentials — Level 3*, Candidate Recommendation Snapshot, 26 May 2026: <https://www.w3.org/TR/webauthn-3/>
- **[S69]** European Union, *Regulation (EU) 2024/1689 (Artificial Intelligence Act)* and Commission implementation guidance: <https://eur-lex.europa.eu/eli/reg/2024/1689/oj> and <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>
- **[S70]** European Commission, *Digital Services Act package*: <https://digital-strategy.ec.europa.eu/en/policies/digital-services-act-package>
- **[S71]** European Commission, *European Accessibility Act*: <https://employment-social-affairs.ec.europa.eu/policies-and-activities/social-protection-social-inclusion/persons-disabilities/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en>
- **[S72]** ETSI, *EN 301 549 accessibility requirements for ICT products and services*; V3.2.1 remains the published harmonised baseline while V4.1.0 was on approval in July 2026: <https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf> and <https://www.etsi.org/technical-groups/hf/>
- **[S73]** CISA, *2025 Minimum Elements for a Software Bill of Materials* and VEX resources: <https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom> and <https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex>

### Databricks, databases, runtimes, and hosting

- **[S05]** Databricks, *Genie Agents Conversation API*: <https://docs.databricks.com/aws/en/genie-agents/conversation-api>
- **[S06]** Databricks, *Set up and manage a Genie Agent*: <https://docs.databricks.com/aws/en/genie-agents/set-up>
- **[S07]** Databricks, *Monitor and benchmark Genie*: <https://docs.databricks.com/aws/en/genie/monitor>
- **[S08]** Databricks, *SQL Statement Execution API tutorial*: <https://docs.databricks.com/aws/en/dev-tools/sql-execution-tutorial>
- **[S09]** Databricks, *Free Edition limitations*: <https://docs.databricks.com/aws/en/getting-started/free-edition-limitations>
- **[S10]** Databricks, *Lakebase Autoscaling compatibility*: <https://docs.databricks.com/aws/en/oltp/projects/compatibility>
- **[S11]** PostgreSQL, *Versioning policy and current releases*: <https://www.postgresql.org/support/versioning/>
- **[S12]** Railway, *Deployment healthchecks*: <https://docs.railway.com/deployments/healthchecks>
- **[S44]** Databricks, *Free Edition limitations, comparison, and terms*: <https://docs.databricks.com/aws/en/getting-started/free-edition-limitations>, <https://docs.databricks.com/aws/en/getting-started/free-trial-vs-free-edition>, and <https://www.databricks.com/legal/databricks-free-edition>
- **[S63]** Python Software Foundation, *Python downloads and release status*: <https://www.python.org/downloads/>
- **[S64]** Pydantic, *release history*: <https://docs.pydantic.dev/latest/changelog/>
- **[S65]** Databricks, *Lakebase Autoscaling overview, compatibility, recovery, and history*: <https://docs.databricks.com/aws/en/oltp/>
- **[S74]** Databricks, *2026 product release notes for Genie/AI-BI*, including naming and capability-history changes; current GA/beta status is revalidated through [S85][S86]: <https://docs.databricks.com/aws/en/release-notes/product/2026/>

### Frontend, backend, graph, entity-resolution, and software supply chain

- **[S13]** React, *Versions*: <https://react.dev/versions>
- **[S14]** React, *Security advisories and blog*: <https://react.dev/blog>
- **[S15]** Vite, *Getting started and runtime requirements*: <https://vite.dev/guide/>
- **[S16]** FastAPI, *Release notes*: <https://fastapi.tiangolo.com/release-notes/>
- **[S17]** Cytoscape.js, official documentation: <https://js.cytoscape.org/>
- **[S18]** GraphFrames, official project documentation: <https://graphframes.io/>
- **[S19]** GraphFrames Python package and release attestations: <https://pypi.org/project/graphframes-py/>
- **[S20]** Zingg, current documentation: <https://docs.zingg.ai/latest>
- **[S21]** Zingg GitHub repository/license and product information; the exact artifact and use model require legal review: <https://github.com/zinggAI/zingg> and <https://www.zingg.ai/product/entity-resolution-platform>
- **[S47]** SLSA, *Supply-chain Levels for Software Artifacts specification v1.2*: <https://slsa.dev/spec/v1.2/>
- **[S62]** OpenTelemetry, *Semantic Conventions*: <https://opentelemetry.io/docs/specs/semconv/>
- **[S75]** React, *Critical Security Vulnerabilities in React Server Components* and follow-up fixes: <https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components> and <https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components>
- **[S76]** Vite, *Vite 8 and Vite 8.1 release announcements*: <https://vite.dev/blog/announcing-vite8> and <https://vite.dev/blog/announcing-vite8-1>

### Open data, public information, and typology sources

- **[S22]** GLEIF, Global Legal Entity Identifier data and mappings: <https://www.gleif.org/>
- **[S23]** Open Ownership, beneficial-ownership data and BODS: <https://www.openownership.org/>
- **[S24]** ICIJ, Offshore Leaks Database, licensing, and disclaimer: <https://offshoreleaks.icij.org/pages/database>
- **[S25]** Publications Office of the European Union, TED Open Data Service: <https://data.ted.europa.eu/>
- **[S26]** USAspending.gov API: <https://api.usaspending.gov/>
- **[S27]** U.S. SEC, EDGAR application programming interfaces: <https://www.sec.gov/search-filings/edgar-application-programming-interfaces>
- **[S28]** UK Companies House API and data products: <https://developer.company-information.service.gov.uk/> and <https://www.gov.uk/government/publications/companies-house-data-products>
- **[S29]** European Commission, consolidated EU financial sanctions dataset: <https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions>
- **[S30]** UK Government, UK Sanctions List: <https://www.gov.uk/government/publications/the-uk-sanctions-list>
- **[S31]** OpenSanctions, source catalogue and provenance: <https://www.opensanctions.org/>
- **[S32]** U.S. FTC, Explore Data: <https://www.ftc.gov/news-events/explore-data>
- **[S33]** FBI IC3, *2025 Internet Crime Report*: <https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf>
- **[S34]** Europol, *Internet Organised Crime Threat Assessment 2026*: <https://www.europol.europa.eu/publication-events/main-reports/internet-organised-crime-threat-assessment-iocta-2026>
- **[S35]** ACFE, reports and statistics, including the *2026 Report to the Nations*: <https://www.acfe.com/fraud-resources/reports-and-statistics>
- **[S36]** Open Contracting Partnership, Open Contracting Data Standard: <https://standard.open-contracting.org/latest/en/>
- **[S48]** World Bank, *Listing of Ineligible Firms and Individuals*: <https://www.worldbank.org/en/projects-operations/procurement/debarred-firms>
- **[S49]** World Bank, procurement notices and opportunities: <https://projects.worldbank.org/en/projects-operations/procurement>
- **[S50]** SAM.gov, public exclusions and entity information: <https://sam.gov/content/entity-information>
- **[S51]** UK Government, *Find a Tender OCDS API*: <https://www.find-tender.service.gov.uk/apidocumentation/1.0/GET-ocdsReleasePackages>
- **[S52]** European Commission, *Financial Transparency System*: <https://ec.europa.eu/budget/financial-transparency-system/index.html>
- **[S57]** European Commission, *Arachne risk-scoring tool* overview; restricted governance/reference input, not open ingestion: <https://ec.europa.eu/social/main.jsp?catId=325&intPageId=3587&langId=en>
- **[S58]** U.S. FTC, 2025 fraud-loss and social-media-origin reporting: <https://www.ftc.gov/news-events/news/press-releases>
- **[S77]** UK Government, *Contracts Finder archive/service documentation*; retained only for historical notices and compatibility research: <https://www.contractsfinder.service.gov.uk/>
- **[S78]** Companies House, *People with Significant Control daily JSON snapshot and data products*: <https://download.companieshouse.gov.uk/en_pscdata.html> and <https://www.gov.uk/government/publications/companies-house-data-products>
- **[S79]** U.S. Internal Revenue Service, *Exempt Organizations Business Master File and Form 990 XML datasets*: <https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf> and <https://www.irs.gov/charities-non-profits/form-990-series-downloads>
- **[S80]** U.S. Centers for Medicare & Medicaid Services, *NPPES/NPI data dissemination*: <https://download.cms.gov/nppes/NPI_Files.html>
- **[S81]** U.S. Centers for Medicare & Medicaid Services, *Open Payments data*: <https://openpaymentsdata.cms.gov/>
- **[S82]** U.S. Department of Health and Human Services OIG, *List of Excluded Individuals/Entities downloadable data*: <https://oig.hhs.gov/exclusions/exclusions_list.asp>
- **[S83]** Charity Commission for England and Wales, *Register API and full-register data*: <https://register-of-charities.charitycommission.gov.uk/register/full-register-download> and <https://www.data.gov.uk/dataset/2c448a55-7a5f-47f3-9bd5-27a2d31a59a3/register-of-charities>
- **[S84]** Open Ownership, *BODS 0.4 support and standards-development pause*, plus 2026 UK data refresh: <https://www.openownership.org/en/topics/beneficial-ownership-data-standard/> and <https://www.openownership.org/en/news/open-ownership-publishes-refreshed-uk-beneficial-ownership-data-in-bods-format/>

### Research watchlist

- **[S37]** *OpenSanctions Pairs: Large-Scale Entity Matching with LLMs*, 2026: <https://arxiv.org/abs/2603.11051>
- **[S38]** *In-context Clustering-based Entity Resolution with Large Language Models: A Design Space Exploration*, 2025/2026: <https://arxiv.org/abs/2506.02509>
- **[S39]** *BEAVER: An Enterprise Benchmark for Text-to-SQL*, updated 2026: <https://arxiv.org/abs/2409.02038>
- **[S40]** Reserved: superseded by the verified Tide and TransXion references [S54][S55].
- **[S41]** *Measuring Privacy Risks and Tradeoffs in Financial Synthetic Data Generation*, 2026: <https://arxiv.org/abs/2602.09288>
- **[S42]** *Leakage-Safe Graph Features for Interpretable Fraud Detection in Temporal Transaction Networks*, 2026: <https://arxiv.org/abs/2603.06632>
- **[S43]** *Data Navigator: Accessible Navigation of Data Visualizations*, 2023: <https://arxiv.org/abs/2308.08475>
- **[S53]** *Finding Connections: Membership Inference Attacks for the Multi-Table Synthetic Data Setting*, 2026: <https://arxiv.org/abs/2602.07126>
- **[S54]** *Tide: A Customisable Dataset Generator for Anti-Money Laundering Research*, 2026: <https://arxiv.org/abs/2603.01863>
- **[S55]** *TransXion: A High-Fidelity Graph Benchmark for Anti-Money Laundering*, 2026: <https://arxiv.org/abs/2604.17420>
- **[S56]** *SynthEval: A Framework for Detailed Utility and Privacy Evaluation of Tabular Synthetic Data*, 2024: <https://arxiv.org/abs/2404.15821>
- **[S59]** *Finding the Right Tables and Columns: A Benchmark and Corpus-Adaptive Embeddings for SQL Schema Retrieval*, 2026: <https://arxiv.org/abs/2607.13311>
- **[S60]** *Realistic Synthetic Financial Transactions for Anti-Money Laundering Models*, 2023: <https://arxiv.org/abs/2306.16424>
- **[S66]** *Counterfactual Methods for Detecting Unfairness in Anti-Money Laundering Algorithms*, 2026: <https://arxiv.org/abs/2607.05101>
- **[S67]** *FERMI: Exploiting Relations for Membership Inference Against Tabular Diffusion Models*, 2026: <https://arxiv.org/abs/2605.11527>


- **[S85]** Databricks, *AI/BI and Genie One release notes 2026* — Genie Conversation API generally available: <https://docs.databricks.com/aws/en/ai-bi/release-notes/2026>
- **[S86]** Databricks, *Agent mode APIs in Genie Agents* — beta status and current naming, updated July 2026: <https://docs.databricks.com/aws/en/genie-agents/api>
- **[S87]** Databricks, *Lakebase is now generally available* and current autoscaling model: <https://docs.databricks.com/aws/en/release-notes/product/2026/january>
- **[S88]** European Commission, *Guidelines on transparency obligations for providers and deployers of AI systems*, 20 July 2026; Article 50 applies from 2 August 2026: <https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems>
- **[S89]** The Update Framework, *Security* — freeze, rollback, mix-and-match, threshold-key, and repository-consistency threats: <https://theupdateframework.io/docs/security/>
- **[S90]** NIST, *Guidelines for Media Sanitization* and cryptographic erase concept: <https://csrc.nist.gov/glossary/term/cryptographic_erase>
- **[S91]** RFC 9421, *HTTP Message Signatures*: <https://www.rfc-editor.org/info/rfc9421/>
- **[S92]** JSON Schema, *Draft 2020-12*: <https://json-schema.org/draft/2020-12>
- **[S93]** RFC 8785, *JSON Canonicalization Scheme (JCS)*: <https://www.rfc-editor.org/info/rfc8785/>
- **[S94]** RFC 9530, *Digest Fields*: <https://www.rfc-editor.org/info/rfc9530/>
- **[S95]** U.S. Consumer Financial Protection Bureau, *Consumer Complaint Database*: <https://www.consumerfinance.gov/data-research/consumer-complaints/>
- **[S96]** European Banking Authority, *Payment services and electronic money* — payment-fraud reporting and analysis: <https://www.eba.europa.eu/regulation-and-policy/payment-services-and-electronic-money>
- **[S97]** U.S. Financial Crimes Enforcement Network, *SAR Stats*: <https://www.fincen.gov/reports/sar-stats>
- **[S98]** U.S. Treasury OFAC, *Sanctions List Service*: <https://ofac.treasury.gov/sanctions-list-service>
- **[S99]** *EntSQL: A Benchmark for Grounding Text-to-SQL in Long-Context Enterprise Knowledge*, 2026: <https://arxiv.org/abs/2606.03363>
- **[S100]** *When Graph Structure Becomes a Liability: A Critical Re-Evaluation of Graph Neural Networks for Bitcoin Fraud Detection under Temporal Distribution Shift*, 2026: <https://arxiv.org/abs/2604.19514>
- **[S101]** *Synthetic Tabular Generators Fail to Preserve Behavioral Dynamics in Fraud Detection*, 2026: <https://arxiv.org/abs/2604.13125>
- **[S102]** *MIDST Challenge at SaTML 2025: Membership Inference over Diffusion-models-based Synthetic Tabular Data*, 2026: <https://arxiv.org/abs/2603.19185>
- **[S103]** *Memory Architectures for Multi-Turn Text-to-SQL: A Benchmark and Empirical Study*, 2026: <https://arxiv.org/abs/2605.26394>
- **[S104]** European Commission, *Code of Practice on Transparency of AI-Generated Content*, July 2026: <https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content>
- **[S105]** W3C, *Web Authentication Level 3 publication history* — Candidate Recommendation Snapshot, 26 May 2026: <https://www.w3.org/standards/history/webauthn-3/>
- **[S106]** PostgreSQL Global Development Group, *PostgreSQL 18.4, 17.10, 16.14, 15.18, and 14.23 Released*, 14 May 2026: <https://www.postgresql.org/about/news/postgresql-184-1710-1614-1518-and-1423-released-3297/>
- **[S107]** React, *Critical Security Vulnerability in React Server Components* — patched 19.2.1 line for affected packages: <https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components>
- **[S108]** Vite, *Vite 8.1 is out!*, 23 June 2026: <https://vite.dev/blog/announcing-vite8-1>
- **[S109]** Python Software Foundation, *Python 3.14.6*, 10 June 2026: <https://www.python.org/downloads/release/python-3146/>


- **[S110]** Databricks, *AI/BI and Genie release notes 2026* — Agent mode generally available 2 July 2026, Conversation API GA, selected result/benchmark APIs Beta, file-upload/history changes, and pay-as-you-go billing from 8 July 2026: <https://docs.databricks.com/aws/en/ai-bi/release-notes/2026>
- **[S111]** Databricks, *Genie Agents concepts* and *Agent mode APIs in Genie Agents* — Agent mode behavior, multi-query execution, data access, and Beta programmatic API status: <https://docs.databricks.com/aws/en/genie-agents/concepts> and <https://docs.databricks.com/aws/en/genie-agents/api>
- **[S112]** PostgreSQL JDBC Project, *PostgreSQL JDBC 42.7.12 Security Release*, 6 July 2026 — CVE-2026-54291 silent channel-binding downgrade: <https://www.postgresql.org/about/news/postgresql-jdbc-42712-security-release-3340/>
- **[S113]** Sigstore, *Rekor v2 GA — Cheaper to run, simpler to maintain*, 10 October 2025 — tile-backed transparency logs, TUF-distributed log configuration, rotation, and bundle verification: <https://blog.sigstore.dev/rekor-v2-ga/>
- **[S114]** Sigstore, *Cosign v3 is now available*, 8 October 2025 — offline-verifiable bundles, trusted-root rotation, and modern transparency-log support: <https://blog.sigstore.dev/cosign-3-0-available/>
- **[S115]** SLSA, *Specification v1.2* — build/source tracks, provenance, and verification requirements: <https://slsa.dev/spec/v1.2/>
- **[S116]** Financial Action Task Force, *Cyber-Enabled Fraud — Digitalisation and Money Laundering, Terrorist Financing and Proliferation Financing Risks*, 24 February 2026: <https://www.fatf-gafi.org/en/publications/Methodsandtrends/cyber-enabled-fraud-digitalisation-ml-tf-pf-risks.html>
- **[S117]** UK Payment Systems Regulator, *APP scams performance data reports* and reimbursement dashboard, latest 2026 publications: <https://www.psr.org.uk/our-work/app-scams/our-app-scams-performance-data-reports/> and <https://www.psr.org.uk/information-for-consumers/app-scams-reimbursement-dashboard/>
- **[S118]** UK Financial Conduct Authority, *Financial Services Register* and data-access information, updated 2026: <https://www.fca.org.uk/firms/financial-services-register> and <https://www.fca.org.uk/firms/financial-services-register/data-extract>
- **[S119]** UK Financial Conduct Authority, *National Storage Mechanism*, updated 21 July 2026 — regulated disclosures and iXBRL/JSON/CSV access: <https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism>
- **[S120]** *PluRel: Synthetic Data unlocks Scaling Laws for Relational Foundation Models*, arXiv v2, 14 July 2026: <https://arxiv.org/abs/2602.04029>
- **[S121]** *Spider 2.0-AIFunc: Extending Real-World Text-to-SQL to AI-Native SQL Workflows*, 7 July 2026: <https://arxiv.org/abs/2607.06229>
- **[S122]** *Do Generative Models Keep Time? A Time-Aware Evaluation of Synthetic Sequential Tabular Data*, 17 July 2026: <https://arxiv.org/abs/2607.15606>
- **[S123]** *Identifiability of Relational Queries in Multi-View Pretraining*, July 2026: <https://arxiv.org/abs/2607.04735>
- **[S124]** *Telco-GAIA: Bilingual Benchmark for Agents in Telecom Domain*, July 2026: <https://arxiv.org/abs/2607.20510>


- **[S125]** Databricks, *Resource limits* — current Genie Agent table/view, instruction, conversation, and message limits, verified 26 July 2026: <https://docs.databricks.com/aws/en/resources/limits>
- **[S126]** Databricks, *Platform release notes* — Genie One and Genie Agents usage free through 31 July 2026 and current July 2026 capability/pricing notices: <https://docs.databricks.com/aws/en/release-notes/product/>
- **[S127]** W3C, *Trusted Types*, Working Draft, 23 June 2026: <https://www.w3.org/TR/trusted-types/>
- **[S128]** W3C, *Content Security Policy Level 3*, current published draft, 5 May 2026: <https://www.w3.org/TR/CSP3/>
- **[S129]** Coalition for Content Provenance and Authenticity, *C2PA Technical Specification 2.4*, April 2026, including `c2pa.ai-disclosure`: <https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html>
- **[S130]** *Verifying Provenance of Digital Media: Why the C2PA Specifications Fall Short*, 2026: <https://arxiv.org/abs/2604.24890>
- **[S131]** *Authenticated Contradictions from Desynchronized Provenance and Watermarking*, 2026: <https://arxiv.org/abs/2603.02378>
- **[S132]** *Flow-A11y: Flow-Aware Accessibility Testing*, 3 July 2026: <https://arxiv.org/abs/2607.03100>
- **[S133]** *DW-Bench: Benchmarking LLMs on Data Warehouse Graph Topology Reasoning*, 2026: <https://arxiv.org/abs/2604.18964>
- **[S134]** NIST, *Privacy Framework 1.1* project and current framework materials: <https://www.nist.gov/privacy-framework> and <https://www.nist.gov/privacy-framework/new-projects/privacy-framework-version-11>
- **[S135]** Financial Action Task Force, *Targeted report on Stablecoins and Unhosted Wallets — Peer-to-Peer Transactions*, 3 March 2026: <https://www.fatf-gafi.org/en/publications/Virtualassets/targeted-report-stablecoins-unhosted-wallets.html>
- **[S136]** European Banking Authority and European Central Bank, current joint payment-fraud reporting and analysis: <https://www.eba.europa.eu/publications-and-media/press-releases/joint-eba-ecb-report-payment-fraud-strong-authentication-remains-effective-fraudsters-are-adapting>


- **[S137]** Railway, *Cron Jobs* — scheduled services start, execute a task, and terminate: <https://docs.railway.com/cron-jobs>
- **[S138]** Railway, *Choose Between Cron Jobs, Background Workers, and Queues*: <https://docs.railway.com/guides/cron-workers-queues>
- **[S139]** Railway, *Private Networking*: <https://docs.railway.com/networking/private-networking>
- **[S140]** NIST, *SP 800-63-4 Digital Identity Guidelines* (final, July 2025) and companion volumes: <https://csrc.nist.gov/pubs/sp/800/63/4/final>
- **[S141]** OWASP, *Large Language Model Security Verification Standard (LLMSVS) 2.0* (2026): <https://owasp.org/www-project-llm-verification-standard/LLMSVS-v2.0-en.html>
- **[S142]** W3C, *Fetch Metadata Request Headers*: <https://www.w3.org/TR/fetch-metadata/>
- **[S143]** WHATWG, *HTML Standard* and *Fetch Standard* — COOP, COEP, CORP, and cross-origin isolation: <https://html.spec.whatwg.org/multipage/browsers.html> and <https://fetch.spec.whatwg.org/>
- **[S144]** European Commission, *Quick Facts: Transparency rules for AI systems* and Article 50 guidance, including the stated December 2026 marking grace for certain pre-existing generative AI systems: <https://digital-strategy.ec.europa.eu/en/factpages/quick-facts-transparency-rules-ai-systems>
- **[S145]** ESMA, *Markets in Crypto-Assets Regulation (MiCA) register* and databases/registers portal: <https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica> and <https://www.esma.europa.eu/publications-and-data/databases-and-registers>
- **[S146]** FinCEN, *SAR Stats* and *Financial Trend Analyses*: <https://www.fincen.gov/reports/sar-stats> and <https://www.fincen.gov/resources/financial-trend-analyses>
- **[S147]** *EntSQL: A Benchmark for Grounding Text-to-SQL in Long-Context Enterprise Knowledge* (2026): <https://arxiv.org/abs/2606.03363>
- **[S148]** *Comparison and Analysis of Value Linking in Text-to-SQL Systems* / VLD-Bench (2026): <https://doi.org/10.1145/3802029>
- **[S149]** *FlexSQL: Flexible Exploration and Execution Make Better Text-to-SQL Agents* (2026): <https://arxiv.org/abs/2605.02815>
- **[S150]** WebAIM, *The WebAIM Million — 2026 report*: <https://webaim.org/projects/million/>
- **[S151]** PostgreSQL Global Development Group, *Transaction Isolation* and *Deadlocks*: <https://www.postgresql.org/docs/current/transaction-iso.html> and <https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS>
- **[S152]** IETF, *RFC 8785 — JSON Canonicalization Scheme (JCS)*: <https://datatracker.ietf.org/doc/html/rfc8785>
- **[S153]** Railway, *Deployment Healthchecks*: <https://docs.railway.com/deployments/healthchecks>

- **[S154]** Databricks, *Use the Genie Agents API* — stateful Conversation APIs, follow-up/history behavior, management APIs, and current prerequisites, verified 26 July 2026: <https://docs.databricks.com/aws/en/genie-agents/conversation-api>
- **[S155]** Databricks, *AI/BI and Genie One release notes 2026* — Conversation API GA, Agent mode/API maturity, file/volume/rich-output changes, and current product behavior, verified 26 July 2026: <https://docs.databricks.com/aws/en/ai-bi/release-notes/2026>
- **[S156]** NIST, *SP 800-218A — Secure Software Development Practices for Generative AI and Dual-Use Foundation Models*: <https://csrc.nist.gov/pubs/sp/800/218/a/final>
- **[S157]** W3C, *Global Privacy Control*, Working Draft, 11 June 2026: <https://www.w3.org/TR/gpc/>
- **[S158]** IETF HTTPAPI Working Group, *The Idempotency-Key HTTP Header Field*, work in progress; revision 07 expired in April 2026 and remains informative rather than a final RFC: <https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/>
- **[S159]** IETF, *RFC 9530 — Digest Fields*: <https://www.rfc-editor.org/rfc/rfc9530>
- **[S160]** IETF, *RFC 9421 — HTTP Message Signatures*: <https://www.rfc-editor.org/rfc/rfc9421>
- **[S161]** Railway, *Choose Between Cron Jobs, Background Workers, and Queues* and *Restart Policy* — long-running worker topology, private networking, restart behavior, and durable-work caveats: <https://docs.railway.com/guides/cron-workers-queues> and <https://docs.railway.com/deployments/restart-policy>
- **[S162]** U.S. Department of the Treasury OFAC, *Sanctions List Service* and API/download information: <https://ofac.treasury.gov/sanctions-list-service>
- **[S163]** European Banking Authority, *Register of payment and electronic money institutions under PSD2*: <https://www.eba.europa.eu/risk-and-data-analysis/data/registers/payment-institutions-register>
- **[S164]** UK Companies House, *Register of Overseas Entities* service and public-register/data information: <https://www.gov.uk/government/organisations/companies-house/about/about-our-services> and <https://www.gov.uk/guidance/companies-house-data-products>
- **[S165]** *RegretBench: A Regret-Based Multi-Turn Benchmark for LLM Clarification Policies under Hidden User Intent*, 23 July 2026: <https://arxiv.org/abs/2607.21143>
- **[S166]** *TSAI-MetaFraud: A Benchmark Dataset for Financial Fraud Transaction and Behavioral Risk Detection in Metaverse Ecosystems*, 10 July 2026: <https://arxiv.org/abs/2607.09528>
- **[S167]** *LakeQuest: A Three-Domain Benchmark for Grounded Data Discovery and Reasoning over Noisy Data Lakes*, July 2026: <https://arxiv.org/abs/2607.12310>
- **[S168]** OWASP, *Dependency-Track 5.0 Is Now Generally Available*, June 2026: <https://owasp.org/blog/2026/06/09/dependency-track-v5>
- **[S169]** OWASP Cheat Sheet Series, *Docker Security Cheat Sheet*: <https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html>
- **[S170]** *SAGA: Synthetic Agentic Graph Architecture for Temporal Graph Generation*, July 2026: <https://arxiv.org/abs/2607.17288>
- **[S171]** *PREF-Gate: Provenance-Constrained Relational Evidence and Validation-Gated Decision Framework for Graph Fraud Detection*, July 2026: <https://arxiv.org/abs/2607.11212>
- **[S172]** CycloneDX, *Specification Overview — current version 1.7*: <https://cyclonedx.org/specification/overview/>
- **[S173]** SPDX, *Specifications — current stable SPDX 3.0; 3.1 release candidate remains preview*: <https://spdx.dev/use/specifications/>
- **[S174]** OpenSSF, *Open Source Project Security Baseline v2026.02.19*: <https://baseline.openssf.org/versions/2026-02-19>
- **[S175]** OpenSSF, *OSPS Baseline project and guidance*: <https://openssf.org/projects/osps-baseline/>
- **[S176]** W3C, *Considerations for Reviewing Differential Privacy Systems*, 12 February 2026: <https://www.w3.org/TR/differential-privacy-guidance/>

- **[S177]** Databricks, *Authorize service principal access to Databricks with OAuth* — OAuth machine-to-machine authentication, service-principal secret limits, and rotation-relevant constraints, verified 26 July 2026: <https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m>
- **[S178]** Databricks, *Manage entitlements* and *Migrate workspace entitlement control* — opt-in, 27 July 2026 auto-enable, 14 September 2026 enforcement, and workspace-local migration behavior: <https://docs.databricks.com/aws/en/security/auth/entitlements> and <https://docs.databricks.com/aws/en/security/auth/system-group-entitlements-migration>
- **[S179]** Databricks, *AI/BI and Genie One release notes 2026* — 15/21 July 2026 free-through-31-July notice and billing correction records that negate earlier billed usage: <https://docs.databricks.com/aws/en/ai-bi/release-notes/2026>
- **[S180]** Databricks, *Audit log system table reference* — regional account audit projection and current Preview status, verified 26 July 2026: <https://docs.databricks.com/aws/en/admin/system-tables/audit-logs>
- **[S181]** Databricks, *Query history system table reference* — regional account query history, sensitive fields, privileges, and current Preview status, verified 26 July 2026: <https://docs.databricks.com/aws/en/admin/system-tables/query-history>
- **[S182]** IETF, *RFC 9700 — Best Current Practice for OAuth 2.0 Security*: <https://www.rfc-editor.org/rfc/rfc9700>
- **[S183]** NIST, *SP 800-57 Part 1 Revision 5 — Recommendation for Key Management: General*: <https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final>
- **[S184]** NIST, *Post-Quantum Cryptography project and migration guidance* — FIPS 203/204/205 and the requirement to inventory and plan replacement of vulnerable cryptography, updated 16 June 2026: <https://csrc.nist.gov/projects/post-quantum-cryptography>
- **[S185]** NIST, *SP 800-61 Revision 3 — Incident Response Recommendations and Considerations for Cybersecurity Risk Management*, final April 2025: <https://csrc.nist.gov/pubs/sp/800/61/r3/final>
- **[S186]** OWASP Cheat Sheet Series, *Logging Cheat Sheet* — security-event coverage, integrity, access, retention, and log-injection protections: <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- **[S187]** OWASP Web Security Testing Guide, *Testing for CSV Injection*: <https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/15-Testing_for_CSV_Injection>
- **[S188]** OWASP Cheat Sheet Series, *File Upload Cheat Sheet*: <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- **[S189]** U.S. CISA, *Known Exploited Vulnerabilities Catalog*: <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- **[S190]** FIRST, *Exploit Prediction Scoring System (EPSS)*: <https://www.first.org/epss/>
- **[S191]** FIRST, *Common Vulnerability Scoring System v4.0*: <https://www.first.org/cvss/v4.0/>
- **[S192]** W3C, *Accessibility Conformance Testing (ACT) Rules Format 1.1*, 5 February 2026: <https://www.w3.org/TR/act-rules-format-1.1/>
- **[S193]** W3C, *Making Content Usable for People with Cognitive and Learning Disabilities*: <https://www.w3.org/TR/coga-usable/>
- **[S194]** W3C WAI, *Understanding Success Criterion 3.3.8: Accessible Authentication (Minimum)* and CAPTCHA accessibility guidance: <https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html> and <https://www.w3.org/TR/turingtest/>
- **[S195]** W3C, *String-Meta — String on the Web: Language and Direction Metadata*, 16 July 2026: <https://www.w3.org/TR/string-meta/>
- **[S196]** PostgreSQL Global Development Group, *Continuous Archiving and Point-in-Time Recovery*, *Warm Standby*, and *Transaction Isolation* in the current PostgreSQL 18 documentation: <https://www.postgresql.org/docs/current/continuous-archiving.html>, <https://www.postgresql.org/docs/current/warm-standby.html>, and <https://www.postgresql.org/docs/current/transaction-iso.html>
- **[S197]** U.S. FDIC, *Open Data at the FDIC*, *BankFind Suite*, and *Bank Data Guide* — current and historical insured-institution, branch, structure, and financial-data interfaces: <https://www.fdic.gov/about/open-data-fdic>, <https://banks.data.fdic.gov/bankfind-suite/>, and <https://www.fdic.gov/bank-data-guide>
- **[S198]** UK Financial Conduct Authority, *Warning List of unauthorised firms* and Financial Services Register access information, updated 30 June 2026: <https://www.fca.org.uk/consumers/warning-list-unauthorised-firms> and <https://www.fca.org.uk/firms/financial-services-register>
- **[S199]** IOSCO, *International Securities & Commodities Alerts Network (I-SCAN)* — member-regulator alerts about potentially unauthorized offerings: <https://www.iosco.org/i-scan/>
- **[S200]** UK Companies House, *Disqualified Directors register* and Public Data API officer-disqualification resources: <https://www.gov.uk/search-the-register-of-disqualified-company-directors> and <https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/officer-disqualifications>
- **[S201]** *SQaLe: A Large Text-to-SQL Corpus Grounded in Real Schemas*, arXiv:2602.22223 — 135,875 relational schemas and 517,676 question/schema/query triples: <https://arxiv.org/abs/2602.22223>
- **[S202]** *SynQuE: Estimating Synthetic Dataset Quality Without Annotations*, arXiv:2511.03928 v5, 30 April 2026: <https://arxiv.org/abs/2511.03928>
- **[S203]** *FRAUDGUESS: Spotting and Explaining New Types of Fraud in Million-Scale Financial Data*, arXiv:2509.15493: <https://arxiv.org/abs/2509.15493>
- **[S204]** *FiFAR: A Fraud Detection Dataset for Learning to Defer*, arXiv:2312.13218 — synthetic analyst predictions and capacity-aware human/AI allocation scenarios: <https://arxiv.org/abs/2312.13218>

### Source-use rule

A citation does **not** authorize ingestion, redistribution, commercial use, trademark use, public accusation, or publication. Every actual source, model, dependency, provider, or asset must pass the current license, terms, attribution, privacy, security, data-residency, provenance, and dual-use gates. Dated platform facts are revalidated at release freeze and before any provider or dependency upgrade.
