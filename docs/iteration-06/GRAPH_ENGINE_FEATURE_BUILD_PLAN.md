# FGA-06 Graph Engine
## Feature Build Plan and Exhaustive Verification Plan

**Document status:** Proposed execution plan for the next engine iteration  
**Scope:** FGA-06 graph engine, static gallery, React board integration, renderer-neutral interaction model and qualification tooling  
**Audience:** Product owner, frontend engineers, data-contract owners, visual-design reviewers, accessibility reviewers and test engineers  
**Language:** English, matching the technical documentation for FGA-06  
**Last updated:** 2026-11-08

---

## 1. Executive summary

FGA-06 should evolve from a visual graph gallery into a small, professional investigation-board engine. The graph must remain the protagonist, but the experience must also make relationships explainable, interaction state reproducible, evidence-safe and fully testable without a human repeatedly reopening the same case.

The implementation must therefore be split into four explicit boundaries:

1. **Graph contract** — stable nodes, edges, metadata, provenance references and safe presentation hints.
2. **Interaction controller** — selection, focus, context menus, commands, movement, camera gestures and replayable state transitions.
3. **Layout and motion services** — deterministic layout strategies, bounded physics and working-position management.
4. **Renderer adapters** — SVG, Cytoscape, Canvas/WebGL or another qualified renderer, all consuming the same contract and producing the same observable semantics.

The static gallery remains the portable design and interaction lab. The React board remains the application integration path. Neither is allowed to become a second source of investigative truth.

The plan prioritises the features that create the largest improvement in investigator experience:

- radial node and edge context menus;
- richer directional and relationship-aware edges;
- lasso and multi-selection;
- explicit layout modes with manual-position preservation;
- evidence-focused inspection and replay;
- deterministic, controllable physics;
- progressive disclosure for large graphs;
- performance and accessibility qualification across renderer adapters.
- a visible, deterministic graph auto-test lab that shows each instruction, expectation, observed result, status and duration without mutating the evidence snapshot.

The plan is deliberately evidence-safe. It does not introduce a fraud verdict, guilt score, accusation command or hidden truth inside the visual engine.

---

## 2. Current baseline

The current FGA-06 implementation already provides a useful base:

| Area | Existing capability | Planning implication |
|---|---|---|
| Contract | Stable graph snapshots, node/edge IDs, direction, family, provenance and safe summaries | Extend the contract only through versioned additions |
| Gallery | Zero-install HTML gallery with five scenarios and four views | Keep it as a portable UX lab and manual review artifact |
| Context | Node and edge dossiers in the gallery and React board | Promote the interaction model into a renderer-neutral controller |
| Motion | Bounded spring/repulsion pass, drag release velocity, damping and settling | Add explicit state, deterministic seeds and property tests |
| Visual language | Full-screen dark board, status colors, type-aware glyphs, legend and minimap | Add richer semantics without relying on color alone |
| React integration | `GraphViewport` and `GraphContextPanel` | Align production DOM semantics with gallery behavior |
| Examples | Empty, compact, temporal, keyboard and dense deterministic examples | Add adversarial and scale fixtures to the qualification catalogue |
| Qualification | Candidate registry, adapters, renderer exhibit and local browser coverage | Expand from lifecycle checks to interaction, accessibility and performance gates |
| Visible auto-testing | The static gallery now exposes a six-check graph suite and a reusable `window.fgaGraphAutoTest` seam | Keep the suite isolated, observable and part of every gallery release check |
| Performance | Frozen targets for first render, selection, fit/reset, resize and fallback | Measure defined user-visible events, not only mount time |

Current implementation evidence is recorded in:

- [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md)
- [`RENDERER_REQUIREMENTS.md`](./RENDERER_REQUIREMENTS.md)
- [`PERFORMANCE_ENVELOPE.md`](./PERFORMANCE_ENVELOPE.md)
- [`examples/README.md`](./examples/README.md)
- [`research/FGA_GRAPH_ENGINE_RESEARCH.md`](./research/FGA_GRAPH_ENGINE_RESEARCH.md)

The current baseline is not treated as proof that the complete future engine is finished. This document is the execution plan for the remaining product-grade capabilities.

### 2.1 Execution checkpoint — first investigation-workflow slice

The first execution slice of this plan is now implemented locally:

- contextual node and relationship preview on hover and keyboard focus;
- persistent selection dossier with visible context actions;
- investigator-added working relationships with dashed rendering and deletion limited to local edges;
- removable marked-target list for nodes and relationships;
- camera centering from the marked-target list or context action;
- renderer-neutral working-state helpers and unit coverage;
- renderer-neutral command/event controller with ordered, source-labelled events and deterministic replay;
- static-gallery and React-board integration;
- browser and Axe coverage for the complete workflow.
- visible graph auto-testing for the graph contract, node dossier, hover context, camera zoom, topology switching and investigator-added relationships; each check runs against an isolated snapshot and reports expected/observed values and duration.

This checkpoint does not mark the entire plan complete. Lasso, multi-selection, additional layout modes, replay bundle export, renderer-scale qualification and later release hardening remain scheduled phases. The controller currently covers the implemented command slice; it is not yet the complete future command catalogue.

---

## 3. Goals and non-goals

### 3.1 Goals

The engine must:

1. Make a graph immediately readable as an investigation board.
2. Let an investigator inspect a node or relationship without losing graph context.
3. Support mouse, touch, keyboard and semantic-list workflows.
4. Keep camera state, layout state and evidence state separate.
5. Make every meaningful interaction expressible as a deterministic command.
6. Replay the same interaction sequence without network access or timing assumptions.
7. Support manual rearrangement without corrupting the source snapshot.
8. Provide context menus with safe, explicit commands rather than ambiguous gestures.
9. Scale from the seven-node T02 fixture to bounded dense graphs and documented stress sizes.
10. Offer a semantic fallback when a visual renderer cannot load or is disabled.
11. Make renderer substitution measurable and observable.
12. Work with open-source-compatible dependencies and avoid commercial-runtime coupling.
13. Give the article/gallery a compelling visual surface without copying proprietary code or assets.
14. Make graph correctness inspectable while it runs: an investigator must be able to see what the engine is checking, what it expected, what it observed and how long it took.

### 3.2 Non-goals

The graph engine must not:

- determine whether a person is guilty;
- calculate or display an undisclosed fraud verdict;
- mutate backend evidence when a user drags a node;
- treat visual proximity as a factual relationship;
- hide stable IDs behind renderer-generated objects;
- require a Databricks connection for local interaction or renderer tests;
- make the gallery a substitute for the production graph contract;
- copy source code, assets, visual templates or license-restricted implementation from a commercial product;
- become a general-purpose graph database or query engine;
- promise infinite-scale rendering without a measured envelope.

---

## 4. Product principles

### P-01 — Evidence is immutable; presentation is mutable

The graph snapshot is the evidence-shaped input. Positions, focus, selection, filters, collapsed clusters, camera transforms and visual themes are presentation state. A layout command may update working positions but must never rewrite the snapshot.

### P-02 — Stable IDs cross every boundary

Application code, tests, semantic HTML, adapters, menus and replay logs use project-owned node and edge IDs. Renderer-native objects are implementation details.

### P-03 — Every gesture has a command equivalent

If a pointer gesture cannot be represented as a deterministic command, it cannot be made a reliable product feature. Pointer, keyboard, touch and semantic-list paths must converge on the same controller operations.

### P-04 — The graph is the protagonist

Controls and panels are overlays or contextual surfaces. They must not permanently consume most of the viewport or force the user to leave the graph to understand a selected relationship.

### P-05 — Colour is a supporting channel

Status and relationship meaning use colour, shape, iconography, stroke, label and text. No critical distinction may depend on colour alone.

### P-06 — Motion is useful only when controllable

Physics must be bounded, pausable, reduced-motion aware, deterministic enough for tests and quiet enough for precise selection.

### P-07 — Progressive disclosure beats a hairball

The engine shows the right amount of context for the current task. It does not attempt to display every property and every relationship at once.

### P-08 — Accessibility is a contract, not a polish pass

Keyboard navigation, focus return, semantic fallback, names, roles, state announcements, contrast and reduced motion are implemented alongside visual features.

### P-09 — Local qualification comes first

The complete interaction and renderer test suite must run without Databricks or network access. Optional environment qualification may validate packaging and data integration separately.

---

## 5. Target experience

### 5.1 Primary investigator journey

1. Open a case and see a stable graph with a clear visual hierarchy.
2. Identify the selected, suspicious or highlighted cluster without reading a wall of text.
3. Hover or focus a node or relationship and receive an anchored contextual preview panel without losing the current graph selection.
4. Open a radial or keyboard context menu.
5. Inspect a node dossier containing identity-safe metadata, status, provenance and relationships.
6. Select an edge and understand source, target, direction, family, time and confidence.
7. Expand, collapse, hide or focus a neighbourhood without changing evidence.
8. Drag a node and feel a bounded, smooth layout response.
9. Use lasso or multi-select to compare a group.
10. Switch layout mode or view while preserving selection and stable IDs.
11. Add a local investigation note or evidence marker without pretending it is backend truth.
12. Replay the same sequence in an automated test and get the same observable result.

### 5.2 Initial viewport composition

The default board should contain:

- a compact header with case/scenario identity and interaction help;
- a graph surface occupying roughly two-thirds or more of the viewport;
- unobtrusive zoom, fit, reset, filter, legend and motion controls;
- a minimap only when graph size justifies it;
- no permanently visible cluster table;
- a contextual dossier that appears or expands when an object is selected;
- a persistent semantic fallback available in the DOM.

### 5.3 Visual status language

| State | Primary shape | Secondary cue | Meaning |
|---|---|---|---|
| Uninvestigated | Empty circle | Cool blue/neutral outline | Present in the snapshot; not yet inspected |
| Candidate | Dashed circle | Amber accent and candidate badge | Worth inspection; not a conclusion |
| Investigated | Ring or check marker | Green accent | Already inspected in the current working session |
| Fraud confirmed | Explicit alert/badge shape | Red accent and textual label | Only shown if supplied by an authoritative upstream state |
| Discarded | Neutral mark | Muted tone and strike/label | Deliberately excluded from the current working view |

The engine must render the textual state for assistive technologies and semantic fallback regardless of the visual theme.

---

## 6. Feature catalogue

Feature IDs are stable planning identifiers. Each feature has a scope, dependencies, acceptance criteria and test obligations.

### 6.1 Foundation and state model

#### FE-001 — Versioned graph snapshot contract

**Purpose:** Provide a renderer-neutral, serialisable input contract.

**Required fields:**

- snapshot ID and schema version;
- node ID, record type, display label and safe summary;
- edge ID, source ID, target ID, direction, family and safe summary;
- status and status explanation where supplied;
- provenance reference and source system;
- optional initial position and layout hint;
- optional timestamp or temporal interval;
- optional presentation metadata clearly separated from evidence metadata.

**Acceptance criteria:**

- IDs are unique within a snapshot and stable across views.
- Dangling edges are rejected or explicitly surfaced as invalid input.
- Unknown record types render with a safe fallback glyph.
- Snapshot validation produces actionable errors.
- The contract can be serialised and replayed without renderer objects.

#### FE-002 — Explicit engine state

Separate state into:

- `snapshot`: immutable graph input;
- `selection`: selected node IDs, edge IDs and active focus target;
- `camera`: pan, zoom and viewport dimensions;
- `layout`: working positions, pinned nodes, layout mode and layout seed;
- `filters`: active filters and hidden IDs;
- `presentation`: theme, label density, minimap, legend and reduced-motion policy;
- `investigation`: local notes, visited IDs and local evidence markers;
- `runtime`: renderer readiness, errors, frame statistics and capabilities.

**Acceptance criteria:** each state group can be reset or replayed independently; changing camera never changes positions; changing filters never mutates the snapshot.

#### FE-003 — Command/event boundary

Define commands such as:

- `SelectNode`, `SelectEdge`, `ClearSelection`;
- `OpenContextMenu`, `DismissContextMenu`, `ExecuteContextAction`;
- `BeginNodeMove`, `PreviewNodeMove`, `CommitNodeMove`, `CancelNodeMove`;
- `PanCamera`, `ZoomCamera`, `FitGraph`, `ResetCamera`;
- `SetFilter`, `ClearFilters`, `FocusNeighbourhood`, `CollapseCluster`;
- `SetLayoutMode`, `RunLayout`, `PinNode`, `UnpinNode`;
- `SetMotionEnabled`, `SetReducedMotion`;
- `AddInvestigationNote`, `MarkVisited`, `AddLocalEvidenceMarker`.

Commands must produce observable events with a source (`pointer`, `keyboard`, `touch`, `semantic`, `system`, `replay`) and a monotonic sequence number.

#### FE-004 — Deterministic replay

The engine must replay a command log against a fixed snapshot and produce the same serialisable state. Time-based animation is excluded from the logical replay state or represented through a fixed simulation clock.

**Acceptance criteria:** replay tests do not wait for arbitrary sleeps; a fixed seed and fixed tick count produce identical positions within the documented tolerance.

### 6.2 Visual system

#### VE-001 — Type-aware glyph system

Provide owned SVG glyphs for person, device, account, bank, organisation, address, cluster and unknown types.

Requirements:

- glyph meaning remains understandable in monochrome;
- glyph has a tooltip/accessible name;
- glyph does not encode factual claims not present in the snapshot;
- icon geometry has a common optical size and baseline;
- theme tokens control fill, stroke, focus ring and disabled state.

#### VE-002 — Multi-channel status styling

Implement colour, shape, stroke pattern, icon, label and focus treatment as independent tokens. Add a high-contrast theme and a colour-vision-safe palette.

#### VE-003 — Relationship-aware edge rendering

Edge appearance must reflect only supplied metadata:

- direction via arrow marker or directional animation;
- relationship family via stroke pattern and optional colour;
- confidence via an explicit, labelled style channel when available;
- temporal state via an optional timeline marker;
- selected path via controlled emphasis;
- hidden/filtered edge via omission or muted style, never silent reinterpretation.

#### VE-004 — Focus and neighbourhood treatment

When an object is selected:

- selected object receives a clear ring and accessible state;
- immediate neighbours remain readable;
- unrelated objects recede but remain discoverable unless the user enables isolate mode;
- selected path and relationship direction remain visible;
- focus treatment never changes IDs or data.

#### VE-005 — Overlay system

Create a consistent layer model:

1. background field;
2. edges;
3. edge labels/markers;
4. nodes;
5. selection/focus halo;
6. gesture overlays;
7. minimap and legend;
8. context menu;
9. dossier and announcements.

Every overlay must define pointer ownership, keyboard ownership, z-index/order, dismissal behavior and test selectors.

### 6.3 Interaction system

#### IN-001 — Radial context menu

The menu appears at the selected node/edge, clamps to the viewport, supports keyboard navigation, and exposes only actions valid for the target.

Node actions may include:

- Inspect dossier;
- Focus neighbourhood;
- Expand one hop;
- Pin/unpin position;
- Mark visited;
- Add local note;
- Hide/show from working view.

Edge actions may include:

- Inspect relationship;
- Focus route;
- Focus both endpoints;
- Hide/show relationship;
- Copy stable ID;
- Add local note.

Actions must be clearly labelled as presentation or local investigation actions. No context action may silently call a fraud verdict or mutate authoritative evidence.

#### IN-002 — Hover contextual panels for nodes and relationships

The engine must provide a real, target-aware contextual panel when the investigator hovers a node or relationship. This is more than a browser tooltip: it is a small, anchored preview surface that explains the object in place while preserving the graph as the primary workspace.

The same preview must be available when a graph target receives keyboard focus. Touch has no hover state, so a tap opens the equivalent persistent preview/dossier through the selection path.

**Node hover panel content:**

- type-aware glyph and display label;
- record type and status, represented with text, icon, shape and colour;
- stable node ID;
- safe summary;
- cluster or presentation group when supplied;
- connection count and visible-neighbour count;
- source system and provenance reference when available;
- compact actions for `Inspect`, `Focus neighbourhood` and `Pin/unpin`.

**Relationship hover panel content:**

- source node and target node, each with stable ID;
- direction shown textually and visually;
- relationship family and safe summary;
- observed time or temporal interval when supplied;
- confidence or strength only when supplied by the contract;
- source system and provenance reference;
- compact actions for `Inspect relationship`, `Focus route` and `Focus endpoints`.

**Interaction policy:**

- open after a short configurable delay, recommended default 120–180 ms, to avoid flicker while crossing a dense graph;
- close after pointer leave with a short grace period so the investigator can move from the target into the panel;
- keep the panel open while the pointer is inside the panel;
- clamp or flip the panel so it never leaves the viewport;
- do not trigger a full graph re-render or a network request for a hover preview;
- cancel stale open/close timers when the pointer or focus target changes;
- keep an explicitly selected node/edge dossier authoritative; hovering another target may show a labelled transient preview but must not replace the active selection;
- allow the user to promote the preview to a persistent dossier with `Inspect` or click/tap;
- close on Escape, target loss, explicit dismissal or selection of a different object according to the configured policy;
- never encode a conclusion, guilt signal or hidden relationship in the preview;
- expose the same information through the semantic graph path even when visual hover is unavailable.

**Accessibility policy:**

- keyboard focus produces the same preview content as pointer hover;
- the panel has a stable accessible name and describes its target;
- an actionable panel uses dialog semantics and a non-actionable short preview may use tooltip semantics;
- hover must not steal keyboard focus automatically;
- focus enters the panel only through an explicit keyboard action or action invocation;
- the panel remains usable at 200% zoom, in high contrast and with reduced motion;
- assistive technology receives a concise update without an announcement for every pointer pixel;
- no critical information is available only on hover.

**Acceptance criteria:**

1. Hovering a node opens the node panel with the correct stable ID and safe fields.
2. Hovering an edge opens a relationship panel with correct source, target and direction.
3. The panel remains reachable when the target is near any viewport edge.
4. Moving from target to panel does not close it prematurely.
5. Hovering another target does not overwrite an explicitly selected dossier.
6. Keyboard focus exposes equivalent information without requiring a mouse.
7. Touch opens the equivalent persistent panel through selection.
8. Rapid target changes never display stale content.
9. Reduced-motion mode removes panel animation but keeps the panel available.
10. The feature is covered by unit, component, browser, accessibility and visual regression tests.

Hover is an enhancement to pointer exploration, not the only access path to any important fact.

#### IN-003 — Lasso selection

Support pointer/touch lasso with:

- visible selection boundary;
- additive selection with `Shift`/equivalent;
- subtractive selection with `Alt`/equivalent where supported;
- Escape cancellation;
- keyboard/semantic alternative through multi-select controls;
- explicit selected-count announcement.

#### IN-004 — Multi-selection and comparison

Allow multiple nodes and edges to be selected, with a compact comparison panel showing common fields, differences and relationship intersection. Avoid implying that co-selection proves a causal link.

#### IN-005 — Node movement and bounded physics

The movement model must support:

- pointer and touch drag;
- keyboard nudge with a documented step;
- optional inertia on release;
- anchor/pin state;
- bounded spring/repulsion forces;
- collision avoidance sufficient for readability;
- stable settle detection;
- explicit Motion toggle;
- reduced-motion default;
- fixed-tick simulation for tests;
- cancellation without committing a position.

#### IN-006 — Camera controls

Support pan, pointer-centred zoom, fit graph, reset camera, keyboard zoom, and predictable resize. Node dragging and background panning must never be ambiguous.

#### IN-007 — Path and route inspection

Selecting an edge or two endpoints may produce a route view showing ordered nodes, directed edges, timestamps and safe summaries. Route emphasis must be derived from the supplied graph, not invented by the renderer.

### 6.4 Layout and disclosure

#### LY-001 — Layout modes

Provide a renderer-neutral layout interface with at least:

- `free` — preserve working positions;
- `force` — deterministic bounded force layout;
- `radial` — selected node or cluster at the centre;
- `hierarchical` — direction-aware layers;
- `timeline` — temporal ordering where timestamps exist;
- `grid` or `matrix` — fallback for dense/ambiguous graphs.

Each layout must declare required metadata, supported graph sizes, determinism guarantees and whether it preserves pinned nodes.

#### LY-002 — Hybrid layout policy

Default policy:

- honour supplied positions;
- honour pinned nodes;
- preserve the selected node’s screen region when practical;
- run expensive layout only on explicit command or initial mount;
- keep a previous layout available for undo/cancel;
- never rearrange a graph continuously without an observable reason.

#### LY-003 — Progressive disclosure

Implement graph-size policies:

- small: show all labels and relationships;
- medium: show selected-neighbourhood labels and filtered context;
- large: cluster, collapse, aggregate or switch to matrix/list views;
- very large: require explicit expansion and use a scale-appropriate renderer.

Thresholds must be configuration, measured and tested rather than hard-coded in individual renderers.

#### LY-004 — Cluster operations

Support cluster focus, collapse, expand, fit cluster and compare clusters. A cluster is a presentation grouping unless the snapshot explicitly supplies a domain grouping.

### 6.5 Investigation utilities

#### EV-001 — Local evidence mode

Add a local working layer for:

- visited entities;
- investigator notes;
- pinned objects;
- local tags;
- selected paths;
- hidden/expanded relationships;
- a chronological action journal.

This layer must be serialisable, replayable and visibly distinct from authoritative evidence.

#### EV-002 — Timeline and provenance panel

Expose source system, provenance reference, observed time and presentation time separately. Use a timeline only when a temporal field exists; otherwise state that no time is supplied.

#### EV-003 — Investigation replay

Allow export/import of a safe replay bundle containing snapshot ID/hash, engine version, commands, layout seed and user-visible configuration. Exclude credentials, raw secrets and unsupported backend mutations.

#### EV-004 — Undo/redo of presentation actions

Undo/redo layout moves, filters, local tags, notes, focus and camera changes. Do not present undo as reversing authoritative evidence.

### 6.6 Accessibility and resilience

#### AX-001 — Semantic graph path

Provide a persistent or easily reachable HTML list/tree/table representation with:

- node/edge names and stable IDs;
- status text;
- relationship source/target and direction;
- keyboard selection and activation;
- focus return after menus/panels close;
- live announcements for selection, count and action result.

#### AX-002 — Reduced motion and high contrast

Respect `prefers-reduced-motion`, expose a visible Motion control, and offer a high-contrast theme. No required action may depend on animation.

#### AX-003 — Failure-safe renderer fallback

If a renderer fails to load, fails qualification, or throws during mount:

- preserve the snapshot and semantic path;
- show a clear non-blocking error;
- provide retry and fallback controls;
- record a diagnostic event without leaking sensitive data.

### 6.7 Performance and scale

#### PF-001 — Defined user-visible milestones

Measure:

- first useful render;
- semantic fallback ready;
- first selection visible;
- context menu visible;
- dossier visible;
- fit/reset complete;
- resize recovery complete;
- layout settle complete;
- frame health during drag and motion;
- long tasks and memory growth.

#### PF-002 — Rendering strategy

Keep the adapter boundary open to:

- SVG for small, semantic, inspectable graphs;
- Canvas/WebGL for larger scenes;
- hybrid DOM overlay for labels, menus and accessibility.

The selected strategy must be evidence-backed by the qualification suite, not by preference.

#### PF-003 — Work scheduling

Use dirty-region or dirty-layer updates, requestAnimationFrame for visual ticks, worker/off-main-thread layout where justified, throttled minimap updates and batched DOM updates. Do not rebuild the full graph for every physics tick.

---

## 7. Target architecture

### 7.1 Module boundaries

```text
GraphSnapshot / Graph DTOs
          |
          v
  Contract validator + normaliser
          |
          v
  Renderer-neutral engine state
          |
          +--> Interaction controller ----> Commands / Events / Replay journal
          |
          +--> Layout service ------------> Working positions / settle state
          |
          +--> Presentation policy --------> Tokens / labels / focus / disclosure
          |
          v
  Adapter view model
          |
          +--> SVG adapter
          +--> Cytoscape adapter
          +--> Canvas/WebGL adapter
          +--> Semantic fallback
          |
          v
  Context panels, menus, minimap, legend and announcements
```

### 7.2 Proposed package structure

```text
apps/web/src/graph-engine/
  contract.ts              # snapshots, IDs, validation and normalisation
  state.ts                 # serialisable engine state
  commands.ts              # command and event types
  reducer.ts               # pure command reducer
  controller.ts            # pointer/keyboard/touch intent translation
  selection.ts             # node, edge, neighbourhood and path selection
  context-menu.ts          # target-aware action catalogue
  layout.ts                # layout interface and shared helpers
  layouts/
    free.ts
    force.ts
    radial.ts
    hierarchical.ts
    timeline.ts
    grid.ts
  physics.ts               # bounded deterministic motion step
  disclosure.ts             # graph-size policy and cluster visibility
  presentation.ts           # glyphs, status and relationship tokens
  replay.ts                # export/import, validation and redaction
  accessibility.ts         # semantic projection and announcements
  performance.ts           # marks, frame counters and long-task hooks
  testkit.ts               # fixtures, command helpers and assertions
  examples.ts              # deterministic scenario catalogue
```

Renderer adapters must remain outside the core state/reducer path. They may translate engine state into renderer-specific objects, but they must not own authoritative selection, IDs or investigation commands.

### 7.3 Core type sketch

```ts
type GraphId = string;
type NodeId = string;
type EdgeId = string;

interface GraphSnapshot {
  schemaVersion: string;
  snapshotId: GraphId;
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata: GraphMetadata;
}

interface GraphEngineState {
  snapshot: GraphSnapshot;
  selection: SelectionState;
  camera: CameraState;
  layout: LayoutState;
  filters: FilterState;
  presentation: PresentationState;
  investigation: LocalInvestigationState;
  runtime: RuntimeState;
}

type GraphCommand =
  | { type: "SelectNode"; nodeId: NodeId; source: InputSource }
  | { type: "SelectEdge"; edgeId: EdgeId; source: InputSource }
  | { type: "PreviewNodeMove"; nodeId: NodeId; position: Point }
  | { type: "CommitNodeMove"; nodeId: NodeId; position: Point }
  | { type: "SetLayoutMode"; mode: LayoutMode; seed: number }
  | { type: "ExecuteContextAction"; action: ContextActionId; target: GraphTarget };
```

The exact names may change during implementation, but the boundaries and invariants must not be weakened without an ADR.

### 7.4 Interaction state machine

```text
Idle
 |- pointer-down on node -> NodePress
 |     |- movement threshold -> NodeDragging
 |     |     |- pointer-up -> CommitNodeMove -> Settling/Idle
 |     |     `- escape -> CancelNodeMove -> Idle
 |     `- pointer-up -> Selected -> DossierOpen/Idle
 |- pointer-down on background -> CameraPress
 |     |- movement threshold -> CameraPanning
 |     |     `- pointer-up -> Idle
 |     `- pointer-up -> ClearSelection or no-op
 |- context-menu -> ContextMenuOpen
 |- keyboard focus -> Focused
 `- lasso start -> LassoSelecting
```

The controller must classify intent explicitly. A click is not a drag, a node drag is not camera pan, and a preview is not a committed investigation action.

---

## 8. Delivery roadmap

The roadmap is ordered by dependency and risk. A phase is complete only when its exit criteria and required tests pass.

### Phase 0 — Contract and evidence freeze

**Objective:** Make the future work safe to implement in parallel.

**Tasks:**

- freeze the versioned graph snapshot additions;
- define selection, layout, camera and investigation state schemas;
- define command/event envelope and source labels;
- add invalid-input fixtures;
- define deterministic seed and simulation-clock rules;
- record ADRs for any contract change;
- update traceability and implementation status documents.

**Deliverables:** contract types, validator, state schema, command catalogue, fixture matrix and ADR.

**Exit criteria:** existing gallery and React board compile; all current examples validate; no renderer imports appear in core types.

### Phase 1 — Pure engine controller

**Objective:** Move interaction semantics out of ad-hoc component handlers.

**Tasks:**

- implement pure reducer;
- implement command validation;
- implement selection/focus/neighbourhood logic;
- implement camera/layout separation;
- implement command journal and deterministic replay;
- add undo/redo for presentation state;
- expose a testkit for actions and state assertions.

**Deliverables:** controller, reducer, replay module, state tests and migration notes for gallery/React integration.

**Exit criteria:** all core journeys pass without a renderer; replay output matches expected state snapshots.

### Phase 2 — Visual system and overlay architecture

**Objective:** Establish the visual language once and consume it from every adapter.

**Tasks:**

- finalise glyph registry and status tokens;
- implement edge-family and direction tokens;
- implement focus, selected, dimmed and disabled states;
- implement overlay layer ownership;
- add high-contrast and reduced-motion themes;
- align gallery and React board visual semantics.

**Deliverables:** token registry, glyph catalogue, overlay primitives, visual examples and screenshot baselines.

**Exit criteria:** each state remains distinguishable without colour; screenshots show consistent node, edge and focus treatments across adapters.

### Phase 3 — Context actions and investigation panels

**Objective:** Make every selected graph object actionable and explainable.

**Tasks:**

- implement radial context menu;
- implement anchored hover/focus panels for nodes and relationships;
- implement keyboard menu and semantic equivalent;
- add node, edge and multi-selection dossiers;
- add route/path panel;
- add focus-neighbourhood and expand-one-hop commands;
- implement focus return and live announcements.

**Deliverables:** context action catalogue, menus, dossiers, route view, accessibility tests and browser journeys.

**Exit criteria:** a user can inspect a node or edge entirely via keyboard; menu commands are replayable; no command mutates authoritative evidence.

### Phase 4 — Movement, layouts and disclosure

**Objective:** Provide a tactile graph that stays readable under manipulation.

**Tasks:**

- extract physics constants and deterministic tick API;
- add pinned nodes and collision policy;
- add free, force, radial, hierarchical, timeline and grid layouts;
- add lasso and multi-selection;
- add cluster collapse/expand/focus;
- add graph-size disclosure policy;
- preserve manual positions across view/layout changes.

**Deliverables:** layout service, layout controls, lasso controller, disclosure policy and scale fixtures.

**Exit criteria:** layout modes are deterministic under fixed seed; manual positions survive mode changes as specified; large fixtures remain usable.

### Phase 5 — Local investigation layer and replay

**Objective:** Let Hercule work through a case without repeatedly reopening it manually.

**Tasks:**

- add visited state and local tags;
- add notes and annotations;
- add local evidence markers with clear non-authoritative styling;
- add journal/timeline of commands;
- export/import replay bundle;
- add redaction and schema validation;
- provide reset/undo/redo.

**Deliverables:** local working-layer model, replay bundle format, import/export UI and end-to-end journey.

**Exit criteria:** a complete investigation session can be exported and replayed offline with no credentials or hidden backend mutation.

### Phase 6 — Performance and renderer qualification

**Objective:** Prove the engine works across the supported rendering strategies.

**Tasks:**

- instrument user-visible milestones;
- add repeated-run performance harness;
- measure frame health, long tasks and memory;
- run the same command script through each adapter;
- qualify SVG, Cytoscape, D3, Sigma, React Flow and any future candidate against frozen requirements;
- document the conditional production decision;
- implement semantic fallback and renderer failure recovery.

**Deliverables:** reproducible reports, comparison exhibit, performance baselines, adapter conformance matrix and ADR update.

**Exit criteria:** no hard requirement fails; performance envelope is supported by repeated evidence; the production renderer decision is explicit.

### Phase 7 — Gallery, documentation and release hardening

**Objective:** Make the result reviewable, embeddable and maintainable.

**Tasks:**

- update the static gallery with every accepted feature;
- add an examples gallery for each engine capability;
- update implementation status and research ledger;
- add screenshots and known limitations;
- run local release gate;
- optionally run environment/package qualification with the `fga` Databricks profile, separately from renderer tests;
- prepare release notes and rollback guidance.

**Deliverables:** final gallery, docs, reports, release checklist and reproducible commands.

**Exit criteria:** local gate passes; browser/accessibility/performance reports are attached; no undocumented feature or dependency remains.

---

## 9. Detailed implementation slices

### 9.1 Context menu slice

1. Define target model: node, edge, multi-selection, cluster or background.
2. Define action catalogue and capability predicates.
3. Render menu with stable test IDs and accessible names.
4. Clamp menu to viewport and avoid selected node occlusion.
5. Add keyboard roving focus and Escape dismissal.
6. Return focus to the originating graph target.
7. Dispatch a command rather than mutating the component directly.
8. Record source and target in the event journal.
9. Add local and browser tests.

### 9.2 Hover contextual panel slice

1. Define the shared `GraphTargetPreview` model for node and relationship targets.
2. Define the node and relationship field policies so the panel cannot invent or infer evidence.
3. Add pointer-enter/focus-in intent handling with configurable open delay and close grace period.
4. Add stale-timer cancellation and target-generation checks.
5. Render a target-anchored panel with viewport collision detection and edge flipping.
6. Keep the selected dossier and transient hover preview as separate state targets.
7. Add promotion from preview to persistent dossier.
8. Add keyboard, touch, Escape and explicit-dismissal paths.
9. Add tooltip/dialog semantics, accessible names and live-update throttling.
10. Add node and relationship fixtures, browser probes and visual baselines at all viewport corners.

### 9.3 Edge-direction slice

1. Validate source/target IDs and direction.
2. Add arrow marker or directional glyph.
3. Add family-specific stroke patterns.
4. Add selected-route emphasis.
5. Add edge hit area larger than the visual stroke.
6. Ensure edge labels do not block node interaction.
7. Add semantic relationship text.
8. Test self-loops, parallel edges, reversed edges and missing metadata.

### 9.4 Lasso and multi-select slice

1. Add explicit gesture state.
2. Convert screen coordinates through camera transform.
3. Use spatial index or bounded scan for hit testing.
4. Render selection rectangle/polygon as an overlay.
5. Support additive/subtractive modifiers.
6. Announce selected count.
7. Expose semantic bulk-selection controls.
8. Add cancel and resize tests.

### 9.5 Layout slice

1. Define `LayoutInput`, `LayoutOptions`, `LayoutResult` and diagnostics.
2. Keep pinned nodes fixed unless explicitly overridden.
3. Preserve existing positions when a layout mode is not authoritative.
4. Use deterministic seed and bounded iteration count.
5. Expose progress and cancellation for expensive layouts.
6. Store previous positions for undo.
7. Add fixtures for disconnected components, self-loops and parallel edges.
8. Add visual and numerical acceptance checks.

### 9.6 Evidence/replay slice

1. Define local working-layer schema.
2. Define safe export envelope and redaction rules.
3. Hash the source snapshot and record engine/schema version.
4. Serialise commands, not renderer events.
5. Validate imported commands before applying them.
6. Reject unsupported or future versions with an actionable message.
7. Add deterministic replay tests and a browser export/import journey.

---

## 10. Complete test strategy

### 10.1 Test principles

The test system must prove both visual usefulness and engineering correctness.

- Prefer pure tests over browser tests when a behavior can be isolated.
- Use browser automation for focus, pointer geometry, rendering integration and accessibility.
- Use deterministic fixtures and fixed seeds.
- Never use arbitrary sleeps for correctness.
- Test user-visible milestones, not internal implementation details alone.
- Run the same command sequences through every candidate renderer.
- Keep Databricks and network access out of local renderer tests.
- Treat snapshots and expected command results as reviewable evidence.
- Keep the visible auto-test suite deterministic, isolated from the investigator's working state and usable as both a manual demonstration and an automation seam.
- Separate visual regression from semantic correctness.
- Record environment, commit, browser, viewport, fixture hash and dependency versions.

### 10.2 Test layers

| Layer | Purpose | Typical tool | Required frequency |
|---|---|---|---|
| T0 Static | Types, lint, import boundaries, generated contract validation | TypeScript/Vite/linter | Every change |
| T1 Contract unit | Snapshot validation, IDs, normalisation, schemas | Vitest | Every change |
| T2 Pure engine unit | Reducer, commands, selection, camera, disclosure | Vitest | Every change |
| T3 Physics/layout unit | Determinism, bounds, convergence, cancellation, pinned nodes | Vitest/property tests | Every change |
| T4 Adapter conformance | Same snapshot and commands across renderers | Vitest/browser | Every adapter change |
| T5 Component integration | React board, panels, menus, semantic fallback | Testing Library/Vitest | Every UI change |
| T6 Browser journey | Pointer, touch, keyboard, lasso, replay, resize and failure states | Playwright | Every feature slice |
| T7 Accessibility | Axe plus keyboard/screen-reader-oriented DOM assertions | Playwright/Axe | Every UI change and release |
| T8 Visual regression | Golden screenshots and state captures | Playwright snapshots | Visual changes and release |
| T9 Performance | Milestones, frame health, long tasks and memory | Playwright/PerformanceObserver | Baseline and release |
| T10 Resilience/security | Invalid data, renderer failure, redaction, dependency/license checks | Vitest/scripts | Release and contract changes |
| T11 Manual exploratory | Usability, visual hierarchy, touch feel and assistive review | Human checklist | Release candidate |
| T12 Environment qualification | Packaging/data integration in target workspace | Databricks/local gate | Deployment or schema changes |

### 10.2.1 Visible graph auto-test contract

The gallery quality gate is part of the engine experience, not a hidden developer-only console. It must:

- expose a compact bottom panel that does not block graph pointer interaction;
- show one row per check with the instruction, expected result, observed result, status and elapsed time;
- support `Run all`, `Run` for one check, `Clear` and collapse/expand;
- isolate every check with a presentation-state snapshot and restore it after execution;
- distinguish `queued`, `running`, `passed`, `failed` and `not applicable`;
- expose a stable automation seam (`window.fgaGraphAutoTest`) without leaking renderer-native objects;
- keep the evidence snapshot and published relationships unchanged when testing working-layer behaviour;
- include browser and accessibility coverage for the panel itself and its interaction with the graph.

### 10.3 Fixture catalogue

Every fixture must have a stable ID, description, expected hash and expected capabilities.

| Fixture | Purpose |
|---|---|
| `empty-academy-board` | Zero evidence, explicit empty state, semantic fallback |
| `single-node` | Node rendering, selection and no-edge dossier |
| `two-node-directed` | Direction, edge selection and route panel |
| `parallel-edges` | Multiple relationships between the same endpoints |
| `self-loop` | Loop geometry, hit testing and semantic description |
| `disconnected-components` | Fit, cluster focus and component layout |
| `shared-device-investigation` | Compact node/edge interaction journey |
| `temporal-path-tracing` | Ordered route and temporal presentation |
| `keyboard-and-semantic-journey` | No-pointer workflow and cancellation |
| `dense-cluster-progressive-disclosure` | 34-node/66-edge dense scene, minimap and disclosure |
| `invalid-dangling-edge` | Contract error and safe rejection |
| `duplicate-id` | Contract error and no partial mount |
| `unknown-record-type` | Fallback glyph and accessible label |
| `large-bounded` | Performance envelope and cluster policy |
| `stress-renderer` | Renderer-specific upper observation, not a hidden product promise |

### 10.4 Contract and state tests

Required assertions:

- duplicate node IDs fail validation;
- duplicate edge IDs fail validation;
- dangling source/target fails or is explicitly reported;
- self-loop behavior is defined;
- parallel edges remain distinct;
- unknown type gets a fallback glyph and label;
- snapshot hash is stable for equivalent serialisation;
- selection accepts only existing IDs;
- clearing selection is idempotent;
- hidden/filtered IDs never disappear from the source snapshot;
- camera operations never change graph positions;
- layout operations never change graph evidence fields;
- local notes and tags remain separate from source fields;
- replay rejects unsupported schema versions;
- imported commands cannot execute backend mutations.

### 10.5 Interaction-controller tests

| Test ID | Scenario | Expected result |
|---|---|---|
| INT-001 | Click node | Node selected, dossier target set, one selection event |
| INT-002 | Click edge | Edge selected, route dossier shown |
| INT-003 | Click background | Selection cleared only according to configured policy |
| INT-004 | Right-click node | Node menu opens at clamped position |
| INT-005 | Right-click edge | Edge-specific menu opens |
| INT-006 | Escape menu | Menu closes and origin focus returns |
| INT-007 | Escape drag | Position preview cancelled, original position restored |
| INT-008 | Drag node below threshold | Remains a click, no movement commit |
| INT-009 | Drag node above threshold | Preview updates, one commit on release |
| INT-010 | Drag background | Camera pans, node positions unchanged |
| INT-011 | Wheel zoom on node | Camera zooms around pointer, selected node remains under pointer |
| INT-012 | Keyboard select | Focused target receives equivalent selection command |
| INT-013 | Keyboard context menu | Same action catalogue as pointer menu |
| INT-014 | Lasso nodes | Expected IDs selected, count announced |
| INT-015 | Shift-lasso | IDs added without clearing existing selection |
| INT-016 | Multi-select comparison | Common/different fields rendered without invented conclusions |
| INT-017 | Focus neighbourhood | Immediate context retained; unrelated graph dimmed/hidden by policy |
| INT-018 | Expand one hop | New visible IDs are from the snapshot only |
| INT-019 | Cluster collapse | Presentation state changes; source graph remains intact |
| INT-020 | Resize during gesture | Gesture cancels safely or transforms predictably |
| HOV-001 | Hover node | Anchored node preview opens after the configured delay with the correct ID and safe fields |
| HOV-002 | Hover relationship | Anchored edge preview opens with correct source, target, direction and family |
| HOV-003 | Leave target | Preview closes after the grace period unless the pointer enters the panel |
| HOV-004 | Move into preview | Panel remains open and actionable while the pointer is inside it |
| HOV-005 | Target near viewport edge | Panel flips or clamps and remains fully visible |
| HOV-006 | Hover selected target | Active dossier remains authoritative and duplicate content is avoided |
| HOV-007 | Hover another target while selected | Transient preview is labelled and does not replace selected IDs |
| HOV-008 | Rapidly cross targets | No stale node/edge content remains after the final target changes |
| HOV-009 | Keyboard focus target | Same preview information is available without a pointer |
| HOV-010 | Touch tap target | Equivalent persistent preview/dossier opens through selection |
| HOV-011 | Escape preview | Preview closes and focus/selection policy is preserved |
| HOV-012 | Reduced motion | Panel remains available with animation disabled |

### 10.6 Physics and layout tests

Required numerical and property assertions:

- fixed seed plus fixed ticks gives identical positions;
- no node leaves configured bounds;
- maximum speed is respected;
- NaN and infinite positions are rejected or corrected;
- empty graph does not start a frame loop;
- isolated nodes remain stable;
- dangling edges do not crash the step;
- self-loops do not create unbounded force;
- parallel edges do not multiply force unexpectedly without an explicit policy;
- pinned nodes remain within tolerance;
- drag release velocity decays toward zero;
- settle detection stops the loop;
- reduced-motion mode does not run continuous animation;
- Motion off immediately stops visual ticks;
- cancellation restores the last committed position;
- layout cancellation returns a valid previous state;
- layout is invariant to input array order when the documented sort/seed policy applies;
- layout never changes node/edge IDs or evidence fields;
- cluster collapse preserves the ability to restore the previous view.

Property-test ranges should include zero, one, two, disconnected, dense, cyclic, self-loop and mixed-type graphs.

### 10.7 Renderer adapter conformance

For each adapter, run the same fixture and command script and assert:

- mount succeeds;
- all stable node and edge IDs are discoverable;
- selection emits project-owned IDs;
- edge source/target direction is preserved;
- pan, zoom, fit and reset work;
- preset positions are honoured;
- node movement preview/commit/cancel behaves identically;
- context menu target is correct;
- semantic fallback remains available;
- unmount removes listeners and animation frames;
- renderer error does not destroy the application state;
- context dossier content is renderer-independent;
- unsupported features are declared rather than silently approximated.

### 10.8 Accessibility tests

Automated checks:

- zero Axe violations on initial, selected, menu-open, panel-open, error and fallback states;
- no nested interactive SVG semantics;
- all interactive targets have accessible names;
- tab order is predictable;
- focus is visible;
- focus returns after menu/panel dismissal;
- Escape closes transient UI;
- keyboard-only user can select a node, edge and menu action;
- keyboard focus exposes the same node/relationship preview information as pointer hover;
- hover preview does not steal focus or become the only route to important information;
- actionable preview panels have correct dialog semantics and focus behavior;
- selected state is announced or represented with an accessible state;
- node and edge status is available as text;
- colour contrast passes for normal and high-contrast themes;
- reduced-motion preference disables non-essential animation;
- touch targets meet the configured minimum size;
- zoom and pan have non-pointer alternatives;
- semantic fallback exposes the complete graph when visual rendering fails.

Manual accessibility review:

- NVDA/JAWS or equivalent screen-reader pass on Windows;
- keyboard-only pass with no mouse or touch;
- 200% zoom and narrow viewport pass;
- high-contrast and forced-colour pass;
- reduced-motion pass;
- cognitive load review of labels, actions and panel hierarchy.

### 10.9 Visual regression tests

Capture deterministic screenshots for:

1. empty board;
2. dense board initial state;
3. selected node;
4. selected edge;
5. node hover preview;
6. relationship hover preview;
7. node/relationship preview near each viewport corner;
8. context menu near each viewport corner;
9. lasso selection;
10. collapsed cluster;
11. radial layout;
12. timeline layout;
13. semantic fallback;
14. high-contrast theme;
15. reduced-motion theme;
16. renderer error fallback;
17. compact/mobile viewport;
18. 200% browser zoom.

Visual baselines must be reviewed for meaning, not merely pixel similarity. A baseline update requires a reason, reviewer and linked feature/ADR.

### 10.10 Performance test plan

#### Milestones

Use the frozen envelope as the starting gate:

| Metric | Initial target |
|---|---:|
| First useful render on T02 | ≤ 1000 ms |
| Selection visible | ≤ 100 ms |
| Fit/reset on fixed fixture | ≤ 500 ms |
| Resize recovery | ≤ 500 ms |
| Semantic fallback after DOM commit | Immediate |

Add the following targets after baseline measurement:

- no sustained frame below the documented interaction floor during node drag;
- no unbounded long-task growth during physics;
- no listener or animation-frame growth after mount/unmount cycles;
- stable memory after repeated scenario switching;
- context menu and dossier appear within the selection milestone;
- hover preview appears within the configured preview budget and never blocks graph input;
- layout cancellation returns control within the configured cancellation budget.

#### Method

Each run records:

- commit SHA;
- dependency lockfile hash;
- browser and version;
- operating system;
- viewport and device scale factor;
- fixture ID and content hash;
- renderer and exact version;
- warm/cold status;
- repetition number;
- discarded-run reason;
- raw marks, percentiles and frame statistics.

At least 10 repetitions are required for a formal baseline. Two-run measurements are exploratory evidence only.

#### Test sizes

- T02: 7 nodes / 7 edges;
- compact: 20–50 nodes;
- dense: 34 nodes / 66 edges;
- medium: 250 nodes / 500 edges;
- large observation: 1,000 nodes / 2,000 edges;
- stress observation: 5,000+ nodes, only if the adapter supports it.

Large and stress observations must not become unannounced product requirements. The supported envelope is declared after evidence and ADR review.

### 10.11 Resilience and security tests

- malformed JSON cannot execute code;
- unsafe labels are escaped in SVG, HTML and menus;
- malicious IDs cannot escape selectors or test hooks;
- provenance URLs are displayed safely and do not auto-navigate without explicit action;
- exported replay bundles contain no token, cookie or secret;
- renderer exceptions are caught and reported without sensitive payloads;
- repeated mount/unmount does not leak listeners, timers or observers;
- oversized labels and unusually large metadata cannot freeze the UI;
- invalid layout coordinates are sanitised;
- dependency and licence inventory is checked in CI;
- commercial-only packages cannot enter the OSS production bundle without an explicit approved ADR.

### 10.12 Optional Databricks qualification

Databricks qualification is an integration concern, not a prerequisite for local graph-engine tests.

When environment credentials and the `fga` profile are available, run a separate qualification track that verifies:

- package/deployment completeness;
- fixture/schema compatibility;
- row and structure counts where applicable;
- report generation and provenance;
- failure behavior when the workspace is unavailable.

The renderer suite must remain runnable with no Databricks profile, no network and no external data. A Databricks failure must not invalidate a local interaction or accessibility result; it receives its own status and evidence report.

---

## 11. Test execution matrix

### 11.1 Fast local gate

Run on every implementation change:

```powershell
cd C:\Users\angel.alvarez\PycharmProjects\fraud-graph-arena\apps\web
npm run typecheck
npm test -- --run
npm run build
```

### 11.2 Focused graph-engine gate

Run when changing the engine, gallery or board interaction:

```powershell
cd C:\Users\angel.alvarez\PycharmProjects\fraud-graph-arena\apps\web
npm test -- src/graph-engine src/board/GraphViewport.test.tsx -- --run
npm run test:e2e -- e2e/gallery-mini-game.spec.ts
npm run test:e2e -- e2e/qualification-exhibit.spec.ts
```

The exact npm script names are part of the repository contract. If a script is renamed, update this file and the release checklist in the same change.

### 11.3 Full local qualification gate

The full local gate must include:

```powershell
cd C:\Users\angel.alvarez\PycharmProjects\fraud-graph-arena
python scripts/run_iteration_06_local_gate.py
```

The gate must report, at minimum:

- contract validation;
- Python checks;
- frontend typecheck/build;
- unit/component tests;
- browser tests;
- accessibility results;
- renderer comparison status;
- generated evidence locations;
- explicit skipped/blocked checks and reasons.

### 11.4 Release candidate gate

The release candidate requires:

- fast local gate green;
- focused graph-engine gate green;
- full local qualification green;
- visual baseline review complete;
- manual accessibility checklist complete;
- performance baseline complete with at least 10 repetitions;
- dependency/licence audit complete;
- no unresolved P0/P1 issue;
- implementation status and research ledger updated;
- release evidence stored with commit and fixture hashes;
- optional `fga` Databricks qualification reported separately when requested.

---

## 12. Acceptance criteria and release gates

### 12.1 Feature-level acceptance

A feature is accepted only when:

1. its contract and state transitions are documented;
2. it has at least one deterministic fixture;
3. it has pure tests where possible;
4. it has browser coverage for user-visible behavior;
5. it has accessibility coverage if interactive;
6. it has visual review if it changes presentation;
7. it has no undocumented evidence mutation;
8. it declares renderer capabilities and limitations;
9. it updates implementation status and traceability;
10. it passes the relevant local gate.

### 12.2 Renderer-level acceptance

A renderer is qualified only if it satisfies every hard requirement in `RENDERER_REQUIREMENTS.md`, including:

- semantic node styling;
- semantic relationship styling;
- stable selected IDs;
- zoom/pan;
- fit/reset;
- preset positions;
- predictable resize;
- lifecycle cleanup;
- persistent details;
- semantic fallback;
- acceptable measured performance;
- production-suitable version;
- compatible licence;
- no renderer-native objects in application contracts.

### 12.3 Release severity

| Severity | Examples | Release rule |
|---|---|---|
| P0 | Data/evidence mutation, security leak, crash on valid fixture | Block release |
| P1 | Cannot select/inspect, keyboard path broken, renderer loses IDs, severe accessibility failure | Block release |
| P2 | Layout instability, incorrect focus, performance target miss, visual regression | Fix or explicitly accept with owner and follow-up |
| P3 | Cosmetic inconsistency, minor copy, non-critical polish | May defer with ticket |

---

## 13. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Physics makes targets move while selecting | High | Stable initial state, explicit Motion control, settle detection, reduced-motion policy |
| Context menu becomes a command dump | Medium | Target-specific capability catalogue and progressive disclosure |
| Visual hierarchy hides evidence details | High | Selection-triggered dossier, graph-first layout and semantic fallback |
| Renderer adapters diverge | High | Shared command scripts, conformance harness and stable-ID assertions |
| Layout changes are mistaken for evidence changes | High | Separate snapshot and working positions, labels and replay events |
| SVG does not scale | Medium | Measure first, retain adapter boundary, qualify Canvas/WebGL independently |
| Large graph becomes a hairball | High | Clustering, disclosure policy, focus neighbourhood and alternate views |
| Accessibility is added too late | High | Semantic projection and Axe checks in every feature slice |
| Browser timing causes flaky tests | High | Deterministic seeds, fixed ticks, observable milestones and no arbitrary sleeps |
| Commercial feature envy leads to licence risk | High | Study behavior, reimplement independently, maintain licence inventory and ADR |
| Databricks availability blocks local progress | Medium | Keep renderer and interaction gates fully local; report environment checks separately |
| Feature scope expands without a decision | Medium | Feature IDs, phase exit criteria, ADRs and explicit non-goals |

---

## 14. Observability and diagnostics

The engine should expose a development-only diagnostic object containing:

- engine version and schema version;
- renderer name/version;
- snapshot ID/hash;
- node/edge counts and visible counts;
- current layout mode and seed;
- selection and focus IDs;
- motion enabled/reduced-motion state;
- frame count, last frame duration and dropped-frame estimate;
- active animation frame/timer counts;
- last command and event sequence;
- renderer capability flags;
- fallback/error state.

Diagnostics must never include credentials, raw secrets or unredacted sensitive metadata. Production logging should use event names and safe IDs only.

---

## 15. Documentation and traceability requirements

Every accepted feature must update:

- this build plan, if scope or acceptance changes;
- `IMPLEMENTATION_STATUS.md` with evidence and status;
- `TRACEABILITY.md` with source requirement, implementation and tests;
- `FGA_GRAPH_ENGINE_RESEARCH.md` with the decision, rejected alternatives and evidence;
- the example library or fixture catalogue;
- the relevant ADR when a boundary, dependency, licence or renderer decision changes;
- user-facing gallery/README documentation when the interaction changes.

The research record must distinguish:

- observed behavior;
- measured evidence;
- inference;
- design choice;
- rejected option;
- open question;
- unresolved blocker.

---

## 16. Definition of done

The feature build is complete when all of the following are true:

- the graph-first board is visually coherent and readable;
- nodes and edges have type-aware, multi-channel semantics;
- context menus work for nodes, edges, clusters and multi-selection;
- hovering or focusing a node/relationship opens a correct anchored contextual panel without replacing the active selection;
- node and edge dossiers are contextual, accessible and renderer-independent;
- node dragging, panning, zooming and layout changes are unambiguous;
- physics is bounded, controllable, deterministic under test and reduced-motion aware;
- lasso, multi-selection, focus and progressive disclosure work;
- layout modes preserve the evidence/presentation boundary;
- local notes, markers and replay are clearly non-authoritative;
- semantic fallback provides a complete non-canvas path;
- renderer adapters pass the same contract and command scripts;
- visual, accessibility, resilience and performance tests are green;
- test evidence is reproducible from local commands;
- optional Databricks qualification is reported separately, never substituted for local proof;
- implementation status, research ledger, traceability and ADRs are current;
- no article source is modified as part of engine implementation;
- no unlicensed or renderer-native implementation leaks into the core contract.

---

## 17. Recommended next implementation slice

The next practical slice should be **Phase 1 plus the first half of Phase 3**:

1. extract the current gallery interaction state into a pure controller;
2. define the command/event envelope and deterministic replay;
3. implement the target-aware context action catalogue;
4. add the radial node/edge menu;
5. add anchored hover/focus panels for nodes and relationships;
6. port the same menu and preview behavior into `GraphContextPanel`;
7. add keyboard, touch, Escape, focus-return and semantic-list coverage;
8. preserve the existing gallery journey while replacing direct DOM mutations with commands;
9. run the fast, focused and browser gates;
10. update traceability and the research ledger.

This slice delivers a major usability improvement while reducing future risk: every later feature—lasso, layouts, evidence markers, replay and renderer qualification—can build on the same explicit interaction boundary instead of adding more renderer-specific handlers.

---

## 18. Evidence checklist template

Use this checklist for every completed feature slice:

```text
[ ] Feature ID and scope recorded
[ ] Contract/state change documented
[ ] Renderer-neutral implementation exists
[ ] Gallery example or fixture added
[ ] Pure unit tests added
[ ] Component/browser tests added where applicable
[ ] Accessibility checks added
[ ] Visual baseline reviewed where applicable
[ ] Performance impact measured where applicable
[ ] Invalid/error/cancel path tested
[ ] Replay/determinism behavior tested
[ ] Security and licence implications reviewed
[ ] Implementation status updated
[ ] Traceability updated
[ ] Research ledger updated
[ ] ADR added or linked when required
[ ] Fast local gate passed
[ ] Focused graph-engine gate passed
[ ] Full local gate passed or explicit exception recorded
```

---

## 19. Closing design position

The engine should not compete with graph products by copying every feature they expose. It should combine the strongest transferable ideas—graph-first composition, direct manipulation, contextual inspection, multiple layouts, semantic fallback, controlled motion and professional diagnostics—inside a smaller, safer and more testable architecture for FGA.

The defining quality is not how many visual effects the board contains. It is whether Hercule can investigate, rearrange, annotate, replay and compare a case without losing the meaning of the underlying graph—and whether the same session can be proven automatically by the test suite.

