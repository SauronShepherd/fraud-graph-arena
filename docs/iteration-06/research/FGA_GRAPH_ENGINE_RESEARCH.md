# FGA Graph Engine Research Dossier

**Working language:** English
**Project:** Fraud Graph Arena
**Iteration:** FGA 06 — graph-engine research and design
**Status:** Living research document; not a final architecture or implementation claim
**Started:** 2026-11-07
**Scope owner:** FGA engineering/design investigation

> **Hercule Perrot's working principle:** A graph library is not merely a dependency. The moment it enters the application, it becomes part of the application's behaviour, lifecycle, risk profile, maintenance burden and future. FGA must decide which ideas it is willing to own.

## 0. Executive reframe

FGA 06 no longer treats graph libraries as contestants in a benchmark. The research question is:

> **Which ideas, mechanisms and product decisions from the graph-visualisation field are worth understanding, adapting, rejecting or reinventing when FGA builds its own game-specific visual graph engine?**

Existing libraries and products are reference implementations, research material and usability evidence. They are not automatically runtime dependencies, finalists or winners. A commercial product can be valuable as a design reference even when its code and distribution terms are unavailable to FGA.

The existing four-engine qualification lab is retained as an experimental instrument. Its lifecycle/selection measurements are evidence about the lab adapters and candidate implementations, not a decision procedure for the final FGA engine.

## 1. Research rules

### 1.1 Evidence status

Every important statement in this dossier must carry one of these statuses:

- **Observed:** directly verified in source, documentation, a running demo, a local experiment or a clearly identified discussion.
- **Measured:** produced by a reproducible FGA experiment with fixture, environment and method recorded.
- **Reported:** attributed to a paper, maintainer, user or source with a link and date.
- **Inferred:** a reasoned engineering interpretation; never presented as a library fact.
- **Proposed:** an FGA design idea awaiting a prototype or test.
- **Rejected:** considered and discarded with a reason and the condition that could reopen it.
- **Unknown:** important but not yet investigated.

### 1.2 What we may study

We may inspect public documentation, public source repositories, public demos, public APIs, public issue discussions, academic papers, standards and observable product behaviour. We may implement independent ideas and clean-room designs.

We do not copy proprietary code, private implementation details, vendor assets, non-redistributable evaluation packages, trademarks, or documentation text beyond lawful quotation limits. Source-available and commercial products are reference material unless their terms explicitly permit redistribution and modification.

### 1.3 Research is not popularity polling

Stars, downloads, a busy issue tracker and a polished demo are signals, not architecture decisions. Community health, maintenance, release cadence, security history, accessibility maturity and user complaints are recorded as evidence with a date and scope. Missing evidence remains missing.

### 1.4 FGA-specific invariants

The engine must remain a projection and interaction surface, never the authority for:

- evidence existence or visibility;
- protected truth;
- record/entity identity beyond stable FGA identifiers;
- relationship direction or evidentiary meaning;
- culpability, guilt or suspicion;
- credits, investigation commands or server-authoritative game consequences.

## 2. Research questions

1. What is the smallest useful graph kernel for FGA?
2. Which graph data structures make identity, direction, provenance and updates explicit?
3. Which rendering architecture gives FGA strong semantics without locking the product to one backend?
4. How should nodes move while preserving a stable investigation mental map?
5. How should context menus expose safe actions without becoming investigation commands?
6. What is the best combination of SVG, Canvas, WebGL, WebGPU, DOM and worker execution for FGA's graph sizes?
7. How can a visual graph have a first-class semantic and keyboard-accessible equivalent?
8. How can every feature be tested autonomously, deterministically and without a human reopening cases?
9. Which ideas from diagramming tools, network analysis, scientific visualisation, games and commercial products generalise to FGA?
10. Which apparently impressive features create more maintenance, ambiguity or cognitive load than value?
11. How should the engine expose observability, replay and failure diagnostics?
12. Which novel ideas should FGA prototype rather than inherit?

## 3. Research method and passes

The research proceeds in complete passes. Each pass revisits the current dossier, adds evidence, challenges earlier assumptions and records what changed.

| Pass | Perspective | Status | Output |
|---:|---|---|---|
| 0 | Scope, evidence rules and local baseline | complete | This dossier and research ledger |
| 1 | Graph models and data structures | in progress | Core-model findings |
| 2 | Rendering pipelines and backends | pending | Renderer architecture findings |
| 3 | Layouts, routing and mental-map stability | pending | Layout design findings |
| 4 | Interaction, movement and context menus | pending | Interaction contract |
| 5 | Accessibility and semantic fallback | pending | Dual-channel UX contract |
| 6 | Autonomous testing and replayability | pending | Test architecture |
| 7 | Performance, workers, GPU and large graphs | pending | Performance strategy |
| 8 | Commercial/product references and user feedback | pending | Product-pattern ledger |
| 9 | Maintenance, security, licensing and exit strategy | pending | Dependency/ownership policy |
| 10 | Synthesis, contradiction review and prototype selection | pending | Proposed engine architecture |

The pass counter is not a claim of completion. A pass is clean only when the current dossier has no justified correction or concrete missing investigation within that perspective.

## 4. Current local baseline

### Observed in the FGA 06 checkout

- Branch: `FGA-06`.
- A renderer-neutral `CandidateInstance` contract already separates FGA IDs and callbacks from renderer-native objects.
- The qualification lab currently exercises Cytoscape.js, Sigma.js, D3 and React Flow through a shared 18-node/26-relationship fixture.
- The lab has a persistent inspector, visual state legend, filters, minimap, fit/zoom/reset controls and contextual node/relationship menus.
- The branch includes automatic lifecycle, resize, node-selection and relationship-selection probes.
- The current production graph path contains a player-safe `ACADEMY_T02` projection and preserves the intentionally empty `ACADEMY_001` regression case.
- Existing evidence records a live `fga` Databricks sandbox qualification for the canonical persistence path, while predecessor formal closure and non-admin security evidence remain separate concerns.

### Interpretation

FGA already has a useful experimental seam. The research should build on it rather than replace it with a library-specific API. The next architectural artifact is not a fifth benchmark adapter; it is an independently specified FGA engine contract plus prototypes that test its ideas.

## 5. Longlist and taxonomy

The longlist is intentionally broader than JavaScript. Candidates will be classified before deep inspection so that graph libraries, diagram editors, layout engines, data models, GPU renderers and complete applications are not compared as if they solved the same problem.

| Family | Representative references to investigate | Research question |
|---|---|---|
| Network-first visualisation | Cytoscape.js, Sigma.js, vis-network, VivaGraph, Helios | What does a network viewer make easy, and which semantics remain application-owned? |
| Visual primitives | D3, SVG, Canvas 2D, WebGL, WebGPU, PixiJS, Three.js | How much control and performance can FGA own directly? |
| Diagram/editor frameworks | React Flow, GoJS, yFiles, JointJS/Rappid, mxGraph/draw.io | Which interaction, routing, editing and overview patterns are worth borrowing? |
| Layout and routing | d3-force, ELK, Graphviz, MSAGL.js, Dagre, Cola.js | Which algorithms and constraints support readable investigations? |
| Graph data and algorithms | Graphology, NetworkX, igraph, graph-tool, JGraphT, Boost Graph Library | Which core representations, traversals and analysis boundaries are useful? |
| Scientific/network applications | Cytoscape Desktop/Web, Gephi, Tulip, Graphistry, Neo4j Bloom | What do serious analysts need beyond drawing nodes and edges? |
| Large-scale/browser research | WebGPU/WebGL graph renderers, WASM graph stores, GPU layout papers | When should FGA use workers, GPU buffers, tiling or progressive disclosure? |
| Accessibility/semantic visualisation | W3C graphics guidance, accessible SVG/HTML patterns, keyboard graph prototypes | How can the visual and semantic investigation paths stay equivalent? |

The longlist is a research queue, not a dependency list. A reference can be investigated deeply and still be rejected for FGA.

## 6. Per-reference dossier template

Every deep dive will use the same structure:

1. Identity, version/date and project scope.
2. Primary source links and source quality.
3. Intended problem and users.
4. Graph/data model.
5. Rendering pipeline and coordinate model.
6. Layout and routing model.
7. Interaction/event model.
8. Node movement, selection and context-menu affordances.
9. Styling, labels, semantic zoom and grouping.
10. Minimap/overview and focus/context techniques.
11. Accessibility and non-visual path.
12. Lifecycle, updates, cleanup and failure modes.
13. Testability, determinism and replayability.
14. Performance architecture and scaling assumptions.
15. Extensibility and integration boundaries.
16. Maintenance/community/security signals.
17. Licence and provenance constraints.
18. Strengths worth borrowing.
19. Weaknesses and complaints to avoid.
20. FGA fit, proposed experiments and open questions.

## 7. Initial hypotheses to challenge

These are hypotheses, not decisions:

- FGA should own a graph kernel and interaction model, but should initially avoid owning every layout algorithm.
- SVG is likely the strongest semantic/reference backend for small and medium investigation scenes.
- Canvas/WebGL/WebGPU should be optional backends selected by measured scene complexity, not by prestige.
- Node movement should be user-controlled but deterministic, replayable and separable from authoritative evidence state.
- Context menus should expose inspect/focus/layout/display actions; investigation consequences must remain outside the renderer.
- A semantic HTML mirror should be generated from the same graph state, not maintained as a second hand-written model.
- The engine should expose a command/event log so interaction can be replayed in tests and bug reports.
- Layout stability may matter more than peak frame rate for an investigation UI.
- “More features” is not automatically better; every feature needs a cognitive, semantic and maintenance justification.

## 8. Proposed engine boundaries — early draft

```text
authoritative workspace projection
            |
            v
FGA Graph Contract / safe graph snapshot
            |
            v
FGA Graph Core
  identity, relationships, indexes, selection, commands, replay
            |
     +------+-------+----------------+
     |              |                |
     v              v                v
layout engine   interaction      semantic mirror
     |              |                |
     +------+-------+----------------+
            v
      viewport/camera
            |
     +------+------+------+
     |             |      |
     v             v      v
    SVG         Canvas   WebGL/WebGPU
```

Renderer backends must consume immutable or versioned view snapshots and emit FGA-owned events. Renderer objects must never become domain state.

## 9. Autonomous testability as a first-class feature

The engine is not research-complete until every important behaviour can be exercised without a human pointing at a canvas. The test design must include:

- deterministic fixture loading and content hashes;
- deterministic layout seeds and a replayable movement log;
- stable node/edge IDs in all events;
- programmatic context-menu open/close and action selection;
- keyboard access to the same inspection path;
- semantic mirror assertions for every visual fact;
- viewport commands: fit, zoom, pan, resize and focus;
- node movement constraints and undo/redo where supported;
- renderer mount/update/unmount and listener cleanup;
- failure injection for renderer, layout worker and asset loading;
- screenshot and structural visual regression with tolerance policy;
- performance traces separated into data, layout, render and interaction phases;
- fuzzing/property tests for graph mutations, duplicate IDs, missing endpoints and cycles;
- record/replay of user interaction sequences;
- browser matrix tests for reduced motion, forced colours, high zoom and narrow layouts.

The test harness must expose readiness and state seams instead of relying on arbitrary sleeps or pixel coordinates.

## 10. Research ledger

| ID | Date | Topic | Finding | Status | Decision/next action |
|---|---|---|---|---|---|
| R-000 | 2026-11-07 | Research scope | The work is a design research program for an FGA-specific engine, not a library benchmark. | accepted | Keep benchmark artefacts as experimental evidence only. |
| R-001 | 2026-11-07 | FGA local baseline | The existing adapter contract and lab provide a reusable experimental boundary. | observed | Preserve the boundary; add engine research beside it. |
| R-002 | 2026-11-07 | Autonomous qualification | A graph engine must expose deterministic state and event seams so tests do not need canvas pointing. | proposed | Validate against all future prototypes. |

## 11. Open questions

- Which graph sizes and update rates define FGA's real qualified envelope?
- Should node movement persist per case/session, per investigation view or only as a replayable presentation preference?
- Which context-menu actions are purely presentational and which must cross into workspace commands?
- How should edge labels, parallel edges, self-loops and edge crossings behave in the semantic mirror?
- Can a single layout model serve SVG and GPU backends without leaking renderer assumptions?
- Which worker/message protocol gives deterministic layout without making debugging painful?
- What accessibility semantics are available for a graph that is larger than a useful tab sequence?
- What visual regressions should be judged by structure rather than screenshots?
- Which novel features improve investigation clarity rather than merely making the demo impressive?

## 12. Pass log

| Pass | Perspective | Findings/corrections | Clean? |
|---:|---|---|---|
| 0 | Scope and baseline | Created the living dossier; separated research from benchmark and recorded local invariants. | pending later regression |

## 13. Sources

This section will grow with the research. Sources must be linked at the finding where they are used, with access date where volatility matters.

## 14. Research pass 1 — graph readability, change and navigation

### 14.1 Stable positions are an investigation feature, not decoration

Research on dynamic graph visualisation repeatedly treats drawing stability, or preservation of the user's mental map, as a task variable. Studies report that stability helps with revisiting locations, following paths and tracking nodes as the graph changes. Animation can help when stability is low, but it is not a universal substitute for stable placement.

**FGA consequence:** node movement must be an explicit, deterministic policy. The engine should prefer preserving anchors and relative positions when data changes, expose the reason for a movement, and make transitions interruptible and testable. A force simulation that produces a visually attractive but constantly moving scene is not an acceptable default for an investigation.

Sources:

- [Can animation support the visualisation of dynamic graphs?](https://doi.org/10.1016/j.ins.2015.04.017) — reports that animation can reduce errors for low-stability drawings, while the broader problem remains the stability of the drawing and the user's mental map.
- [Evaluation of two interaction techniques for visualization of dynamic graphs](https://doi.org/10.48550/arXiv.1608.08936) — reports improved accuracy from layout stability and adjacent highlighting, sometimes at a time cost.
- [Survey of the intersection of mental maps and visualization](https://link.springer.com/article/10.1186/s42492-026-00225-1) — recent survey framing stability as a consistency mechanism for time-varying graph layouts.
- [GraphDiaries: Animated Transitions and Temporal Navigation for Dynamic Networks](https://doi.org/10.1109/TVCG.2013.254) — task-oriented temporal navigation and animated transitions for dynamic networks.

**Adopt:** stable anchors, deterministic seeds, explicit movement reasons, transition cancellation, replayable movement events.
**Reject:** unbounded force simulation as the default source of truth for positions.
**Open experiment:** compare anchored incremental layout, stable force relaxation and a user-pinned layout on FGA's case-update scenarios.

### 14.2 Node-link diagrams are not always the best representation

A classic comparison found that matrix-based representations can outperform node-link diagrams for many tasks once graphs exceed roughly twenty vertices, while node-link diagrams remain strong for path finding. That result does not mean FGA should replace its graph; it means the engine should be able to expose a complementary adjacency/evidence view when density makes links ambiguous.

**FGA consequence:** the engine's semantic model must not assume that one visual representation is sufficient. A future dense-cluster view could offer a relationship matrix, a ranked adjacency list or a path-focused view generated from the same graph snapshot. This is a representation strategy, not a new source of truth.

Source: [A Comparison of the Readability of Graphs Using Node-Link and Matrix-Based Representations](https://doi.org/10.1109/INFVIS.2004.1).

**Adopt:** representation switching by task and density.
**Reject:** treating a node-link canvas as the only way to inspect evidence.
**Open experiment:** define a density threshold from task performance and test node-link, adjacency matrix and path view on the same FGA fixture.

### 14.3 Focus+context and semantic zoom deserve a controlled prototype

Fisheye and semantic-zoom research explores keeping local detail while preserving surrounding context. The benefit depends on the task, the distortion model and the user's ability to understand the transformation. A graph engine should not add a fisheye effect merely because it looks sophisticated.

**FGA consequence:** focus+context should be a task-specific mode with a reversible state, a visible focus anchor and deterministic geometry. Semantic zoom should change what is displayed—labels, metadata, relationship detail and grouping—not only scale pixels.

Sources:

- [Evaluation of Semantic Fisheye Zooming to Provide Focus+Context](https://doi.org/10.1177/154193120705100507).
- [Structure-aware Fisheye Views for Graph Visualization](https://visvar.github.io/assets/pdf/wang2019fisheye.pdf).

**Adopt:** reversible focus, context preservation, semantic level-of-detail.
**Reject:** invisible distortion or a mode that makes stable IDs and edge direction harder to follow.
**Open experiment:** prototype focus on a selected node with nearby detail, muted far context and an inspector explanation of the current level of detail.

### 14.4 Edge crossings and crossing angles are functional concerns

Graph-drawing research treats edge crossings, crossing angles, edge lengths and symmetry as readability factors. Crossing minimisation alone is not enough: an algorithm can reduce crossings while destroying clusters, direction or the user's mental map.

**FGA consequence:** layout quality must be multi-objective. The engine should calculate diagnostics such as crossing count, shallow crossing angles, label collisions, long-edge outliers, disconnected visual components and movement from the previous layout. These diagnostics support development and automated regression; they are not a universal visual-quality score.

Source: [Larger crossing angles make graphs easier to read](https://doi.org/10.1016/j.jvlc.2014.05.001).

**Adopt:** diagnostic layout metrics and task-specific quality envelopes.
**Reject:** a single aesthetic score treated as human readability.
**Open experiment:** generate FGA layouts with different crossing-angle and cluster-preservation weights and compare structural metrics with task-oriented review.

## 15. Research pass 2 — accessibility as a graph traversal system

### 15.1 A table is not enough semantic access

Recent accessibility research argues that a basic text alternative or raw data table does not reproduce the interactive exploration affordances of a visualisation. Data Navigator proposes navigable structures for lists, trees, graphs and flows across screen reader, keyboard and other modalities. TADA explores searching, filtering and navigating between nodes in node-link diagrams. Benthic proposes a perceptually congruent traversal structure using relational groupings rather than forcing every graphic into a simple tree.

**FGA consequence:** the semantic channel should be a first-class graph traversal interface, not a hidden fallback table. It should support:

- search and direct focus by stable ID or label;
- next/previous node and relationship traversal;
- incoming/outgoing neighbours;
- relationship type, family, direction and safe provenance;
- current focus, selected state and context;
- filtering and reversible return to the prior location;
- equivalent context-menu actions;
- a concise overview followed by detail-on-demand.

Sources:

- [Data Navigator: An Accessibility-Centered Data Navigation Toolkit](https://doi.org/10.1109/TVCG.2023.3327393).
- [TADA: Making Node-link Diagrams Accessible to Blind and Low-Vision People](https://doi.org/10.1145/3613904.3642222).
- [Benthic: Perceptually Congruent Structures for Accessible Charts and Diagrams](https://vis.csail.mit.edu/pubs/benthic/).
- [Rich Screen Reader Experiences for Accessible Data Visualization](https://vis.csail.mit.edu/pubs/rich-screen-reader-vis-experiences/).
- [WAI-ARIA overview and SVG accessibility mappings](https://www.w3.org/WAI/standards-guidelines/aria/).
- [W3C SVG accessibility support](https://www.w3.org/TR/SVG/access).

**Adopt:** one shared graph state producing visual and semantic projections; relational traversal; goal-directed navigation; reversible focus.
**Reject:** a visual canvas with an unrelated afterthought table; hover-only essential evidence; a keyboard path that exposes labels but not relationships.
**Open experiment:** implement a semantic traversal panel against the existing 18-node/26-relationship fixture and assert parity with the visual inspector.

### 15.2 Canvas and GPU rendering require an intentional alternative

Canvas and WebGL do not expose a useful DOM graph automatically. W3C guidance describes SVG focus, keyboard events and ARIA support, while practical accessibility guidance warns that interactive canvas needs focusable fallback content and keyboard-equivalent behaviour.

**FGA consequence:** the engine must not promise that every GPU primitive becomes a focusable DOM element. It must promise that every investigation-critical operation has a stable, testable semantic path. The semantic mirror should remain available when the renderer is unavailable, degraded, hidden, zoomed or inaccessible.

Source: [Canvas focusable fallback guidance](https://www.ssa.gov/accessibility/andi/help/alerts.html).

## 16. Research pass 3 — library feedback as design evidence

User and maintainer discussions are not controlled studies, but they reveal failure modes that polished feature pages omit. Each report below is treated as a design prompt, not as proof that the whole library is defective.

### 16.1 Sigma: label and picking pipelines need budgets

Recent Sigma discussions and issues describe label-buffer rebuild costs during animation, GPU picking via synchronous `readPixels` during pointer movement, edge-event settings, label direction problems and WebGL-context cleanup. The project has also responded with fixes and redesign work, which is itself evidence that these concerns are real engineering dimensions rather than hypothetical objections.

Sources:

- [Label buffer rebuilt every frame during animation](https://github.com/jacomyal/sigma.js/issues/1553).
- [Sigma issues and recent bug reports](https://github.com/jacomyal/sigma.js/issues).
- [GPU picking and pointer-move stalls](https://github.com/jacomyal/sigma.js/issues/1546).
- [Sigma changelog: cleanup, events and rendering changes](https://github.com/jacomyal/sigma.js/blob/main/CHANGELOG.md).
- [Sigma settings including edge-event controls](https://github.com/jacomyal/sigma.js/blob/main/packages/sigma/src/settings.ts).

**FGA ideas:** dirty flags for labels and geometry; separate animation uniforms from static buffers; hover throttling or hover suspension during camera movement; explicit picking budgets; asynchronous or deferred hit testing; context ownership diagnostics; a hard destroy contract.

### 16.2 Cytoscape: labels, GPU memory, batch updates and migration matter

Cytoscape's public performance redesign discussion identifies label cost, GPU memory limits, readback stalls, dynamic update rebuilding, floating-point reproducibility and custom-format isolation as architectural concerns. The public issue tracker also shows that mature libraries still accumulate browser, font, input and rendering edge cases.

Sources:

- [Cytoscape.js performance redesign discussion](https://github.com/cytoscape/cytoscape.js/issues/3486).
- [Cytoscape.js issue tracker](https://github.com/cytoscape/cytoscape.js/issues).
- [Cytoscape.js factsheet and architecture](https://js.cytoscape.org/).

**FGA ideas:** mutation batches, tombstones plus controlled compaction, explicit label budgets, compact transferable buffers, deterministic CPU/worker fallback, open interchange schema and diagnostics that explain when the engine changes rendering strategy.

### 16.3 React Flow: application state can become the bottleneck

A React Flow discussion describes a common performance trap: rebuilding all node and edge state to style neighbours after a click. The maintainer response points toward derived styles, built-in selected classes and avoiding unnecessary full-array updates.

Source: [React Flow performance discussion for large graphs](https://github.com/xyflow/xyflow/discussions/4975).

**FGA ideas:** immutable graph data separated from transient view state; selection as a small indexed set; derived highlighting; subscription granularity; no requirement to re-render every node for a local selection.

### 16.4 Feedback is a source of tests

Each recurring complaint should become a regression scenario:

| Failure signal | FGA regression |
|---|---|
| label work repeats on animation | static label buffers remain unchanged across uniform-only animation |
| pointer picking stalls | hover latency is bounded while panning and dense pointer motion is active |
| WebGL context is not cleaned | mount/destroy leaves no renderer, listener or context leak |
| full-array React updates lag | selecting one node updates only derived affected state |
| labels mirror or disappear | directed edge label orientation has fixture-based assertions |
| dynamic updates destroy the mental map | unchanged nodes remain within the stability envelope |

## 17. Initial synthesis from the completed passes

The strongest early design direction is a **semantic, deterministic, multi-backend graph engine** with these principles:

1. **One graph state, multiple projections.** Visual, semantic, minimap and inspector views derive from the same versioned snapshot.
2. **Stable identity everywhere.** FGA node and relationship IDs are the only identity that crosses boundaries.
3. **Layouts are planners, not authorities.** Layout output is a versioned presentation result with seeds, constraints, diagnostics and replay.
4. **Movement is a product feature.** Pinned nodes, anchors, transition policy and mental-map preservation are explicit.
5. **Labels are a budgeted subsystem.** Label decisions, caches and updates are observable and independently testable.
6. **Picking is policy-driven.** Node and edge hit testing can use DOM, spatial indexes, CPU geometry, GPU picking or a hybrid without changing FGA events.
7. **The semantic mirror is first-class.** It is not only for screen readers; it is also a deterministic test oracle and renderer failure path.
8. **Interaction is replayable.** Commands and events can be recorded, serialized and replayed without a browser pointer.
9. **Rendering backends are optional.** SVG is the reference/semantic backend; Canvas/WebGL/WebGPU are progressive backends, not separate products.
10. **Density changes representation.** Node-link, adjacency, path and cluster views may be different projections of the same graph.
11. **Diagnostics are part of the engine.** The engine reports layout quality, dropped frames, label budgets, picking cost, memory/context state and fallback transitions.
12. **The engine can fail gracefully.** A renderer failure cannot erase safe graph evidence or selection.

## 18. Novel FGA design proposals

These are original FGA proposals, not claims that any reference library implements them:

### 18.1 Evidence-aware semantic zoom

At each zoom level, the engine declares which information is visible, hidden, grouped or deferred. The decision is based on graph role, relationship importance and task context, not only pixel size. The semantic mirror exposes the same level-of-detail decision in text.

### 18.2 Layout replay and movement provenance

Every layout change records its input graph version, seed, constraints, user pins, algorithm and reason. A bug report can replay the exact movement sequence. This also lets tests assert that an unchanged node did not move without justification.

### 18.3 Context-menu capability tokens

The graph engine receives a safe set of presentational capabilities from FGA. A context menu renders only those capabilities and emits typed intents. It cannot invent investigation actions, spend credits or call a provider. The UI can therefore be rich without giving the renderer authority.

### 18.4 Dual-oracle testing

Every visual interaction is tested against two oracles: the emitted FGA event/state and the semantic mirror. Screenshots remain useful for appearance, but they are not the only proof of correctness.

### 18.5 Representation negotiation

The engine chooses or recommends node-link, matrix, path, cluster or table projections based on density, task and viewport. The recommendation is explainable and reversible. The user can always return to the primary graph view.

### 18.6 Interaction flight recorder

The engine records a privacy-safe sequence of graph commands, state hashes, layout versions, renderer transitions and errors. A failing investigation scene can be replayed locally without shipping protected truth.

## 19. Current decisions and non-decisions

### Adopted direction

- Research first; no renderer winner.
- FGA owns the semantic contract, graph state, interaction intents, accessibility path and test seams.
- Reference libraries may inform independent designs without becoming dependencies.
- Commercial products may be studied as products; their code and restricted assets are not implementation inputs.
- Existing benchmark evidence remains useful for adapter experiments and regression, not for selecting the engine.

### Not decided

- SVG, Canvas, WebGL or WebGPU as the first production backend.
- Whether the first layout engine is fully custom or wraps an independently licensed algorithm package.
- Exact density thresholds for representation negotiation.
- The persistence scope of user node movement.
- Whether animation or small multiples should represent temporal graph changes in FGA.
- The final graph-core data structure and worker protocol.

## 20. Next research queue

1. Inspect Graphology, NetworkX, igraph, graph-tool, JGraphT and Boost Graph Library data-model choices.
2. Inspect Graphviz, ELK, MSAGL.js, Dagre, Cola.js and constrained-layout research.
3. Deep-dive render pipelines in Cytoscape.js, Sigma.js, D3, vis-network, Helios and MSAGL.js.
4. Study yFiles, GoJS, JointJS/Rappid and Neo4j Bloom as product/UX references, without treating commercial code as reusable.
5. Investigate WebGPU/WASM graph stores and worker-friendly layout protocols.
6. Build local micro-experiments for stable layout, semantic traversal, dirty labels, picking policies and interaction replay.
7. Add a per-reference complaint ledger from issue trackers, forums and migration discussions.
8. Revisit the FGA architecture after the prototypes, not before.

## 21. Updated pass log

| Pass | Perspective | Findings/corrections | Clean? |
|---:|---|---|---|
| 0 | Scope and baseline | Created the living dossier; separated research from benchmark and recorded local invariants. | pending later regression |
| 1 | Readability, dynamic change, accessibility and user feedback | Added mental-map stability, representation switching, semantic traversal, accessibility research, issue-derived failure modes and initial synthesis. | pending contradiction review |

## 22. Sources added in pass 1

- [Can animation support the visualisation of dynamic graphs?](https://doi.org/10.1016/j.ins.2015.04.017)
- [Evaluation of two interaction techniques for visualization of dynamic graphs](https://doi.org/10.48550/arXiv.1608.08936)
- [Survey of the intersection of mental maps and visualization](https://link.springer.com/article/10.1186/s42492-026-00225-1)
- [GraphDiaries](https://doi.org/10.1109/TVCG.2013.254)
- [A Comparison of the Readability of Graphs Using Node-Link and Matrix-Based Representations](https://doi.org/10.1109/INFVIS.2004.1)
- [Evaluation of Semantic Fisheye Zooming](https://doi.org/10.1177/154193120705100507)
- [Structure-aware Fisheye Views](https://visvar.github.io/assets/pdf/wang2019fisheye.pdf)
- [Larger crossing angles make graphs easier to read](https://doi.org/10.1016/j.jvlc.2014.05.001)
- [Data Navigator](https://doi.org/10.1109/TVCG.2023.3327393)
- [TADA](https://doi.org/10.1145/3613904.3642222)
- [Benthic](https://vis.csail.mit.edu/pubs/benthic/)
- [Rich Screen Reader Experiences for Accessible Data Visualization](https://vis.csail.mit.edu/pubs/rich-screen-reader-vis-experiences/)
- [WAI-ARIA overview](https://www.w3.org/WAI/standards-guidelines/aria/)
- [W3C SVG accessibility](https://www.w3.org/TR/SVG/access)
- [Sigma label buffer issue](https://github.com/jacomyal/sigma.js/issues/1553)
- [Sigma picking issue](https://github.com/jacomyal/sigma.js/issues/1546)
- [Sigma changelog](https://github.com/jacomyal/sigma.js/blob/main/CHANGELOG.md)
- [Cytoscape performance redesign](https://github.com/cytoscape/cytoscape.js/issues/3486)
- [React Flow performance discussion](https://github.com/xyflow/xyflow/discussions/4975)

## 23. Research pass 4 — graph data models and algorithm boundaries

This pass asks a narrower question than “which graph library is best?”: which abstractions should survive if FGA owns the engine and every renderer is replaceable?

### 23.1 Graphology: a useful browser-shaped reference, not the FGA contract

Graphology deliberately unifies directed, undirected, mixed, simple, self-loop and parallel-edge graphs behind one JavaScript/TypeScript interface. It also exposes events and a standard library of algorithms, layouts, traversals and generators. Sigma.js uses it as its data backend.

What is attractive:

- one graph object can express more than one relationship model;
- mutation events are immediately useful for renderer invalidation;
- algorithms and renderers can be separate packages;
- the documentation explicitly acknowledges that a specialized implementation may replace the core while preserving the standard-library idea.

What does not transfer directly:

- a mutable object with many convenience methods is not automatically a safe snapshot boundary;
- renderer-facing events are not the same thing as FGA domain events;
- a generic attribute bag must not be allowed to carry authoritative fraud evidence or silently change its meaning;
- the standard bundle may lag behind the package versions, which is a reminder to pin and verify every algorithm dependency.

Decision: borrow the unified graph vocabulary and event discipline, but put a versioned `GraphSnapshot` and a typed FGA projection boundary in front of it. The engine may use a Graphology-compatible adapter during experimentation; Graphology is not the public FGA domain model.

Source: [Graphology documentation](https://graphology.github.io/).

### 23.2 NetworkX: views are a powerful answer to filtering

NetworkX exposes distinct graph classes for directed, undirected and parallel-edge graphs and offers live, read-only graph views for subgraphs, reversal and filtering. Its documentation explicitly warns that view chains can become slow and that writable attribute dictionaries can mutate the underlying graph.

The transferable idea is not the Python implementation. It is the distinction between:

1. the authoritative graph;
2. a cheap, inspectable view;
3. a materialized snapshot when stable iteration or serialization is required.

FGA consequence: filters should normally create a `GraphView` with a predicate and a provenance record. A view must expose its source graph version, node/edge predicates and estimated cost. Deep view chains should be flattened or materialized deliberately, never accidentally.

The warning about writable views also becomes a test requirement: a renderer or inspector must not be able to mutate the investigation graph by changing a returned attribute object.

Source: [NetworkX graph types and views](https://networkx.org/documentation/stable/reference/classes/index.html).

### 23.3 Boost Graph Library: algorithms should depend on the minimum interface

Boost Graph Library factors graph capabilities into small concepts. An algorithm can require only incidence, mutability, property access or another minimal capability instead of depending on one concrete graph class. Its property-map abstraction lets algorithms read and write data without owning the storage; the storage can be bundled, external, computed or temporary.

This is one of the strongest ideas found in the research so far. It suggests that FGA should not make every algorithm understand every domain and presentation field. Instead:

- graph topology is one capability;
- evidence metadata is a separate read-only capability;
- layout coordinates are an external presentation property map;
- temporary algorithm state such as distance, predecessor and color lives in short-lived work buffers;
- renderer state is never stored as graph truth.

This separation is particularly valuable for autonomous tests: the same algorithm can run over a small fixture, a worker-owned compact representation or a diagnostic view, while the oracle can inspect the property maps independently.

Source: [Boost Graph concepts](https://www.boost.org/doc/libs/latest/libs/graph/doc/graph_concepts.html), [Boost property maps](https://www.boost.org/latest/libs/graph/doc/html/graph/property_maps/overview.html).

### 23.4 JGraphT: interfaces, graph paths, events and interchangeable storage

JGraphT provides a root `Graph<V,E>` interface, graph types, paths, mappings, import/export, traversal, metrics, graph tests, listenable graphs and compact or succinct storage extensions. Its public package structure separates graph structure, algorithms, traversal, I/O and optional storage modules.

The useful lesson is organizational: algorithms and import/export should not be entangled with the interactive renderer. The event mechanism is also a useful reference for making structural changes observable without making event listeners the owner of truth.

The main limitation for the browser product is runtime and object overhead. A Java-oriented object graph is a good algorithm reference, not a browser memory layout. FGA should keep the contract language-neutral and permit a packed worker representation later.

Sources: [JGraphT project](https://github.com/jgrapht/jgrapht), [JGraphT API package summary](https://jgrapht.org/javadoc/org.jgrapht.core/org/jgrapht/package-summary.html).

### 23.5 GraphStream: model change as a first-class timeline

GraphStream is explicitly a dynamic graph library. Its model includes topology changes and value changes over time, and separate viewers can consume the evolving graph. That is directly relevant to FGA because a case investigation is not just a static picture: nodes can be discovered, classified, linked, filtered, pinned and revisited.

The transferable idea is an append-only change vocabulary: add node, remove node, add relationship, update attribute, update layout, change selection and change visibility should be distinguishable. The engine can then replay a scene without a browser.

The caution is project freshness: the public site still presents the 2.0 release as the latest news. It is useful as a conceptual reference, but its maintenance posture must be checked before any dependency decision.

Sources: [GraphStream overview](https://graphstream-project.org/), [GraphStream dynamic graph FAQ](https://graphstream-project.org/doc/FAQ/General-Questions/What-is-GraphStream/).

### 23.6 OGDF: rich graph drawing structures and replaceable algorithm phases

OGDF is a C++ framework focused on graph algorithms and automatic drawing. Its documentation covers graph representations, embeddings, clustered graphs, planarity, crossings, shortest paths, clustering, hierarchical and force-directed layouts. Its stated goal includes replacing particular algorithm phases through dedicated modules.

This is a valuable architecture reference for a future layout worker: a layout should be a pipeline with named phases and replaceable policies, not one opaque “run layout” function. For example:

1. normalize topology;
2. choose or preserve anchors;
3. rank or cluster;
4. route edges;
5. minimize crossings or stress;
6. assign coordinates;
7. validate constraints;
8. emit diagnostics and replay metadata.

OGDF is not a direct browser dependency for the first FGA engine because of C++/WASM integration cost, GPL obligations and the need to keep game interaction latency predictable. It remains a high-value algorithmic reference and possible offline/worker backend candidate only after a license and build audit.

Sources: [OGDF documentation](https://ogdf.github.io/doc/ogdf/index.html), [OGDF goals and algorithms](https://www.ogdf.uni-osnabrueck.de/about/).

### 23.7 Graphviz: a declarative interchange and layout oracle

Graphviz separates a graph description language from layout programs and output formats. DOT supports graph, node, edge and subgraph attributes; clusters are a convention recognized by some layout engines rather than universal graph semantics. The `dot` layout targets hierarchical directed drawings and explicitly considers ranks, crossings and edge length.

What FGA should borrow:

- a small human-readable interchange format for fixtures and bug reports;
- graph-level, node-level and edge-level defaults;
- subgraph/cluster grouping as a presentation hint;
- layout attributes that are inspectable and replayable.

What FGA should reject:

- treating DOT attributes as the domain schema;
- assuming a single static layout is enough for interaction;
- assuming a cluster is always a semantic entity rather than a layout hint.

Graphviz is therefore a useful import/export and offline-layout oracle, not the interactive engine.

Sources: [DOT language](https://graphviz.org/doc/info/lang), [Graphviz `dot` layout](https://www.graphviz.org/docs/layouts/dot/), [Graphviz documentation](https://www.graphviz.org/doc/info/).

### 23.8 ELK: layout configuration belongs in the graph model, but not in domain truth

The Eclipse Layout Kernel describes an `ElkGraph` data structure that represents graphs and annotates them with layout configuration information. The project supports compound graph layout and ports as explicit edge anchor points, and its scope deliberately excludes graphical editing frameworks.

This is a strong precedent for putting layout constraints beside the presentation graph while keeping the editing/interaction shell separate. FGA should support ports, groups and constraints for visual clarity, but every such field must be tagged as `layout` or `view`, never as evidence.

The implementation should make layout configuration serializable and schema-checked. A constraint that cannot be satisfied should produce a diagnostic and a fallback layout, not silently change the graph.

Sources: [Eclipse Layout Kernel project scope](https://projects.eclipse.org/projects/modeling.elk/governance), [ELK technical paper](https://arxiv.org/abs/2311.00533).

### 23.9 Gephi and Tulip: exploration tools teach us to separate analysis, editing and rendering

Gephi's toolkit separates graph, layout, filters and I/O modules from the user interface. Its desktop workflow separates Overview, Data Laboratory, Statistics, Appearance and Preview. Tulip combines graph analysis, visual analytics, interaction, multiple views and a plugin architecture; its older handbook describes an MVC-like separation of graph, views, controllers and interactors.

The strong idea is not to reproduce a desktop application in the game. It is to expose distinct surfaces:

- the graph canvas for spatial investigation;
- an inspector for the selected object;
- a filter/query surface;
- a metrics/diagnostics surface;
- a replay/export surface;
- an accessibility/semantic surface.

The risk is feature gravity. Gephi and Tulip are powerful analysis workbenches; importing their entire product model would make FGA slower to learn and harder to test. The FGA engine should adopt modular seams, not every module.

Sources: [Gephi Toolkit architecture](https://gephi.org/toolkit/), [Gephi quickstart workflow](https://gephi.org/quickstart/), [Gephi desktop roadmap](https://gephi.org/desktop/), [Tulip overview](https://tulip.labri.fr/), [Tulip handbook](https://tulip.labri.fr/Documentation/3_8/userHandbook/html/ch01.html).

### 23.10 Data-model synthesis

The current preferred core is a layered model:

```text
GraphDocument
├── topology: stable nodes and relationships
├── domain projection: FGA-safe evidence references and statuses
├── presentation projection: labels, semantic roles, pins, groups, layout hints
├── interaction state: selection, hover, focus, menu, camera, filters
├── derived indexes: adjacency, spatial index, label index, visibility index
└── event journal: commands, state hashes, layout versions, diagnostics
```

The topology and domain projection are versioned snapshots. Presentation and interaction are derived and disposable. Algorithms receive narrow capability interfaces or property maps. Views are lazy when cheap and materialized when replay, iteration or serialization requires stability.

This model is deliberately more explicit than most front-end libraries. The cost is implementation work; the benefit is that an accidental renderer mutation, a hidden filter, or a nondeterministic layout becomes observable and testable.

## 24. Research pass 5 — renderer architecture and interaction trade-offs

### 24.1 Sigma.js: a coherent GPU pipeline with explicit performance switches

Sigma's current documentation exposes a particularly instructive pipeline: process graph attributes and reducers, upload display data as GPU data textures, then render depth layers. Nodes use quads and signed-distance-field shapes; labels use an SDF text atlas; an off-screen picking framebuffer identifies objects under the cursor. Edge and label events are disabled by default because picking has a performance cost.

Good ideas:

- declarative primitives describe what can render while styles describe how it looks;
- coarse depth layers and fine z-order avoid reprocessing the whole graph for every visual priority change;
- one renderer can support custom HTML layers and custom WebGL layers;
- expensive interaction features are opt-in and documented as budgets.

Risks and complaints to carry into FGA tests:

- rebuilding label buffers on every frame is a real regression class;
- synchronous pixel readback can stall pointer movement;
- enabling edge and label events indiscriminately can turn a smooth graph into a slow one;
- GPU context ownership and destruction must be observable.

FGA decision: adopt a renderer pipeline with explicit process/render phases, dirty regions, depth bands, label budgets and a picking policy. Do not assume GPU picking is always the right default; the same `HitTest` contract must support a semantic/DOM or CPU spatial-index fallback.

Sources: [Sigma rendering](https://www.sigmajs.org/concepts/rendering/), [Sigma lifecycle](https://www.sigmajs.org/concepts/lifecycle/), [Sigma settings](https://www.sigmajs.org/reference/settings/), [Sigma styles and primitives](https://www.sigmajs.org/concepts/styles-and-primitives/).

### 24.2 Cytoscape.js: precise canvas interaction, evolving GPU path

Cytoscape.js historically used a JavaScript Canvas renderer because it supports precise shapes and curves with broad browser compatibility, but its maintainers have also published a WebGL preview for larger networks. The public performance discussion highlights label cost, GPU memory, readback stalls, dynamic update rebuilding, floating-point reproducibility and the need for an open schema.

The lesson is not “Canvas is bad” or “WebGL is always better.” It is that rendering is a workload-specific policy. FGA should be able to render a small, semantically rich scene with a reference backend and switch to a GPU backend as density grows. The switch must be visible in diagnostics and must preserve selection, identity, labels and replay.

Source: [Cytoscape WebGL renderer preview](https://blog.js.cytoscape.org/2025/01/13/webgl-preview/), [Cytoscape performance redesign discussion](https://github.com/cytoscape/cytoscape.js/issues/3486).

### 24.3 D3 and SVG: reference implementation and accessibility oracle

D3 provides low-level data binding and DOM/SVG primitives rather than a complete graph editor. That flexibility is precisely why it is valuable for FGA's reference backend: SVG elements can carry stable IDs, semantic attributes, keyboard focus, test selectors and accessible names. The trade-off is poor scaling if thousands of individual DOM objects remain live and update together.

Decision: SVG is the reference backend for correctness, snapshots and accessibility. It is not required to be the high-density backend.

### 24.4 React Flow: excellent editing affordances, DOM ceiling

React Flow demonstrates how useful node dragging, handles, edge creation, contextual interaction and custom React nodes can be. Its public discussions and issue history also show the cost of DOM-based rendering at high density: full-array updates can make local selection expensive, and the maintainers explicitly recommend Canvas-like solutions for very large node counts.

Decision: borrow the interaction vocabulary—dragging, handles, selection, keyboard actions, viewport controls and contextual tools—but do not make React component identity the identity of a graph node. The engine core must remain framework-neutral.

Sources: [React Flow large graph performance discussion](https://github.com/xyflow/xyflow/discussions/4975), [React Flow 10k-node issue](https://github.com/xyflow/xyflow/issues/3044).

### 24.5 Force-graph family: simple exploration across 2D, 3D, VR and AR

The force-graph family offers consistent interfaces across 2D Canvas, Three.js/WebGL 3D, VR and AR, with zoom/pan, drag and hover/click interactions. The abstraction is useful for treating camera and interaction commands as renderer-independent. Its default force-directed mental model is not sufficient for an investigation graph where direction, evidence role, grouping and reproducibility matter.

Decision: use force simulation as one layout strategy and an experiment source, never as the definition of “graph visualization.”

Source: [react-force-graph package description](https://www.npmjs.com/package/react-force-graph).

### 24.6 GraphStream and Graphviz: dynamic model versus static diagram

GraphStream reinforces live updates and multiple viewers. Graphviz reinforces declarative diagrams, clusters, constraints and export. Together they show that “the graph” and “a drawing of the graph” must be separate objects. FGA should be able to produce a static evidence snapshot even if the interactive renderer has failed, and should be able to animate a legitimate state change without rebuilding the domain model.

### 24.7 Renderer contract proposed for FGA

The renderer should implement a narrow contract:

```text
mount(scene, surface, capabilities) -> RendererHandle
update(snapshot, viewState, dirtySet) -> RenderReceipt
hitTest(screenPoint, policy) -> HitResult | None
focus(target, cameraPolicy) -> CameraReceipt
export(format, options) -> Artifact
inspect() -> RendererDiagnostics
destroy() -> void
```

`RenderReceipt` includes graph version, layout version, renderer name, visible counts, label counts, frame cost and fallback decisions. `HitResult` carries a stable FGA ID and hit source. `destroy()` is mandatory and idempotent. A renderer cannot emit domain mutations directly; it emits typed intents for the game shell.

## 25. Research pass 6 — the autonomous test strategy

The testability requirement is now treated as an architectural constraint, not a QA phase added later. Hercule must be able to reopen the same case repeatedly, with the same data and commands, and obtain evidence that the engine behaved correctly without a human clicking through every scene.

### 25.1 Two independent oracles

Every interaction test should verify at least two independent results:

1. **State/event oracle:** the engine emitted the correct typed intent or updated only the allowed presentation state.
2. **Semantic mirror oracle:** the selected node, edge, menu, label and visible relationship are represented correctly in the accessible/semantic tree.

Screenshots are a third oracle for visual appearance, not a replacement for the first two. This avoids a test suite that passes because the screenshot is unchanged even though the wrong entity was selected.

### 25.2 Contract tests for every backend

The same backend-neutral suite must run against SVG, Canvas, WebGL and future WebGPU adapters:

- mount and unmount repeatedly;
- render an empty graph, a single node, a self-loop, parallel relationships, a disconnected graph and a dense cluster;
- select, hover, drag, pin, unpin, focus, fit, zoom and reset;
- open and dismiss node, edge and cluster context menus;
- apply and clear filters without mutating the source snapshot;
- preserve FGA IDs through layout and renderer replacement;
- export a deterministic artifact;
- report diagnostics and clean up all listeners/contexts.

The backend may render differently, but it must satisfy the same semantic and interaction contract.

### 25.3 Property-based and metamorphic tests

The graph engine needs properties stronger than hand-written examples:

- adding an isolated node cannot change unrelated node IDs;
- serializing and reloading a snapshot preserves topology and status;
- applying the same command log twice produces the same state hash;
- filtering never invents an edge whose endpoints are absent;
- reversing a directed view does not mutate the source graph;
- pinning a node survives a layout pass unless the command explicitly releases the pin;
- a renderer replacement preserves selection and camera policy where supported;
- removing a node removes or reports all incident visual relationships;
- a context menu can only emit capabilities granted by the scene;
- layout output is deterministic for a fixed graph version, algorithm, seed, constraints and viewport.

Random graph generators should include adversarial shapes: long chains, stars, hubs, cycles, grids, disconnected islands, multigraphs, self-loops, duplicate labels, extreme degree skew and large label text.

### 25.4 Model-based interaction testing

The interaction model should be a state machine whose commands include `Select`, `OpenContextMenu`, `InvokeCapability`, `DragNode`, `Pan`, `Zoom`, `Fit`, `ApplyFilter`, `ChangeRepresentation`, `RunLayout`, `ReplaceRenderer`, `Export`, `Undo` and `Redo`. Generated traces can then find illegal transitions such as a stale menu action after selection changed or a drag that remains active after focus loss.

This follows the event-interaction-graph idea from GUI testing research: the model is not only a list of happy-path scripts, but a map of event combinations that can expose faults.

Sources: [pilot-derived event-interaction graphs for GUI testing](https://www.cs.umd.edu/~atif/papers/XieMemonTOSEM2008-abstract.html), [GraphWalker model-based testing case study](https://www.es.mdh.se/pdf_publications/6101.pdf).

### 25.5 Deterministic visual regression

Playwright can wait for two consecutive equal screenshots before comparing them and can compare screenshots, text or arbitrary binary snapshots. Its own documentation warns that screenshots vary by operating system, browser, fonts, hardware and rendering mode.

FGA should therefore:

- pin the browser image, fonts, viewport and device scale for golden tests;
- freeze time, randomness, network and animation;
- wait for a renderer readiness receipt, not an arbitrary timeout;
- use semantic assertions before screenshot assertions;
- mask only explicitly volatile regions;
- keep per-backend baselines and record the renderer/driver version;
- attach diff images and interaction flight records on failure.

Source: [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots).

### 25.6 Performance and resilience tests

The test plan must measure more than average FPS:

- time to first useful render;
- p50/p95/p99 frame cost during pan, zoom, hover and drag;
- long tasks and input delay;
- label rebuild count and label cache hit rate;
- picking latency under pointer movement;
- layout time and cancellation latency;
- memory before/after mount, update, renderer replacement and destroy;
- WebGL/WebGPU context loss and fallback time;
- graph sizes and degree distributions at which representation negotiation changes;
- repeated open/close/reopen cycles to detect leaks.

The suite should run several repetitions and report dispersion. One fast run is not proof of stability.

### 25.7 Accessibility and keyboard tests

The semantic mirror is tested as a navigable graph, not merely as a hidden list:

- tab and arrow navigation reaches nodes, edges, clusters and tools;
- focused objects expose stable names, roles, status and relationship counts;
- every color-coded state also has icon/shape/text;
- context menus can open, navigate and dismiss from the keyboard;
- the canvas/GPU backend retains equivalent semantic access;
- zoom and motion preferences are respected;
- focus is restored after menu dismissal or representation change.

Relevant references include [WAI-ARIA](https://www.w3.org/WAI/standards-guidelines/aria/), [W3C SVG accessibility](https://www.w3.org/TR/SVG/access), [Data Navigator](https://doi.org/10.1109/TVCG.2023.3327393), [TADA](https://doi.org/10.1145/3613904.3642222) and [Rich Screen Reader Experiences](https://vis.csail.mit.edu/pubs/rich-screen-reader-vis-experiences/).

### 25.8 Manual exploratory protocol

Automation cannot decide whether the graph feels legible or whether an investigation layout communicates the intended hierarchy. Manual review remains necessary, but it should be a structured exploratory protocol:

- inspect every renderer at the same fixture and viewport;
- drag hubs, leaves, clusters and overlapping nodes;
- open menus near all four viewport edges;
- test pointer, touch, keyboard and focus-loss paths;
- toggle labels, filters, minimap, matrix/path view and semantic mode;
- interrupt layouts and transitions;
- resize the window and change device pixel ratio;
- trigger context loss/fallback where the browser permits it;
- record a short interaction flight and attach defects to a reproducible fixture.

Manual review is a complement to autonomous tests, not a reason to leave behavior unrecorded.

## 26. Proposed implementation architecture

The current architecture is now specific enough to implement incrementally:

```text
FGA case / API projection
        │ typed, versioned, evidence-safe snapshot
        ▼
Graph core
  topology + domain projection + invariants
        │
        ├── Query/view layer (filters, paths, clusters, matrix projection)
        ├── Layout planner (seed, constraints, pins, replay metadata)
        ├── Interaction state machine (commands, capabilities, undo/redo)
        ├── Semantic mirror (keyboard/accessibility/test oracle)
        ├── Spatial/picking index
        └── Diagnostics + interaction flight recorder
        │
        ├── SVG reference renderer
        ├── Canvas renderer
        ├── WebGL renderer
        └── WebGPU renderer (future, capability-gated)
```

### 26.1 Core packages

- `graph-contract`: serializable node, relationship, group, status, evidence-reference and layout types;
- `graph-core`: snapshot validation, stable IDs, adjacency indexes, immutable views and command journal;
- `graph-query`: neighborhood, path, cluster, filter and representation projections;
- `graph-layout`: deterministic layout interface, seed handling, pins, constraints and quality metrics;
- `graph-interaction`: pointer/keyboard gestures, capability tokens, menus, selection and camera policy;
- `graph-semantic`: accessible tree, text traversal and test selectors;
- `graph-renderer-contract`: renderer interface, dirty sets, hit testing and diagnostics;
- `graph-renderer-svg`: correctness/reference implementation;
- `graph-renderer-canvas` and `graph-renderer-gpu`: progressive backends;
- `graph-testkit`: fixtures, generators, command traces, semantic assertions, screenshot helpers and leak probes.

### 26.2 Worker boundary

Layout and graph queries that can exceed an input budget should run in a worker or a cancellable task. The protocol should send compact snapshots or deltas, not mutable object graphs. Every response carries `graphVersion`, `requestId`, `layoutVersion`, `seed`, `constraintsHash` and a cancellation status.

Late results are discarded by version, not guessed away. A worker may suggest positions, but the main thread remains responsible for accepting or rejecting them and preserving user pins.

### 26.3 Context menus

Menus are declarative scene capabilities:

```text
MenuContext {
  target: StableId
  graphVersion: Version
  selection: StableId[]
  capabilities: CapabilityToken[]
  anchor: ScreenPoint
}
```

The renderer can offer a polished menu with evidence summary, neighbor expansion, path highlighting, pin/unpin, status legend, “show in table”, “show semantically”, “copy stable ID” and “record investigation note” where authorized. It must not directly call Databricks, rewrite truth, confirm fraud or spend an investigation credit.

### 26.4 Layout quality metrics

Every layout should return metrics relevant to the fixture and the task:

- node overlap count;
- edge crossing count or a bounded estimate;
- minimum crossing angle distribution;
- label collision estimate;
- edge length dispersion;
- cluster separation;
- displacement from previous layout;
- pinned-node violations;
- viewport occupancy;
- computation time and cancellation state.

Metrics are diagnostics and test inputs, not a universal scalar “best layout” score. The literature shows that layout evaluation depends on graph features, tasks, datasets and metrics; an aggregate leaderboard would recreate the benchmark trap the research intentionally moved beyond.

Source: [systematic review of graph-layout evaluation methods](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.15073).

## 27. Implementation roadmap derived from the research

### Phase A — contract and reference correctness

1. Freeze the FGA-safe `GraphDocument` schema and version rules.
2. Implement immutable snapshots, stable IDs, capability tokens and semantic mirror.
3. Implement SVG reference renderer and `graph-testkit`.
4. Add command journal, state hashes and deterministic fixture generators.
5. Make the existing qualification fixture run through this contract.

Exit condition: all interaction commands have semantic/event assertions and can replay without a browser.

### Phase B — investigation interaction

1. Add node/edge/cluster menus and keyboard equivalents.
2. Add dragging, pins, explicit movement provenance and undo/redo.
3. Add filters, path expansion, cluster expansion and representation negotiation.
4. Add accessibility traversal and focus restoration.

Exit condition: manual exploratory protocol is reproducible from a recorded command trace.

### Phase C — renderer progression

1. Add Canvas with the same contract and diagnostics.
2. Add WebGL only for workloads where measured frame and label budgets justify it.
3. Add GPU picking as one policy, with CPU/semantic fallback.
4. Prototype WebGPU only behind capability detection and a separate test matrix.

Exit condition: backend contract suite passes, renderer replacement preserves state, and no backend is allowed to become the domain authority.

### Phase D — scale and research features

1. Add worker-side layout/query execution with cancellation.
2. Add semantic level-of-detail and matrix/path projections.
3. Add tiled or multiscale graph browsing only if the game fixture demonstrates a real need.
4. Add long-run memory, context-loss and performance repetitions.

Exit condition: declared FGA workload envelopes are met with evidence, not optimistic demos.

## 28. Explicit rejections and open risks

| Idea | Status | Reason |
|---|---|---|
| Pick a single existing library and make it the engine | Rejected | It couples domain, interaction, rendering and lifecycle to another project’s assumptions. |
| Treat the old five-adapter benchmark as the decision procedure | Rejected | The current objective is research and independent design; adapters remain regression evidence. |
| Make a commercial renderer the production dependency | Rejected for current scope | The project is open-source/non-commercial and must remain redistributable and independently testable. Product study is still allowed. |
| Use screenshots as the only automated oracle | Rejected | Screenshots do not prove stable IDs, correct intents, semantic access or absence of stale state. |
| Use force-directed layout for every scene | Rejected | It is visually attractive but can destroy direction, hierarchy, replayability and mental-map stability. |
| Use WebGPU immediately | Deferred | Potentially powerful, but adds capability, browser, shader, fallback and test-matrix risk before the reference contract exists. |
| Keep every graph object mutable and globally observable | Rejected | It makes filtering, replay, worker boundaries and renderer isolation harder to prove. |
| Copy restricted code or assets from commercial products | Rejected | We may study public behavior and ideas, but the implementation must be independently authored and license-clean. |

Open risks:

- semantic level-of-detail can become confusing if the engine hides important evidence without a clear explanation;
- multiple representations may fragment the user’s mental map;
- a highly instrumented renderer can itself become a performance cost;
- property-map-like flexibility can make TypeScript contracts too abstract for everyday feature work;
- worker snapshots and layout cancellation add versioning complexity;
- visual quality remains partly human-judged and needs disciplined exploratory review.

## 29. Updated research ledger

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-010 | Should graph filters mutate the graph? | NetworkX live read-only views and view-chain cautions. | Use immutable/lazy views with provenance; test source immutability and chain flattening. |
| R-011 | Where should algorithm state live? | Boost property maps separate algorithm storage from graph storage. | Use external work buffers and typed property maps; test allocation reuse and isolation. |
| R-012 | Should layout be a monolith? | OGDF module phases and ELK layout-configured graph model. | Use named layout phases with replaceable policies and replay metadata. |
| R-013 | Can a static description support an interactive engine? | Graphviz separates DOT descriptions/layout/output. | Keep a human-readable fixture/export format, but do not use it as the domain schema. |
| R-014 | What does a GPU renderer need to expose? | Sigma process/render phases, data textures, SDF labels and GPU picking. | Add dirty sets, label/picking budgets, diagnostics and CPU fallback to the renderer contract. |
| R-015 | Is DOM rendering always appropriate? | React Flow maintainers recommend Canvas-like approaches for very large graphs. | Use SVG/DOM as reference and interaction backend; negotiate to Canvas/GPU by measured workload. |
| R-016 | How can autonomous tests prove graph behavior? | Playwright visual comparisons plus model-based GUI testing research. | Combine state/event, semantic, screenshot, property-based and model-based oracles. |
| R-017 | How should community complaints influence design? | Sigma, Cytoscape, React Flow, vis-network and JointJS issue records. | Convert each recurring complaint into a named regression test and diagnostic. |

## 30. Updated pass log

| Pass | Perspective | Findings/corrections | Clean? |
|---:|---|---|---|
| 0 | Scope and baseline | Created the living dossier; separated research from benchmark and recorded local invariants. | pending later regression |
| 1 | Readability, dynamic change, accessibility and user feedback | Added mental-map stability, representation switching, semantic traversal, accessibility research, issue-derived failure modes and initial synthesis. | pending contradiction review |
| 4 | Graph data models and algorithm boundaries | Added Graphology, NetworkX, Boost, JGraphT, GraphStream, OGDF, Graphviz, ELK, Gephi and Tulip; derived layered snapshots, views, property maps and modular layouts. | pending prototype validation |
| 5 | Renderer architecture and interaction trade-offs | Added Sigma, Cytoscape, D3/SVG, React Flow, force-graph and static/dynamic separation; defined renderer contract and renderer-specific risks. | pending local contract tests |
| 6 | Autonomous testing and implementation architecture | Added dual oracles, property/model-based testing, visual regression discipline, accessibility, performance, lifecycle, worker protocol and roadmap. | pending implementation |

## 31. Sources added in passes 4–6

- [Graphology](https://graphology.github.io/)
- [NetworkX graph types and views](https://networkx.org/documentation/stable/reference/classes/index.html)
- [Boost Graph concepts](https://www.boost.org/doc/libs/latest/libs/graph/doc/graph_concepts.html)
- [Boost property maps](https://www.boost.org/latest/libs/graph/doc/html/graph/property_maps/overview.html)
- [JGraphT](https://github.com/jgrapht/jgrapht)
- [JGraphT API](https://jgrapht.org/javadoc/org.jgrapht.core/org/jgrapht/package-summary.html)
- [GraphStream](https://graphstream-project.org/)
- [OGDF](https://ogdf.github.io/doc/ogdf/index.html)
- [Graphviz DOT language](https://graphviz.org/doc/info/lang)
- [Graphviz `dot` layout](https://www.graphviz.org/docs/layouts/dot/)
- [Eclipse Layout Kernel](https://projects.eclipse.org/projects/modeling.elk/governance)
- [ELK paper](https://arxiv.org/abs/2311.00533)
- [Gephi Toolkit](https://gephi.org/toolkit/)
- [Tulip](https://tulip.labri.fr/)
- [Sigma rendering](https://www.sigmajs.org/concepts/rendering/)
- [Sigma lifecycle](https://www.sigmajs.org/concepts/lifecycle/)
- [Sigma settings](https://www.sigmajs.org/reference/settings/)
- [Cytoscape WebGL preview](https://blog.js.cytoscape.org/2025/01/13/webgl-preview/)
- [react-force-graph](https://www.npmjs.com/package/react-force-graph)
- [vis-network issue tracker](https://github.com/visjs/vis-network/issues)
- [xyflow issue tracker](https://github.com/xyflow/xyflow/issues)
- [JointJS issue tracker](https://github.com/clientIO/joint/issues)
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [Graph-layout evaluation systematic review](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.15073)

## 32. Research pass 7 — commercial and product UX as a clean-room idea source

The purpose of this pass is deliberately narrow: study public documentation, demos and product behavior for interaction ideas, while keeping implementation and licensing boundaries explicit. No restricted source code, evaluation packages or commercial assets become implementation inputs.

### 32.1 yFiles: interaction completeness is a feature, not decoration

yFiles documents a mature graph model with directed and undirected edges, self-loops, parallel edges, labels, ports, nested groups, filtering, overview navigation, keyboard commands, clipboard, undo/redo, context menus, tooltips, selection/focus/highlighting, edge bridges, level-of-detail rendering, interactive editing, snapping, orthogonal routing and group collapse/expand.

The key product insight is that a graph editor feels complete because the interaction model is coherent across all graph elements. A node is not just a circle: it can have labels, ports, focus, a context menu, drag affordances, keyboard behavior, undo semantics and a representation at different zoom levels.

FGA should adopt the following ideas independently:

- separate selection, focus, hover and highlight states;
- context menus that are populated from the target and current permissions;
- group nodes that can collapse with an explainable transition;
- labels and ports as first-class presentation objects;
- edge bridges or other crossing cues when they materially improve reading;
- undo/redo of presentation commands and explicitly authorized investigation notes;
- overview/minimap and LOD as navigation aids.

FGA should not adopt the product's assumptions that arbitrary graph editing is always allowed, that business data can be attached without a domain boundary, or that a commercial SDK is an acceptable runtime dependency for the open-source game.

Sources: [yFiles supported interactions](https://docs.yworks.com/yfileshtml/dguide/interaction-support), [yFiles features](https://docs.yworks.com/yfiles-html/dguide/features/index.html), [yFiles licensing](https://docs.yworks.com/yfiles-html/dguide/licensing/).

### 32.2 GoJS: context menus should be target-aware but may be rendered outside the graph surface

GoJS documents context menus as diagram adornments bound to the same data as their target, with support for node-specific and background menus. It also exposes automatic layouts, data binding, undo/redo, keyboard commands, subgraphs/groups and framework integrations.

One useful design tension is explicit in the docs: an in-diagram menu is convenient and visually integrated, but it cannot render outside the diagram; an HTML menu is more flexible around viewport edges. FGA should make this a policy choice rather than a renderer accident:

- use a graph-anchored menu when the target is fully visible and the menu benefits from visual attachment;
- promote to an HTML/DOM surface when clipping, keyboard navigation, accessibility or viewport boundaries require it;
- preserve the same capability token and command identity in both cases.

GoJS also reinforces a product-health point: context menus and undo are not secondary widgets. They are integrated with the graph’s data and command model.

Sources: [GoJS context menus](https://gojs.net/latest/learn/contextMenus), [GoJS deployment and commercial license](https://gojs.net/latest/learn/deployment), [GoJS feature/pricing page](https://gojs.net/latest/pricing).

### 32.3 JointJS: the open core/commercial extension split is instructive

JointJS states that its core is open source under MPL 2.0 while JointJS+ is a commercial extension with advanced features and support. Public issue history shows recurring integration concerns around browser events, TypeScript module resolution, export, context menus, geometry and scroller behavior.

The engineering lesson is not that open cores are bad. It is that the boundary must be explicit. FGA cannot design a core whose essential features are secretly dependent on a paid extension. Context menus, keyboard access, selection, test hooks, lifecycle and serialization must be first-class in the open engine.

JointJS is also a useful reference for diagram-oriented features such as reusable tools, element buttons, remove/boundary tools, link labels and routers. These should be evaluated by FGA task value rather than copied as a general diagram editor.

Sources: [JointJS licensing](https://www.jointjs.com/license), [JointJS issue tracker](https://github.com/clientIO/joint/issues), [JointJS changelog](https://github.com/clientIO/joint/blob/master/CHANGELOG).

### 32.4 Neo4j Bloom: search-to-visualization reduces the “blank canvas” problem

Neo4j Bloom presents a business-facing exploration workflow: search suggestions/templates, an animated graph, panning and zooming, selection, adjacency expansion, styling and property inspection. The important idea is not the database integration; it is that the user can begin from a question rather than from an empty canvas.

FGA should consider an investigation command bar with safe, local suggestions such as:

- “show neighbors of this entity”;
- “highlight relationships with this type”;
- “find paths between these selected nodes”;
- “show the cluster containing this node”;
- “reopen the last recorded scene.”

These commands must compile into the same typed intents as menus and keyboard actions. Natural-language or suggestion UX must not become a hidden authority path to external queries or truth changes.

Sources: [Neo4j graph visualization overview](https://neo4j.com/graph-visualization-neo4j/), [Neo4j Bloom user guide](https://neo4j.com/docs/bloom-user-guide/current/), [Neo4j visualization tools](https://neo4j.com/docs/getting-started/graph-visualization/graph-visualization-tools/).

### 32.5 Clean-room feature extraction table

| Public product idea | FGA interpretation | License-safe implementation boundary |
|---|---|---|
| Target-aware context menu | Capability-driven command palette for node/edge/cluster/background | Own command schema and HTML/SVG implementation |
| Ports and edge anchors | Presentation constraints that improve direction and edge routing | Own typed `PortSpec` and layout adapter |
| Undo/redo | Replayable presentation and authorized investigation commands | Own command journal and state hashes |
| Groups and collapse/expand | Explicit projection of a cluster with an explainable identity mapping | Own cluster projection and semantic mirror |
| LOD | Evidence-aware representation policy | Own rules, thresholds and diagnostics |
| Property browser | Inspector projection with provenance and stable IDs | Own inspector model; no renderer authority |
| Search suggestions | Safe query/intent templates over the local graph projection | Own parser and capability gate |
| Overview/minimap | Camera projection, not a second graph source | Own minimap renderer from the same snapshot |
| Bridges and routing | Readability aids with measurable crossing/overlap effects | Own geometry and visual regression fixtures |

## 33. Research pass 8 — community feedback and maintenance signals

Issue trackers are noisy, but recurring issue categories expose the hidden cost of a graph engine. This pass treats public issues as reported evidence, not as proof of a library-wide defect rate.

### 33.1 Recurring complaint categories

The surveyed trackers expose several repeated classes:

- full-array or broad state updates for a local selection cause lag;
- DOM/SVG graphs become unsuitable at high node counts or when custom nodes are heavy;
- hover and pointer handling can trigger expensive hit testing or GPU readback;
- labels are disproportionately expensive and can be rebuilt unnecessarily;
- drag state can remain active after focus loss or modal interaction;
- edge labels, arrow orientation, curved edges and self-loops have browser/geometry edge cases;
- context-menu default prevention, tooltips and viewport clipping require application-specific handling;
- TypeScript declarations and module resolution can fail independently of runtime correctness;
- dynamic layouts and animation can destroy the user’s mental map;
- export paths can diverge from on-screen rendering.

Examples include [Sigma label-buffer and picking issues](https://github.com/jacomyal/sigma.js/issues/1553), [Sigma pointer readback issue](https://github.com/jacomyal/sigma.js/issues/1546), [React Flow large-graph performance](https://github.com/xyflow/xyflow/issues/3044), [React Flow broad selection updates](https://github.com/xyflow/xyflow/discussions/4975), [vis-network open issues](https://github.com/visjs/vis-network/issues), and [JointJS integration/context-menu issues](https://github.com/clientIO/joint/issues).

### 33.2 Maintenance is part of the architecture decision

For every candidate idea or dependency, the research record should capture:

1. last release and release cadence;
2. source repository activity and issue response;
3. browser/runtime support policy;
4. TypeScript and package-format quality;
5. test and example coverage;
6. extension/API stability;
7. license compatibility and provenance;
8. security/bug-fix communication;
9. exit strategy if the project stalls;
10. whether the project’s internal design is understandable enough to maintain or reimplement independently.

This is why “popular” is not a sufficient selection criterion. A graph library is a long-lived behavioral dependency, and its lifecycle becomes part of FGA’s lifecycle.

### 33.3 Complaint-to-design regression map

| Reported complaint class | FGA design response | Regression/diagnostic |
|---|---|---|
| local selection updates every object | derived state and indexed neighborhood sets | assert update scope and frame budget |
| DOM graph ceiling | representation negotiation and GPU-ready contract | density fixture chooses backend with reason |
| pointer readback stall | picking policy with budgets and fallback | p95 hover latency under pan |
| label rebuilds | immutable label atlas/cache and dirty flags | label rebuild counter |
| drag stuck after focus loss | explicit gesture cancellation | blur/escape/modal trace |
| edge geometry bugs | canonical geometry fixtures | self-loop, parallel edge, curve, label snapshots |
| menu clipping/context race | viewport-aware menu promoter + graphVersion | open near every edge after selection change |
| type/dependency mismatch | API contract tests and lockfile audit | clean install/typecheck matrix |
| mental-map jumps | movement provenance and stability threshold | unchanged-node displacement assertion |
| export differs from screen | export receipt and semantic fixture | compare IDs/labels/edge counts in export |

### 33.4 Claims that remain unproven

The research must not overstate the following:

- issue counts are not comparable popularity or defect rates;
- a published “supports tens of thousands” claim is not an FGA workload guarantee;
- a commercial demo’s visual polish does not prove its accessibility or testability;
- WebGPU performance depends on browser, driver, data layout and shader strategy;
- a layout metric does not predict investigative success for every user;
- a paper’s task study does not automatically transfer to fraud investigations;
- a project’s current release date does not prove future maintenance.

Each remains an explicit uncertainty or requires a local experiment.

## 34. Research pass 9 — contradiction review and design corrections

The previous passes contain tensions that must be resolved rather than hidden:

### Contradiction A: rich interactivity versus autonomous determinism

Free node movement and animated layouts are desirable, but unconstrained physics is nondeterministic and can erase the mental map. Resolution: user movement is an explicit command; automatic layout has a seed, constraints and cancellation; animation is a presentation of a known before/after state and can be disabled in test mode.

### Contradiction B: GPU scale versus accessibility and test selectors

GPU rendering can draw dense scenes efficiently but does not inherently expose individual semantic objects. Resolution: the semantic mirror and stable ID registry are renderer-independent and remain live even when the visual surface is Canvas/WebGL/WebGPU.

### Contradiction C: generic graph flexibility versus domain safety

Libraries commonly allow arbitrary node/edge attributes. FGA needs extensibility, but arbitrary attributes can smuggle truth or actions into the renderer. Resolution: separate `domain`, `presentation`, `interaction` and `diagnostic` namespaces with schema validation and capability gates.

### Contradiction D: one graph view versus multiple representations

Node-link is visually central, but matrices, paths, tables and clusters can answer dense-graph questions better. Resolution: representations are projections with stable IDs and explicit return-to-graph actions; changing representation never creates a second source of truth.

### Contradiction E: independent engine versus reuse of mature algorithms

Reimplementing every layout and graph algorithm would be wasteful. Reusing a dependency can create license, build, runtime and maintenance coupling. Resolution: own the public interfaces and fixtures; use independently licensed algorithms only behind adapters after provenance, behavior and test audits; allow offline/reference implementations without making them domain authorities.

### Correction to the earlier synthesis

“SVG is the reference backend” is now refined to “SVG is the first correctness and semantic backend.” It is not a permanent performance promise. The engine should be able to run headless with no renderer at all, and it should be possible to test the semantic mirror and command journal without a DOM.

## 35. Research pass 10 — closure criteria for the current research phase

This is not a claim that graph visualization is exhausted. It is a closure rule for this research phase so that implementation can begin without pretending that unknowns are solved.

The current phase is complete enough to implement when:

- the layered data model and renderer contract are documented;
- commercial/reference ideas are separated from license-safe implementation inputs;
- context menus, node movement, LOD, accessibility and representation switching are explicit requirements;
- the autonomous test plan has independent state/event and semantic oracles;
- local fixtures cover empty, small, dense, dynamic, adversarial and long-label graphs;
- each rejected idea has a reason and a re-entry condition;
- unresolved claims are listed as experiments rather than prose assumptions;
- the local baseline remains green or failures are tracked with root cause.

The next work is implementation and measurement, not endless cataloguing. Future research should be triggered by a concrete unanswered question, a failing fixture, a new renderer backend or a real FGA workload—not by adding libraries without a decision consequence.

## 36. Final current synthesis

The proposed FGA graph engine is not “a better Cytoscape” or “a clone of a commercial diagramming SDK.” It is a task-specific visual investigation engine with a deliberately boring core and an expressive shell:

- boring core: versioned topology, stable IDs, typed projections, immutable views, deterministic commands and testable invariants;
- expressive shell: large graph canvas, node movement, evidence-aware symbols, contextual menus, inspector, minimap, LOD, path/cluster/matrix projections, keyboard navigation and polished transitions;
- measured rendering: SVG first for correctness, Canvas/GPU when the workload justifies it, with semantic fallback and diagnostics;
- autonomous proof: replayable command traces, property-based generators, contract tests, semantic assertions, visual baselines, performance repetitions, memory/lifecycle probes and structured manual exploration;
- clean-room posture: ideas and public behavior may inspire design, but code, restricted assets and incompatible licenses are not dependencies.

The central architectural sentence is now:

> The graph engine renders a versioned, evidence-safe projection and records every meaningful interaction; it never becomes the authority for the case itself.

## 37. Pass log after contradiction review

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 7 | Commercial/product UX | Extracted context menus, ports, groups, undo, LOD, property browsers and search-to-visualization as independent ideas; recorded license boundaries. | yes for research scope |
| 8 | Community feedback and maintenance | Converted recurring complaints into architecture responses and regression classes; separated issue evidence from defect-rate claims. | yes for research scope |
| 9 | Contradiction review | Resolved determinism/interactivity, GPU/accessibility, flexibility/safety, representation/identity and reuse/ownership tensions. | yes with open experiments |
| 10 | Closure criteria | Defined when research is implementation-ready and recorded remaining uncertainties. | yes for current phase |

## 38. Sources added in passes 7–10

- [yFiles interaction support](https://docs.yworks.com/yfileshtml/dguide/interaction-support)
- [yFiles features](https://docs.yworks.com/yfiles-html/dguide/features/index.html)
- [yFiles licensing](https://docs.yworks.com/yfiles-html/dguide/licensing/)
- [GoJS context menus](https://gojs.net/latest/learn/contextMenus)
- [GoJS deployment](https://gojs.net/latest/learn/deployment)
- [GoJS pricing and features](https://gojs.net/latest/pricing)
- [JointJS licensing](https://www.jointjs.com/license)
- [JointJS issue tracker](https://github.com/clientIO/joint/issues)
- [JointJS changelog](https://github.com/clientIO/joint/blob/master/CHANGELOG)
- [Neo4j graph visualization](https://neo4j.com/graph-visualization-neo4j/)
- [Neo4j Bloom user guide](https://neo4j.com/docs/bloom-user-guide/current/)
- [Neo4j visualization tools](https://neo4j.com/docs/getting-started/graph-visualization/graph-visualization-tools/)

## 39. Local validation log for the research pass

The dossier itself and the current FGA06 workspace were checked locally after the research additions.

| Check | Result | Notes |
|---|---|---|
| `npm run typecheck` in `apps/web` | PASS | TypeScript project compilation completed. |
| `npm test` in `apps/web` | PASS | 18 files, 33 tests passed. |
| `npm run qualification:build` | PASS | The four-engine exhibit builds; Vite reports only the existing large-chunk warning. |
| `npm run qualification:e2e` | PASS | 5 Playwright tests passed, including all engine tabs, lifecycle probes and contextual menus. |
| Research Markdown audit | PASS | 1,265 lines, no trailing whitespace, 105 Markdown links, 58 unique URLs. |
| `pytest -q tests/iteration_06` | PASS | 7 tests passed in 1.68 seconds. |
| Focused governance closure test | PASS | `test_qualified_candidate_and_evidence_only_closure_pass`, 1 test passed in 93.84 seconds. |
| `python scripts/run_iteration_06_local_gate.py` | PASS | Fixture hash `b70611256e3dfe5bf84664fe7a57298c2be22163fe53fc924c15917c735d3fef`; 4 candidates; profile `fga`; 44 objects; 32 tables; 13 idempotency packages. |

### 39.1 Incomplete global-suite run and root cause

The first full `python -m pytest -q` run exposed a real Markdown failure caused by 15 trailing-whitespace lines in this dossier. Those lines were corrected. The focused governance test then passed.

Two subsequent broad runs progressed beyond the original failure without another functional failure, but both became resource-heavy while repeatedly creating temporary validated repositories on Windows. One run reached approximately 48% and another approximately 53%, with the Python process growing beyond 1 GB of memory and no progress for over a minute. They were interrupted to protect the workspace. Therefore:

- the global suite is **not** claimed as complete in this pass;
- the original deterministic content failure is fixed and its focused regression passes;
- the web/qualification suite, Iteration 06 suite and local gate are green;
- the remaining test-infrastructure issue is to isolate or cap the memory/time cost of the broad governance subprocess tests.

This distinction is important for the engine design: autonomous tests must be complete and reproducible, but the runner itself must also have bounded resource behavior. A future `graph-testkit` should expose per-suite budgets, process cleanup, memory telemetry and resumable shards instead of requiring one unbounded command.

## 40. Remaining implementation experiments

The research is implementation-ready, but these questions remain empirical:

1. Which compact snapshot layout gives the best FGA trade-off between object ergonomics, worker transfer and renderer updates?
2. At what density and label complexity should FGA promote SVG to Canvas or GPU?
3. Which picking strategy gives acceptable p95 latency on the target browser while preserving edge and label context menus?
4. How much movement can be allowed before users lose the case’s mental map?
5. What semantic zoom levels are understandable for the T02 fraud fixture and the largest expected game scene?
6. Which open-source layout implementation is safe and maintainable enough for the first worker backend?
7. How should screenshot baselines be partitioned by browser/driver without producing maintenance noise?
8. How can the broad governance suite be sharded so that a single test run has a hard memory ceiling?

These are now explicit experiments with inputs, outputs and acceptance conditions. They are no longer hidden assumptions inside a library choice.

## 41. Research pass 11 — worker boundaries, transfer costs and ownership

The browser platform gives FGA several different ways to move graph work away from the main thread, but they have different correctness and deployment consequences.

### 41.1 Structured cloning is convenient but not free

The structured clone algorithm can copy plain objects, arrays, maps, sets and typed arrays across worker boundaries. It does not preserve functions, DOM nodes, private class state, property descriptors or prototype chains. This matters because a rich mutable graph object is a poor worker protocol: its behavior and identity do not survive the boundary in the way a renderer may expect.

Decision: the worker protocol uses plain, versioned messages and typed arrays or compact records for bulk data. It never sends a live graph instance or a renderer object. The receiver reconstructs an implementation-specific view from the message.

### 41.2 Transferable buffers change ownership

Transferable `ArrayBuffer` resources can move between contexts without copying, but the sender’s buffer becomes detached. That is useful for one-way worker pipelines, but dangerous for a shared snapshot that the main thread still needs to inspect for semantic assertions or replay.

FGA should distinguish:

- **snapshot messages:** cloned or immutable serialized records, safe to retain on both sides;
- **bulk work buffers:** transferable buffers with explicit ownership and lifecycle;
- **shared state:** an opt-in optimization only after race, security-header and fallback behavior are tested.

Every worker response must identify the graph version and request ID. A late response from an older graph version is discarded, not merged heuristically.

### 41.3 SharedArrayBuffer is an operational choice, not a free optimization

Shared memory requires cross-origin isolation in normal browser contexts. That brings deployment headers, iframe compatibility, security review and a separate fallback path. It can reduce copies, but introduces synchronization and race bugs that are harder to reproduce than message passing.

Decision: the first engine uses message passing and transferable buffers. `SharedArrayBuffer` is deferred until a measured workload proves that copying is a bottleneck and a deployment can guarantee cross-origin isolation.

Sources: [MDN structured clone](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm), [MDN transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects), [MDN SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer).

### 41.4 OffscreenCanvas can move pixels, not product responsibility

OffscreenCanvas can be transferred to a worker and used for rendering. This can keep expensive drawing away from the UI thread, but it does not provide semantic nodes, context-menu policy, keyboard navigation, stable test selectors or domain authority. Those remain main-thread engine responsibilities.

Decision: an OffscreenCanvas renderer may be an implementation of the visual backend contract, but the command journal, semantic mirror, capability tokens, focus policy and diagnostics remain renderer-independent.

Source: [MDN OffscreenCanvasRenderingContext2D](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvasRenderingContext2D).

### 41.5 Worker protocol proposed

```text
Request {
  requestId
  graphVersion
  operation: layout | query | hit-index | export
  snapshotEncoding: records | typed-buffers
  payload
  seed
  constraintsHash
  cancellationToken
}

Response {
  requestId
  graphVersion
  status: completed | cancelled | stale | failed
  result
  diagnostics
}
```

The test suite must include stale responses, cancellation during layout, detached buffers, malformed messages and worker restart. These cases are not edge decoration; they define whether a visual investigation remains trustworthy under interaction.

## 42. Research pass 12 — layouts, ports, routing and mental-map evidence

### 42.1 Ports are semantic presentation constraints

Research on layered drawing with port constraints shows that ports affect crossing minimization and edge routing, not only the final paint step. A port can express that a relationship enters from the left, exits from the right, belongs to a group or must remain attached to a specific visual socket.

For FGA, ports are useful when a node has multiple relationship roles: a device may have incoming account links on one side, outgoing merchant links on another, and evidence links attached to a dedicated “evidence” region. This can make direction and relationship type legible without relying on color.

The boundary is important: a port is not a new relationship and must not alter domain topology. It is a presentation constraint with a stable source relationship ID.

Source: [Drawing layered graphs with port constraints](https://doi.org/10.1016/j.jvlc.2013.11.005).

### 42.2 Stability is task-dependent, not always the primary objective

The literature on mental maps is not a license to freeze every node forever. A controlled study found that layout stability and adjacent highlighting can improve accuracy, sometimes at the cost of completion time, and that highlighting can outperform stability for many tasks except more complex ones. Another study reports that the value of preserving a mental map depends on the task and graph type.

FGA consequence: the layout policy needs a task profile:

- `orientation`: preserve stable anchors and neighborhood arrangement;
- `path-finding`: emphasize selected paths and adjacent relationships;
- `cluster-review`: preserve cluster identity but allow internal rearrangement;
- `dense-discovery`: allow representation switching or aggregation rather than forcing node-link stability;
- `manual-investigation`: respect pins and user movement above aesthetic optimization.

The engine should report the trade-off it chose instead of pretending that one stability scalar is universally correct.

Sources: [Evaluation of two interaction techniques for dynamic graphs](https://doi.org/10.48550/arXiv.1608.08936), [The “Map” in the mental map](https://doi.org/10.1016/j.ijhcs.2013.08.004).

### 42.3 Layout stitching suggests persistence for local exploration

Layout stitching research addresses the problem of revisiting a local view of a large graph and seeing a recognizable arrangement. It combines overlapping subgraph layouts to create a larger persistent layout, supporting orientation and recognition across navigation.

This is directly relevant to “expand neighbors” in FGA. If the user collapses a cluster, opens another neighborhood and later returns, the engine should not randomly reshuffle the same entities. A future `LayoutMemory` can retain anchor coordinates and overlap correspondences, while allowing new nodes to be inserted around a stable local frame.

Decision: add layout memory as an explicit optional subsystem, not as hidden force-simulation state. Its retention policy, privacy scope and invalidation reason must be inspectable.

Source: [Using Layout Stitching to create deterministic Local Graph Layouts](https://dspace.zcu.cz/items/74d59f72-91da-4002-abbf-c63a54787f7a).

### 42.4 Layout evaluation must use a portfolio of metrics and tasks

The systematic review of graph-layout evaluation found no single standard methodology across papers and catalogued differences in graph features, datasets, tasks, metrics and reporting. This supports the research decision to avoid an all-purpose “best layout” benchmark.

FGA should evaluate a layout against a scene-specific envelope:

- topology comprehension: can the intended path or neighborhood be followed;
- spatial stability: how much did unaffected content move;
- clutter: crossings, overlap, label collisions and ink density;
- interaction: drag, focus, menu and hit-test latency;
- semantics: whether stable IDs and relationship roles remain discoverable;
- resource budget: layout time, frame cost and memory.

Source: [Evaluating Graph Layout Algorithms: A Systematic Review](https://doi.org/10.1111/cgf.15073).

## 43. Research pass 13 — renderer scale and progressive degradation

### 43.1 MSAGL.js demonstrates an explicit split between small and large graphs

MSAGL.js exposes a core layout package, an SVG renderer for smaller editable graphs and a WebGL/deck.gl renderer for larger browsing workloads. Its documentation also exposes layout and routing options and warns that some advanced routing capabilities exist only on development branches or are expensive for large graphs.

This is a useful model for FGA: a backend should state which workload it is intended for, which features it degrades, and which routing modes are too expensive. “WebGL supported” is not enough; the product must explain whether edge labels, context menus, editing, accessibility and exports are equivalent.

Decision: add an explicit `CapabilityMatrix` to renderer diagnostics. It reports support for node/edge picking, labels, menus, semantic mirror, export, animation, edge routing, minimap and worker execution. A backend can be fast and still be rejected for a task if it lacks a required capability.

Sources: [MSAGL.js introduction](https://microsoft.github.io/msagljs/docs/intro/), [MSAGL.js getting started](https://microsoft.github.io/msagljs/docs/getting-started/), [MSAGL layout and routing guidance](https://github.com/microsoft/msagljs/blob/main/skills/msagljs/references/layout-and-routing.md).

### 43.2 Tile pyramids and sleeve routing are promising but not a first feature

Recent MSAGL work explores tile pyramids and sleeve routing for browser-based large-graph browsing. The idea is to precompute or construct multiscale representations so the viewport does not need to render every edge at every zoom level.

This is attractive for a future very large FGA case, but it introduces tile invalidation, cross-tile edge continuity, hit testing across levels, semantic synchronization and export complexity. The game’s first graph scenes are small enough that a correct semantic projection and robust context menus are more valuable.

Decision: keep multiscale tiles in the research queue with a re-entry condition: implement only when measured FGA scenes exceed the declared interaction envelope and aggregation/representation switching cannot solve the problem.

Source: [Browsing Large Graphs with Tile Pyramids and Sleeve Routing in the Browser](https://arxiv.org/abs/2605.17498).

### 43.3 WebGPU is powerful but does not solve layout, accessibility or product semantics

GraphWaGu demonstrates GPU-based graph layout and rendering with WebGPU, including force-directed and Barnes–Hut methods. Public implementation notes also expose browser and feature prerequisites. The research value is a data-parallel approach to layout and rendering; the product risk is assuming that high throughput automatically yields a usable investigation view.

FGA should treat WebGPU as one progressive renderer and possibly a compute backend. It must still use:

- explicit layout seeds and cancellation;
- semantic mirror and keyboard navigation;
- CPU/DOM picking fallback;
- capability diagnostics;
- deterministic fixture mode;
- a browser-compatible fallback when WebGPU is unavailable.

Sources: [GraphWaGu repository](https://github.com/harp-lab/GraphWaGu), [GraphWaGu paper](https://stevepetruzza.io/pubs/graphwagu/).

### 43.4 Progressive degradation policy

The engine should degrade by information priority, not by silently removing arbitrary features:

1. preserve identity, direction, status symbols, selection and semantic access;
2. reduce decorative effects, shadows and edge animation;
3. reduce label density using evidence-aware rules;
4. simplify routing from bundled/orthogonal to spline or straight lines;
5. aggregate low-priority nodes into explicit clusters;
6. switch representation if node-link is no longer task-effective;
7. preserve a static semantic/export fallback even when the visual GPU path fails.

Every degradation emits a diagnostic with reason, threshold, previous mode and recovery action. The user should never have to guess why a relationship disappeared.

## 44. Micro-experiment result — contract properties

The dependency-free experiment at [`experiments/engine_contract_experiment.py`](experiments/engine_contract_experiment.py) was run locally:

```text
status: PASS
projected_nodes: 2
projected_edges: 1
semantic_visual_id_sets_equal: true
unauthorized_command_dropped: true
```

It validates only contract properties, not renderer quality. It caught the intended design distinction between a projection and a mutable source graph, demonstrated deterministic replay, retained a pinned node, dropped an unauthorized annotation command and checked that the semantic mirror exposes the same stable IDs as the visual projection.

The experiment deliberately does not prove:

- frame-rate or memory envelopes;
- human readability;
- layout quality;
- browser accessibility tree behavior;
- concurrent worker correctness;
- the suitability of the toy circular layout.

Those require separate experiments and browser/worker harnesses.

## 45. Updated research ledger — continuation

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-018 | Should workers receive rich graph objects? | Structured clone loses functions, prototypes and DOM state; transferable buffers change ownership. | Use versioned plain messages and explicit buffer ownership. |
| R-019 | Should FGA start with shared memory? | SharedArrayBuffer requires cross-origin isolation and synchronization. | Defer until measured copy cost and deployment headers are acceptable. |
| R-020 | Are ports only a visual detail? | Port-constraint research changes crossing minimization and routing. | Model ports as typed presentation constraints linked to relationship IDs. |
| R-021 | Should layout always maximize stability? | Dynamic-graph studies show task-dependent trade-offs. | Select layout policy by task profile and report the trade-off. |
| R-022 | How can local exploration remain recognizable? | Layout stitching preserves overlapping local layouts. | Prototype `LayoutMemory` with explicit retention and invalidation. |
| R-023 | Does WebGL/WebGPU solve large-graph UX? | MSAGL and GraphWaGu show scale techniques; semantic and layout problems remain. | Require capability matrices and progressive degradation. |
| R-024 | Can the architecture be tested without a renderer? | Local contract experiment passes projection, replay, capability and semantic-ID properties. | Expand into property-based generators and worker message tests. |

## 46. Updated pass log — continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 11 | Worker boundaries and ownership | Added structured-clone, transferable-buffer, SharedArrayBuffer and OffscreenCanvas analysis; specified a versioned worker protocol. | yes for research scope |
| 12 | Layout constraints and mental maps | Added ports, task-dependent stability, layout stitching and portfolio evaluation metrics. | yes with layout experiments open |
| 13 | Renderer scale and degradation | Added MSAGL, tile pyramids, GraphWaGu and capability-based degradation policy. | yes with scale experiments open |
| 14 | Contract micro-experiment | Added and ran a dependency-free experiment for projection, replay, capability gating and semantic/visual ID parity. | yes for tested properties |

## 47. Sources added in the continuation

- [Drawing layered graphs with port constraints](https://doi.org/10.1016/j.jvlc.2013.11.005)
- [The “Map” in the mental map](https://doi.org/10.1016/j.ijhcs.2013.08.004)
- [Using Layout Stitching to create deterministic Local Graph Layouts](https://dspace.zcu.cz/items/74d59f72-91da-4002-abbf-c63a54787f7a)
- [MDN structured clone](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm)
- [MDN transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects)
- [MDN SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)
- [MDN OffscreenCanvas](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvasRenderingContext2D)
- [MSAGL.js introduction](https://microsoft.github.io/msagljs/docs/intro/)
- [MSAGL.js getting started](https://microsoft.github.io/msagljs/docs/getting-started/)
- [MSAGL layout and routing guidance](https://github.com/microsoft/msagljs/blob/main/skills/msagljs/references/layout-and-routing.md)
- [Browsing large graphs with tile pyramids](https://arxiv.org/abs/2605.17498)
- [GraphWaGu repository](https://github.com/harp-lab/GraphWaGu)
- [GraphWaGu paper](https://stevepetruzza.io/pubs/graphwagu/)

## 48. Research pass 15 — compact graph cores from C, C++, Python and Rust

This pass revisits non-JavaScript ecosystems specifically for data-structure ideas, not for browser dependencies.

### 48.1 graph-tool: property maps and compile-time specialization

graph-tool is a Python module whose core data structures and algorithms are implemented in C++ with template metaprogramming and the Boost Graph Library. Its documentation exposes graph property maps and an efficient core, while retaining Python usability for analysis.

The transferable idea is to keep a high-level authoring surface while allowing a compact, specialized representation underneath. The risk is that template-heavy or native-bound designs can be difficult to ship in a browser and difficult to inspect in a deterministic test.

FGA decision: use an explicit “friendly contract versus packed execution view” boundary. Do not expose native/internal indices as user-facing IDs. Test serialization and replay against the contract rather than against memory layout.

Source: [graph-tool documentation](https://graph-tool.skewed.de/static/docs/stable/index.html), [graph-tool core API](https://graph-tool.skewed.de/static/docs/stable/graph_tool.html).

### 48.2 igraph: attribute handlers and a broad algorithm surface

igraph provides a C core with interfaces in Python, R and other environments. Its reference manual covers graph, vertex and edge attributes, selectors, iterators, generators, graph operators, visitors, layouts, structural algorithms, community detection and I/O. Attributes are abstracted through an attribute-handler interface, allowing different storage implementations.

The strong idea is that attribute storage is a replaceable service rather than a fixed field layout. The caution is licensing and scope: a broad algorithm library does not automatically provide the product-level interaction, semantics or accessibility FGA needs.

FGA decision: treat graph algorithms as services over a typed property capability. Keep renderer fields out of the graph algorithm API and use adapters only when the dependency’s license and bundle size are acceptable.

Sources: [igraph C reference manual](https://igraph.org/c/html/main/), [igraph attributes](https://igraph.org/c/html/develop/igraph-Attributes.html), [igraph overview paper](https://arxiv.org/abs/2311.10260).

### 48.3 NetworKit: parallel algorithm engineering is a separate concern

NetworKit targets network analysis from thousands to billions of edges, with performance-aware algorithms written in C++ and exposed to Python through Cython. Its focus is parallel algorithm engineering, standard network measures and interactive analysis workflows.

The important lesson is that graph analytics and visual presentation have different scaling bottlenecks. A graph engine should not make the renderer calculate centrality, clustering or path metrics synchronously on pointer movement. FGA should schedule expensive analytics as cancellable jobs and render the results as versioned derived properties.

Decision: add an `AnalyticsReceipt` containing graph version, algorithm, parameters, duration, cancellation status and result schema. A stale analytics result cannot silently color nodes in a newer graph.

Source: [NetworKit official site](https://networkit.github.io/), [NetworKit repository](https://github.com/networkit/networkit).

### 48.4 petgraph: compact indices are not stable identity

petgraph provides directed and undirected graphs, multiple graph types, algorithm traits, DOT integration and compact node/edge indices. Its documentation explicitly notes that ordinary graph indices may shift when nodes or edges are removed, while `StableGraph` exists for a different stability trade-off.

This is a decisive FGA distinction:

- internal compact indices are ideal for dense arrays, typed buffers and fast traversal;
- external stable IDs are required for evidence, menus, replay, semantic navigation and cross-renderer selection;
- a mapping layer must survive compaction, filtering, worker transfer and renderer replacement.

FGA decision: use `StableId <-> DenseIndex` maps per snapshot. Never serialize or expose a dense index as an evidence identifier. Mutation or compaction invalidates the index map but not the stable ID.

Source: [petgraph graph data structure](https://docs.rs/petgraph/latest/petgraph/graph/struct.Graph.html), [petgraph project](https://github.com/petgraph/petgraph).

### 48.5 Core representation proposal after the comparison

```text
External contract:
  StableId, RelationshipId, GraphVersion, semantic/domain fields

Snapshot index:
  stableIdToDenseIndex
  denseIndexToStableId
  dense source/target arrays
  adjacency offsets and neighbor arrays

Attribute planes:
  domain read-only records
  presentation records
  transient interaction arrays
  analytics receipts/results

Renderer planes:
  positions, sizes, visibility, label slots, picking IDs
```

The engine can use object records during development and packed arrays for large scenes without changing the external contract. The mapping layer is the test seam. A property-based test should randomly remove, filter, compact, serialize and reload graphs while asserting stable-ID parity.

## 49. New open questions after pass 15

- Should `StableId` be globally unique strings, scoped numeric IDs plus namespace, or opaque branded values in TypeScript?
- Which packed adjacency representation supports the required dynamic updates without frequent full rebuilds?
- Should the layout worker receive dense arrays directly, or a compact binary format with schema versioning?
- How should removed nodes appear in a replay so that old menu events fail safely rather than target a reused index?
- Can analytics results be streamed incrementally while retaining a single graph-version oracle?

These questions are implementation experiments, not reasons to pull a general-purpose graph library into the domain core.

## 50. Updated research ledger — data-core continuation

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-025 | Are dense indices safe as graph identity? | petgraph indices can shift on removal; stable variants trade flexibility for stability. | Keep opaque stable IDs at the contract boundary and remap dense indices per snapshot. |
| R-026 | How can a high-level API coexist with compact storage? | graph-tool and igraph separate user-facing bindings from specialized cores/property handlers. | Separate contract records from packed execution views. |
| R-027 | Where should analytics run? | NetworKit separates parallel analytics from Python interaction. | Use cancellable versioned analytics receipts, never synchronous pointer work. |
| R-028 | Are attributes part of graph topology? | igraph attribute handlers and BGL property maps make storage replaceable. | Keep domain, presentation, transient and analytics planes distinct. |

## 51. Updated pass log — data-core continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 15 | Compact cores and non-JavaScript ecosystems | Added graph-tool, igraph, NetworKit and petgraph; corrected the stable-ID versus dense-index boundary and proposed packed snapshot planes. | yes with implementation experiments open |

## 52. Sources added in pass 15

- [graph-tool](https://graph-tool.skewed.de/static/docs/stable/index.html)
- [graph-tool core API](https://graph-tool.skewed.de/static/docs/stable/graph_tool.html)
- [igraph C reference](https://igraph.org/c/html/main/)
- [igraph attributes](https://igraph.org/c/html/develop/igraph-Attributes.html)
- [igraph overview paper](https://arxiv.org/abs/2311.10260)
- [NetworKit](https://networkit.github.io/)
- [NetworKit repository](https://github.com/networkit/networkit)
- [petgraph graph data structure](https://docs.rs/petgraph/latest/petgraph/graph/struct.Graph.html)
- [petgraph repository](https://github.com/petgraph/petgraph)

## 53. Research pass 16 — non-JavaScript complaints and maintenance evidence

The non-JavaScript projects show the same pattern as the browser libraries: the useful abstractions are strong, but the failure modes move to build systems, bindings, indices, memory ownership and platform-specific behavior.

### 53.1 Graphology: convenience APIs can hide allocation costs

An open Graphology issue discusses optimizing shortest-path code by reducing array-method allocations and costly lookups. This is not evidence that Graphology is generally slow; it is evidence that high-level convenience code can become a hot path when an algorithm is invoked repeatedly.

FGA response: algorithm implementations must expose allocation and cache diagnostics in research mode. A renderer must not call a convenience traversal on every pointer move. Precompute neighborhood indexes or use a bounded query job.

Source: [Graphology shortest-path optimization issue](https://github.com/graphology/graphology/issues/335).

### 53.2 NetworKit: native speed brings native failure surfaces

The public NetworKit issue tracker includes reports involving segmentation faults, invalid input dtypes, Python-version support and dynamic algorithm tests. These reports do not invalidate NetworKit’s performance model; they show that Python bindings and native kernels require strict input validation, version matrices and failure containment.

FGA response: if a native/WASM algorithm backend is adopted, it must be treated as an isolated worker capability. The core engine needs a safe fallback and must convert native failure into a diagnostic, not a lost investigation state.

Source: [NetworKit issue tracker](https://github.com/networkit/networkit/issues).

### 53.3 igraph: changelogs are part of the algorithm contract

igraph’s changelog records fixes involving layout coordinates, large GraphML input, memory leaks, interruptibility, edge ordering, attribute preservation and numerical convergence. This is a useful reminder that graph algorithms have operational contracts beyond their mathematical names.

FGA response: each layout/analytics adapter gets a versioned behavior record and fixtures for null graphs, edgeless graphs, repeated IDs, large input, interruption, disconnected components and attribute preservation. The engine must pin and periodically requalify adapters.

Source: [igraph changelog](https://github.com/igraph/igraph/blob/main/CHANGELOG.md).

### 53.4 petgraph: contribution culture reinforces regression discipline

petgraph’s contribution guidance asks for benchmarks for performance changes, tests, documentation, generic graph traits and multiple toolchain coverage. That is directly compatible with FGA’s desire to make every performance or rendering claim testable.

FGA response: performance work is accepted only with a reproducible fixture, baseline, environment, variance and regression threshold. A faster path without a semantic oracle is not an engine improvement.

Source: [petgraph contribution and testing guidance](https://github.com/petgraph/petgraph/blob/master/CONTRIBUTING.md).

### 53.5 Maintenance signals to record per adapter

The research ledger now adds these adapter-health fields:

- native/runtime boundary and failure containment;
- input-validation behavior;
- cancellation and interruption support;
- allocation/cache profile;
- release and compatibility matrix;
- regression-test expectations;
- stable-ID and attribute-preservation behavior;
- export and serialization fidelity;
- fallback strategy when the adapter is unavailable.

The result is a dependency dossier that is useful even if FGA later chooses to reimplement the idea rather than take the library.

## 54. Updated research ledger — maintenance continuation

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-029 | Can high-level graph convenience hide hot-path allocation? | Graphology shortest-path optimization discussion. | Add allocation/cache telemetry and keep pointer interaction off algorithm hot paths. |
| R-030 | Does native performance reduce operational risk? | NetworKit issues show input, crash and binding-version failure classes. | Isolate native/WASM adapters behind workers and explicit fallbacks. |
| R-031 | Are algorithm names enough for compatibility? | igraph changelog documents changes in layout, interruption, memory and attribute behavior. | Pin versions and qualify behavioral fixtures, not just API signatures. |
| R-032 | What should a performance contribution prove? | petgraph requires benchmarks, tests, docs and toolchain coverage. | Require a fixture, variance, semantic oracle and regression threshold. |

## 55. Updated pass log — maintenance continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 16 | Non-JavaScript issues and maintenance | Added complaints and changelog signals from Graphology, NetworKit, igraph and petgraph; expanded adapter-health criteria. | yes with adapter experiments open |

## 56. Sources added in pass 16

- [Graphology shortest-path optimization issue](https://github.com/graphology/graphology/issues/335)
- [NetworKit issue tracker](https://github.com/networkit/networkit/issues)
- [igraph changelog](https://github.com/igraph/igraph/blob/main/CHANGELOG.md)
- [petgraph contributing and testing](https://github.com/petgraph/petgraph/blob/master/CONTRIBUTING.md)

## 57. Research pass 17 — bounded autonomous test execution

The broad Python suite exposed a second-order failure: a test strategy can be logically comprehensive yet operationally unsafe if one process accumulates temporary repositories, subprocess state or native allocations.

### 57.1 Sharding is a correctness feature

The experimental runner [`run_pytest_shards.py`](experiments/run_pytest_shards.py) executes test groups in independent subprocesses, applies a timeout per shard and returns machine-readable results. A targeted run against `tests/iteration_06` passed with 7 tests.

The full shard run was intentionally stopped after a child process exceeded roughly 3 GB of working-set memory. This is not a reason to hide the test; it is evidence that the governance shard needs further isolation, smaller cases or explicit cleanup. The runner itself successfully avoided orphaned Python processes after interruption.

### 57.2 Test architecture requirements refined

The autonomous test system must include:

- deterministic fixture and random seeds;
- test groups that can run independently;
- hard timeouts and process cleanup;
- memory and CPU telemetry per group;
- JSON summaries with stdout/stderr tails;
- resumable execution from the first failing shard;
- semantic/event checks independent of screenshots;
- explicit reports when a shard is incomplete or resource-bound;
- no global mutable server or browser state shared across shards;
- a release gate that refuses to interpret timeout as pass.

### 57.3 What remains to fix in the current project suite

The current governance tests create temporary copies and launch full validators. The next engineering task is to profile the individual test cases inside the governance shard, identify the subprocess or fixture that retains memory, and split it into smaller scenario shards. Candidate mitigations include:

1. run one repository fixture per subprocess;
2. remove generated evidence before the next scenario;
3. use a test-only reduced validator for unit-level cases;
4. keep one integration test for the full validator path;
5. record peak RSS and child process counts;
6. run the heaviest cases in a separate CI job with a larger but explicit budget.

This is a direct example of the design principle that the test harness is part of the system, not an afterthought.

## 58. Updated research ledger — test execution continuation

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-033 | Can broad autonomous tests run in one process safely? | Full suite and shard runner exposed memory growth above 1–3 GB in governance scenarios. | Use isolated shards and treat resource limits as test failures. |
| R-034 | Does process isolation alone solve the issue? | The targeted Iteration 06 shard passed; the governance shard still grew substantially. | Profile and subdivide the governance scenarios. |
| R-035 | Can partial results be machine-readable? | The shard runner returned status, duration, return code and output tail as JSON. | Integrate the format into future graph-testkit gates. |

## 59. Updated pass log — bounded testing

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 17 | Test-runner resilience | Added an isolated shard runner, ran the Iteration 06 shard successfully and recorded the global governance memory blocker. | clean for runner behavior; project suite blocker remains |

## 60. Sources and experiment artifacts added in pass 17

- [Isolated shard runner](experiments/run_pytest_shards.py)
- [Contract micro-experiment](experiments/engine_contract_experiment.py)

## 61. Research pass 18 — context menus, direct manipulation and keyboard parity

The request for “cool” context menus needs a stronger definition than animation and icons. The menu is part of the investigation interaction model, and its keyboard/semantic behavior must be equivalent to the pointer path.

### 61.1 A context menu is a command surface, not a bag of buttons

The WAI-ARIA Authoring Practices describe context menus as menus opened by a context-specific command such as `Shift+F10`, with focus entering the menu and `Escape` returning it to the invoking context. Arrow-key navigation, disabled-but-focusable items and submenu behavior are part of the interaction contract.

FGA menu requirements:

- right-click, long press, keyboard context-menu key and `Shift+F10` invoke the same command;
- the menu records target stable ID, graph version, selection and capability tokens;
- opening the menu freezes the target context; a stale command is rejected if the graph version or selection changed;
- focus moves into the menu and returns to the invoking graph item after dismissal;
- disabled commands explain why they are unavailable rather than disappearing silently;
- icons and color supplement readable labels and status text;
- menu actions emit typed intents and never call a provider directly.

Source: [WAI-ARIA Menu and Menubar Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/).

### 61.2 Graph semantics need a navigation model, not only ARIA labels

The WAI-ARIA treegrid pattern demonstrates a useful model for hierarchical, interactive data: rows/cells have explicit focus behavior, expand/collapse commands, selection semantics and predictable arrow-key navigation. FGA is not a treegrid, but the semantic mirror can borrow the discipline:

- `Tab` enters the graph once rather than forcing every node into the page tab order;
- arrow keys move through a deterministic adjacency or spatial order;
- `Enter` opens the selected node’s details or expands a projection;
- `Shift+F10` opens the contextual menu;
- `Escape` exits menu/focus modes without losing selection;
- `Home`/`End` and search provide escape hatches for large scenes;
- relationships are navigable objects, not only implied by a node’s text.

Source: [WAI-ARIA Treegrid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/).

### 61.3 Direct manipulation must disclose what will change

Research on direct visual editing argues that changing a graphical encoding can provide immediate feedback in local and global context, but also highlights the need to distinguish intentional manipulation from accidental dragging. A long press or explicit drag affordance can help separate selection from movement.

FGA consequence: dragging a node changes presentation state only and must show a movement receipt in the flight recorder. It must not modify evidence, relationship direction or fraud status. For touch, use a deliberate press threshold and a visible “move mode” affordance; for pointer, preserve click-to-select and drag-to-move without making a tiny pointer jitter into a layout command.

Source: [Direct Visual Editing of Node Attributes in Graphs](https://www.mdpi.com/2227-9709/3/4/17).

### 61.4 Brushing and linking should connect views without multiplying truth

The visual analytics literature treats brushing and linking as a way to select objects in one view and update related views. For FGA, that means selecting a node in node-link view can highlight the same stable IDs in a path view, matrix view, table, minimap and semantic mirror.

Decision: selection is a versioned set of stable IDs in the interaction state. Each representation derives its own highlight, and no representation owns or rewrites the selection. The test oracle checks cross-view ID parity.

Source: [Towards Ubiquitous Brushing for Information Visualization](https://www.cs.kent.ac.uk/pubs/2006/2437/index.html).

### 61.5 Context-menu design for FGA

The proposed menu groups actions by investigation intent, not by internal APIs:

```text
Inspect
  Open evidence summary
  Show relationships
  Show in semantic navigator

Explore
  Expand neighbors
  Find paths to selected
  Focus this cluster
  Switch representation

Presentation
  Pin / unpin
  Hide / reveal in this view
  Change label density
  Copy stable ID

Investigation record
  Add note
  Record current scene
  Compare with previous scene
```

Actions that require game authority are not presentational capabilities and must be supplied by the game shell, not invented by the graph renderer. A future game-specific menu may add “reopen case” or “spend credit” only through an explicit external capability.

## 62. Updated research ledger — interaction continuation

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-036 | What makes a context menu autonomous-testable? | WAI-ARIA specifies invoking context, focus, arrows and Escape; stale target behavior is an FGA concern. | Test pointer, touch and keyboard invocation against the same command trace. |
| R-037 | How should a graph be navigable without pointer? | Treegrid pattern provides explicit focus, expand/collapse and selection discipline. | Implement a semantic graph navigator with deterministic adjacency ordering. |
| R-038 | How should dragging avoid accidental domain mutation? | Direct manipulation research and current FGA authority boundary. | Movement is a presentation command with threshold, receipt and undo. |
| R-039 | How can multiple representations stay coherent? | Brushing and linking literature. | Keep one stable-ID selection set and assert cross-view parity. |

## 63. Updated pass log — interaction continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 18 | Context menus and direct manipulation | Converted “cool menus” into an accessible, capability-gated command surface with keyboard/touch parity and cross-view selection rules. | yes with browser interaction tests open |

## 64. Sources added in pass 18

- [WAI-ARIA Menu and Menubar Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/)
- [WAI-ARIA Treegrid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/)
- [Direct Visual Editing of Node Attributes in Graphs](https://www.mdpi.com/2227-9709/3/4/17)
- [Towards Ubiquitous Brushing for Information Visualization](https://www.cs.kent.ac.uk/pubs/2006/2437/index.html)

## 65. Research pass 19 — audit of the current FGA06 exhibit versus the target engine

The current qualification exhibit and the proposed engine must not be conflated.

### 65.1 What the current exhibit already proves

- four renderer adapters can consume a shared 18-node/26-edge fixture;
- stable FGA IDs survive the adapter boundary;
- node and relationship selection can be probed automatically;
- hover/selection details can be shown in a shared inspector;
- filters, legend, minimap, fit/zoom/reset and contextual detail cards are exposed;
- lifecycle and selection probes run through the browser test suite;
- SVG provides a semantic reference path, while Cytoscape, Sigma, D3 and React Flow remain comparison adapters.

### 65.2 What the current exhibit does not yet prove

Source inspection shows that the “context menu” is currently an inspector card rendered after hover/selection, not a target-anchored menu with a WAI-ARIA menu interaction model. The adapters expose selection and some hover callbacks, but there is no renderer-neutral drag command with movement provenance and replay. D3/SVG support Enter/Space selection, but the shared graph contract does not yet expose `Shift+F10`, menu focus return, keyboard adjacency navigation or stale command rejection.

This is not a defect in the qualification exhibit’s stated purpose. It is a boundary correction:

```text
Qualification exhibit:
  compare adapters and demonstrate shared fixture behavior

Target FGA engine:
  own snapshots, commands, menus, movement, semantics, replay and renderer policy
```

### 65.3 Required implementation increments

1. Add a renderer-neutral `PointerTarget` and `KeyboardTarget` contract.
2. Add a target-anchored context-menu controller with a DOM fallback for clipping.
3. Add `MoveNodeStart`, `MoveNode`, `MoveNodeCommit` and `MoveNodeCancel` commands.
4. Add stable `graphVersion` and `selectionVersion` to menu actions.
5. Add keyboard adjacency traversal and `Shift+F10` tests.
6. Add movement receipts and deterministic replay fixtures.
7. Add cross-renderer contract tests; do not infer behavior from the current adapter’s default drag implementation.

### 65.4 Rejection of a misleading completion claim

The research dossier must not say “context menus and movable nodes are implemented” merely because one adapter or an inspector card can display context-like information. The accurate claim is: “the qualification exhibit demonstrates contextual inspection and adapter interaction; the target engine specification now defines the stronger menu and movement contract, which remains to be implemented and tested.”

## 66. Updated research ledger — current implementation boundary

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-040 | Is the current inspector card a full context menu? | Current exhibit source renders a context card in the inspector and binds action buttons there. | Keep it as a qualification affordance; implement a real target-anchored menu in the engine. |
| R-041 | Is node movement a shared contract? | Adapters expose preset positions and selection, but no common movement journal/receipt. | Add explicit movement commands and replay tests before claiming support. |
| R-042 | Is keyboard parity complete? | SVG/D3 support selection keys; shared menu/focus/adjacency contract is absent. | Add WAI-ARIA menu and semantic navigation tests. |

## 67. Updated pass log — current implementation audit

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 19 | Source audit of the current exhibit | Corrected the distinction between adapter qualification and the target engine; recorded missing drag/menu/replay contracts and the implementation increments. | yes for audit; implementation gaps remain |

## 68. Research pass 20 — interaction should follow investigation tasks

The latest literature suggests that a graph UI should be designed around user intent—select, explore, reconfigure, encode, abstract/elaborate, filter and connect—rather than around the renderer’s event names.

### 68.1 Contextual edge inspection is a first-class task

The “Unfolding Edges” work treats an edge as a target that may need its own contextual explanation. It proposes highlighting relevant edges, panning and zooming, relocating obscured elements, dragging nodes to resolve occlusion, and revealing edge context on demand.

FGA consequence: an edge menu must not be a reduced version of the node menu. It needs relationship-specific actions:

- inspect source and destination;
- show relationship provenance and confidence;
- highlight adjacent relationships;
- unfold a detail card without destroying the surrounding graph;
- trace the relationship in a path or table view;
- pin or dismiss the contextual detail;
- return focus to the exact edge after dismissal.

Source: [Unfolding Edges: Adding Context to Edges in Multivariate Graph Visualization](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.14831).

### 68.2 History is more than undo

The CGV system combines multiple coordinated views, dynamic filtering, graph lenses, edge-based navigation, a radar view and an interaction history. A graphical-history paper argues that interaction history can support analysis, communication and evaluation, not only reversal.

FGA should therefore distinguish:

- **undo/redo:** reversible command stack for presentation and authorized changes;
- **scene history:** named snapshots that can be compared or reopened;
- **flight recorder:** low-level diagnostic event stream for reproduction;
- **evidence notes:** user-authored investigation record, never silently deleted by undo.

This separation prevents the common mistake of treating a single undo stack as the entire investigation history.

Sources: [CGV interactive graph visualization system](https://doi.org/10.1016/j.cag.2009.06.002), [Graphical Histories for Visualization](https://idl.uw.edu/papers/graphical-histories).

### 68.3 Coordinated views need shared selection and independent focus

Research on linked node-link and matrix visualizations supports combining representations during dynamic graph exploration. The node-link view can provide topology and path context while a matrix can make dense adjacency easier to inspect.

FGA consequence: each view has its own camera/focus and detail policy, but they share stable selection, graph version and command provenance. Selecting an edge in the matrix must focus the corresponding edge in node-link view; changing camera position in one view must not silently change the selected IDs in another.

Source: [Dynamic graph exploration by interactively linked node-link diagrams and matrix visualizations](https://pmc.ncbi.nlm.nih.gov/articles/PMC8423958/).

### 68.4 Natural-language commands are an optional command front-end, not the engine

A recent study comparing GUI, textual command and natural-language interaction for editing visual knowledge graphs reports that context popups, highlights and undo remain important in the GUI condition. It also logs operations and processing time, which is useful for evaluating command-based interaction.

FGA may eventually offer a typed search/command bar, but it must compile into the same validated intent model as menus and keyboard actions. Natural language must not bypass capability checks, graph-version checks or replay logging.

Source: [Natural Language Interaction for Editing Visual Knowledge Graphs](https://doi.org/10.1145/3731443.3771344).

## 69. Research pass 21 — interaction-contract micro-experiment

The new dependency-free experiment at [`experiments/interaction_contract_experiment.py`](experiments/interaction_contract_experiment.py) was run locally and passed:

```text
status: PASS
pointer_keyboard_equivalent: true
stale_menu_rejected: true
movement_cancel_restored: true
movement_commit_applied: true
cross_representation_selection_equal: true
stale_worker_response_rejected: true
```

This closes several design assumptions at the pure-command level:

- pointer and keyboard invocation can converge on one command path;
- a menu opened against an old selection cannot act on a new selection;
- node movement has a preview phase and explicit commit/cancel semantics;
- the same stable selection projects to node-link, matrix, path and semantic views;
- a worker result from an old graph version is rejected.

It does not close browser focus, pointer geometry, screen-reader output, race timing or visual quality. Those remain browser/renderer tests.

## 70. Research pass 22 — design corrections after the interaction experiment

The experiment exposed two refinements that were not explicit enough before:

### 70.1 Selection version is separate from graph version

A graph can remain unchanged while the user’s selection changes. Menu commands therefore need both `graphVersion` and `selectionVersion`. Checking only graph version would allow a menu opened for one selection to act after another selection is active.

### 70.2 Movement preview is not a mutation

Pointer movement during a drag is a preview state. Only `MoveNodeCommit` enters the replayable presentation journal. `MoveNodeCancel` restores the original position, and losing focus or pressing Escape must cancel the preview rather than commit it.

### 70.3 Edge context needs its own focus target

An edge’s source and destination are related objects, but they do not replace the edge as the focus return target. The menu and semantic mirror must preserve the edge ID so that dismissing its context does not strand the user at an endpoint.

## 71. Updated research ledger — interaction experiments

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-043 | Does an edge need a first-class context experience? | Unfolding Edges identifies edge-specific selection, context unfolding and occlusion strategies. | Add edge menus, focus return and edge-context fixtures. |
| R-044 | Is undo enough for investigation history? | CGV and graphical-history research distinguish history, analysis and reversal. | Maintain separate command stack, scene history and flight recorder. |
| R-045 | Can coordinated views remain coherent? | Linked node-link/matrix exploration and local experiment. | Share stable selection/version; isolate each view’s camera and detail state. |
| R-046 | Is a natural-language interface an engine feature? | Recent user study compares GUI/context popups, textual commands and natural language. | Treat language as an optional validated command front-end. |
| R-047 | What version checks do menus require? | Interaction experiment found graph version alone insufficient. | Require graph and selection versions for menu invocation. |
| R-048 | What counts as a movement mutation? | Interaction experiment separates preview, commit and cancel. | Journal only committed movement; cancel on Escape/blur/focus loss. |

## 72. Updated pass log — interaction continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 20 | Investigation task model | Added edge-specific context, history layers, coordinated views and optional command-bar research. | yes with browser studies open |
| 21 | Interaction contract experiment | Passed pointer/keyboard equivalence, stale menu rejection, movement commit/cancel, selection parity and stale worker rejection. | yes for pure-command properties |
| 22 | Contract correction | Separated graph and selection versions; made movement preview non-mutating; made edge focus first-class. | yes with browser tests open |

## 73. Sources and artifacts added in passes 20–22

- [Unfolding Edges](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.14831)
- [CGV interactive graph visualization system](https://doi.org/10.1016/j.cag.2009.06.002)
- [Graphical Histories for Visualization](https://idl.uw.edu/papers/graphical-histories)
- [Dynamic graph exploration with node-link and matrix views](https://pmc.ncbi.nlm.nih.gov/articles/PMC8423958/)
- [Natural Language Interaction for Editing Visual Knowledge Graphs](https://doi.org/10.1145/3731443.3771344)
- [Interaction contract experiment](experiments/interaction_contract_experiment.py)

## 74. Research pass 23 — reproducibility and local closure

The interaction continuation was re-run after the dossier update rather than relying on the first output.

### 74.1 Dependency-free experiments

`engine_contract_experiment.py` passed with deterministic projection, layout and replay digests:

```json
{"layout_digest": "c3418378aae7b8de", "projected_edges": 1, "projected_nodes": 2, "replay_digest": "c302be370babbcb7", "semantic_visual_id_sets_equal": true, "snapshot_version": "T02:v1", "status": "PASS", "unauthorized_command_dropped": true}
```

`interaction_contract_experiment.py` passed the interaction properties:

```json
{"cross_representation_selection_equal": true, "movement_cancel_restored": true, "movement_commit_applied": true, "pointer_keyboard_equivalent": true, "stale_menu_rejected": true, "stale_worker_response_rejected": true, "status": "PASS"}
```

All three experiment scripts compile with `py_compile`.

### 74.2 Isolated FGA-06 test shard

The subprocess-isolated runner passed `tests/iteration_06` without invoking Databricks:

```text
status: PASS
shard: tests/iteration_06
duration: 5.909 seconds
result: 7 passed in 1.87s
timeout: 60 seconds per shard
```

The runner is useful for bounded autonomous execution, but it does not make the entire repository suite safe. Earlier full-suite attempts still became memory-heavy before completion; that remains a test-infrastructure issue to solve separately.

### 74.3 Dossier integrity

The Markdown audit reports 2,054 lines, 207 Markdown links, 105 unique URLs, zero trailing-whitespace lines and all sections 68–73 present. This is a structural check, not a claim that every external URL is permanently available.

## 75. Updated research ledger — reproducibility boundary

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-049 | Are the engine and interaction contracts reproducible locally? | Both dependency-free experiments returned `status: PASS`; their scripts compile. | Keep them as deterministic contract fixtures and add browser implementations against the same assertions. |
| R-050 | Is the FGA-06 test shard bounded and isolated? | The subprocess runner completed `tests/iteration_06` with 7 passing tests under a 60-second child timeout. | Use shard execution for local iteration; redesign the global pytest collection/execution path before claiming repository-wide green. |
| R-051 | Does dossier integrity imply research completeness? | Link/whitespace/section audit passes, while browser and external-source checks remain open. | Report structural closure separately from implementation and evidence closure. |

## 76. Updated pass log — reproducibility closure

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 23 | Re-run and integrity audit | Reproduced both contract experiments, compiled all experiment scripts, passed the isolated FGA-06 shard and verified dossier structure. | yes for local contract scope; browser, race, accessibility and global-suite work remain |

## 77. Current honest status after this continuation

The research record now supports a more precise implementation boundary:

```text
Proven locally:
  projection and capability filtering at the pure-command level
  deterministic layout/replay fixtures
  pointer/keyboard command convergence
  stale menu and stale worker rejection
  movement preview/commit/cancel semantics
  cross-representation stable selection
  isolated FGA-06 test execution

Not yet proven:
  target-anchored browser menus with focus return and clipping behavior
  real pointer geometry, drag cancellation and blur handling in each renderer
  screen-reader announcements and keyboard adjacency traversal in the app
  browser-level stale-response races
  repository-wide pytest completion under a bounded memory budget
```

The next implementation increment should be a renderer-neutral interaction controller plus browser contract tests, not another adapter-specific visual flourish. The dossier should retain this distinction until those tests exist.

## 78. Research pass 24 — examples as executable architecture

The project now has a renderer-neutral example catalogue at [`apps/web/src/graph-engine/examples.ts`](../../../apps/web/src/graph-engine/examples.ts), with documentation in [`docs/iteration-06/examples/README.md`](../examples/README.md).

The catalogue is intentionally a contract fixture rather than a second graph implementation. Each scenario carries:

- a versioned safe snapshot with stable node and relationship IDs;
- explicit recommended views: node-link, matrix, path and semantic list;
- pointer, keyboard and semantic-list action origins;
- node-menu and edge-menu targets;
- movement preview, commit and cancel cases;
- expected outcomes that a renderer adapter or browser test can assert.

This structure makes the “same crime, different engine” idea concrete without forcing every renderer to share a visual implementation. The adapters consume the same snapshot and action intent; the shell remains responsible for capability checks, version checks, focus management and evidence-safe detail.

### 78.1 Scenarios included

1. **The empty Academy board** — a valid zero-node/zero-edge state, including safe fit/reset and semantic fallback.
2. **Shared device cluster** — node and edge context, cluster focus, matrix linking and committed movement.
3. **Temporal path tracing** — directional edge context, source/target inspection, path view and filtering.
4. **Keyboard and semantic journey** — pointer-independent selection, keyboard menu invocation and cancelled movement.
5. **Dense cluster and progressive disclosure** — a deterministic twelve-node graph for minimap policy, filtering and bounded rendering.

### 78.2 Why examples belong in the engine architecture

The examples prevent the interaction contract from being specified only in prose or only through one renderer. They also create a smaller test vocabulary than the full qualification fixture: a browser test can say “run the shared-device scenario” and assert the same invariants across Cytoscape, Sigma, D3 and React Flow.

The catalogue does not authorize investigation actions, expose canonical truth, perform layout or decide guilt. It is therefore safe to reuse in demos, documentation, adapter qualification, storybook-style exploration and replay fixtures, while keeping the production boundary explicit.

## 79. Research pass 25 — example-library verification

The new library was verified locally:

```text
npm run typecheck                         PASS
npm test -- src/graph-engine/examples.test.ts
  Test Files: 1 passed
  Tests: 4 passed
npm run build                             PASS
  vite: 60 modules transformed
```

The focused tests cover deterministic ordering and serialization, empty/connected/dense scenarios, explicit menu and movement actions, and rejection of dangling relationships or unknown action targets.

The full Vitest command was started as a regression check but did not complete within the bounded execution window and was stopped after leaving test workers active. It is not reported as green. The focused library suite and production build are the reliable evidence for this change; full-suite bounded execution remains an open infrastructure concern already recorded in this dossier.

## 80. Updated research ledger — example catalogue

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-052 | Can examples be shared without sharing renderer objects? | `examples.ts` contains snapshots and intents only; no Cytoscape, Sigma, D3 or React Flow import. | Keep the catalogue renderer-neutral and require adapters to consume the same contract. |
| R-053 | Does the catalogue cover the engine’s high-risk interactions? | Five scenarios cover empty state, node/edge menus, keyboard parity, movement commit/cancel, coordinated views and dense rendering. | Add browser replay tests against the catalogue before calling interaction support production-ready. |
| R-054 | Can invalid example data fail early? | `validateGraphEngineExample` rejects duplicate IDs, dangling edges, unknown targets and unknown clusters; four focused tests pass. | Run validation at fixture load and in every adapter qualification harness. |
| R-055 | Is the library a production engine already? | It describes safe snapshots and actions but does not render, authorize commands, manage focus or run layout. | Call it an executable example/contract library; implement the renderer-neutral interaction controller next. |

## 81. Updated pass log — example-library continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 24 | Architecture and reuse | Added five executable scenarios and documented their intended consumers and boundaries. | yes for catalogue design; browser integration remains open |
| 25 | Type safety and local execution | Typecheck, focused tests and production build passed; full Vitest completion was bounded and unresolved. | yes for focused scope; full-suite closure remains open |

## 82. Sources and artifacts added in passes 24–25

- [Graph engine example catalogue](../../../apps/web/src/graph-engine/examples.ts)
- [Graph engine example tests](../../../apps/web/src/graph-engine/examples.test.ts)
- [Graph engine example usage guide](../examples/README.md)

## 83. Research pass 26 — zero-install gallery

The example catalogue now has a directly runnable visual companion at [`docs/iteration-06/examples/gallery.html`](../examples/gallery.html). It is intentionally a single static HTML file with inline CSS, SVG and JavaScript.

The gallery exposes five tabs without mixing renderer packages:

- node-link view with status color, icon and shape;
- matrix view for dense adjacency inspection;
- path view for directional context;
- semantic-list view for keyboard and non-canvas access;
- target-specific node and edge context menus;
- zoom, fit and reset controls;
- status filters, cluster focus and minimap;
- pointer drag with committed movement, Escape cancellation and keyboard arrow movement;
- pointer, keyboard and semantic-list selection paths.

Because it is static, the gallery is useful for visual design review, interaction discovery and portability checks before the production controller and renderer adapter exist. It does not call the backend, read Databricks, import a graph library or claim that its presentation state is investigative truth.

## 84. Research pass 27 — static browser verification

The file was opened with a headless browser using a `file://` URL rather than a development server. The check passed:

```text
status: PASS
title: FGA Graph Engine · Example Gallery
tabs: 5
shared-device tab: loaded
node context menu: opened by right-click
Escape dismissal: passed
semantic-list view: rendered and selectable
external server dependency: none
```

This proves basic static execution and interaction wiring. It does not replace browser coverage for all drag geometry, screen-reader output, renderer adapters or production routing.

## 85. Updated research ledger — static gallery boundary

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-056 | Can the examples be explored without installing the application? | `gallery.html` runs directly from `file://`; five tabs and core interactions passed. | Keep the gallery as a portable design/review artifact. |
| R-057 | Does the static gallery prove the production renderer? | It uses owned inline SVG/HTML and no candidate adapter. | Treat it as a contract and UX lab, never as Cytoscape/Sigma/D3/React Flow qualification. |
| R-058 | Can context interaction be inspected before the controller exists? | Node menu, Escape dismissal and semantic-list selection pass in a headless browser. | Port the interaction assertions to the renderer-neutral controller and candidate adapters. |

## 86. Updated pass log — static gallery continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 26 | Portability and visual review | Added a single-file gallery with five scenarios, multiple views and interaction affordances. | yes for static artifact; production integration remains open |
| 27 | Browser execution | Loaded through `file://` and verified tabs, context menu, Escape dismissal and semantic list. | yes for smoke scope; full accessibility and renderer coverage remain open |

## 87. Research pass 28 — visual hierarchy audit

The first static gallery was functional but still looked like a technical qualification workbench. The audit identified four presentation gaps:

1. selection did not sufficiently separate the active neighborhood from background graph noise;
2. node and edge context used nearly the same flat information pattern;
3. connected relationships were not directly navigable from the selected node;
4. the graph surface had no compact state summary for visible entities, relationships, selection and snapshot identity.

The correction keeps the graph dominant while giving the right panel a dossier hierarchy: identity/route header, status or relationship signal, compact metrics, stable IDs, connected items, timeline-style context and actions.

## 88. Research pass 29 — contextual visual implementation

`gallery.html` now implements the visual corrections without external dependencies:

- selected nodes receive a halo and their immediate neighborhood remains legible while unrelated nodes and edges recede;
- selected edges receive a glow, a route label and explicit source/target endpoints;
- node dossiers show icon, status pill, record type, connection count, cluster, position, stable ID and selectable connected relationships;
- edge dossiers show source-to-target route cards, relationship family, direction, confidence bar and stable IDs;
- both dossiers expose actions to keep, focus, close, inspect source/target or change the presentation-only status;
- graph metrics expose visible entities, visible relationships, selection count and snapshot label;
- reduced-motion users do not receive the rotating selection halo;
- click and drag are separated by a five-pixel movement threshold so selection is not incorrectly journaled as movement.

The panel language continues to distinguish presentation metadata from investigative conclusions. The gallery remains a safe fixture lab, not a truth or scoring authority.

## 89. Research pass 30 — visual and interaction verification

The revised artifact was opened via `file://` in a headless browser and inspected as a rendered page. The checks passed:

```text
status: PASS
initial empty example: loaded
shared-device node dossier: rendered
connected relationship navigation: rendered
edge dossier: rendered
source navigation from edge dossier: rendered
simple click: did not create a movement commit
real drag: created one movement commit
external server dependency: none
```

The rendered inspection shows a stronger visual hierarchy and differentiated node/edge panels. A follow-up sweep exercised all 5 tabs across all 4 views (20 view combinations), reported no page errors, and returned zero axe violations. This is still not a full manual screen-reader audit or renderer-adapter qualification.

## 90. Updated research ledger — visual engine iteration

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-059 | How should selection reduce graph noise? | Rendered capture and focus logic show selected target plus immediate neighborhood while unrelated items dim. | Carry the focus policy into every production renderer adapter. |
| R-060 | What belongs in a node context panel? | Node dossier now combines identity, state, cluster, position, relationships and presentation timeline. | Keep node context entity-centric and make connected targets first-class actions. |
| R-061 | What belongs in an edge context panel? | Edge dossier now exposes route, source, target, family, direction, confidence and context actions. | Treat edge context as its own information architecture, not a reduced node menu. |
| R-062 | Can visual polish introduce misleading interaction telemetry? | Browser check found and fixed click-as-drag logging with a five-pixel threshold. | Keep pointer intent classification explicit and test click, drag, cancel and keyboard separately. |

## 91. Updated pass log — visual engine continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 28 | Rendered visual hierarchy | Diagnosed the technical-workbench feel and redesigned focus, metrics and dossier structure. | yes for visual audit; implementation follow-up required |
| 29 | Node/edge information architecture | Added differentiated node and edge panels, connected-item navigation and timeline/provenance-style signals. | yes for focused implementation scope |
| 30 | Interaction regression | Verified node dossier, edge dossier, source navigation, click/drag distinction and static execution. | yes for smoke scope; full accessibility and renderer coverage remain open |

## 92. Research pass 31 — production component parity

The previous pass improved the static gallery, but the real React board still used a small inspector sentence and a flat SVG. That was a valid implementation gap: a visual research artifact cannot be the only place where the intended engine behavior exists.

The board now has a reusable [`GraphContextPanel.tsx`](../../../apps/web/src/board/GraphContextPanel.tsx) and an upgraded [`GraphViewport.tsx`](../../../apps/web/src/board/GraphViewport.tsx). The production component now provides:

- node context with glyph, record type, safe summary, stable ID, source system and provenance reference;
- connected relationship list with direct edge selection;
- edge context with source/target route cards, relationship family, direction, event time, provenance and player-safe summary;
- direct source/target navigation from an edge;
- node/edge focus behavior that dims unrelated graph elements;
- SVG markers for direction, semantic list fallback, keyboard activation, context-menu selection and drag/escape interaction;
- explicit empty graph context rather than a blank canvas.

The context panel is renderer-neutral at the application boundary: it consumes FGA graph DTOs and stable IDs, never Cytoscape/Sigma/D3/React Flow objects.

## 93. Research pass 32 — regression correction

The first production-component rewrite broke two existing test assertions because the old copy said “nodes” and the new panel intentionally says “entities”, and because the empty context panel now explains identity, connections and provenance. The tests were updated to assert the new contract instead of preserving stale wording.

The test was strengthened to verify the new behavior, not just the labels:

1. select a node;
2. observe the connected-relationships section;
3. navigate from a relationship row to the edge;
4. observe the safe relationship dossier.

## 94. Research pass 33 — local component verification

The production integration passed locally:

```text
npm run typecheck                         PASS
npm test -- GraphViewport.test.tsx examples.test.ts
  Test Files: 2 passed
  Tests: 7 passed
npm run build                             PASS
  vite: 61 modules transformed
```

The static gallery’s separate browser sweep remains green at 5 tabs × 4 views, with no page errors and zero axe violations. The React component has focused DOM/interaction coverage; full application browser qualification and manual screen-reader review remain separate tasks.

## 95. Updated research ledger — application visual parity

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-063 | Does the real board expose the same context model as the gallery? | `GraphContextPanel` now renders node and edge dossiers from application graph DTOs. | Keep gallery and board assertions aligned through shared stable-ID scenarios. |
| R-064 | Can a selected node lead to its relationships without reopening another screen? | Connected relationship buttons select the corresponding edge directly. | Preserve in-panel navigation as a core investigation task. |
| R-065 | Can an edge explain itself without being reduced to two node labels? | Edge panel exposes route, family, direction, time, provenance and safe summary. | Treat edge context as a first-class application contract. |
| R-066 | Does visual focus work with parent-owned selection? | Parent-controlled node/edge IDs and local fallback are both handled; focused neighbors are retained. | Add browser coverage for controlled selection and focus return when the production route is available. |

## 96. Updated pass log — production visual continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 31 | Source-of-truth parity | Ported the rich node/edge dossier from the static lab into the real React GraphViewport. | yes for implementation scope; browser route coverage remains open |
| 32 | Regression and contract | Repaired stale test expectations and strengthened tests around connected relationship navigation. | yes |
| 33 | Build and focused execution | Typecheck, 6 focused tests and production build passed. | yes for focused scope; full app/browser qualification remains open |

## 97. Research pass 34 — comparison against the supplied demo

The supplied `fraud_graph_arena_demo_english.html` was treated as a visual reference, not as an implementation instruction or code source. Its strongest ideas are:

- a graph-first full-screen composition;
- a dense, legible network that communicates clusters immediately;
- entity glyphs inside nodes rather than color alone;
- a framed investigation-board atmosphere;
- explicit zoom, fit, reset, minimap and legend affordances;
- selection rings and relationship-family colors.

Its main limitation for FGA is that the contextual information remains a small hover/attribute hint and does not provide a structured node/edge dossier, connected-item navigation, safe provenance boundary or replay-oriented interaction contract.

The FGA gallery now combines the visual strengths with the stronger application contract: the dense scenario opens first, a target is selected, immediate neighbors stay readable, unrelated items recede, and the right panel explains the selected object without making the graph secondary.

## 98. Research pass 35 — premium investigation surface

The static gallery received a focused visual uplift:

- investigation frame and concentric graph-field treatment around the SVG surface;
- brighter, outlined entity glyphs for legibility against dark node fills;
- dense-cluster default with an active target, so the first render demonstrates exploration rather than an empty inspector;
- selective labels: dense graphs show labels for the selected neighborhood instead of turning every node into a text collision;
- persistent metrics for entities, relationships, selection and snapshot version;
- the contextual dossier remains the richer differentiator: connected relationships, route cards, safe summaries, confidence/provenance-style signals and actions.

The design goal is not to imitate the reference image pixel by pixel. It is to use the reference’s visual confidence while preserving FGA’s renderer-neutral, testable and evidence-safe boundaries.

## 99. Research pass 36 — accessibility correction after visual uplift

The first post-uplift browser audit exposed two valid defects:

1. the candidate status pill did not meet contrast thresholds;
2. an SVG with `role="img"` contained child graph targets with `role="button"`, which axe correctly reported as nested interactive semantics.

The fixes are now applied in both the static gallery and the real React GraphViewport:

- status pills use a dark backing with the high-contrast state color;
- the SVG is a non-interactive drawing surface; node and edge targets plus the semantic list own interaction and keyboard semantics.

This preserves keyboard access while avoiding an accessibility tree that claims the entire drawing is one image and simultaneously contains controls.

## 100. Research pass 37 — final visual verification

The updated gallery and board path were verified locally:

```text
static gallery initial state: dense cluster with selected entity
static gallery functional sweep: 5 tabs × 4 views = 20 checks, PASS
static gallery node dossier: PASS
static gallery edge dossier: PASS
static gallery page errors: 0
static gallery axe audit after correction: 0 violations
npm run typecheck: PASS
focused Vitest suites: 2 files, 7 tests passed
npm run build: PASS, 61 modules transformed
```

The exhaustive axe attempt across every view was bounded after it exceeded the execution window; the final initial-state audit and functional 20-view sweep both pass. This is reported explicitly rather than presented as a full manual accessibility certification.

## 101. Updated research ledger — reference-demo uplift

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-067 | What should be borrowed from the supplied demo? | Full-screen graph composition, framed board, glyphs, selection rings, minimap and legend. | Keep the visual language, reimplement cleanly inside FGA’s own contracts. |
| R-068 | How can the first render feel investigative rather than empty? | Dense scenario opens with an active entity and contextual dossier. | Keep empty state as a scenario, not as the default gallery impression. |
| R-069 | How should dense labels behave? | Selected-neighborhood labels reduce collisions while stable IDs remain available in panels and semantic list. | Make label density a policy controlled by focus and graph size. |
| R-070 | Does visual polish preserve accessibility? | Contrast and nested-interactive defects were found and fixed; final initial-state axe audit has zero violations. | Keep accessibility checks attached to every visual uplift. |

## 102. Updated pass log — reference-demo continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 34 | Comparative visual audit | Extracted the reference demo’s strongest visual ideas and its FGA-specific information gaps. | yes for comparison |
| 35 | Product visual uplift | Added dense first render, investigation frame, focus policy, glyph legibility and selective labels. | yes for visual scope |
| 36 | Accessibility regression | Fixed contrast and nested SVG interaction semantics in both gallery and React component. | yes |
| 37 | Final local verification | 20-view functional sweep, node/edge context checks, axe initial-state pass, typecheck, 7 tests and build pass. | yes for local scope; full manual/renderer qualification remains open |

## 103. Research pass 38 — Neo4j-inspired interaction patterns

The user’s reference to Neo4j was translated into interaction patterns rather than an implementation dependency. Neo4j’s official Browser documentation describes a graph result frame with zoom and fit controls, node selection that exposes properties, right-click context menus, double-click expansion, and node dragging/re-layout. It also documents panning from empty scene space and selection-driven inspection in Aura’s scene interaction guidance ([Browser result frames](https://neo4j.com/docs/browser/operations/result-frames/), [Aura scene interactions](https://neo4j.com/docs/aura//explore/explore-visual-tour/scene-interactions/)).

These patterns fit FGA because they reduce the distance between “I see a suspicious connection” and “I can inspect the safe context around it”. They do not transfer Neo4j’s data model, renderer, code or license into FGA. The gallery therefore implements its own small interaction controller with explicit node, edge, camera and replay boundaries.

## 104. Research pass 39 — turn the gallery into a mini-game

The gallery is now an embeddable investigation exercise rather than a passive component catalogue. The mini-game has four deliberately non-accusatory steps:

1. select an evidence node and open its dossier;
2. inspect a relationship and its source-to-target route;
3. reposition a node to create a working layout;
4. pan or zoom the camera to compare the scene.

The HUD gives progress, a contextual next objective, a hint and a restart action. Completion means that the interaction path was exercised, not that fraud was proven. The empty scenario has no scored challenge because inventing a task for zero evidence would violate the gallery’s evidence-safe contract.

## 105. Research pass 40 — separate layout from camera

A graph UI becomes difficult to reason about when dragging a node, panning the viewport and zooming the camera all mutate one coordinate system. The gallery now keeps `positions` separate from `panX`, `panY` and `zoom`:

- node movement updates only the working position map;
- background dragging updates only camera translation;
- modifier-wheel zoom preserves the point under the pointer;
- fit/reset restores camera state without rewriting the source snapshot;
- Escape cancels either in-progress gesture.

This is the important Neo4j-like feel for FGA: the investigator can rearrange the board without accidentally changing the evidence graph, and can inspect the same arrangement from several camera positions.

## 106. Research pass 41 — implementation and accessibility correction

The mini-game is implemented inside the zero-install `docs/iteration-06/examples/gallery.html` file so it can be embedded without a framework bundle or network connection. A transparent SVG background owns the pan gesture; node and edge targets stop propagation so their own interactions remain precise. A five-pixel drag threshold prevents a click from becoming a movement commit. The contextual dossier remains the source of relationship navigation, so the mini-game does not add a second graph truth.

The first accessibility audit of this pass found that the interaction log was scrollable but not keyboard-focusable. The log now exposes `tabindex="0"` and an accessible label. This is a useful regression lesson: visual polish and gesture richness must continue to be checked against keyboard and assistive-technology paths.

## 107. Research pass 42 — browser qualification

The new browser qualification is `apps/web/e2e/gallery-mini-game.spec.ts`. It verifies:

```text
mini-game objective loop, hint, relationship inspection, node drag and camera pan: PASS
restart after completion: PASS
five scenarios × four views reachable: PASS
initial-state Axe audit after the complete journey: PASS, 0 violations
```

The test is self-contained and opens the static file directly. The Playwright project may still start the repository’s configured local web server, but the gallery itself is loaded from a `file:` URL and uses no API, Databricks profile or network dependency.

## 108. Updated research ledger — mini-game iteration

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-071 | Which Neo4j interaction ideas transfer cleanly? | Empty-space pan, node drag, zoom/fit, selection dossier and context menus are documented in Neo4j’s official interaction guides. | Adopt the interaction patterns, reimplement independently, preserve FGA’s snapshot boundary. |
| R-072 | How can the gallery become playable without becoming a verdict engine? | Four interaction objectives exercise investigation mechanics without scoring guilt or changing evidence. | Use progress as interaction coverage only; keep the empty board unscored. |
| R-073 | How should node movement and camera movement coexist? | Separate `positions` and camera transform; cancel gestures before commit. | Keep layout and camera state independent in future renderer adapters. |
| R-074 | Can the mini-game be embedded without a toolchain? | Single HTML file, no imports, no network, iframe snippet documented. | Keep the static artifact portable for the article. |
| R-075 | Did richer gestures introduce accessibility debt? | Axe found the scrollable log defect; focusability fixed and full mini-game audit passes. | Run accessibility checks after each new interaction surface. |

## 109. Updated pass log — mini-game continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 38 | Interaction research | Mapped official Neo4j exploration patterns to FGA-safe, renderer-neutral behaviours. | yes |
| 39 | Playability design | Added a four-step investigation loop with hint, progress and restart semantics. | yes |
| 40 | Camera/layout architecture | Separated node positions from pan/zoom state and added cancelable gestures. | yes |
| 41 | Browser debugging | Fixed viewport-scroll sensitivity in the qualification path and made the SVG background an explicit pan target. | yes |
| 42 | Accessibility regression | Made the scrollable interaction log keyboard-focusable after Axe found the defect. | yes |
| 43 | Final local qualification | 2 Playwright tests passed, including the full journey, five scenarios, four views and Axe with zero violations. | yes for static-gallery scope |

## 110. Research pass 44 — visual correction against the supplied reference

The rendered comparison exposed a real product mismatch: the previous gallery was a well-structured application shell, but it read as a documentation dashboard rather than as an investigation board. The supplied demo’s visual hierarchy is different: the graph owns nearly the whole viewport, the chrome is compact, the surface is almost black, and the legend/minimap are overlays inside a framed scene.

The gallery has therefore been reskinned around that hierarchy without copying the reference HTML or assets:

- full-viewport dark board with a double amber frame and subtle scanline/radial field;
- compact `INVESTIGATION GRAPH` top bar with interaction guidance and selection count;
- the five scenario tabs reduced to a thin board navigation strip;
- compact graph controls grouped into a reference-like top-right control block;
- legend and minimap moved inside the board as anchored overlays;
- a deterministic three-cluster dense scene with green, red and blue visual families, large hubs and person glyphs;
- the context dossier hidden in the initial state and shown only after a node/edge selection, so it cannot obscure the graph by default.

The mini-game HUD remains available as a restrained overlay rather than consuming a full application row. This keeps the investigation mechanics while restoring the visual priority requested by the reference.

## 111. Research pass 45 — visual regression check

A local 1440×1000 render was inspected against the supplied demo. The revised version now shares the reference’s key composition: dark immersive canvas, amber frame, top investigation bar, colored radial clusters, hub emphasis, status legend and minimap. The FGA-specific additions remain visible only where useful: scenario tabs, progress HUD and contextual dossier-on-selection.

The browser qualification was updated for the new initial state: it now begins with `0 / 4` progress, selects the target entity explicitly, then exercises relationship inspection, node dragging, camera panning, restart, all five scenarios and all four views. The panning probe deliberately starts below the tab overlay, matching the real hit-test boundary of the board.

## 112. Updated research ledger — visual correction

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-076 | Why did the first gallery still feel unlike the demo? | It used a large page header, always-visible inspector, light brown application panels and a sparse grid-like dense fixture. | Rebuild the visual hierarchy around a full-screen graph board. |
| R-077 | What makes the reference read as an investigation graph? | Near-black surface, amber frame, compact chrome, large radial hubs, colored clusters, legend and minimap overlays. | Keep those as the board skin while retaining FGA-safe data and interaction contracts. |
| R-078 | When should contextual information appear? | A permanent right panel hides the graph and clips the right cluster; selection-triggered overlay preserves both. | Hide the inspector until a node or edge is selected. |
| R-079 | How can the dense fixture carry visual meaning? | Three deterministic radial clusters provide immediate spatial grouping without canonical truth. | Use visual families for exploration; keep status, IDs and evidence semantics explicit in the dossier. |

## 113. Updated pass log — reference look-and-feel correction

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 44 | Visual comparison | Identified the dashboard-versus-investigation-board mismatch from rendered screenshots. | yes for diagnosis |
| 45 | Visual reskin | Applied immersive board composition, cluster fixture, person glyphs, overlays and selection-triggered inspector. | yes for implementation scope |
| 46 | Regression qualification | Re-ran the browser journey after changing the initial selection state and pan hit area; both gallery tests passed. | yes for current local scope |

## 114. Research pass 47 — entity glyph language

The reference demo communicates entity type through pictograms inside nodes, not through color alone. The gallery’s previous text glyphs (`●`, `▣`, `▥`) were too generic and did not scale to a richer investigation scene. The renderer-neutral fixture now maps record types to small, self-contained SVG glyphs:

- people use a head-and-shoulders silhouette;
- devices use a handset outline and indicator;
- accounts use a wallet/card shape;
- banks use a building with columns;
- organisations use a briefcase/office mark;
- claim clusters use a starburst.

The glyphs remain presentation metadata. Stable IDs, status, relationship direction and safe context continue to come from the graph object rather than from the icon.

## 115. Research pass 48 — billiard-like graph motion

The graph now includes a small physics controller designed for investigation-board feel rather than scientific simulation. It combines:

- spring attraction along visible relationships;
- local repulsion to reduce node overlap;
- anchor force to keep the scene bounded and recognisable;
- velocity damping and hard speed/viewport limits;
- pointer release velocity so a dragged node carries momentum;
- a quiet-frame threshold so the scene settles instead of running forever.

The initial scene is intentionally stable so clicking a target remains easy and deterministic. Physics wakes on a committed drag, keyboard reposition, explicit `Motion` toggle or view re-entry. The toggle is exposed as a real pressed-state control and respects `prefers-reduced-motion` on first load.

The physics loop updates existing SVG transforms in place rather than rebuilding the whole graph on every animation frame. This keeps the visual motion smooth and preserves event handlers, context menus and the semantic boundary while the nodes move.

## 116. Research pass 49 — interaction regression after physics

The first browser pass found that continuous initial motion made Playwright correctly reject a moving node as unstable. That exposed a real usability trade-off, not merely a test inconvenience: an investigator should not have to chase a target just to click it. The corrected policy is:

1. load a stable board;
2. let explicit investigation gestures wake the physics;
3. preserve the drag momentum and relationship response;
4. settle to a bounded layout;
5. offer `Motion` pause/resume for user control.

The browser test now checks the Motion toggle, node/edge selection, committed drag, the presence of moving nodes after the drag, camera pan, restart, all five scenarios, all four views and the Axe audit.

## 117. Updated research ledger — tactile motion and glyphs

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-080 | Why did the nodes still feel generic? | Text symbols did not communicate people, devices, accounts or institutional hubs like the supplied demo. | Use type-aware SVG glyphs with explicit semantic labels. |
| R-081 | What should “Neo4j-like” motion mean here? | Direct drag, release momentum, spring relationships, local repulsion, damping and settling capture the tactile behaviour without copying code. | Implement a bounded controller behind the renderer-neutral interaction layer. |
| R-082 | Should physics run continuously? | Continuous movement makes precise selection harder and can create nondeterministic tests. | Start stable; wake on explicit motion and settle automatically. |
| R-083 | Can animation remain testable? | In-place SVG transforms preserve handlers; Motion toggle and reduced-motion support make state explicit. | Keep motion state observable and controllable in browser qualification. |

## 118. Updated pass log — tactile graph continuation

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 47 | Visual semantics | Replaced generic text symbols with per-record-type SVG glyphs. | yes |
| 48 | Motion architecture | Added bounded springs, repulsion, damping, release velocity and settling. | yes for local scope |
| 49 | Usability/accessibility | Made initial state stable, added Motion toggle and reduced-motion default. | yes |
| 50 | Browser regression | 2 Playwright tests passed, including moving-node assertion, all scenarios/views and Axe. | yes for current local scope |

## 119. Research pass 51 — contextual hover versus selection

The previous implementation had a rich selection dossier, but the graph did not explain itself during pointer exploration. A right panel that appears only after a click is not enough for dense scenes: the investigator needs a low-friction preview before committing selection. The new policy separates three states:

1. pointer hover or keyboard focus opens a lightweight target preview;
2. click, tap or an explicit keyboard action promotes the target to the persistent context dossier;
3. an existing selection remains authoritative while a transient preview is shown for another target.

Node previews expose type, label, status, stable ID and safe summary. Relationship previews expose relationship type, source, target, family and stable ID. Preview content is presentation-only and does not replace the semantic fallback or create a second graph truth.

## 120. Research pass 52 — local working relationships

An investigator may need to record a working hypothesis between two already visible entities. This is not an authoritative relationship and must not be confused with a detected edge. The implementation therefore keeps two edge origins:

- `detected`: supplied by the snapshot, continuous and not deletable from the graph surface;
- `investigator-added`: local working state, rendered with a dashed line, included in the same selection/context path, and deletable.

Working relationships use stable local IDs, remain in the presentation layer, and carry explicit copy that they are not part of the published projection. The same separation exists in the pure `workingState` engine helpers, the React board and the static gallery composer.

## 121. Research pass 53 — marked targets and recentering

Favorites are implemented as a target list rather than as a node-only feature. A node or relationship can be marked, unmarked, selected from the list and recentered in the graph. Centering changes camera state only; it does not move the node, alter the snapshot or create a relationship.

The marked-target list is intentionally local and removable. It provides a working set for Hercule when comparing a case and prevents repeated manual searching without implying that a mark is a fraud conclusion.

## 122. Updated research ledger — contextual investigation state

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-084 | Is a selection dossier sufficient for dense graph exploration? | Browser review showed that selection-only context delayed understanding and made the graph feel inert. | Add immediate node/relationship hover and focus previews while preserving selection authority. |
| R-085 | How can new relationships remain useful without rewriting evidence? | A local edge origin cleanly separates detected immutable edges from investigator hypotheses. | Render investigator-added edges dashed and allow deletion only for that origin. |
| R-086 | How can repeated targets be revisited efficiently? | A target list with node/edge IDs and camera centering reduces repeated manual navigation. | Add removable marked-target state and center-on-target commands. |
| R-087 | Can the features remain accessible and autonomous? | React tests cover hover, mark, center, add/delete; gallery Playwright covers the full journey plus Axe. | Keep the same command/state contract when the controller is extracted from components. |

## 123. Updated pass log — working investigation features

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 51 | Context interaction | Added visible hover/focus previews and explicit selection dossiers for nodes and relationships. | yes for local scope |
| 52 | Working graph state | Added renderer-neutral helpers for investigator-added edges, deletion and target position lookup. | yes |
| 53 | Investigator workflow | Added removable marked targets and camera centering in React and static gallery paths. | yes |
| 54 | Browser/accessibility regression | Added HOV/working-relationship journey; 3 gallery tests passed with zero Axe violations. | yes for current local scope |

## 124. Research pass 55 — marking must be visible on the graph

The first marked-target implementation correctly maintained a list but did not provide a strong visual cue on the graph itself. That weakened the investigator’s spatial memory: a marked target could be selected from the list but was not distinguishable when scanning the scene. The corrected presentation uses a dashed gold ring and star marker on marked nodes, a stronger glow on marked relationships, and an accessible `marked` state in the target name.

The correction remains presentation-only. The mark does not change status, confidence, provenance, layout truth or the underlying snapshot.

## 125. Research pass 56 — working-state lifetime

Local relationships, marks and manual positions must belong to one graph snapshot. Carrying them into a new projection could create dangling endpoints or falsely suggest that a previous investigation note applies to a different case. The React board now derives a graph identity from projection version and stable IDs and resets the local working layer when that identity changes. The static gallery already resets working state when switching examples.

## 126. Updated research ledger — marked and scoped working state

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-088 | Is a list entry enough to mark an investigation target? | Visual review found no spatial cue after the target was marked. | Add node ring/star and relationship glow while retaining the list and accessible text. |
| R-089 | Can local marks or relationships leak across cases? | Component state outlived a graph prop change unless the snapshot identity was observed. | Reset local working state on projection/ID identity changes. |
| R-090 | Does the correction preserve the feature contract? | React focused tests and browser Axe flow remain green after the visual/state changes. | Keep highlight and lifetime behavior in the adapter conformance checklist. |

## 127. Updated pass log — visual marking and lifecycle

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 55 | Visual semantics | Added visible mark rings/stars for nodes and glow for marked relationships. | yes for implementation scope |
| 56 | Lifecycle safety | Scoped local favorites, relationships and layout overrides to the current graph identity. | yes |
| 57 | Browser/accessibility | Re-ran the contextual workflow with marking, centering, relationship creation/deletion and Axe. | yes for current local scope |

## 128. Research pass 58 — atomic highlight propagation

The browser regression exposed that updating the marked-target list without re-rendering the graph created split state: the list said a target was marked while the SVG still looked unchanged. The corrected path uses one render transition for mark/unmark, so the target list, contextual panel, accessible label, node ring/star and relationship glow update together. This is preferable to a DOM-only patch because it keeps the graph, panel and list derived from the same local state.

## 129. Updated research ledger — highlight consistency

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-091 | Can the marked list and graph diverge? | A focused browser test caught the list changing before the SVG highlight. | Treat marking as a state transition that rerenders all dependent surfaces. |
| R-092 | Is the visible mark available for nodes and relationships? | The regression journey now asserts a node mark and an edge glow before removing both. | Keep both target kinds in the conformance fixture. |

## 130. Research pass 59 — command/event boundary extraction

The visual surfaces now share a renderer-neutral controller slice. It applies the current interaction vocabulary as pure state transitions: selection and context targets, camera fitting and centering, movement preview/commit/cancel, filters, views, local relationship lifecycle and marked targets. Each dispatch emits a monotonic sequence number plus its source (`pointer`, `keyboard`, `touch`, `semantic`, `system` or `replay`).

This is deliberately smaller than a promise that the whole future engine is finished. Lasso, multi-selection, full replay export, undo/redo and renderer-scale scheduling still need their own contracts. The controller does, however, remove a major source of drift: a future adapter can replay the same serialisable commands without mounting React, starting a browser or contacting Databricks.

## 131. Updated research ledger — controller boundary

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-093 | Can the current investigation workflow run without a renderer? | A pure controller reducer now covers selection, context, movement, filters, local edges, marks and centering; focused tests pass. | Keep renderer adapters as projections of controller state, then add lasso and multi-selection to the same boundary. |
| R-094 | Can replay avoid timing and network assumptions? | The same command sequence produces byte-equivalent serialisable controller state in the Vitest replay test. | Extend the log with fixed simulation ticks only when motion state becomes part of logical replay. |

## 132. Updated pass log — command/event boundary

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 59 | State architecture | Extracted a pure interaction controller with ordered source-labelled events and no DOM/timer/network dependency. | yes for implemented command slice |
| 60 | Replay determinism | Replayed selection, mark, centering, view and filter actions against the same snapshot; serialised state matched exactly. | yes |

## 133. Research pass 61 — hover panels must be traversable

The first contextual preview was deliberately passive: it disappeared as soon as the pointer left the node and it ignored pointer input. That is acceptable for a tooltip, but not for an investigation surface whose actions are meant to be clicked. The corrected interaction contract distinguishes a tooltip from a hover panel:

- the preview has pointer events enabled and exposes the same `+`, `−` highlight and `⌖` center actions as the persistent dossier;
- leaving the node schedules a short hide rather than removing the panel synchronously;
- entering the card cancels that hide, and leaving the card closes it;
- clicking the card body promotes the target to the persistent context dossier, while action buttons stop propagation and perform their own command.

The static gallery and React board now implement the same behaviour. This avoids making the user race across a gap between the graph and its controls, while retaining a bounded transient surface and a keyboard-accessible persistent path.

## 134. Updated research ledger — interactive hover context

| ID | Question | Evidence | Decision/next experiment |
|---|---|---|---|
| R-095 | Is a non-interactive hover tooltip sufficient for graph actions? | Manual reproduction showed that the panel disappeared on pointer exit and could not receive a click. | Treat actionable context as a traversable panel, not a tooltip; add a bounded hide delay and pointer cancellation. |
| R-096 | Can hover actions remain equivalent to selection actions? | React and Playwright coverage click `+`, `−` and `⌖` directly from the hover preview, then continue through the dossier. | Keep hover and selection actions backed by the same target/state contract. |

## 135. Updated pass log — traversable context panel

| Pass | Perspective | Outcome | Clean? |
|---:|---|---|---|
| 61 | Interaction usability | Made hover previews interactive, delayed hide during node-to-card movement and preserved explicit escape/selection paths. | yes for current scope |
| 62 | Regression/accessibility | Full Vitest (22 files, 49 tests), full gallery E2E (3 tests) and Axe all passed after the correction. | yes |

