import { useMemo, useState } from "react";
import type { Graph } from "../api/contracts";
import { GRAPH_NODE_TOKENS, GRAPH_RELATIONSHIP_TOKENS } from "./graphTokens";

export interface GraphViewProps { graph: Graph; selectedNodeId?: string | null; selectedEdgeId?: string | null; onNodeSelect?(id: string | null): void; onEdgeSelect?(id: string | null): void; }
type LayoutMode = "GRID" | "CIRCLE";

export function GraphViewport({ graph, selectedNodeId = null, selectedEdgeId = null, onNodeSelect, onEdgeSelect }: GraphViewProps) {
  const [localSelection, setLocalSelection] = useState<string | null>(null);
  const [families, setFamilies] = useState<string[]>([]);
  const [layout, setLayout] = useState<LayoutMode>("GRID");
  const [zoom, setZoom] = useState(1);
  const selected = selectedNodeId ?? selectedEdgeId ?? localSelection;
  const visibleEdges = useMemo(() => families.length ? graph.edges.filter((edge) => families.includes(edge.relationship_family)) : graph.edges, [families, graph.edges]);
  const positions = useMemo(() => graph.nodes.map((node, index) => {
    if (layout === "CIRCLE") { const angle = (index / Math.max(graph.nodes.length, 1)) * Math.PI * 2; return { node, x: 250 + Math.cos(angle) * 170, y: 135 + Math.sin(angle) * 90 }; }
    return { node, x: 70 + (index % 4) * 125, y: 70 + Math.floor(index / 4) * 100 };
  }), [graph.nodes, layout]);
  const byId = new Map(positions.map((item) => [item.node.record_id, item]));
  const selectNode = (id: string | null) => { setLocalSelection(id); onNodeSelect?.(id); onEdgeSelect?.(null); };
  const selectEdge = (id: string | null) => { setLocalSelection(id); onEdgeSelect?.(id); onNodeSelect?.(null); };
  const resetView = () => { setLocalSelection(null); setZoom(1); setLayout("GRID"); onNodeSelect?.(null); onEdgeSelect?.(null); };
  const familyOptions = [...new Set(graph.edges.map((edge) => edge.relationship_family))].sort();
  if (!graph.nodes.length) return <section className="graph-panel" aria-labelledby="graph-title"><h2 id="graph-title">Evidence graph</h2><p>No evidence has been revealed.</p><p className="sr-only">Graph contains zero entities and zero relationships.</p></section>;
  const node = graph.nodes.find((item) => item.record_id === selected);
  const edge = graph.edges.find((item) => item.relationship_id === selected);
  return <section className="graph-panel graph-panel--ready" aria-labelledby="graph-title">
    <div className="graph-toolbar"><h2 id="graph-title">Evidence graph</h2><span aria-live="polite">{graph.node_count} visible nodes · {visibleEdges.length} visible relationships</span><button type="button" onClick={resetView}>Reset view</button></div>
    <div className="graph-controls" aria-label="Graph controls"><button type="button" onClick={() => setZoom((value) => Math.min(2, value + .1))} aria-label="Zoom in">+</button><button type="button" onClick={() => setZoom((value) => Math.max(.6, value - .1))} aria-label="Zoom out">−</button><button type="button" onClick={() => setLayout("GRID")} aria-pressed={layout === "GRID"}>Grid layout</button><button type="button" onClick={() => setLayout("CIRCLE")} aria-pressed={layout === "CIRCLE"}>Circle layout</button><fieldset><legend>Relationship filters</legend><label><input type="checkbox" checked={!families.length} onChange={() => setFamilies([])} /> All</label>{familyOptions.map((family) => <label key={family}><input type="checkbox" checked={families.includes(family)} onChange={(event) => setFamilies((current) => event.target.checked ? [...current, family] : current.filter((item) => item !== family))} /> {family}</label>)}</fieldset></div>
    <svg className="graph-canvas" viewBox="0 0 500 270" role="img" aria-label="Interactive published evidence graph" onClick={() => selectNode(null)}><g transform={`translate(${250 - 250 * zoom} ${135 - 135 * zoom}) scale(${zoom})`}>{visibleEdges.map((item) => { const a = byId.get(item.source_record_id); const b = byId.get(item.target_record_id); const token = GRAPH_RELATIONSHIP_TOKENS[item.relationship_family as keyof typeof GRAPH_RELATIONSHIP_TOKENS] ?? GRAPH_RELATIONSHIP_TOKENS.DEFAULT; return a && b ? <line key={item.relationship_id} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={token.stroke} strokeWidth={selected === item.relationship_id ? 4 : 2} onClick={(event) => { event.stopPropagation(); selectEdge(item.relationship_id); }} /> : null; })}{positions.map(({ node: item, x, y }) => { const token = GRAPH_NODE_TOKENS[item.record_type as keyof typeof GRAPH_NODE_TOKENS] ?? GRAPH_NODE_TOKENS.DEFAULT; return <g key={item.record_id} tabIndex={0} role="button" aria-label={`${item.label}, ${item.record_id}`} onClick={(event) => { event.stopPropagation(); selectNode(item.record_id); }} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectNode(item.record_id); } }}><circle cx={x} cy={y} r="23" fill={token.fill} stroke={selected === item.record_id ? "#fff1bd" : "#d9b46c"} strokeWidth="3" /><text x={x} y={y + 4} textAnchor="middle" fill="#fff" fontSize="9">{item.label.slice(0, 12)}</text></g>; })}</g></svg>
    <div className="graph-legend" aria-label="Graph legend"><strong>Legend</strong><span><i className="legend-swatch legend-swatch--person" /> Person record</span><span><i className="legend-swatch legend-swatch--organization" /> Organization record</span><span><i className="legend-line" /> Direct source relationship</span></div><div className="graph-inspector" aria-live="polite">{node ? <><strong>{node.label}</strong><span>{node.record_type} · {node.record_id}</span><p>{node.safe_summary}</p></> : edge ? <><strong>{edge.relationship_type}</strong><span>{edge.relationship_family} · {edge.source_record_id} → {edge.target_record_id}</span><p>{edge.player_safe_summary}</p></> : <p>Select a node or relationship to inspect its safe published meaning.</p>}</div><details className="graph-semantic"><summary>Semantic evidence list</summary><ul>{graph.nodes.map((item) => <li key={item.record_id}><button type="button" onClick={() => selectNode(item.record_id)}>{item.label} ({item.record_id})</button></li>)}{visibleEdges.map((item) => <li key={item.relationship_id}><button type="button" onClick={() => selectEdge(item.relationship_id)}>{item.relationship_type}: {item.source_record_id} → {item.target_record_id}</button></li>)}</ul></details>
  </section>;
}
