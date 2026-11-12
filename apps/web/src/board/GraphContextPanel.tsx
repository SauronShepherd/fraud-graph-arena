import type { Graph, GraphEdge, GraphNode } from "../api/contracts";

export type GraphTarget = { kind: "node" | "edge"; id: string };

export interface GraphContextPanelProps {
  graph: Graph;
  selectedNodeId: string | null;
  selectedEdgeId: string | null;
  onNodeSelect(id: string | null): void;
  onEdgeSelect(id: string | null): void;
  favoriteTargets?: readonly GraphTarget[];
  onToggleFavorite?(target: GraphTarget): void;
  onCenterTarget?(target: GraphTarget): void;
  userAddedEdgeIds?: ReadonlySet<string>;
  onDeleteRelationship?(id: string): void;
}

function glyphFor(recordType: string): string {
  if (recordType.includes("PERSON")) return "◉";
  if (recordType.includes("ORGANIZATION")) return "▦";
  if (recordType.includes("DEVICE")) return "⌁";
  if (recordType.includes("ADDRESS")) return "⌂";
  if (recordType.includes("ACCOUNT")) return "◈";
  return "○";
}

function otherEnd(edge: GraphEdge, nodeId: string): string {
  return edge.source_record_id === nodeId ? edge.target_record_id : edge.source_record_id;
}

function nodeLabel(graph: Graph, id: string): string {
  return graph.nodes.find((node) => node.record_id === id)?.label ?? id;
}

function targetIsFavorite(target: GraphTarget, favoriteTargets: readonly GraphTarget[]): boolean {
  return favoriteTargets.some((item) => item.kind === target.kind && item.id === target.id);
}

function IconAction({ icon, label, pressed, danger = false, onClick }: { icon: string; label: string; pressed?: boolean; danger?: boolean; onClick(): void }) {
  return <button type="button" className={`graph-icon-action${danger ? " graph-danger-action" : ""}`} aria-label={label} title={label} aria-pressed={pressed} data-tooltip={label} onMouseDown={(event) => event.stopPropagation()} onPointerDown={(event) => event.stopPropagation()} onClick={(event) => { event.stopPropagation(); onClick(); }}><span className="graph-action-glyph" aria-hidden="true">{icon}</span><span className="sr-only">{label}</span></button>;
}

function FavoriteActions({ target, favoriteTargets, onToggleFavorite, onCenterTarget }: { target: GraphTarget; favoriteTargets: readonly GraphTarget[]; onToggleFavorite?: (target: GraphTarget) => void; onCenterTarget?: (target: GraphTarget) => void }) {
  const favorite = targetIsFavorite(target, favoriteTargets);
  return <div className="graph-context-actions">
    {onToggleFavorite ? <IconAction icon={favorite ? "−" : "+"} label={favorite ? "Remove from highlights" : "Add to highlights"} pressed={favorite} onClick={() => onToggleFavorite(target)} /> : null}
    {onCenterTarget ? <IconAction icon="⌖" label="Center on graph" onClick={() => onCenterTarget(target)} /> : null}
  </div>;
}

function ConnectionList({ graph, node, onEdgeSelect }: { graph: Graph; node: GraphNode; onEdgeSelect(id: string): void }) {
  const relationships = graph.edges.filter((edge) => edge.source_record_id === node.record_id || edge.target_record_id === node.record_id);
  return <section className="graph-context-section" aria-labelledby="graph-connections-title">
    <div className="graph-context-section-heading"><h3 id="graph-connections-title">Connected relationships</h3><span>{relationships.length}</span></div>
    {relationships.length ? <ul className="graph-connection-list">{relationships.map((edge) => <li key={edge.relationship_id}>
      <button type="button" onClick={() => onEdgeSelect(edge.relationship_id)}>
        <span className="graph-connection-family">{edge.relationship_family.replaceAll("_", " ")}</span>
        <strong>{edge.relationship_type}</strong>
        <span>{nodeLabel(graph, otherEnd(edge, node.record_id))}</span>
      </button>
      <small>{edge.directed ? "→" : "↔"}</small>
    </li>)}</ul> : <p className="graph-context-muted">No visible relationships are attached to this node.</p>}
  </section>;
}

function NodePanel({ graph, node, onNodeSelect, onEdgeSelect, favoriteTargets, onToggleFavorite, onCenterTarget }: { graph: Graph; node: GraphNode; onNodeSelect(id: string | null): void; onEdgeSelect(id: string): void; favoriteTargets: readonly GraphTarget[]; onToggleFavorite?: (target: GraphTarget) => void; onCenterTarget?: (target: GraphTarget) => void }) {
  const target: GraphTarget = { kind: "node", id: node.record_id };
  return <>
    <div className="graph-context-kicker">Context menu · selected node</div>
    <div className="graph-entity-hero"><span className="graph-entity-glyph" aria-hidden="true">{glyphFor(node.record_type)}</span><div><h2>{node.label}</h2><span className="graph-status-pill">Published projection</span></div></div>
    <p className="graph-context-subtitle">{node.record_type} · {node.record_subtype || "record"}</p>
    <dl className="graph-context-facts"><div><dt>Stable ID</dt><dd>{node.record_id}</dd></div><div><dt>Source system</dt><dd>{node.source_system_id}</dd></div><div><dt>Provenance</dt><dd>{node.provenance_ref}</dd></div></dl>
    <section className="graph-context-section"><h3>Safe summary</h3><p>{node.safe_summary || "No player-safe summary supplied."}</p></section>
    <FavoriteActions target={target} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} />
    <ConnectionList graph={graph} node={node} onEdgeSelect={onEdgeSelect} />
    <div className="graph-context-actions"><button type="button" onClick={() => onNodeSelect(node.record_id)}>Keep node selected</button><button type="button" onClick={() => onNodeSelect(null)}>Clear selection</button></div>
  </>;
}

function EdgePanel({ graph, edge, onNodeSelect, onEdgeSelect, favoriteTargets, onToggleFavorite, onCenterTarget, isUserAdded, onDeleteRelationship }: { graph: Graph; edge: GraphEdge; onNodeSelect(id: string): void; onEdgeSelect(id: string | null): void; favoriteTargets: readonly GraphTarget[]; onToggleFavorite?: (target: GraphTarget) => void; onCenterTarget?: (target: GraphTarget) => void; isUserAdded: boolean; onDeleteRelationship?: (id: string) => void }) {
  const target: GraphTarget = { kind: "edge", id: edge.relationship_id };
  return <>
    <div className="graph-context-kicker">Context menu · {isUserAdded ? "working relationship" : "selected relationship"}</div>
    <h2 className="graph-edge-title">{edge.relationship_type}</h2>
    <p className="graph-context-subtitle">{edge.relationship_family.replaceAll("_", " ")} · {edge.directed ? "directed relationship" : "undirected relationship"}</p>
    {isUserAdded ? <p className="graph-working-note">Dashed working relationship · removable local investigation state</p> : null}
    <div className="graph-route"><button type="button" onClick={() => onNodeSelect(edge.source_record_id)}><strong>{nodeLabel(graph, edge.source_record_id)}</strong><small>source</small></button><span aria-hidden="true">→</span><button type="button" onClick={() => onNodeSelect(edge.target_record_id)}><strong>{nodeLabel(graph, edge.target_record_id)}</strong><small>target</small></button></div>
    <dl className="graph-context-facts"><div><dt>Stable ID</dt><dd>{edge.relationship_id}</dd></div><div><dt>Event time</dt><dd>{edge.event_time || "Not supplied"}</dd></div><div><dt>Provenance</dt><dd>{edge.provenance || "Not supplied"}</dd></div></dl>
    <section className="graph-context-section"><h3>Safe relationship meaning</h3><p>{edge.player_safe_summary || "No player-safe relationship summary supplied."}</p></section>
    <FavoriteActions target={target} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} />
    {isUserAdded && onDeleteRelationship ? <div className="graph-context-actions"><IconAction icon="×" label="Delete working relationship" danger onClick={() => onDeleteRelationship(edge.relationship_id)} /></div> : null}
    <div className="graph-context-actions"><button type="button" onClick={() => onEdgeSelect(edge.relationship_id)}>Keep relationship selected</button><button type="button" onClick={() => onEdgeSelect(null)}>Clear selection</button></div>
  </>;
}

export function GraphContextPreview({ graph, target, favoriteTargets = [], onToggleFavorite, onCenterTarget }: { graph: Graph; target: GraphTarget; favoriteTargets?: readonly GraphTarget[]; onToggleFavorite?: (target: GraphTarget) => void; onCenterTarget?: (target: GraphTarget) => void }) {
  const node = target.kind === "node" ? graph.nodes.find((item) => item.record_id === target.id) : undefined;
  const edge = target.kind === "edge" ? graph.edges.find((item) => item.relationship_id === target.id) : undefined;
  if (node) return <div className="graph-hover-preview-content"><span className="graph-context-kicker">Hover preview · node</span><strong>{glyphFor(node.record_type)} {node.label}</strong><span>{node.record_type} · {node.record_id}</span><small>{node.safe_summary || "No player-safe summary supplied."}</small><FavoriteActions target={{ kind: "node", id: node.record_id }} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} /><em>Click the card to open full context</em></div>;
  if (edge) return <div className="graph-hover-preview-content"><span className="graph-context-kicker">Hover preview · relationship</span><strong>{edge.relationship_type}</strong><span>{nodeLabel(graph, edge.source_record_id)} → {nodeLabel(graph, edge.target_record_id)}</span><small>{edge.relationship_family.replaceAll("_", " ")} · {edge.relationship_id}</small><FavoriteActions target={{ kind: "edge", id: edge.relationship_id }} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} /><em>Click the card to open full context</em></div>;
  return null;
}

export function GraphContextPanel({ graph, selectedNodeId, selectedEdgeId, onNodeSelect, onEdgeSelect, favoriteTargets = [], onToggleFavorite, onCenterTarget, userAddedEdgeIds = new Set<string>(), onDeleteRelationship }: GraphContextPanelProps) {
  const node = selectedNodeId ? graph.nodes.find((item) => item.record_id === selectedNodeId) : undefined;
  const edge = selectedEdgeId ? graph.edges.find((item) => item.relationship_id === selectedEdgeId) : undefined;
  return <aside className="graph-context-panel graph-context-panel--visible" aria-live="polite" aria-label="Graph context panel">
    {node ? <NodePanel graph={graph} node={node} onNodeSelect={onNodeSelect} onEdgeSelect={(id) => onEdgeSelect(id)} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} /> : edge ? <EdgePanel graph={graph} edge={edge} onNodeSelect={(id) => onNodeSelect(id)} onEdgeSelect={onEdgeSelect} favoriteTargets={favoriteTargets} onToggleFavorite={onToggleFavorite} onCenterTarget={onCenterTarget} isUserAdded={userAddedEdgeIds.has(edge.relationship_id)} onDeleteRelationship={onDeleteRelationship} /> : <div className="graph-context-empty"><span className="graph-context-empty-mark" aria-hidden="true">⌘</span><h2>Context dossier</h2><p>Select a node or relationship to inspect its player-safe identity, connections and provenance.</p><p>Hover opens a contextual preview without changing the active selection.</p><div className="graph-context-empty-stats"><span><strong>{graph.node_count}</strong> entities</span><span><strong>{graph.edge_count}</strong> relationships</span></div></div>}
  </aside>;
}
