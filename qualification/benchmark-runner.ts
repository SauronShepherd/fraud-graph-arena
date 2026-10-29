import fixture from "./fixture-v1.json";
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

function runAll(): void {
  const results = candidates.map(runCandidate);
  const report = { fixture_sha256: "REPLACE_WITH_SHA256_OF_QUALIFICATION_FIXTURE", environment: { browser: navigator.userAgent, os: "RECORD_HOST_OS", viewport: `${innerWidth}x${innerHeight}`, node_version: "RECORD_NODE_VERSION" }, candidates: results, status: "RAW_MEASUREMENTS_NOT_QUALIFIED" };
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
