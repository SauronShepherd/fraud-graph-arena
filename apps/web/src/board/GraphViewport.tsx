import { useMemo, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import type { Graph, GraphEdge, GraphNode } from "../api/contracts";
import { GRAPH_NODE_TOKENS, GRAPH_RELATIONSHIP_TOKENS } from "./graphTokens";

export interface GraphViewProps {
  graph: Graph;
  selectedNodeId?: string | null;
  selectedEdgeId?: string | null;
  onNodeSelect?(id: string | null): void;
  onEdgeSelect?(id: string | null): void;
  onExpand?(id: string): void;
  expandingNodeId?: string | null;
}

type LayoutMode = "GRID" | "CIRCLE";
type PositionedNode = { node: GraphNode; x: number; y: number };
type PanGesture = { pointerId: number; startX: number; startY: number; panX: number; panY: number; moved: boolean };

const VIEW_WIDTH = 500;
const VIEW_HEIGHT = 270;

export function GraphViewport({ graph, selectedNodeId = null, selectedEdgeId = null, onNodeSelect, onEdgeSelect, onExpand, expandingNodeId = null }: GraphViewProps) {
  const [localSelection, setLocalSelection] = useState<string | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [families, setFamilies] = useState<string[] | null>(null);
  const [layout, setLayout] = useState<LayoutMode>("GRID");
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [collapsed, setCollapsed] = useState<string[]>([]);
  const [focusMode, setFocusMode] = useState(false);
  const gesture = useRef<PanGesture | null>(null);
  const suppressBackgroundClick = useRef(false);

  const selected = selectedNodeId ?? selectedEdgeId ?? localSelection;
  const selectedEdge = graph.edges.find((edge) => edge.relationship_id === selected);
  const focusNodeIds = new Set(selectedEdge ? [selectedEdge.source_record_id, selectedEdge.target_record_id] : [selected ?? ""]);
  const familyEdges = useMemo(() => families === null ? graph.edges : graph.edges.filter((edge) => families.includes(edge.relationship_family)), [families, graph.edges]);
  const visibleNodes = useMemo(() => graph.nodes.filter((node) => {
    if (collapsed.includes(node.record_id)) return false;
    if (!focusMode || !selected) return true;
    return focusNodeIds.has(node.record_id) || familyEdges.some((edge) =>
      (focusNodeIds.has(edge.source_record_id) && edge.target_record_id === node.record_id) ||
      (focusNodeIds.has(edge.target_record_id) && edge.source_record_id === node.record_id));
  }), [collapsed, familyEdges, focusMode, graph.nodes, selected, selectedEdge]);
  const visibleNodeIds = new Set(visibleNodes.map((node) => node.record_id));
  const visibleEdges = useMemo(() => familyEdges
    .filter((edge) => visibleNodeIds.has(edge.source_record_id) && visibleNodeIds.has(edge.target_record_id))
    .filter((edge) => !focusMode || !selected || focusNodeIds.has(edge.source_record_id) || focusNodeIds.has(edge.target_record_id)),
  [familyEdges, focusMode, selected, selectedEdge, visibleNodes]);
  const positions = useMemo<PositionedNode[]>(() => visibleNodes.map((node, index) => {
    if (layout === "CIRCLE") {
      const angle = (index / Math.max(visibleNodes.length, 1)) * Math.PI * 2;
      return { node, x: 250 + Math.cos(angle) * 170, y: 135 + Math.sin(angle) * 90 };
    }
    return { node, x: 70 + (index % 4) * 125, y: 70 + Math.floor(index / 4) * 100 };
  }), [layout, visibleNodes]);
  const byId = new Map(positions.map((item) => [item.node.record_id, item]));
  const familyOptions = [...new Set(graph.edges.map((edge) => edge.relationship_family))].sort();
  const selectedNode = graph.nodes.find((node) => node.record_id === selected);
  const edge = graph.edges.find((item) => item.relationship_id === selected);
  const inspectedNode = graph.nodes.find((node) => node.record_id === (hoveredId ?? selected));
  const inspectedEdge = graph.edges.find((item) => item.relationship_id === (hoveredId ?? selected));

  const selectNode = (id: string | null) => { setLocalSelection(id); onNodeSelect?.(id); onEdgeSelect?.(null); };
  const selectEdge = (id: string | null) => { setLocalSelection(id); onEdgeSelect?.(id); onNodeSelect?.(null); };
  const resetView = () => { setLocalSelection(null); setHoveredId(null); setFamilies(null); setZoom(1); setPan({ x: 0, y: 0 }); setLayout("GRID"); setCollapsed([]); setFocusMode(false); onNodeSelect?.(null); onEdgeSelect?.(null); };
  const fitNodes = (targets: PositionedNode[]) => {
    if (!targets.length) return;
    const minX = Math.min(...targets.map((item) => item.x)) - 35;
    const maxX = Math.max(...targets.map((item) => item.x)) + 35;
    const minY = Math.min(...targets.map((item) => item.y)) - 35;
    const maxY = Math.max(...targets.map((item) => item.y)) + 35;
    const nextZoom = Math.min(2, Math.max(.05, Math.min((VIEW_WIDTH - 30) / (maxX - minX), (VIEW_HEIGHT - 30) / (maxY - minY))));
    setZoom(nextZoom);
    setPan({ x: (250 - (minX + maxX) / 2) * nextZoom, y: (135 - (minY + maxY) / 2) * nextZoom });
  };
  const fitSelection = () => {
    if (selectedNode) fitNodes(positions.filter((item) => item.node.record_id === selectedNode.record_id));
    else if (edge) fitNodes(positions.filter((item) => item.node.record_id === edge.source_record_id || item.node.record_id === edge.target_record_id));
  };
  const panBy = (x: number, y: number) => setPan((current) => ({ x: current.x + x, y: current.y + y }));
  const beginPan = (event: ReactPointerEvent<SVGSVGElement>) => {
    if (event.target !== event.currentTarget) return;
    event.currentTarget.setPointerCapture(event.pointerId);
    gesture.current = { pointerId: event.pointerId, startX: event.clientX, startY: event.clientY, panX: pan.x, panY: pan.y, moved: false };
  };
  const movePan = (event: ReactPointerEvent<SVGSVGElement>) => {
    const current = gesture.current;
    if (!current || current.pointerId !== event.pointerId) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const dx = (event.clientX - current.startX) * VIEW_WIDTH / Math.max(rect.width, 1);
    const dy = (event.clientY - current.startY) * VIEW_HEIGHT / Math.max(rect.height, 1);
    current.moved ||= Math.abs(dx) > 1 || Math.abs(dy) > 1;
    setPan({ x: current.panX + dx, y: current.panY + dy });
  };
  const endPan = (event: ReactPointerEvent<SVGSVGElement>) => {
    const current = gesture.current;
    if (!current || current.pointerId !== event.pointerId) return;
    suppressBackgroundClick.current = current.moved;
    if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId);
    gesture.current = null;
  };

  if (!graph.nodes.length) return <section className="graph-panel" aria-labelledby="graph-title"><h2 id="graph-title">Evidence graph</h2><p>No evidence has been revealed.</p><p className="sr-only">Graph contains zero entities and zero relationships.</p></section>;
  return <section className="graph-panel graph-panel--ready" aria-labelledby="graph-title">
    <div className="graph-toolbar"><h2 id="graph-title">Evidence graph</h2><span aria-live="polite">{visibleNodes.length} visible nodes · {visibleEdges.length} visible relationships</span><button type="button" onClick={() => fitNodes(positions)}>Fit graph</button><button type="button" onClick={fitSelection} disabled={!selected}>Fit selection</button><button type="button" onClick={resetView}>Reset view</button></div>
    <div className="graph-controls" aria-label="Graph controls"><button type="button" onClick={() => setZoom((value) => Math.min(2, value + .1))} aria-label="Zoom in">+</button><button type="button" onClick={() => setZoom((value) => Math.max(.05, value - .1))} aria-label="Zoom out">−</button><button type="button" onClick={() => panBy(-30, 0)} aria-label="Pan left">←</button><button type="button" onClick={() => panBy(30, 0)} aria-label="Pan right">→</button><button type="button" onClick={() => panBy(0, -30)} aria-label="Pan up">↑</button><button type="button" onClick={() => panBy(0, 30)} aria-label="Pan down">↓</button><button type="button" onClick={() => setLayout("GRID")} aria-pressed={layout === "GRID"}>Grid layout</button><button type="button" onClick={() => setLayout("CIRCLE")} aria-pressed={layout === "CIRCLE"}>Circle layout</button><button type="button" onClick={() => setFocusMode((value) => !value)} aria-pressed={focusMode} disabled={!selected}>{focusMode ? "Show all nodes" : "Focus selection"}</button><fieldset><legend>Relationship filters</legend><label><input type="checkbox" checked={families === null} onChange={() => setFamilies(null)} /> All</label>{familyOptions.map((family) => <label key={family}><input type="checkbox" checked={families?.includes(family) ?? false} onChange={(event) => setFamilies((current) => { const next = current === null ? familyOptions : current; return event.target.checked ? [...next, family] : next.filter((item) => item !== family); })} /> {family}</label>)}</fieldset></div>
    <svg className="graph-canvas" viewBox={`0 0 ${VIEW_WIDTH} ${VIEW_HEIGHT}`} role="img" aria-label="Interactive published evidence graph" onPointerDown={beginPan} onPointerMove={movePan} onPointerUp={endPan} onPointerCancel={endPan} onClick={() => { if (suppressBackgroundClick.current) { suppressBackgroundClick.current = false; return; } selectNode(null); }}><defs><marker id="graph-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#d9b46c" /></marker></defs><g data-testid="graph-transform" transform={`translate(${250 - 250 * zoom + pan.x} ${135 - 135 * zoom + pan.y}) scale(${zoom})`}>{visibleEdges.map((item: GraphEdge) => { const a = byId.get(item.source_record_id); const b = byId.get(item.target_record_id); const token = GRAPH_RELATIONSHIP_TOKENS[item.relationship_family as keyof typeof GRAPH_RELATIONSHIP_TOKENS] ?? GRAPH_RELATIONSHIP_TOKENS.DEFAULT; return a && b ? <g key={item.relationship_id} data-edge-id={item.relationship_id} onMouseEnter={() => setHoveredId(item.relationship_id)} onMouseLeave={() => setHoveredId(null)}><line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="transparent" strokeWidth="14" pointerEvents="stroke" onClick={(event) => { event.stopPropagation(); selectEdge(item.relationship_id); }} /><line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={token.stroke} strokeWidth={selected === item.relationship_id ? 4 : 2} markerEnd={item.directed ? "url(#graph-arrow)" : undefined} pointerEvents="none" /></g> : null; })}{positions.map(({ node: item, x, y }) => { const token = GRAPH_NODE_TOKENS[item.record_type as keyof typeof GRAPH_NODE_TOKENS] ?? GRAPH_NODE_TOKENS.DEFAULT; return <g key={item.record_id} tabIndex={0} role="button" aria-label={`${item.label}, ${item.record_id}`} onClick={(event) => { event.stopPropagation(); selectNode(item.record_id); }} onMouseEnter={() => setHoveredId(item.record_id)} onMouseLeave={() => setHoveredId(null)} onFocus={() => setHoveredId(item.record_id)} onBlur={() => setHoveredId(null)} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectNode(item.record_id); } }}><circle cx={x} cy={y} r="23" fill={token.fill} stroke={selected === item.record_id ? "#fff1bd" : "#d9b46c"} strokeWidth="3" /><text x={x} y={y + 4} textAnchor="middle" fill="#fff" fontSize="9" pointerEvents="none">{item.label.slice(0, 12)}</text></g>; })}</g></svg>
    <div className="graph-node-actions" aria-label="Graph expansion"><p>Expand one hop from a visible node. Hidden evidence remains unavailable.</p>{visibleNodes.map((item) => <span key={item.record_id}><button type="button" onClick={() => onExpand?.(item.record_id)} disabled={!onExpand || expandingNodeId === item.record_id}>{expandingNodeId === item.record_id ? "Expanding…" : `Expand ${item.label}`}</button><button type="button" onClick={() => setCollapsed((current) => current.includes(item.record_id) ? current : [...current, item.record_id])}>Collapse {item.label}</button></span>)}{collapsed.map((id) => { const item = graph.nodes.find((node) => node.record_id === id); return item ? <button key={id} type="button" onClick={() => setCollapsed((current) => current.filter((value) => value !== id))}>Restore {item.label}</button> : null; })}</div>
    <div className="graph-legend" aria-label="Graph legend"><strong>Legend</strong><span><i className="legend-swatch legend-swatch--person" /> Person record</span><span><i className="legend-swatch legend-swatch--organization" /> Organization record</span><span><i className="legend-line" /> Direct source relationship</span></div>
    <div className="graph-inspector" aria-live="polite">{inspectedNode ? <><strong>{inspectedNode.label}</strong><span>{inspectedNode.record_type} · {inspectedNode.record_id}</span><p>{inspectedNode.safe_summary}</p></> : inspectedEdge ? <><strong>{inspectedEdge.relationship_type}</strong><span>{inspectedEdge.relationship_family} · {inspectedEdge.source_record_id} → {inspectedEdge.target_record_id}</span><p>{inspectedEdge.player_safe_summary}</p></> : <p>Select a node or relationship to inspect its safe published meaning.</p>}</div>
    <aside className="graph-minimap" aria-label="Graph minimap"><strong>Minimap</strong><svg viewBox="0 0 100 54" role="img" aria-label={`${visibleNodes.length} nodes in current graph view`}>{positions.map(({ node, x, y }) => <circle key={node.record_id} cx={x / 5} cy={y / 5} r="2" aria-label={node.label} />)}<rect x={Math.max(0, 50 - (250 + pan.x) / zoom / 5)} y={Math.max(0, 27 - (135 + pan.y) / zoom / 5)} width={100 / zoom} height={54 / zoom} fill="none" stroke="#fff1bd" /></svg></aside>
    <details className="graph-semantic"><summary>Semantic evidence list</summary><ul>{visibleNodes.map((item) => <li key={item.record_id}><button type="button" onClick={() => selectNode(item.record_id)}>{item.label} ({item.record_id})</button></li>)}{visibleEdges.map((item) => <li key={item.relationship_id}><button type="button" onClick={() => selectEdge(item.relationship_id)}>{item.relationship_type}: {item.source_record_id} → {item.target_record_id}</button></li>)}</ul></details>
  </section>;
}
