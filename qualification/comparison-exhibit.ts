import fixture from "./fixture-v1.json";
import "@xyflow/react/dist/style.css";
import { cytoscapeCandidate } from "./adapters/cytoscape";
import { d3Candidate } from "./adapters/d3";
import { reactFlowCandidate } from "./adapters/react-flow";
import { sigmaCandidate } from "./adapters/sigma";
import { buildHarnessResult, runQualificationLifecycle, type HarnessResult } from "./harness";
import type { CandidateInstance, FgaEdge, FgaNode, QualificationCandidate } from "./candidate-contract";
import { NODE_STATUS_META, type InvestigationStatus, relationshipColor, statusOf, visualMeta } from "./visual-semantics";

type ManualCheck = "selection" | "viewport" | "semantic" | "resize" | "cleanup";
type AutoStatus = "PENDING" | "PASS" | "BLOCKED";
type Target = { kind: "node" | "edge"; id: string };
type CardState = {
  key: string;
  candidate: QualificationCandidate;
  card: HTMLElement;
  surface: HTMLElement;
  instance: CandidateInstance | null;
  selected: Target | null;
  hovered: Target | null;
  autoStatus: AutoStatus;
  autoMessage: string;
  result: HarnessResult | null;
  manual: Record<ManualCheck, boolean>;
  visibleStatuses: Set<InvestigationStatus>;
  nodeOverrides: Record<string, InvestigationStatus>;
  clusterFilter: string | null;
  zoom: number;
};

type Tradeoff = { pros: readonly string[]; cons: readonly string[]; fit: string };
const tradeoffs: Record<string, Tradeoff> = {
  "Cytoscape.js": { pros: ["Graph-native styling, layouts and events", "Excellent relationship semantics", "MIT licence"], cons: ["Canvas-first integration needs a semantic companion", "React lifecycle needs an adapter boundary", "Large-scale rendering needs profiling"], fit: "Strongest graph-native baseline for FGA's replaceable adapter." },
  "Sigma.js": { pros: ["WebGL-focused network rendering", "Graphology model and scalable viewport", "Good fit for dense visible networks"], cons: ["Details and semantic UI remain application-owned", "Version pairing needs discipline", "Performance does not replace semantic review"], fit: "The scale candidate when visible-network rendering dominates." },
  D3: { pros: ["Maximum control over SVG and interaction", "Small primitives with no opinionated graph model", "ISC licence and modular composition"], cons: ["FGA owns hit-testing and graph behaviours", "Highest generic graph maintenance burden", "Accessibility bridges are application work"], fit: "Best when the visual language itself is the product." },
  "React Flow": { pros: ["Native React node composition", "Excellent zoom, selection and application ergonomics", "Straightforward custom node surfaces"], cons: ["Optimised for flows and editors", "Network layouts are usually external", "Dense graphs need careful subscriptions"], fit: "Best when rich React nodes outweigh graph-native analysis." },
};

const candidates: readonly QualificationCandidate[] = [cytoscapeCandidate, sigmaCandidate, d3Candidate, reactFlowCandidate];
const nodes: FgaNode[] = fixture.nodes.map((node) => ({ id: node.id, recordType: node.record_type, label: node.label, x: node.x, y: node.y, investigationStatus: node.investigation_status as InvestigationStatus, icon: node.icon, clusterId: node.cluster_id }));
const edges: FgaEdge[] = fixture.edges.map((edge) => ({ id: edge.id, sourceId: edge.source_id, targetId: edge.target_id, relationshipFamily: edge.relationship_family, relationshipType: edge.relationship_type, directed: edge.directed, confidence: edge.confidence }));
const statuses = Object.keys(NODE_STATUS_META) as InvestigationStatus[];
const matrix = document.querySelector<HTMLElement>("#matrix");
const tabs = document.querySelector<HTMLElement>("#engine-tabs");
const inspector = document.querySelector<HTMLElement>("#inspector");
const summaryBody = document.querySelector<HTMLTableSectionElement>("#summary-body");
const overallStatus = document.querySelector<HTMLElement>("#overall-status");
const reportElement = document.querySelector<HTMLElement>("#report");
if (!matrix || !tabs || !inspector || !summaryBody || !overallStatus || !reportElement) throw new Error("FGA06 comparison exhibit is missing required regions");
const tabsRoot: HTMLElement = tabs;
const inspectorRoot: HTMLElement = inspector;
const summaryBodyRoot: HTMLTableSectionElement = summaryBody;
const overallStatusRoot: HTMLElement = overallStatus;

const manualChecks: readonly { id: ManualCheck; label: string }[] = [
  { id: "selection", label: "Node and edge selection" },
  { id: "viewport", label: "Fit, zoom and pan" },
  { id: "semantic", label: "Labels, direction and semantic cues" },
  { id: "resize", label: "Resize and responsive surface" },
  { id: "cleanup", label: "Remount and cleanup" },
];
const states = new Map<string, CardState>();
let activeKey = "cytoscape-js";

const slug = (value: string): string => value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const storageKey = (candidate: string): string => `fga06-manual-review-${slug(candidate)}`;
const escapeHtml = (value: string): string => value.replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char] ?? char);

function loadManual(candidate: string): Record<ManualCheck, boolean> {
  const blank = Object.fromEntries(manualChecks.map(({ id }) => [id, false])) as Record<ManualCheck, boolean>;
  try {
    const raw = localStorage.getItem(storageKey(candidate));
    return raw ? { ...blank, ...JSON.parse(raw) as Partial<Record<ManualCheck, boolean>> } : blank;
  } catch { return blank; }
}

function formatMs(value: number): string { return `${value.toFixed(1)} ms`; }
function average(result: HarnessResult | null, field: "mountMs" | "destroyMs"): string {
  if (!result) return "—";
  const values = result.runs.map((run) => run.measurements[field]);
  return formatMs(values.reduce((sum, value) => sum + value, 0) / values.length);
}
function manualCount(state: CardState): number { return manualChecks.filter(({ id }) => state.manual[id]).length; }
function activeState(): CardState { return states.get(activeKey) ?? [...states.values()][0]; }
function nodeFor(state: CardState, id: string): FgaNode | undefined {
  const base = nodes.find((node) => node.id === id);
  return base ? { ...base, investigationStatus: state.nodeOverrides[id] ?? base.investigationStatus } : undefined;
}
function visibleNodes(state: CardState): FgaNode[] {
  return nodes.map((node) => ({ ...node, investigationStatus: state.nodeOverrides[node.id] ?? node.investigationStatus }))
    .filter((node) => state.visibleStatuses.has(statusOf(node)))
    .filter((node) => !state.clusterFilter || node.clusterId === state.clusterFilter);
}
function visibleEdges(state: CardState): FgaEdge[] {
  const ids = new Set(visibleNodes(state).map((node) => node.id));
  return edges.filter((edge) => ids.has(edge.sourceId) && ids.has(edge.targetId));
}
function statusCount(state: CardState, status: InvestigationStatus): number { return visibleNodes(state).filter((node) => statusOf(node) === status).length; }

function renderTabs(): void {
  tabsRoot.replaceChildren();
  for (const candidate of candidates) {
    const key = slug(candidate.name);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "engine-tab";
    button.id = `tab-${key}`;
    button.setAttribute("role", "tab");
    button.setAttribute("aria-controls", `panel-${key}`);
    button.setAttribute("aria-selected", String(key === activeKey));
    button.dataset.tab = key;
    button.innerHTML = `<span class="engine-name">${escapeHtml(candidate.name)}</span><span class="engine-version">${escapeHtml(candidate.version)}</span><span class="tab-status" data-role="tab-status">AUTO PENDING</span>`;
    button.addEventListener("click", () => switchTab(key));
    tabsRoot.append(button);
  }
}

function renderLegend(state: CardState): string {
  return statuses.map((status) => {
    const meta = NODE_STATUS_META[status];
    const shapeClass = meta.shape === "roundrectangle" ? "roundrect" : meta.shape;
    return `<span class="legend-item"><span class="legend-symbol ${shapeClass}" style="--legend-color:${meta.stroke};--legend-bg:${meta.color};--legend-border-style:${meta.borderStyle}"><span>${meta.glyph}</span></span>${meta.label} <strong>${statusCount(state, status)}</strong></span>`;
  }).join("");
}

function renderMinimap(state: CardState): string {
  const shownNodes = visibleNodes(state);
  const shownIds = new Set(shownNodes.map((node) => node.id));
  const edgeMarkup = visibleEdges(state).map((edge) => {
    const source = nodes.find((node) => node.id === edge.sourceId);
    const target = nodes.find((node) => node.id === edge.targetId);
    return source && target ? `<line class="mini-edge" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}" stroke="${relationshipColor(edge.relationshipFamily)}"/>` : "";
  }).join("");
  const nodeMarkup = shownNodes.map((node) => `<circle class="mini-node${state.selected?.id === node.id ? " active" : ""}" cx="${node.x}" cy="${node.y}" r="8" fill="${visualMeta(node).color}"/>`).join("");
  return `<svg viewBox="0 0 900 560" role="img" aria-label="Miniature overview of the visible graph"><rect class="mini-frame" x="18" y="18" width="864" height="524" rx="8"/><g transform="translate(0 0) scale(1)">${edgeMarkup}${nodeMarkup}</g></svg>`;
}

function updateDecorations(state: CardState): void {
  const legend = state.card.querySelector<HTMLElement>(".legend-content");
  if (legend) legend.innerHTML = renderLegend(state);
  const minimap = state.card.querySelector<HTMLElement>(".minimap");
  if (minimap) minimap.innerHTML = renderMinimap(state);
  const nodeCount = state.card.querySelector<HTMLElement>("[data-role=node-count]");
  const edgeCount = state.card.querySelector<HTMLElement>("[data-role=edge-count]");
  if (nodeCount) nodeCount.textContent = String(visibleNodes(state).length);
  if (edgeCount) edgeCount.textContent = String(visibleEdges(state).length);
}

function setAutoStatus(state: CardState, status: AutoStatus, message: string): void {
  state.autoStatus = status;
  state.autoMessage = message;
  const badge = state.card.querySelector<HTMLElement>("[data-role=auto-badge]");
  const messageElement = state.card.querySelector<HTMLElement>("[data-role=auto-result]");
  const tabStatus = tabsRoot.querySelector<HTMLElement>(`button[data-tab="${state.key}"] [data-role=tab-status]`);
  if (badge) { badge.textContent = `AUTO ${status}`; badge.className = `auto-badge ${status === "PASS" ? "pass" : status === "BLOCKED" ? "blocked" : ""}`; }
  if (messageElement) messageElement.textContent = state.autoMessage;
  if (tabStatus) { tabStatus.textContent = `AUTO ${status}`; tabStatus.className = `tab-status ${status === "PASS" ? "pass" : ""}`; }
  updateSummary();
}

function mount(state: CardState): void {
  state.instance?.destroy();
  state.surface.replaceChildren();
  state.instance = state.candidate.mount(state.surface, visibleNodes(state), visibleEdges(state), {
    onNodeSelect: (id) => { state.selected = id ? { kind: "node", id } : null; state.hovered = state.selected; state.manual.selection = true; persistManual(state); renderInspector(); updateDecorations(state); },
    onEdgeSelect: (id) => { state.selected = id ? { kind: "edge", id } : null; state.hovered = state.selected; state.manual.selection = true; persistManual(state); renderInspector(); updateDecorations(state); },
    onNodeHover: (id) => { if (id) { state.hovered = { kind: "node", id }; renderInspector(); } },
    onEdgeHover: (id) => { if (id) { state.hovered = { kind: "edge", id }; renderInspector(); } },
  });
  updateDecorations(state);
}

function persistManual(state: CardState): void {
  localStorage.setItem(storageKey(state.candidate.name), JSON.stringify(state.manual));
  updateSummary();
}

function switchTab(key: string): void {
  activeKey = key;
  for (const state of states.values()) {
    const active = state.key === activeKey;
    state.card.hidden = !active;
    const button = tabsRoot.querySelector<HTMLButtonElement>(`button[data-tab="${state.key}"]`);
    button?.setAttribute("aria-selected", String(active));
    if (!active) { state.instance?.destroy(); state.instance = null; state.surface.replaceChildren(); }
  }
  const state = activeState();
  mount(state);
  renderInspector();
  updateDecorations(state);
}

function runAuto(state: CardState): HarnessResult {
  const container = document.createElement("div");
  container.style.width = "1000px";
  container.style.height = "650px";
  container.style.position = "absolute";
  container.style.left = "-10000px";
  document.body.append(container);
  const runs = [
    runQualificationLifecycle(state.candidate, container, nodes, edges, 1, "A_RENDERER"),
    runQualificationLifecycle(state.candidate, container, nodes, edges, 2, "B_SOLUTION"),
  ];
  container.remove();
  const result = buildHarnessResult(state.candidate, nodes, edges, runs);
  const probesPass = runs.every((run) => run.measurements.probedNodeId === nodes[0].id && run.measurements.probedEdgeId === edges[0].id && run.measurements.callbackEvents >= 2);
  state.result = result;
  setAutoStatus(state, probesPass ? "PASS" : "BLOCKED", probesPass ? "Lifecycle and node/edge selection probes passed." : "Selection probes or lifecycle evidence did not pass.");
  if (state.key === activeKey) mount(state);
  return result;
}

function updateSummary(): void {
  summaryBodyRoot.replaceChildren();
  for (const state of states.values()) {
    const row = document.createElement("tr");
    const autoText = state.result ? state.autoStatus : "PENDING";
    const gate = state.autoStatus === "PASS" && manualCount(state) === manualChecks.length ? "READY" : "OPEN";
    row.innerHTML = `<td><strong>${escapeHtml(state.candidate.name)}</strong> <code>${escapeHtml(state.candidate.version)}</code></td><td>${autoText}</td><td>${average(state.result, "mountMs")} / ${average(state.result, "destroyMs")}</td><td>${state.result ? state.result.runs.reduce((sum, run) => sum + run.measurements.callbackEvents, 0) : "—"}</td><td>${manualCount(state)}/${manualChecks.length}</td><td>${gate}</td>`;
    summaryBodyRoot.append(row);
  }
  const allAuto = [...states.values()].every((state) => state.autoStatus === "PASS");
  const allManual = [...states.values()].every((state) => manualCount(state) === manualChecks.length);
  overallStatusRoot.textContent = allAuto && allManual ? "All evidence inputs complete" : allAuto ? "Automatic probes complete · manual review remains" : "Manual review and automatic qualification pending";
}

function targetDetails(state: CardState, target: Target | null): string {
  if (!target) return `<div class="inspector-empty"><p>Hover a node or relationship to open its contextual menu.</p><p>Click to keep the selection here while you explore the graph. The visual state is a lab fixture, not a guilt verdict or an investigation command.</p></div>`;
  if (target.kind === "node") {
    const node = nodeFor(state, target.id);
    if (!node) return "";
    const meta = visualMeta(node);
    const connectionCount = edges.filter((edge) => edge.sourceId === node.id || edge.targetId === node.id).length;
    const clusterLabel = node.clusterId ?? "unclassified";
    return `<div class="context-card" data-context-kind="node" data-context-id="${escapeHtml(node.id)}"><div class="context-kicker">Context menu · node</div><h3 class="context-title">${escapeHtml(node.icon ?? meta.glyph)} ${escapeHtml(node.label)}</h3><div class="context-subtitle">${escapeHtml(meta.label)} · ${escapeHtml(node.recordType)}</div><dl class="context-grid"><dt>Stable ID</dt><dd class="mono">${escapeHtml(node.id)}</dd><dt>Cluster</dt><dd>${escapeHtml(clusterLabel)}</dd><dt>Connections</dt><dd>${connectionCount}</dd></dl><div class="context-actions"><button data-context-action="keep">Keep selection</button><button data-context-action="focus-cluster">Focus cluster</button>${statuses.filter((status) => status !== statusOf(node)).map((status) => `<button data-context-action="set-status" data-status="${status}">${NODE_STATUS_META[status].label}</button>`).join("")}</div></div>`;
  }
  const edge = edges.find((item) => item.id === target.id);
  if (!edge) return "";
  const source = nodeFor(state, edge.sourceId);
  const destination = nodeFor(state, edge.targetId);
  return `<div class="context-card" data-context-kind="edge" data-context-id="${escapeHtml(edge.id)}"><div class="context-kicker">Context menu · relationship</div><h3 class="context-title">${escapeHtml(edge.relationshipType)}</h3><div class="context-subtitle">${escapeHtml(edge.relationshipFamily)} · ${edge.directed ? "directed" : "undirected"}</div><dl class="context-grid"><dt>Stable ID</dt><dd class="mono">${escapeHtml(edge.id)}</dd><dt>From</dt><dd>${escapeHtml(source?.label ?? edge.sourceId)}</dd><dt>To</dt><dd>${escapeHtml(destination?.label ?? edge.targetId)}</dd><dt>Confidence</dt><dd>${escapeHtml(edge.confidence ?? "not supplied")}</dd></dl><div class="context-actions"><button data-context-action="keep">Keep selection</button><button data-context-action="trace-source">Inspect source</button><button data-context-action="trace-target">Inspect target</button></div></div>`;
}

function renderInspector(): void {
  const state = activeState();
  const target = state.hovered ?? state.selected;
  const tradeoff = tradeoffs[state.candidate.name];
  inspectorRoot.innerHTML = `<div class="inspector-header"><div><div class="eyebrow">Active engine</div><h2>${escapeHtml(state.candidate.name)}</h2><p>${escapeHtml(state.candidate.version)} · <span data-role="node-count">${visibleNodes(state).length}</span> nodes · <span data-role="edge-count">${visibleEdges(state).length}</span> relationships</p></div><div class="selection-count">${state.selected ? "1 selected" : "No selection"}</div></div>${targetDetails(state, target)}<section class="inspector-section" id="filters-heading"><h3>Filters</h3><p>Presentation-only filters recalculate the visible subset; they do not change the fixture.</p><div class="filter-list">${statuses.map((status) => `<label><input type="checkbox" data-filter-status="${status}" ${state.visibleStatuses.has(status) ? "checked" : ""}> <span>${NODE_STATUS_META[status].glyph} ${NODE_STATUS_META[status].label} (${statusCount(state, status)})</span></label>`).join("")}</div>${state.clusterFilter ? `<div class="context-actions"><button data-context-action="clear-cluster">Clear cluster focus</button></div>` : ""}</section><section class="inspector-section"><h3>Engine fit</h3><div class="pros-cons"><div><strong>Why it is interesting</strong><ul>${tradeoff.pros.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div><div><strong>What to watch</strong><ul>${tradeoff.cons.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div></div><p>${escapeHtml(tradeoff.fit)}</p></section><section class="inspector-section"><details><summary>Legend · color + icon + shape</summary><div class="legend-content" style="margin-top:.7rem">${renderLegend(state)}</div></details></section><section class="inspector-section"><h3>Manual review · ${manualCount(state)}/${manualChecks.length}</h3>${manualChecks.map(({ id, label }) => `<label class="filter-list"><span><input type="checkbox" data-check="${id}" ${state.manual[id] ? "checked" : ""}> ${escapeHtml(label)}</span></label>`).join("")}</section>`;
  inspectorRoot.querySelectorAll<HTMLInputElement>("input[data-filter-status]").forEach((input) => input.addEventListener("change", () => {
    const status = input.dataset.filterStatus as InvestigationStatus;
    if (input.checked) state.visibleStatuses.add(status); else state.visibleStatuses.delete(status);
    state.selected = null;
    state.hovered = null;
    mount(state);
    renderInspector();
  }));
  inspectorRoot.querySelectorAll<HTMLInputElement>("input[data-check]").forEach((input) => input.addEventListener("change", () => {
    const id = input.dataset.check as ManualCheck;
    state.manual[id] = input.checked;
    persistManual(state);
    renderInspector();
  }));
  inspectorRoot.querySelectorAll<HTMLButtonElement>("button[data-context-action]").forEach((button) => button.addEventListener("click", () => {
    const action = button.dataset.contextAction;
    const context = state.hovered ?? state.selected;
    if (action === "keep" && context) state.selected = context;
    if (action === "focus-cluster" && context?.kind === "node") state.clusterFilter = nodeFor(state, context.id)?.clusterId ?? null;
    if (action === "clear-cluster") state.clusterFilter = null;
    if (action === "set-status" && context?.kind === "node") state.nodeOverrides[context.id] = button.dataset.status as InvestigationStatus;
    if (action === "trace-source" && context?.kind === "edge") state.selected = { kind: "node", id: edges.find((edge) => edge.id === context.id)?.sourceId ?? "" };
    if (action === "trace-target" && context?.kind === "edge") state.selected = { kind: "node", id: edges.find((edge) => edge.id === context.id)?.targetId ?? "" };
    if (action === "set-status" || action === "focus-cluster" || action === "clear-cluster") { mount(state); }
    state.hovered = state.selected;
    renderInspector();
    updateDecorations(state);
  }));
}

function reportPayload() {
  return { schema: "fga06-renderer-comparison-v3", generated_at: new Date().toISOString(), fixture_sha256: __FGA_FIXTURE_SHA256__, fixture: { version: fixture.fixture_version, nodes: nodes.length, edges: edges.length }, candidates: [...states.values()].map((state) => ({ candidate: state.candidate.name, version: state.candidate.version, automatic_status: state.autoStatus, result: state.result, manual_review: state.manual, manual_checks: manualCount(state) })), decision: "PENDING_MANUAL_AND_HARD_REQUIREMENT_REVIEW" };
}

for (const candidate of candidates) {
  const key = slug(candidate.name);
  const card = document.createElement("article");
  card.className = "engine-card";
  card.id = `panel-${key}`;
  card.setAttribute("role", "tabpanel");
  card.setAttribute("aria-labelledby", `tab-${key}`);
  card.hidden = key !== activeKey;
  card.innerHTML = `<div class="engine-card-header"><div><h2>${escapeHtml(candidate.name)}</h2><p>${escapeHtml(candidate.version)} · shared renderer-neutral fixture</p></div><span class="auto-badge" data-role="auto-badge">AUTO PENDING</span><span class="auto-message" data-role="auto-result">Automatic probes have not run.</span></div><div class="graph-frame"><div class="engine-surface" data-testid="surface-${key}" aria-label="${escapeHtml(candidate.name)} graph surface"></div><div class="graph-toolbar" aria-label="${escapeHtml(candidate.name)} graph controls"><button data-action="zoom-out" aria-label="Zoom out">−</button><button data-action="zoom-in" aria-label="Zoom in">+</button><button data-action="fit">Fit</button><button data-action="clear">Clear</button><button data-action="node">Select node</button><button data-action="edge">Select relationship</button><button data-action="filters">Filters</button><button data-action="legend">Legend</button><button data-action="reset">Reset</button></div><details class="floating-legend"><summary>Graph legend · <span data-role="node-count">${nodes.length}</span> nodes</summary><div class="legend-content">${renderLegend({ visibleStatuses: new Set(statuses), nodeOverrides: {}, clusterFilter: null } as CardState)}</div></details><div class="minimap">${renderMinimap({ visibleStatuses: new Set(statuses), nodeOverrides: {}, clusterFilter: null, selected: null } as CardState)}</div></div>`;
  matrix.append(card);
  const surface = card.querySelector<HTMLElement>(".engine-surface");
  if (!surface) throw new Error(`Missing surface for ${candidate.name}`);
  const state: CardState = { key, candidate, card, surface, instance: null, selected: null, hovered: null, autoStatus: "PENDING", autoMessage: "Automatic probes have not run.", result: null, manual: loadManual(candidate.name), visibleStatuses: new Set(statuses), nodeOverrides: {}, clusterFilter: null, zoom: 1 };
  states.set(key, state);
  card.querySelectorAll<HTMLButtonElement>("button[data-action]").forEach((button) => button.addEventListener("click", () => {
    const action = button.dataset.action;
    if (action === "fit") { state.instance?.fit(); state.zoom = 1; state.manual.viewport = true; persistManual(state); renderInspector(); }
    if (action === "zoom-in") { state.zoom = Math.min(2.3, state.zoom + .25); state.instance?.setViewport({ zoom: state.zoom, panX: 0, panY: 0 }); state.manual.viewport = true; persistManual(state); renderInspector(); }
    if (action === "zoom-out") { state.zoom = Math.max(.55, state.zoom - .25); state.instance?.setViewport({ zoom: state.zoom, panX: 0, panY: 0 }); state.manual.viewport = true; persistManual(state); renderInspector(); }
    if (action === "node") { state.instance?.probeNode(nodes[0].id); state.manual.selection = true; persistManual(state); }
    if (action === "edge") { state.instance?.probeEdge(edges[0].id); state.manual.selection = true; persistManual(state); }
    if (action === "clear") { state.selected = null; state.hovered = null; renderInspector(); updateDecorations(state); }
    if (action === "filters") { document.querySelector("#filters-heading")?.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
    if (action === "legend") { const legend = state.card.querySelector<HTMLDetailsElement>(".floating-legend"); if (legend) legend.open = !legend.open; }
    if (action === "reset") { state.visibleStatuses = new Set(statuses); state.nodeOverrides = {}; state.clusterFilter = null; state.selected = null; state.hovered = null; state.zoom = 1; state.manual.cleanup = true; mount(state); persistManual(state); renderInspector(); }
  }));
  updateDecorations(state);
}

renderTabs();
switchTab(activeKey);
updateSummary();

document.querySelector<HTMLButtonElement>("#run-all")?.addEventListener("click", () => {
  const results = [...states.values()].map(runAuto);
  reportElement.textContent = JSON.stringify({ ...reportPayload(), results }, null, 2);
  updateSummary();
});
document.querySelector<HTMLButtonElement>("#download-report")?.addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(reportPayload(), null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "fga06-renderer-comparison.json";
  link.click();
  URL.revokeObjectURL(url);
});
