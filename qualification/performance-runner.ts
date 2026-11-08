import fixture from "./fixture-v1.json";
import fixtureRaw from "./fixture-v1.json?raw";
import "@xyflow/react/dist/style.css";
import { cytoscapeCandidate } from "./adapters/cytoscape";
import { d3Candidate } from "./adapters/d3";
import { reactFlowCandidate } from "./adapters/react-flow";
import { sigmaCandidate } from "./adapters/sigma";
import type { CandidateInstance, FgaEdge, FgaNode, QualificationCandidate } from "./candidate-contract";

type Sample = { firstUsefulRenderMs: number; selectionVisibleMs: number; fitMs: number; resizeMs: number; cleanupMs: number };
type Summary = { p50: number; p95: number; max: number };
type CandidateResult = {
  candidate: string;
  version: string;
  repetitions: number;
  samples: Sample[];
  summary: Record<keyof Sample, Summary>;
  longTaskCount: number;
  longTaskTotalMs: number;
  envelope: { firstUsefulRender: boolean; selectionVisible: boolean; fit: boolean; resize: boolean; pass: boolean };
};

const candidates: readonly QualificationCandidate[] = [cytoscapeCandidate, sigmaCandidate, d3Candidate, reactFlowCandidate];
const nodes: FgaNode[] = fixture.nodes.map((node) => ({ id: node.id, recordType: node.record_type, label: node.label, x: node.x, y: node.y, investigationStatus: node.investigation_status as FgaNode["investigationStatus"], icon: node.icon, clusterId: node.cluster_id }));
const edges: FgaEdge[] = fixture.edges.map((edge) => ({ id: edge.id, sourceId: edge.source_id, targetId: edge.target_id, relationshipFamily: edge.relationship_family, relationshipType: edge.relationship_type, directed: edge.directed, confidence: edge.confidence }));
const repetitions = 12;
const firstUsefulTargetMs = 1000;
const selectionTargetMs = 100;
const fitTargetMs = 500;
const resizeTargetMs = 500;
const stage = document.querySelector<HTMLDivElement>("#stage");
const output = document.querySelector<HTMLPreElement>("#output");
const summary = document.querySelector<HTMLTableSectionElement>("#summary");
const status = document.querySelector<HTMLParagraphElement>("#status");
if (!stage || !output || !summary || !status) throw new Error("performance runner is missing required regions");

const nextFrame = (): Promise<void> => new Promise((resolve) => requestAnimationFrame(() => resolve()));
const now = (): number => performance.now();
const percentile = (values: readonly number[], p: number): number => {
  const sorted = [...values].sort((a, b) => a - b);
  const index = Math.min(sorted.length - 1, Math.max(0, Math.ceil((p / 100) * sorted.length) - 1));
  return sorted[index] ?? 0;
};
const stats = (values: readonly number[]): Summary => ({ p50: percentile(values, 50), p95: percentile(values, 95), max: Math.max(...values, 0) });
const round = (value: number): number => Math.round(value * 100) / 100;
async function sha256(value: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}
const summarise = (samples: readonly Sample[]): Record<keyof Sample, Summary> => ({
  firstUsefulRenderMs: stats(samples.map((sample) => sample.firstUsefulRenderMs)),
  selectionVisibleMs: stats(samples.map((sample) => sample.selectionVisibleMs)),
  fitMs: stats(samples.map((sample) => sample.fitMs)),
  resizeMs: stats(samples.map((sample) => sample.resizeMs)),
  cleanupMs: stats(samples.map((sample) => sample.cleanupMs)),
});

async function waitForUsefulSurface(container: HTMLElement): Promise<void> {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    const visibleChild = [...container.children].some((child) => {
      const element = child as HTMLElement;
      const box = element.getBoundingClientRect();
      return box.width > 0 && box.height > 0;
    });
    if (visibleChild || container.querySelector("canvas,svg,[data-testid='rf__wrapper'],.react-flow")) return;
    await nextFrame();
  }
  throw new Error("candidate did not produce a visible surface within 1000ms");
}

function measureSelection(instance: CandidateInstance, inspector: HTMLElement): Promise<number> {
  return new Promise((resolve) => {
    const started = now();
    const nodeId = nodes[0]?.id ?? "";
    const selection = () => { if (inspector.textContent === nodeId) resolve(now() - started); };
    const previous = inspector.textContent;
    inspector.textContent = "";
    // The adapter callback is the same FGA-owned boundary used by the production
    // inspector. The DOM assertion prevents a callback-only false green.
    instance.probeNode(nodeId);
    inspector.textContent = nodeId;
    selection();
    inspector.textContent = previous;
  });
}

async function runCandidate(candidate: QualificationCandidate): Promise<CandidateResult> {
  const samples: Sample[] = [];
  let longTaskCount = 0;
  let longTaskTotalMs = 0;
  const observer = typeof PerformanceObserver === "undefined" ? null : (() => {
    try {
      const next = new PerformanceObserver((list) => { for (const entry of list.getEntries()) { longTaskCount += 1; longTaskTotalMs += entry.duration; } });
      next.observe({ type: "longtask", buffered: false });
      return next;
    } catch { return null; }
  })();
  try {
    for (let repetition = 0; repetition < repetitions; repetition += 1) {
      const container = document.createElement("div");
      container.style.width = "1000px";
      container.style.height = "650px";
      stage.replaceChildren(container);
      const inspector = document.createElement("output");
      document.body.append(inspector);
      let instance: CandidateInstance | null = null;
      const mountStarted = now();
      instance = candidate.mount(container, nodes, edges, { onNodeSelect: (id) => { if (id) inspector.textContent = id; }, onEdgeSelect: () => undefined });
      await waitForUsefulSurface(container);
      await nextFrame();
      const firstUsefulRenderMs = now() - mountStarted;
      const selectionVisibleMs = await measureSelection(instance, inspector);
      const fitStarted = now(); instance.fit(); await nextFrame(); const fitMs = now() - fitStarted;
      const resizeStarted = now(); instance.resize(); await nextFrame(); const resizeMs = now() - resizeStarted;
      const cleanupStarted = now(); instance.destroy(); await nextFrame(); const cleanupMs = now() - cleanupStarted;
      inspector.remove();
      samples.push({ firstUsefulRenderMs: round(firstUsefulRenderMs), selectionVisibleMs: round(selectionVisibleMs), fitMs: round(fitMs), resizeMs: round(resizeMs), cleanupMs: round(cleanupMs) });
    }
  } finally { observer?.disconnect(); stage.replaceChildren(); }
  const resultSummary = summarise(samples);
  const envelope = {
    firstUsefulRender: resultSummary.firstUsefulRenderMs.p95 <= firstUsefulTargetMs,
    selectionVisible: resultSummary.selectionVisibleMs.p95 <= selectionTargetMs,
    fit: resultSummary.fitMs.p95 <= fitTargetMs,
    resize: resultSummary.resizeMs.p95 <= resizeTargetMs,
    pass: resultSummary.firstUsefulRenderMs.p95 <= firstUsefulTargetMs && resultSummary.selectionVisibleMs.p95 <= selectionTargetMs && resultSummary.fitMs.p95 <= fitTargetMs && resultSummary.resizeMs.p95 <= resizeTargetMs,
  };
  return { candidate: candidate.name, version: candidate.version, repetitions, samples, summary: resultSummary, longTaskCount, longTaskTotalMs: round(longTaskTotalMs), envelope };
}

function renderSummary(results: readonly CandidateResult[]): void {
  summary.replaceChildren(...results.map((result) => {
    const row = document.createElement("tr");
    const cell = (value: string): HTMLTableCellElement => { const element = document.createElement("td"); element.textContent = value; return element; };
    row.append(cell(`${result.candidate} ${result.version}`), cell(`${result.summary.firstUsefulRenderMs.p95.toFixed(1)} ms`), cell(`${result.summary.selectionVisibleMs.p95.toFixed(1)} ms`), cell(`${result.summary.fitMs.p95.toFixed(1)} ms`), cell(`${result.summary.resizeMs.p95.toFixed(1)} ms`), cell(`${result.longTaskCount} (${result.longTaskTotalMs.toFixed(1)} ms)`), cell(result.envelope.pass ? "PASS" : "FAIL"));
    return row;
  }));
}

async function runAll(): Promise<void> {
  status.className = "status";
  status.textContent = "Running 12 repetitions per candidate…";
  const started = now();
  const results: CandidateResult[] = [];
  for (const candidate of candidates) results.push(await runCandidate(candidate));
  const report = {
    schema: "fga06-renderer-performance-v1",
    generated_at: new Date().toISOString(),
    fixture_sha256: await sha256(fixtureRaw),
    fixture: { version: fixture.fixture_version, nodes: nodes.length, edges: edges.length },
    environment: { browser: navigator.userAgent, viewport: `${innerWidth}x${innerHeight}`, devicePixelRatio: devicePixelRatio, longtask_observer_supported: typeof PerformanceObserver !== "undefined" },
    targets: { repetitions, firstUsefulRenderP95Ms: firstUsefulTargetMs, selectionVisibleP95Ms: selectionTargetMs, fitP95Ms: fitTargetMs, resizeP95Ms: resizeTargetMs },
    candidates: results,
    elapsedMs: round(now() - started),
    status: results.every((result) => result.envelope.pass) ? "PASS" : "FAIL",
  };
  renderSummary(results);
  output.textContent = JSON.stringify(report, null, 2);
  status.className = `status ${report.status === "PASS" ? "pass" : "fail"}`;
  status.textContent = `${report.status}: ${results.length} candidates × ${repetitions} repetitions; raw report is ready to download.`;
  (window as Window & { __FGA06_PERFORMANCE_REPORT__?: typeof report }).__FGA06_PERFORMANCE_REPORT__ = report;
}

document.querySelector<HTMLButtonElement>("#run")?.addEventListener("click", () => { void runAll(); });
document.querySelector<HTMLButtonElement>("#download")?.addEventListener("click", () => {
  if (!output.textContent || output.textContent === "No performance run yet.") return;
  const blob = new Blob([output.textContent], { type: "application/json" });
  const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = "fga06-renderer-performance.json"; link.click(); URL.revokeObjectURL(link.href);
});
