import { useEffect, useMemo, useRef, useState, type PointerEvent as ReactPointerEvent, type ReactNode } from "react";
import type { Graph, GraphEdge } from "../api/contracts";
import { GraphContextPanel, GraphContextPreview, type GraphTarget } from "./GraphContextPanel";
import { GRAPH_NODE_TOKENS, GRAPH_RELATIONSHIP_TOKENS } from "./graphTokens";

export interface GraphViewProps {
  graph: Graph;
  selectedNodeId?: string | null;
  selectedEdgeId?: string | null;
  onNodeSelect?(id: string | null): void;
  onEdgeSelect?(id: string | null): void;
}

type LayoutMode = "GRID" | "CIRCLE";
type Point = { x: number; y: number };

function nodeGlyph(recordType: string): string {
  if (recordType.includes("PERSON")) return "◉";
  if (recordType.includes("ORGANIZATION")) return "▦";
  if (recordType.includes("DEVICE")) return "⌁";
  if (recordType.includes("ADDRESS")) return "⌂";
  if (recordType.includes("ACCOUNT")) return "◈";
  return "○";
}

function VisualNodeGlyph({ recordType }: { recordType: string }): ReactNode {
  if (recordType.includes("PERSON")) return <><circle cx="0" cy="-5" r="4" /><path d="M -8 9 C -8 2 -5 0 0 0 C 5 0 8 2 8 9 Z" /></>;
  if (recordType.includes("DEVICE")) return <><rect className="graph-node-glyph-outline" x="-7" y="-10" width="14" height="20" rx="3" /><circle cx="0" cy="6" r="1.2" /><path d="M -4 -6 H 4" /></>;
  if (recordType.includes("ACCOUNT")) return <path d="M -10 -6 H 7 C 9 -6 10 -4 10 -1 V 8 H -10 Z M -10 -6 V -9 H 7 V -6 M 3 2 H 9" />;
  if (recordType.includes("BANK")) return <path d="M -10 -4 L 0 -10 L 10 -4 Z M -8 -2 V 7 M -3 -2 V 7 M 3 -2 V 7 M 8 -2 V 7 M -11 9 H 11" />;
  if (recordType.includes("ORGANIZATION")) return <path d="M -10 -5 H 10 V 9 H -10 Z M -4 -5 V -9 H 4 V -5 M -7 0 H 7 M -7 5 H 7" />;
  if (recordType.includes("ADDRESS")) return <path d="M 0 11 L -8 1 C -11 -5 -6 -10 0 -10 C 6 -10 11 -5 8 1 Z M 0 -5 A 3 3 0 1 0 0 1 A 3 3 0 1 0 0 -5" />;
  return <text y="5">◆</text>;
}

function GraphRelationshipComposer({ graph, onCreate, onCancel }: { graph: Graph; onCreate(edge: GraphEdge): void; onCancel(): void }) {
  const [source, setSource] = useState(graph.nodes[0]?.record_id ?? "");
  const [target, setTarget] = useState(graph.nodes[1]?.record_id ?? graph.nodes[0]?.record_id ?? "");
  const [relationshipType, setRelationshipType] = useState("WORKING_HYPOTHESIS");
  const [directed, setDirected] = useState(true);
  const canSubmit = Boolean(source && target && relationshipType.trim());
  return <form className="graph-relationship-composer" onSubmit={(event) => { event.preventDefault(); if (!canSubmit) return; onCreate({ relationship_id: `LOCAL-REL-${Date.now()}`, source_record_id: source, target_record_id: target, relationship_family: "INVESTIGATOR_ADDED", relationship_type: relationshipType.trim(), directed, provenance: "local-investigation", event_time: "", player_safe_summary: "Investigator-added working relationship; not part of the published projection." }); }}>
    <div><strong>Add working relationship</strong><span>Dashed, local and removable. Published relationships stay untouched.</span></div>
    <label>From<select aria-label="Relationship source" value={source} onChange={(event) => setSource(event.target.value)}>{graph.nodes.map((node) => <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>)}</select></label>
    <label>To<select aria-label="Relationship target" value={target} onChange={(event) => setTarget(event.target.value)}>{graph.nodes.map((node) => <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>)}</select></label>
    <label>Relationship label<input aria-label="Relationship label" value={relationshipType} onChange={(event) => setRelationshipType(event.target.value)} /></label>
    <label className="graph-checkbox"><input type="checkbox" checked={directed} onChange={(event) => setDirected(event.target.checked)} /> Directed</label>
    <div className="graph-context-actions"><button type="submit" disabled={!canSubmit}>Add dashed relationship</button><button type="button" onClick={onCancel}>Cancel</button></div>
  </form>;
}

export function GraphViewport({ graph, selectedNodeId = null, selectedEdgeId = null, onNodeSelect, onEdgeSelect }: GraphViewProps) {
  const [localSelection, setLocalSelection] = useState<string | null>(null);
  const [layout, setLayout] = useState<LayoutMode>("GRID");
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState<Point>({ x: 0, y: 0 });
  const [positionOverrides, setPositionOverrides] = useState<Record<string, Point>>({});
  const [dragging, setDragging] = useState<{ id: string; original: Point } | null>(null);
  const [addedEdges, setAddedEdges] = useState<GraphEdge[]>([]);
  const [favoriteTargets, setFavoriteTargets] = useState<GraphTarget[]>([]);
  const [hoverTarget, setHoverTarget] = useState<GraphTarget | null>(null);
  const hoverHideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [composerOpen, setComposerOpen] = useState(false);
  const nextRelationshipNumber = useRef(1);
  const graphIdentity = `${graph.projection_version}|${graph.nodes.map((node) => node.record_id).join(",")}|${graph.edges.map((edge) => edge.relationship_id).join(",")}`;
  const showHover = (target: GraphTarget) => { if (hoverHideTimer.current) clearTimeout(hoverHideTimer.current); setHoverTarget(target); };
  const scheduleHideHover = () => { if (hoverHideTimer.current) clearTimeout(hoverHideTimer.current); hoverHideTimer.current = setTimeout(() => { setHoverTarget(null); hoverHideTimer.current = null; }, 220); };
  useEffect(() => {
    setLocalSelection(null);
    setAddedEdges([]);
    setFavoriteTargets([]);
    setHoverTarget(null);
    setComposerOpen(false);
    setPositionOverrides({});
    setPan({ x: 0, y: 0 });
    setZoom(1);
    nextRelationshipNumber.current = 1;
  }, [graphIdentity]);
  useEffect(() => () => { if (hoverHideTimer.current) clearTimeout(hoverHideTimer.current); }, []);
  const activeLocalNodeId = localSelection && graph.nodes.some((node) => node.record_id === localSelection) ? localSelection : null;
  const activeLocalEdgeId = localSelection && [...graph.edges, ...addedEdges].some((edge) => edge.relationship_id === localSelection) ? localSelection : null;
  const activeNodeId = selectedNodeId ?? activeLocalNodeId;
  const activeEdgeId = selectedEdgeId ?? activeLocalEdgeId;
  const selected = activeNodeId ?? activeEdgeId;
  const workingGraph = useMemo<Graph>(() => ({ ...graph, edges: [...graph.edges, ...addedEdges], edge_count: graph.edges.length + addedEdges.length }), [addedEdges, graph]);
  const userAddedEdgeIds = useMemo(() => new Set(addedEdges.map((edge) => edge.relationship_id)), [addedEdges]);
  const positions = useMemo(() => graph.nodes.map((node, index) => {
    const base = layout === "CIRCLE"
      ? { x: 285 + Math.cos((index / Math.max(graph.nodes.length, 1)) * Math.PI * 2) * 205, y: 190 + Math.sin((index / Math.max(graph.nodes.length, 1)) * Math.PI * 2) * 125 }
      : { x: 80 + (index % 4) * 155, y: 80 + Math.floor(index / 4) * 105 };
    return { node, ...(positionOverrides[node.record_id] ?? base) };
  }), [graph.nodes, layout, positionOverrides]);
  const byId = new Map(positions.map((item) => [item.node.record_id, item]));
  const focusedIds = useMemo(() => {
    if (!selected) return new Set<string>();
    if (activeNodeId) return new Set([activeNodeId, ...workingGraph.edges.filter((edge) => edge.source_record_id === activeNodeId || edge.target_record_id === activeNodeId).flatMap((edge) => [edge.source_record_id, edge.target_record_id])]);
    const edge = workingGraph.edges.find((item) => item.relationship_id === activeEdgeId);
    return edge ? new Set([edge.source_record_id, edge.target_record_id]) : new Set<string>();
  }, [activeEdgeId, activeNodeId, selected, workingGraph.edges]);
  const targetPosition = (target: GraphTarget): Point | null => {
    if (target.kind === "node") return byId.get(target.id) ? { x: byId.get(target.id)!.x, y: byId.get(target.id)!.y } : null;
    const edge = workingGraph.edges.find((item) => item.relationship_id === target.id);
    const source = edge ? byId.get(edge.source_record_id) : null;
    const destination = edge ? byId.get(edge.target_record_id) : null;
    return source && destination ? { x: (source.x + destination.x) / 2, y: (source.y + destination.y) / 2 } : null;
  };
  const targetLabel = (target: GraphTarget) => {
    if (target.kind === "node") return graph.nodes.find((node) => node.record_id === target.id)?.label ?? target.id;
    return workingGraph.edges.find((edge) => edge.relationship_id === target.id)?.relationship_type ?? target.id;
  };
  const selectNode = (id: string | null) => { setLocalSelection(id); setHoverTarget(null); onNodeSelect?.(id); onEdgeSelect?.(null); };
  const selectEdge = (id: string | null) => { setLocalSelection(id); setHoverTarget(null); onEdgeSelect?.(id); onNodeSelect?.(null); };
  const centerOnTarget = (target: GraphTarget) => {
    const point = targetPosition(target);
    if (!point) return;
    const nextZoom = Math.max(zoom, 1.15);
    setZoom(nextZoom);
    setPan({ x: (285 - point.x) * nextZoom, y: (190 - point.y) * nextZoom });
    if (target.kind === "node") selectNode(target.id);
    else selectEdge(target.id);
  };
  const toggleFavorite = (target: GraphTarget) => setFavoriteTargets((current) => current.some((item) => item.kind === target.kind && item.id === target.id) ? current.filter((item) => item.kind !== target.kind || item.id !== target.id) : [...current, target]);
  const resetView = () => { setLocalSelection(null); setHoverTarget(null); setZoom(1); setPan({ x: 0, y: 0 }); setLayout("GRID"); setPositionOverrides({}); onNodeSelect?.(null); onEdgeSelect?.(null); };
  const updateDraggedPosition = (event: ReactPointerEvent<SVGSVGElement>) => {
    if (!dragging) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const offsetX = 285 - 285 * zoom + pan.x;
    const offsetY = 190 - 190 * zoom + pan.y;
    const x = ((((event.clientX - rect.left) / rect.width) * 570) - offsetX) / zoom;
    const y = ((((event.clientY - rect.top) / rect.height) * 380) - offsetY) / zoom;
    setPositionOverrides((current) => ({ ...current, [dragging.id]: { x: Math.max(35, Math.min(535, x)), y: Math.max(35, Math.min(345, y)) } }));
  };
  const finishDrag = () => setDragging(null);
  const cancelDrag = () => { if (!dragging) return; setPositionOverrides((current) => ({ ...current, [dragging.id]: dragging.original })); setDragging(null); };
  const createRelationship = (edge: GraphEdge) => { const nextId = `LOCAL-REL-${String(nextRelationshipNumber.current).padStart(4, "0")}`; nextRelationshipNumber.current += 1; setAddedEdges((current) => [...current, { ...edge, relationship_id: nextId }]); setComposerOpen(false); selectEdge(nextId); };
  const deleteRelationship = (id: string) => { setAddedEdges((current) => current.filter((edge) => edge.relationship_id !== id)); if (activeEdgeId === id) selectEdge(null); };
  const hoverPoint = hoverTarget ? targetPosition(hoverTarget) : null;

  if (!graph.nodes.length) return <section className="graph-panel graph-panel--ready" aria-labelledby="graph-title"><div className="graph-toolbar"><h2 id="graph-title">Evidence graph</h2><span aria-live="polite">0 entities · 0 relationships</span></div><div className="graph-layout"><div className="graph-empty-state"><span aria-hidden="true">⌁</span><h2>No evidence has been revealed</h2><p>The engine keeps the empty projection explicit instead of inventing a graph.</p><p className="sr-only">Graph contains zero entities and zero relationships.</p></div><GraphContextPanel graph={workingGraph} selectedNodeId={null} selectedEdgeId={null} onNodeSelect={() => undefined} onEdgeSelect={() => undefined} /></div></section>;

  return <section className="graph-panel graph-panel--ready" aria-labelledby="graph-title">
    <div className="graph-toolbar"><div><p className="graph-kicker">Investigation graph</p><h2 id="graph-title">Evidence graph</h2></div><span aria-live="polite">{graph.nodes.length} entities · {workingGraph.edges.length} relationships</span><button type="button" onClick={resetView}>Reset view</button></div>
    <div className="graph-controls" aria-label="Graph controls"><button type="button" onClick={() => setZoom((value) => Math.min(2, value + .1))} aria-label="Zoom in">+</button><button type="button" onClick={() => setZoom((value) => Math.max(.6, value - .1))} aria-label="Zoom out">−</button><button type="button" onClick={() => setLayout("GRID")} aria-pressed={layout === "GRID"}>Grid layout</button><button type="button" onClick={() => setLayout("CIRCLE")} aria-pressed={layout === "CIRCLE"}>Circle layout</button><button type="button" onClick={() => setComposerOpen((value) => !value)} aria-expanded={composerOpen}>Add relationship</button><span className="graph-hint">Hover or focus a target · drag a node · Escape cancels</span></div>
    {composerOpen ? <GraphRelationshipComposer graph={graph} onCreate={createRelationship} onCancel={() => setComposerOpen(false)} /> : null}
    <div className="graph-layout">
      <div className="graph-stage">
        <svg className="graph-canvas" viewBox="0 0 570 380" aria-label="Interactive published evidence graph" onClick={() => selectNode(null)} onPointerMove={updateDraggedPosition} onPointerUp={finishDrag} onPointerCancel={finishDrag} onKeyDown={(event) => { if (event.key === "Escape") cancelDrag(); }}>
          <defs><marker id="fga-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#b6a384" /></marker></defs>
          <g transform={`translate(${285 - 285 * zoom + pan.x} ${190 - 190 * zoom + pan.y}) scale(${zoom})`}>
            {workingGraph.edges.map((item) => { const source = byId.get(item.source_record_id); const destination = byId.get(item.target_record_id); const token = GRAPH_RELATIONSHIP_TOKENS[item.relationship_family as keyof typeof GRAPH_RELATIONSHIP_TOKENS] ?? GRAPH_RELATIONSHIP_TOKENS.DEFAULT; const focused = !focusedIds.size || focusedIds.has(item.source_record_id) || focusedIds.has(item.target_record_id); const selectedEdge = activeEdgeId === item.relationship_id; const favoriteEdge = favoriteTargets.some((target) => target.kind === "edge" && target.id === item.relationship_id); const isAdded = userAddedEdgeIds.has(item.relationship_id); return source && destination ? <line key={item.relationship_id} className={`graph-edge${selectedEdge ? " graph-edge--selected" : ""}${favoriteEdge ? " graph-edge--favorite" : ""}${focused ? "" : " graph-edge--dimmed"}${isAdded ? " graph-edge--working" : ""}`} x1={source.x} y1={source.y} x2={destination.x} y2={destination.y} stroke={token.stroke} strokeWidth={selectedEdge ? 5 : favoriteEdge ? 4 : 2.5} strokeDasharray={isAdded ? "10 8" : undefined} markerEnd="url(#fga-arrow)" tabIndex={0} role="button" aria-label={`Graph relationship ${item.relationship_type} from ${item.source_record_id} to ${item.target_record_id}${favoriteEdge ? ", marked" : ""}`} onMouseEnter={() => showHover({ kind: "edge", id: item.relationship_id })} onMouseLeave={scheduleHideHover} onFocus={() => showHover({ kind: "edge", id: item.relationship_id })} onBlur={scheduleHideHover} onClick={(event) => { event.stopPropagation(); selectEdge(item.relationship_id); }} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectEdge(item.relationship_id); } }} onContextMenu={(event) => { event.preventDefault(); event.stopPropagation(); selectEdge(item.relationship_id); }} /> : null; })}
            {positions.map(({ node, x, y }) => { const token = GRAPH_NODE_TOKENS[node.record_type as keyof typeof GRAPH_NODE_TOKENS] ?? GRAPH_NODE_TOKENS.DEFAULT; const focused = !focusedIds.size || focusedIds.has(node.record_id); const selectedNode = activeNodeId === node.record_id; const favoriteNode = favoriteTargets.some((target) => target.kind === "node" && target.id === node.record_id); return <g key={node.record_id} className={`graph-node${selectedNode ? " graph-node--selected" : ""}${favoriteNode ? " graph-node--favorite" : ""}${focused ? "" : " graph-node--dimmed"}`} tabIndex={0} role="button" aria-label={`${node.label}, ${node.record_id}${favoriteNode ? ", marked" : ""}`} transform={`translate(${x} ${y})`} onMouseEnter={() => showHover({ kind: "node", id: node.record_id })} onMouseLeave={scheduleHideHover} onFocus={() => showHover({ kind: "node", id: node.record_id })} onBlur={scheduleHideHover} onClick={(event) => { event.stopPropagation(); selectNode(node.record_id); }} onContextMenu={(event) => { event.preventDefault(); event.stopPropagation(); selectNode(node.record_id); }} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectNode(node.record_id); } if (event.key === "F10" && event.shiftKey) { event.preventDefault(); selectNode(node.record_id); } }} onPointerDown={(event) => { if (event.button === 0) { event.stopPropagation(); setDragging({ id: node.record_id, original: { x, y } }); } }}><circle className="graph-node-halo" r={selectedNode ? 32 : 0} />{favoriteNode ? <><circle className="graph-node-favorite-ring" r="28" /><text className="graph-node-favorite-mark" y="-30" textAnchor="middle" aria-hidden="true">★</text></> : null}<circle className="graph-node-shape" r="22" fill={token.fill} stroke={selectedNode ? "#fff1bd" : "#d9b46c"} strokeWidth="3" /><g className="graph-node-glyph" aria-hidden="true"><VisualNodeGlyph recordType={node.record_type} /></g><text className="graph-node-label" textAnchor="middle" y="42">{node.label.slice(0, 17)}</text></g>; })}
          </g>
        </svg>
        {hoverTarget && hoverPoint ? <div className="graph-hover-preview" style={{ left: `${(hoverPoint.x / 570) * 100}%`, top: `${(hoverPoint.y / 380) * 100}%` }} role="status" onMouseEnter={() => showHover(hoverTarget)} onMouseLeave={scheduleHideHover} onClick={() => { if (hoverTarget.kind === "node") selectNode(hoverTarget.id); else selectEdge(hoverTarget.id); }}><GraphContextPreview graph={workingGraph} target={hoverTarget} favoriteTargets={favoriteTargets} onToggleFavorite={toggleFavorite} onCenterTarget={centerOnTarget} /></div> : null}
        {favoriteTargets.length ? <section className="graph-favorites-panel" aria-label="Marked graph targets"><div className="graph-favorites-header"><strong>Marked targets</strong><span>{favoriteTargets.length}</span></div><ul>{favoriteTargets.map((target) => <li key={`${target.kind}:${target.id}`}><button type="button" onClick={() => { if (target.kind === "node") selectNode(target.id); else selectEdge(target.id); centerOnTarget(target); }}>{target.kind === "node" ? "◉" : "—"} {targetLabel(target)}</button><button type="button" className="graph-favorite-remove" aria-label={`Remove ${targetLabel(target)} mark`} onClick={() => toggleFavorite(target)}>×</button></li>)}</ul></section> : null}
        <div className="graph-legend" aria-label="Graph legend"><strong>Legend</strong><span><i className="legend-swatch legend-swatch--person" /> Person</span><span><i className="legend-swatch legend-swatch--organization" /> Organisation</span><span><i className="legend-line" /> Detected relationship</span><span><i className="legend-line legend-line--working" /> Working relationship</span></div>
        <details className="graph-semantic"><summary>Semantic evidence list</summary><ul>{graph.nodes.map((item) => <li key={item.record_id}><button type="button" onClick={() => selectNode(item.record_id)}>{nodeGlyph(item.record_type)} {item.label} ({item.record_id})</button></li>)}{workingGraph.edges.map((item) => <li key={item.relationship_id}><button type="button" onClick={() => selectEdge(item.relationship_id)}>{item.relationship_type}: {item.source_record_id} → {item.target_record_id}</button></li>)}</ul></details>
      </div>
      <GraphContextPanel graph={workingGraph} selectedNodeId={activeNodeId} selectedEdgeId={activeEdgeId} onNodeSelect={(id) => selectNode(id || null)} onEdgeSelect={selectEdge} favoriteTargets={favoriteTargets} onToggleFavorite={toggleFavorite} onCenterTarget={centerOnTarget} userAddedEdgeIds={userAddedEdgeIds} onDeleteRelationship={deleteRelationship} />
    </div>
  </section>;
}
