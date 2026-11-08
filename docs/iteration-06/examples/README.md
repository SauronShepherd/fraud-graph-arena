# FGA Graph Engine Example Library

This directory documents the example library in `apps/web/src/graph-engine/examples.ts`.

For a zero-install visual gallery, open [`gallery.html`](gallery.html) directly in a browser. It is a self-contained static file: double-click it, or use the browser’s “Open File” command. It does not require Vite, npm, an API, Databricks or network access.

The gallery opens on the dense-cluster scenario as an immersive investigation board, with no entity selected so the graph remains the protagonist. Selecting a node or relationship opens the contextual dossier as an overlay. The empty Academy board remains available as the first tab and still proves that zero evidence is an intentional state.

The gallery is deliberately a presentation and interaction lab. It mirrors the example contract but is not a production renderer, does not call the API, and does not authorize investigative actions.

The contextual dossier changes shape with the target: node selection shows identity, status, cluster, position, connected relationships and a presentation timeline; edge selection shows source-to-target routing, family, direction, confidence and relationship context. Selecting a connected item keeps the graph and panel in the same investigation flow.

The same information architecture now exists in the real React board through `apps/web/src/board/GraphContextPanel.tsx`; the static gallery remains the portable visual lab, while the board component is the application integration path.

The gallery is also a small, embeddable investigation game. It opens the dense case with one objective already primed, then guides the investigator through selecting an entity, interrogating a relationship, repositioning evidence and exploring the camera. `Hint` and `Restart` are intentionally local UI controls; they do not change the snapshot or claim a conclusion. The empty board remains free exploration because there is no evidence to score.

The interaction model separates camera state from graph layout state: dragging a node changes only its working position, while dragging the background pans the camera and the mouse wheel zooms around the pointer. Escape cancels an in-progress node or camera gesture. This follows a familiar graph-exploration pattern documented in [Neo4j Browser result frames](https://neo4j.com/docs/browser/operations/result-frames/) while keeping the implementation independent and renderer-neutral.

The dense board now has type-aware SVG glyphs for people, devices, accounts, banks, organisations and claim clusters. A lightweight, bounded physics pass uses relationship springs, local repulsion, damping and release velocity; it is dormant in the initial state, wakes when the investigator moves the graph, and can be paused or resumed with the `Motion` control. This gives the graph a tactile billiard-table response without turning the evidence snapshot into an uncontrolled animation.

The board also exposes an explicit contextual interaction layer: hover or keyboard focus opens a lightweight node/relationship preview that is itself interactive, while selection opens the full dossier and its actions. The preview remains alive for the short pointer transition from the target into the card, so its `+`, `−` highlight and `⌖` center actions can be clicked without the card disappearing. The investigator can mark nodes or relationships in a removable working list and click a marked target to recenter the camera on it. New working relationships can be composed between visible nodes; they use dashed lines, participate in the same context and selection path as detected relationships, and can be deleted because they belong to local presentation state. Detected relationships remain continuous and immutable.

For an article or static page, publish the file as an asset and embed it without a build dependency:

```html
<iframe
  title="FGA graph investigation mini-game"
  src="./gallery.html"
  loading="lazy"
  style="display:block;width:100%;min-height:900px;border:0"
></iframe>
```

The browser qualification lives in `apps/web/e2e/gallery-mini-game.spec.ts`. It exercises the objective loop, node movement, camera pan, wheel zoom, reset, all five scenarios, all four views, the visible six-check auto-test suite and an Axe accessibility audit. The article itself is not modified by this implementation.

The graph is also self-testable from the same surface. `Run all` makes the engine show each instruction, expected result, observed result, status and duration; `Run` executes one check. Every check restores the working graph state afterwards, and the automation seam is available as `window.fgaGraphAutoTest.runAll()`, `runOne(id)` and `getReport()`.

The library is a renderer-neutral contract catalogue. Each example contains:

- a safe graph snapshot with stable node and relationship IDs;
- recommended views (`node-link`, `matrix`, `path`, and `semantic-list`);
- explicit actions for pointer, keyboard and semantic-list entry points;
- movement preview/commit/cancel cases;
- expected outcomes that can be asserted by an adapter or browser test.

It deliberately contains no canonical truth, culpability, solve gate, scoring rule or renderer-native object. It is suitable for demos, adapter qualification, storybook-style exploration, contract tests and future replay fixtures.

## Included examples

| Example | What it teaches | Main engine capabilities |
|---|---|---|
| `empty-academy-board` | An honest empty projection | empty state, semantic fallback, safe fit/reset |
| `shared-device-investigation` | A compact investigation cluster | node/edge menus, cluster focus, matrix linking, movement commit |
| `temporal-path-tracing` | A directed sequence | edge focus, path view, source/target context, filtering |
| `keyboard-and-semantic-journey` | Non-pointer interaction | keyboard menus, semantic list, cancelled movement |
| `dense-cluster-progressive-disclosure` | A bounded dense graph | minimap policy, filtering, matrix view, progressive disclosure |

## Basic usage

```ts
import {
  createGraphEngineExampleLibrary,
  getGraphEngineExample,
  validateGraphEngineExample,
} from "./graph-engine";

const examples = createGraphEngineExampleLibrary();
const scenario = getGraphEngineExample("shared-device-investigation");

validateGraphEngineExample(scenario);
renderer.mount(scenario.snapshot);

for (const action of scenario.actions) {
  engine.dispatch(action);
}
```

The renderer receives only `snapshot`; the action sequence belongs to the engine/application boundary. A candidate adapter must not reinterpret the example as evidence or silently change its IDs.

## Recommended consumers

1. **Renderer adapters:** mount every snapshot and execute the same action sequence.
2. **Browser qualification:** assert menu anchoring, focus return, movement cancellation, view linking and semantic fallback.
3. **Manual comparison lab:** show each example in the same tabbed shell across all candidate renderers.
4. **Replay fixtures:** record only committed movement and validated commands; keep preview state out of the journal.
5. **Documentation:** use the examples as small, teachable stories instead of one overloaded 18-node fixture.

## Deliberate boundary

This is an example and contract library, not yet the production graph engine. It does not render, own investigation truth, perform layout, or authorize commands. Those responsibilities remain in the engine specification and the future renderer-neutral interaction controller.

