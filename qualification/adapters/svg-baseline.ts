import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";

const SVG_NS = "http://www.w3.org/2000/svg";

function svgElement<K extends keyof SVGElementTagNameMap>(name: K): SVGElementTagNameMap[K] {
  return document.createElementNS(SVG_NS, name);
}

function nodeColor(recordType: string): string {
  return recordType === "PERSON_RECORD" ? "#496b68" : "#765b82";
}

function render(instance: { root: SVGSVGElement; layer: SVGGElement; nodes: readonly FgaNode[]; edges: readonly FgaEdge[]; viewport: FgaViewport; onNodeSelect: (id: string | null) => void; onEdgeSelect: (id: string | null) => void }): void {
  instance.layer.replaceChildren();
  instance.layer.setAttribute("transform", `translate(${250 - 250 * instance.viewport.zoom} ${135 - 135 * instance.viewport.zoom}) scale(${instance.viewport.zoom}) translate(${instance.viewport.panX} ${instance.viewport.panY})`);
  const byId = new Map(instance.nodes.map((node) => [node.id, node]));
  for (const edge of instance.edges) {
    const source = byId.get(edge.sourceId);
    const target = byId.get(edge.targetId);
    if (!source || !target) continue;
    const line = svgElement("line");
    line.setAttribute("x1", String(source.x));
    line.setAttribute("y1", String(source.y));
    line.setAttribute("x2", String(target.x));
    line.setAttribute("y2", String(target.y));
    line.setAttribute("stroke", "#d9b46c");
    line.setAttribute("stroke-width", "2");
    line.setAttribute("data-edge-id", edge.id);
    line.setAttribute("tabindex", "0");
    line.setAttribute("role", "button");
    line.setAttribute("aria-label", `${edge.relationshipType}: ${edge.id}`);
    line.addEventListener("click", () => instance.onEdgeSelect(edge.id));
    instance.layer.append(line);
  }
  for (const node of instance.nodes) {
    const group = svgElement("g");
    group.setAttribute("data-node-id", node.id);
    group.setAttribute("tabindex", "0");
    group.setAttribute("role", "button");
    group.setAttribute("aria-label", `${node.label}, ${node.id}`);
    group.addEventListener("click", () => instance.onNodeSelect(node.id));
    group.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); instance.onNodeSelect(node.id); } });
    const circle = svgElement("circle");
    circle.setAttribute("cx", String(node.x));
    circle.setAttribute("cy", String(node.y));
    circle.setAttribute("r", "23");
    circle.setAttribute("fill", nodeColor(node.recordType));
    circle.setAttribute("stroke", "#d9b46c");
    group.append(circle);
    instance.layer.append(group);
  }
}

export const svgBaselineCandidate: QualificationCandidate = {
  name: "FGA SVG semantic baseline",
  version: "native-svg-1",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const root = svgElement("svg");
    root.setAttribute("viewBox", "0 0 500 270");
    root.setAttribute("role", "img");
    root.setAttribute("aria-label", "FGA qualification graph");
    const layer = svgElement("g");
    root.append(layer);
    container.replaceChildren(root);
    const state = { root, layer, nodes, edges, viewport: { zoom: 1, panX: 0, panY: 0 }, onNodeSelect: callbacks.onNodeSelect, onEdgeSelect: callbacks.onEdgeSelect };
    render(state);
    return {
      fit: () => { state.viewport = { zoom: 1, panX: 0, panY: 0 }; render(state); },
      setViewport: (viewport: FgaViewport) => { state.viewport = viewport; render(state); },
      resize: () => { render(state); },
      destroy: () => { root.replaceChildren(); root.remove(); },
    };
  },
};
