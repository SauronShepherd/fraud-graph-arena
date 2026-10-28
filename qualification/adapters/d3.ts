import * as d3 from "d3";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";

export const d3Candidate: QualificationCandidate = {
  name: "D3",
  version: "7.9.0",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const svg = d3.select(container).append("svg").attr("viewBox", "0 0 500 270").attr("role", "img").attr("aria-label", "FGA qualification graph");
    const layer = svg.append("g");
    const byId = new Map(nodes.map((node) => [node.id, node]));
    const viewport = { zoom: 1, panX: 0, panY: 0 };
    const render = () => {
      layer.attr("transform", `translate(${250 - 250 * viewport.zoom + viewport.panX} ${135 - 135 * viewport.zoom + viewport.panY}) scale(${viewport.zoom})`);
      layer.selectAll<SVGLineElement, FgaEdge>("line").data(edges, (edge) => edge.id).join(
        (enter) => enter.append("line"),
        (update) => update,
        (exit) => exit.remove(),
      ).attr("x1", (edge) => byId.get(edge.sourceId)?.x ?? 0).attr("y1", (edge) => byId.get(edge.sourceId)?.y ?? 0)
        .attr("x2", (edge) => byId.get(edge.targetId)?.x ?? 0).attr("y2", (edge) => byId.get(edge.targetId)?.y ?? 0)
        .attr("stroke", "#d9b46c").attr("stroke-width", 2).attr("data-edge-id", (edge) => edge.id)
        .attr("tabindex", 0).attr("role", "button").attr("aria-label", (edge) => `${edge.relationshipType}: ${edge.id}`)
        .on("click", (_event, edge) => callbacks.onEdgeSelect(edge.id));
      layer.selectAll<SVGGElement, FgaNode>("g[data-node-id]").data(nodes, (node) => node.id).join(
        (enter) => enter.append("g"),
        (update) => update,
        (exit) => exit.remove(),
      ).attr("data-node-id", (node) => node.id).attr("tabindex", 0).attr("role", "button")
        .attr("aria-label", (node) => `${node.label}, ${node.id}`).attr("transform", (node) => `translate(${node.x} ${node.y})`)
        .on("click", (_event, node) => callbacks.onNodeSelect(node.id))
        .each(function (node) {
          const group = d3.select(this);
          group.selectAll("circle").data([node]).join("circle").attr("r", 23).attr("fill", node.recordType === "PERSON_RECORD" ? "#496b68" : "#765b82").attr("stroke", "#d9b46c");
          group.selectAll("text").data([node]).join("text").text((item) => item.label.slice(0, 14)).attr("fill", "#fff").attr("font-size", 9).attr("text-anchor", "middle").attr("y", 4);
        });
    };
    render();
    return {
      fit: () => { viewport.zoom = 1; viewport.panX = 0; viewport.panY = 0; render(); },
      setViewport: (next: FgaViewport) => { Object.assign(viewport, next); render(); },
      resize: () => render(),
      destroy: () => { svg.remove(); },
    };
  },
};
