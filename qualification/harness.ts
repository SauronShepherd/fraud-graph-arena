import type { CandidateInstance, FgaEdge, FgaNode, QualificationCandidate } from "./candidate-contract";

export type QualificationMode = "A_RENDERER" | "B_SOLUTION";

export type HarnessMeasurement = {
  mountMs: number;
  fitMs: number;
  viewportMs: number;
  resizeMs: number;
  destroyMs: number;
  selectedNodeId: string | null;
  selectedEdgeId: string | null;
  callbackEvents: number;
};

export type HarnessRun = {
  runNumber: number;
  mode: QualificationMode;
  measurements: HarnessMeasurement;
};

export type HarnessResult = {
  candidate: string;
  candidateVersion: string;
  fixtureNodeCount: number;
  fixtureEdgeCount: number;
  runs: HarnessRun[];
};

const now = (): number => typeof performance === "undefined" ? Date.now() : performance.now();

function elapsed(action: () => void): number {
  const started = now();
  action();
  return Math.max(0, now() - started);
}

/**
 * Execute the same adapter lifecycle for every candidate. Native renderer
 * objects remain inside the candidate and never enter the returned report.
 */
export function runQualificationLifecycle(
  candidate: QualificationCandidate,
  container: HTMLElement,
  nodes: readonly FgaNode[],
  edges: readonly FgaEdge[],
  runNumber: number,
  mode: QualificationMode,
): HarnessRun {
  let selectedNodeId: string | null = null;
  let selectedEdgeId: string | null = null;
  let callbackEvents = 0;
  let instance: CandidateInstance | null = null;
  const callbacks = {
    onNodeSelect: (id: string | null) => { selectedNodeId = id; selectedEdgeId = null; callbackEvents += 1; },
    onEdgeSelect: (id: string | null) => { selectedEdgeId = id; selectedNodeId = null; callbackEvents += 1; },
  };
  const mountMs = elapsed(() => { instance = candidate.mount(container, nodes, edges, callbacks); });
  if (!instance) throw new Error(`${candidate.name} did not return a candidate instance`);
  const fitMs = elapsed(() => instance?.fit());
  const viewportMs = elapsed(() => instance?.setViewport({ zoom: 1.25, panX: 18, panY: -12 }));
  const resizeMs = elapsed(() => instance?.resize());
  const destroyMs = elapsed(() => instance?.destroy());
  return { runNumber, mode, measurements: { mountMs, fitMs, viewportMs, resizeMs, destroyMs, selectedNodeId, selectedEdgeId, callbackEvents } };
}

export function buildHarnessResult(
  candidate: QualificationCandidate,
  nodes: readonly FgaNode[],
  edges: readonly FgaEdge[],
  runs: readonly HarnessRun[],
): HarnessResult {
  return { candidate: candidate.name, candidateVersion: candidate.version, fixtureNodeCount: nodes.length, fixtureEdgeCount: edges.length, runs: [...runs] };
}
