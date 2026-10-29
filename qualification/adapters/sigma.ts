import Sigma from "sigma";
import Graph from "graphology";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";

export const sigmaCandidate: QualificationCandidate = {
  name: "Sigma.js",
  version: "4.0.3",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const graph = new Graph({ multi: false, type: "directed" });
    for (const node of nodes) graph.addNode(node.id, { label: node.label, x: node.x, y: node.y, size: 12, color: node.recordType === "PERSON_RECORD" ? "#496b68" : "#765b82" });
    for (const edge of edges) graph.addDirectedEdge(edge.sourceId, edge.targetId, { key: edge.id, label: edge.relationshipType, color: "#d9b46c", size: 2 });
    const renderer = new Sigma(graph, container);
    renderer.on("clickNode", ({ node }) => callbacks.onNodeSelect(node));
    renderer.on("clickEdge", ({ edge }) => callbacks.onEdgeSelect(edge));
    return {
      fit: () => renderer.getCamera().setState({ ratio: 1, x: 0.5, y: 0.5, angle: 0 }),
      setViewport: (viewport: FgaViewport) => renderer.getCamera().setState({ ratio: 1 / viewport.zoom, x: viewport.panX, y: viewport.panY, angle: 0 }),
      resize: () => renderer.refresh(),
      destroy: () => { renderer.kill(); graph.clear(); },
    };
  },
};
