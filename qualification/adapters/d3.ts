import * as d3 from "d3";
import type { CandidateInstance, FgaEdge, FgaNode, FgaViewport, QualificationCandidate } from "../candidate-contract";
import { relationshipColor, visualMeta } from "../visual-semantics";

const WIDTH = 900;
const HEIGHT = 560;

function nodeShape(group: d3.Selection<SVGGElement, FgaNode, null, undefined>, node: FgaNode): void {
  const meta = visualMeta(node);
  if (meta.shape === "roundrectangle") {
    group.append("rect").attr("x", -28).attr("y", -28).attr("width", 56).attr("height", 56).attr("rx", 15);
  } else if (meta.shape === "diamond") {
    group.append("path").attr("d", "M0,-29 L29,0 L0,29 L-29,0 Z");
  } else if (meta.shape === "star") {
    group.append("path").attr("d", d3.symbol().type(d3.symbolStar).size(2200)());
  } else {
    group.append("circle").attr("r", 29);
  }
  group.select("circle,rect,path")
    .attr("fill", meta.color)
    .attr("stroke", meta.stroke)
    .attr("stroke-width", 3)
    .attr("stroke-dasharray", meta.borderStyle === "dashed" ? "7 4" : meta.borderStyle === "dotted" ? "2 4" : null);
  group.append("text").attr("class", "node-icon").text(node.icon ?? meta.glyph).attr("text-anchor", "middle").attr("dy", "6");
  group.append("text").attr("class", "node-label").text(node.label).attr("text-anchor", "middle").attr("y", 45);
}

export const d3Candidate: QualificationCandidate = {
  name: "D3",
  version: "7.9.0",
  mount(container, nodes, edges, callbacks): CandidateInstance {
    const svg = d3.select(container).append("svg").attr("viewBox", `0 0 ${WIDTH} ${HEIGHT}`).attr("role", "img").attr("aria-label", "FGA qualification graph");
    const defs = svg.append("defs");
    defs.append("marker").attr("id", "fga-d3-arrow").attr("viewBox", "0 -5 10 10").attr("refX", 8).attr("refY", 0).attr("markerWidth", 6).attr("markerHeight", 6).attr("orient", "auto").append("path").attr("d", "M0,-5L10,0L0,5").attr("fill", "#cdbb99");
    const layer = svg.append("g");
    const byId = new Map(nodes.map((node) => [node.id, node]));
    const viewport = { zoom: 1, panX: 0, panY: 0 };
    const render = () => {
      layer.attr("transform", `translate(${WIDTH / 2 - WIDTH / 2 * viewport.zoom + viewport.panX} ${HEIGHT / 2 - HEIGHT / 2 * viewport.zoom + viewport.panY}) scale(${viewport.zoom})`);
      const edgeGroups = layer.selectAll<SVGGElement, FgaEdge>("g[data-edge-group]").data(edges, (edge) => edge.id).join(
        (enter) => {
          const group = enter.append("g").attr("data-edge-group", "true");
          group.append("line").attr("class", "edge-hit");
          group.append("line").attr("class", "edge-line").attr("marker-end", "url(#fga-d3-arrow)");
          return group;
        },
        (update) => update,
        (exit) => exit.remove(),
      );
      edgeGroups.each(function (edge) {
        const source = byId.get(edge.sourceId);
        const target = byId.get(edge.targetId);
        if (!source || !target) return;
        const group = d3.select(this);
        group.select("line.edge-hit").attr("x1", source.x).attr("y1", source.y).attr("x2", target.x).attr("y2", target.y).attr("data-edge-id", edge.id)
          .attr("tabindex", 0).attr("role", "button").attr("aria-label", `${edge.relationshipType}: ${edge.id}`)
          .on("click", () => callbacks.onEdgeSelect(edge.id))
          .on("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); callbacks.onEdgeSelect(edge.id); } })
          .on("mouseenter", () => callbacks.onEdgeHover?.(edge.id)).on("mouseleave", () => callbacks.onEdgeHover?.(null));
        group.select("line.edge-line").attr("x1", source.x).attr("y1", source.y).attr("x2", target.x).attr("y2", target.y).attr("stroke", relationshipColor(edge.relationshipFamily)).attr("stroke-width", edge.relationshipFamily === "TRANSACTIONAL" ? 3 : 2).attr("stroke-dasharray", edge.relationshipFamily === "SHARED_ATTRIBUTE" ? "5 4" : null).attr("data-edge-id", edge.id);
      });
      const nodeGroups = layer.selectAll<SVGGElement, FgaNode>("g[data-node-id]").data(nodes, (node) => node.id).join(
        (enter) => enter.append("g"),
        (update) => update,
        (exit) => exit.remove(),
      ).attr("data-node-id", (node) => node.id).attr("tabindex", 0).attr("role", "button")
        .attr("aria-label", (node) => `${node.label}, ${node.id}, ${visualMeta(node).label}`).attr("transform", (node) => `translate(${node.x} ${node.y})`)
        .on("click", (_event, node) => callbacks.onNodeSelect(node.id))
        .on("keydown", (event, node) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); callbacks.onNodeSelect(node.id); } })
        .on("mouseenter", (_event, node) => callbacks.onNodeHover?.(node.id))
        .on("mouseleave", () => callbacks.onNodeHover?.(null));
      nodeGroups.each(function (node) {
        const group = d3.select(this);
        group.selectAll("*").remove();
        nodeShape(group as d3.Selection<SVGGElement, FgaNode, null, undefined>, node);
      });
    };
    render();
    return {
      fit: () => { viewport.zoom = 1; viewport.panX = 0; viewport.panY = 0; render(); },
      setViewport: (next: FgaViewport) => { Object.assign(viewport, next); render(); },
      resize: () => render(),
      probeNode: (id: string) => { container.querySelector<SVGGElement>(`g[data-node-id="${id}"]`)?.dispatchEvent(new MouseEvent("click", { bubbles: true })); },
      probeEdge: (id: string) => { container.querySelector<SVGLineElement>(`line.edge-hit[data-edge-id="${id}"]`)?.dispatchEvent(new MouseEvent("click", { bubbles: true })); },
      destroy: () => { svg.remove(); },
    };
  },
};
