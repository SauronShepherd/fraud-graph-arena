import fixture from "./fixture-v1.json";
import fixtureRaw from "./fixture-v1.json?raw";
import { cytoscapeCandidate } from "./adapters/cytoscape";
import { d3Candidate } from "./adapters/d3";
import { reactFlowCandidate } from "./adapters/react-flow";
import { sigmaCandidate } from "./adapters/sigma";
import { buildHarnessResult, runQualificationLifecycle } from "./harness";
import type { FgaEdge, FgaNode, QualificationCandidate } from "./candidate-contract";

const candidates: readonly QualificationCandidate[] = [cytoscapeCandidate, sigmaCandidate, d3Candidate, reactFlowCandidate];
const nodes: FgaNode[] = fixture.nodes.map((node) => ({ id: node.id, recordType: node.record_type, label: node.label, x: node.x, y: node.y }));
const edges: FgaEdge[] = fixture.edges.map((edge) => ({ id: edge.id, sourceId: edge.source_id, targetId: edge.target_id, relationshipFamily: edge.relationship_family, relationshipType: edge.relationship_type, directed: edge.directed }));
const output = document.querySelector<HTMLPreElement>("#output");
const stage = document.querySelector<HTMLDivElement>("#stage");

function runCandidate(candidate: QualificationCandidate): ReturnType<typeof buildHarnessResult> {
  if (!stage) throw new Error("benchmark stage is missing");
  const container = document.createElement("div");
  container.className = "candidate-stage";
  container.style.width = "900px";
  container.style.height = "500px";
  stage.replaceChildren(container);
  const runs = [
    runQualificationLifecycle(candidate, container, nodes, edges, 1, "A_RENDERER"),
    runQualificationLifecycle(candidate, container, nodes, edges, 2, "B_SOLUTION"),
  ];
  return buildHarnessResult(candidate, nodes, edges, runs);
}

async function sha256(value: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function runAll(): Promise<void> {
  const results = candidates.map(runCandidate);
  const report = { fixture_sha256: await sha256(fixtureRaw), environment: { browser: navigator.userAgent, os: "browser-host-not-exposed", viewport: `${innerWidth}x${innerHeight}`, node_version: "browser-runner-not-applicable" }, candidates: results, status: "RAW_MEASUREMENTS_NOT_QUALIFIED", interaction_status: "MANUAL_SELECTION_REVIEW_REQUIRED" };
  if (output) output.textContent = JSON.stringify(report, null, 2);
}

document.querySelector("#run")?.addEventListener("click", runAll);
document.querySelector("#download")?.addEventListener("click", () => {
  if (!output?.textContent) return;
  const blob = new Blob([output.textContent], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "fga06-renderer-raw-measurements.json";
  link.click();
  URL.revokeObjectURL(link.href);
});
