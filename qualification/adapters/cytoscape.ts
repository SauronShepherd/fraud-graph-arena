import cytoscape from "cytoscape";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";

export const cytoscapeCandidate: QualificationCandidate = {
  name: "Cytoscape.js",
  version: "3.34.4",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const graph = cytoscape({
      container,
      elements: [
        ...nodes.map((node) => ({ data: { id: node.id, label: node.label, recordType: node.recordType }, position: { x: node.x, y: node.y } })),
        ...edges.map((edge) => ({ data: { id: edge.id, source: edge.sourceId, target: edge.targetId, family: edge.relationshipFamily, type: edge.relationshipType } })),
      ],
      layout: { name: "preset", fit: false },
      style: [
        { selector: "node", style: { label: "data(label)", "background-color": (element: cytoscape.NodeSingular) => element.data("recordType") === "PERSON_RECORD" ? "#496b68" : "#765b82", color: "#fff", "text-valign": "center", "text-halign": "center" } },
        { selector: "edge", style: { label: "data(type)", width: 2, "line-color": "#d9b46c", "target-arrow-color": "#d9b46c", "target-arrow-shape": "triangle", "curve-style": "bezier" } },
      ],
    });
    graph.on("tap", "node", (event) => callbacks.onNodeSelect(event.target.id()));
    graph.on("tap", "edge", (event) => callbacks.onEdgeSelect(event.target.id()));
    return {
      fit: () => graph.fit(undefined, 30),
      setViewport: (viewport: FgaViewport) => { graph.zoom(viewport.zoom); graph.pan({ x: viewport.panX, y: viewport.panY }); },
      resize: () => { graph.resize(); },
      destroy: () => { graph.destroy(); },
    };
  },
};
