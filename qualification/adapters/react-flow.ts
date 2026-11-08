import React from "react";
import { createRoot, type Root } from "react-dom/client";
import { Background, Handle, Position, ReactFlow, ReactFlowProvider, type Edge, type Node, type ReactFlowInstance } from "@xyflow/react";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";
import { relationshipColor, visualMeta } from "../visual-semantics";

function FgaNodeView({ data }: { data: { label: string; icon: string; investigationStatus: FgaNode["investigationStatus"] } }) {
  const meta = visualMeta(data);
  return React.createElement("div", {
    className: "fga-flow-node",
    style: { background: meta.color, borderColor: meta.stroke, borderStyle: meta.borderStyle, borderRadius: meta.shape === "diamond" ? "5px" : meta.shape === "star" ? "18px 4px 18px 4px" : meta.shape === "roundrectangle" ? "15px" : "50%" },
    "aria-label": `${data.label}, ${meta.label}`,
  },
  React.createElement(Handle, { type: "target", position: Position.Top, style: { opacity: 0 } }),
  React.createElement("span", { className: "fga-flow-icon", "aria-hidden": "true" }, data.icon ?? meta.glyph),
  React.createElement("span", { className: "fga-flow-label" }, data.label),
  React.createElement(Handle, { type: "source", position: Position.Bottom, style: { opacity: 0 } }));
}

const nodeTypes = { fga: FgaNodeView };

function FlowCanvas({ nodes, edges, onInit, onNodeSelect, onEdgeSelect, onNodeHover, onEdgeHover }: { nodes: Node[]; edges: Edge[]; onInit: (instance: ReactFlowInstance) => void; onNodeSelect: (id: string) => void; onEdgeSelect: (id: string) => void; onNodeHover: (id: string | null) => void; onEdgeHover: (id: string | null) => void }) {
  return React.createElement(ReactFlow, {
    nodes,
    edges,
    nodeTypes,
    fitView: true,
    nodesDraggable: false,
    onInit,
    onNodeClick: (_event: React.MouseEvent, node: Node) => onNodeSelect(node.id),
    onEdgeClick: (_event: React.MouseEvent, edge: Edge) => onEdgeSelect(edge.id),
    onNodeMouseEnter: (_event: React.MouseEvent, node: Node) => onNodeHover(node.id),
    onNodeMouseLeave: () => onNodeHover(null),
    onEdgeMouseEnter: (_event: React.MouseEvent, edge: Edge) => onEdgeHover(edge.id),
    onEdgeMouseLeave: () => onEdgeHover(null),
    children: React.createElement(React.Fragment, null, React.createElement(Background, { color: "#574737", gap: 18, size: 1 })),
  });
}

export const reactFlowCandidate: QualificationCandidate = {
  name: "React Flow",
  version: "12.12.0",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const root: Root = createRoot(container);
    let instance: ReactFlowInstance | null = null;
    const flowNodes: Node[] = nodes.map((node) => ({ id: node.id, type: "fga", position: { x: node.x, y: node.y }, data: { label: node.label, icon: node.icon ?? "○", recordType: node.recordType, investigationStatus: node.investigationStatus } }));
    const flowEdges: Edge[] = edges.map((edge) => ({ id: edge.id, source: edge.sourceId, target: edge.targetId, animated: false, style: { stroke: relationshipColor(edge.relationshipFamily), strokeWidth: edge.relationshipFamily === "TRANSACTIONAL" ? 3 : 2 } }));
    root.render(React.createElement(ReactFlowProvider, null, React.createElement(FlowCanvas, { nodes: flowNodes, edges: flowEdges, onInit: (next) => { instance = next; }, onNodeSelect: callbacks.onNodeSelect as (id: string) => void, onEdgeSelect: callbacks.onEdgeSelect as (id: string) => void, onNodeHover: callbacks.onNodeHover as (id: string | null) => void, onEdgeHover: callbacks.onEdgeHover as (id: string | null) => void })));
    return {
      fit: () => { instance?.fitView({ duration: 0 }); },
      setViewport: (viewport: FgaViewport) => { instance?.setViewport({ x: viewport.panX, y: viewport.panY, zoom: viewport.zoom }); },
      resize: () => { instance?.fitView({ duration: 0 }); },
      probeNode: (id: string) => { if (flowNodes.some((node) => node.id === id)) callbacks.onNodeSelect(id); },
      probeEdge: (id: string) => { if (flowEdges.some((edge) => edge.id === id)) callbacks.onEdgeSelect(id); },
      destroy: () => { root.unmount(); },
    };
  },
};
