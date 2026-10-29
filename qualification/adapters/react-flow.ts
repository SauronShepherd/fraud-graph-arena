import React from "react";
import { createRoot, type Root } from "react-dom/client";
import { Background, MiniMap, ReactFlow, ReactFlowProvider, type Edge, type Node, type ReactFlowInstance } from "@xyflow/react";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";

function FlowCanvas({ nodes, edges, onInit, onNodeSelect, onEdgeSelect }: { nodes: Node[]; edges: Edge[]; onInit: (instance: ReactFlowInstance) => void; onNodeSelect: (id: string) => void; onEdgeSelect: (id: string) => void }) {
  return React.createElement(ReactFlow, {
    nodes,
    edges,
    fitView: true,
    nodesDraggable: false,
    onInit,
    onNodeClick: (_event: React.MouseEvent, node: Node) => onNodeSelect(node.id),
    onEdgeClick: (_event: React.MouseEvent, edge: Edge) => onEdgeSelect(edge.id),
    children: React.createElement(React.Fragment, null, React.createElement(Background), React.createElement(MiniMap)),
  });
}

export const reactFlowCandidate: QualificationCandidate = {
  name: "React Flow",
  version: "12.12.0",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const root: Root = createRoot(container);
    let instance: ReactFlowInstance | null = null;
    const flowNodes: Node[] = nodes.map((node) => ({ id: node.id, position: { x: node.x, y: node.y }, data: { label: node.label, recordType: node.recordType }, style: { background: node.recordType === "PERSON_RECORD" ? "#496b68" : "#765b82", color: "#fff" } }));
    const flowEdges: Edge[] = edges.map((edge) => ({ id: edge.id, source: edge.sourceId, target: edge.targetId, label: edge.relationshipType, animated: false }));
    root.render(React.createElement(ReactFlowProvider, null, React.createElement(FlowCanvas, { nodes: flowNodes, edges: flowEdges, onInit: (next) => { instance = next; }, onNodeSelect: callbacks.onNodeSelect as (id: string) => void, onEdgeSelect: callbacks.onEdgeSelect as (id: string) => void })));
    return {
      fit: () => { instance?.fitView({ duration: 0 }); },
      setViewport: (viewport: FgaViewport) => { instance?.setViewport({ x: viewport.panX, y: viewport.panY, zoom: viewport.zoom }); },
      resize: () => { instance?.fitView({ duration: 0 }); },
      destroy: () => { root.unmount(); },
    };
  },
};
