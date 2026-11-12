import Sigma from "sigma";
import Graph from "graphology";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";
import { relationshipColor, visualMeta } from "../visual-semantics";

export const sigmaCandidate: QualificationCandidate = {
  name: "Sigma.js",
  version: "4.0.3",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const graph = new Graph({ multi: false, type: "directed" });
    for (const node of nodes) {
      const meta = visualMeta(node);
      graph.addNode(node.id, { label: `${node.icon ?? meta.glyph}  ${node.label}`, labelVisibility: "visible", labelColor: "#f1e7d0", labelSize: 12, backdropVisibility: "visible", backdropColor: "#11100e", backdropPadding: 3, x: node.x, y: node.y, size: node.investigationStatus === "FRAUD_CONFIRMED" ? 18 : 14, color: meta.color, borderColor: meta.stroke, borderSize: node.investigationStatus === "CANDIDATE" ? 3 : 2, status: node.investigationStatus, clusterId: node.clusterId });
    }
    for (const edge of edges) graph.addDirectedEdgeWithKey(edge.id, edge.sourceId, edge.targetId, { label: edge.relationshipType, color: relationshipColor(edge.relationshipFamily), size: edge.relationshipFamily === "TRANSACTIONAL" ? 3 : 2 });
    const renderer = new Sigma(graph, container, {
      settings: { renderLabels: true, renderEdgeLabels: false, enableEdgeEvents: true, labelRenderedSizeThreshold: 0, labelDensity: 1, labelGridCellSize: 100 },
      nodeReducer: (_key, data) => { const styled = data as typeof data & { borderColor?: string; borderSize?: number }; return { ...data, labelColor: "#f1e7d0", labelVisibility: "visible", labelSize: 12, backdropVisibility: "visible", backdropColor: "#11100e", backdropPadding: 3, borderColor: styled.borderColor ?? "#d1c3a4", borderSize: styled.borderSize ?? 2 }; },
    });
    renderer.getCamera().setState({ ratio: 1.28, x: 0.5, y: 0.5, angle: 0 });
    renderer.on("clickNode", ({ node }) => callbacks.onNodeSelect(node));
    renderer.on("clickEdge", ({ edge }) => callbacks.onEdgeSelect(edge));
    renderer.on("enterNode", ({ node }) => callbacks.onNodeHover?.(node));
    renderer.on("leaveNode", () => callbacks.onNodeHover?.(null));
    renderer.on("enterEdge", ({ edge }) => callbacks.onEdgeHover?.(edge));
    renderer.on("leaveEdge", () => callbacks.onEdgeHover?.(null));
    return {
      fit: () => renderer.getCamera().setState({ ratio: 1.28, x: 0.5, y: 0.5, angle: 0 }),
      setViewport: (viewport: FgaViewport) => renderer.getCamera().setState({ ratio: 1.28 / viewport.zoom, x: viewport.panX, y: viewport.panY, angle: 0 }),
      resize: () => renderer.refresh(),
      probeNode: (id: string) => { if (graph.hasNode(id)) callbacks.onNodeSelect(id); },
      probeEdge: (id: string) => { if (graph.hasEdge(id)) callbacks.onEdgeSelect(id); },
      destroy: () => { renderer.kill(); graph.clear(); },
    };
  },
};
