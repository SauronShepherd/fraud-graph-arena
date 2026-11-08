import cytoscape from "cytoscape";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";
import { relationshipColor, visualMeta } from "../visual-semantics";

export const cytoscapeCandidate: QualificationCandidate = {
  name: "Cytoscape.js",
  version: "3.34.4",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const graph = cytoscape({
      container,
      elements: [
        ...nodes.map((node) => ({ data: { id: node.id, label: `${node.icon ?? visualMeta(node).glyph}  ${node.label}`, recordType: node.recordType, status: node.investigationStatus ?? "UNINVESTIGATED", clusterId: node.clusterId }, position: { x: node.x, y: node.y } })),
        ...edges.map((edge) => ({ data: { id: edge.id, source: edge.sourceId, target: edge.targetId, family: edge.relationshipFamily, type: edge.relationshipType, confidence: edge.confidence } })),
      ],
      layout: { name: "preset", fit: false },
      style: [
        { selector: "node", style: { label: "data(label)", shape: (element: cytoscape.NodeSingular) => visualMeta({ investigationStatus: element.data("status") }).shape, "background-color": (element: cytoscape.NodeSingular) => visualMeta({ investigationStatus: element.data("status") }).color, "border-color": (element: cytoscape.NodeSingular) => visualMeta({ investigationStatus: element.data("status") }).stroke, "border-style": (element: cytoscape.NodeSingular) => visualMeta({ investigationStatus: element.data("status") }).borderStyle, "border-width": 3, color: "#f1e7d0", "font-size": "9px", "text-max-width": "100px", "text-wrap": "ellipsis", "text-valign": "center", "text-halign": "center", "text-outline-color": "#11100e", "text-outline-width": 2, "text-outline-opacity": 0.95, width: 54, height: 54 } },
        { selector: "edge", style: { label: "", width: (element: cytoscape.EdgeSingular) => element.data("family") === "TRANSACTIONAL" ? 3 : 2, "line-color": (element: cytoscape.EdgeSingular) => relationshipColor(element.data("family")), "target-arrow-color": (element: cytoscape.EdgeSingular) => relationshipColor(element.data("family")), "target-arrow-shape": "triangle", "curve-style": "bezier" } },
      ],
    });
    graph.on("tap", "node", (event) => callbacks.onNodeSelect(event.target.id()));
    graph.on("tap", "edge", (event) => callbacks.onEdgeSelect(event.target.id()));
    graph.on("mouseover", "node", (event) => callbacks.onNodeHover?.(event.target.id()));
    graph.on("mouseout", "node", () => callbacks.onNodeHover?.(null));
    graph.on("mouseover", "edge", (event) => callbacks.onEdgeHover?.(event.target.id()));
    graph.on("mouseout", "edge", () => callbacks.onEdgeHover?.(null));
    graph.fit(undefined, 64);
    return {
      fit: () => graph.fit(undefined, 64),
      setViewport: (viewport: FgaViewport) => { graph.zoom(viewport.zoom); graph.pan({ x: viewport.panX, y: viewport.panY }); },
      resize: () => { graph.resize(); },
      probeNode: (id: string) => { graph.getElementById(id).emit("tap"); },
      probeEdge: (id: string) => { graph.getElementById(id).emit("tap"); },
      destroy: () => { graph.destroy(); },
    };
  },
};
