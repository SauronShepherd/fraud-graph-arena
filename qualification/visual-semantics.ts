import type { FgaNode } from "./candidate-contract";

export type InvestigationStatus = "UNINVESTIGATED" | "CANDIDATE" | "INVESTIGATED" | "FRAUD_CONFIRMED" | "DISCARDED";

export type NodeVisualMeta = {
  label: string;
  color: string;
  stroke: string;
  glyph: string;
  shape: "ellipse" | "roundrectangle" | "star" | "diamond";
  borderStyle: "solid" | "dashed" | "dotted";
};

export const NODE_STATUS_META: Record<InvestigationStatus, NodeVisualMeta> = {
  UNINVESTIGATED: { label: "Sin investigar", color: "#4f514d", stroke: "#d1c3a4", glyph: "○", shape: "ellipse", borderStyle: "solid" },
  CANDIDATE: { label: "Candidato", color: "#a66b2d", stroke: "#f3c76e", glyph: "?", shape: "ellipse", borderStyle: "dashed" },
  INVESTIGATED: { label: "Investigado", color: "#28677a", stroke: "#7cd9e8", glyph: "◉", shape: "roundrectangle", borderStyle: "solid" },
  FRAUD_CONFIRMED: { label: "Fraude confirmado", color: "#8f3028", stroke: "#ff9a72", glyph: "✦", shape: "star", borderStyle: "solid" },
  DISCARDED: { label: "Descartado", color: "#4b4a47", stroke: "#96958e", glyph: "—", shape: "diamond", borderStyle: "dotted" },
};

export function statusOf(node: Pick<FgaNode, "investigationStatus">): InvestigationStatus {
  return node.investigationStatus ?? "UNINVESTIGATED";
}

export function visualMeta(node: Pick<FgaNode, "investigationStatus">): NodeVisualMeta {
  return NODE_STATUS_META[statusOf(node)];
}

export function nodeGlyph(node: Pick<FgaNode, "investigationStatus" | "icon">): string {
  return node.icon ?? visualMeta(node).glyph;
}

export function relationshipColor(family: string): string {
  if (family === "TRANSACTIONAL") return "#e58d55";
  if (family === "DEVICE_OBSERVATION") return "#79c6c0";
  if (family === "SHARED_ATTRIBUTE") return "#d3a85e";
  return "#938c79";
}
