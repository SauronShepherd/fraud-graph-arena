import type {
  GraphEngineEdge,
  GraphEnginePosition,
  GraphEngineSnapshot,
  GraphEngineTarget,
} from "./examples";

export type GraphEngineWorkingEdge = GraphEngineEdge & { readonly origin: "investigator-added" };

export type GraphEngineWorkingState = {
  readonly addedEdges: readonly GraphEngineWorkingEdge[];
  readonly favorites: readonly GraphEngineTarget[];
};

export function createGraphEngineWorkingState(): GraphEngineWorkingState {
  return { addedEdges: [], favorites: [] };
}

export function addGraphEngineRelationship(
  snapshot: GraphEngineSnapshot,
  state: GraphEngineWorkingState,
  relationship: Omit<GraphEngineWorkingEdge, "origin">,
): GraphEngineWorkingState {
  const nodeIds = new Set(snapshot.nodes.map((node) => node.id));
  if (!nodeIds.has(relationship.sourceId) || !nodeIds.has(relationship.targetId)) {
    throw new Error("Investigator-added relationship endpoints must exist in the snapshot");
  }
  if ([...snapshot.edges, ...state.addedEdges].some((edge) => edge.id === relationship.id)) {
    throw new Error(`Relationship ID already exists: ${relationship.id}`);
  }
  return {
    ...state,
    addedEdges: [...state.addedEdges, { ...relationship, origin: "investigator-added" }],
  };
}

export function removeGraphEngineRelationship(state: GraphEngineWorkingState, edgeId: string): GraphEngineWorkingState {
  return { ...state, addedEdges: state.addedEdges.filter((edge) => edge.id !== edgeId) };
}

export function toggleGraphEngineFavorite(state: GraphEngineWorkingState, target: GraphEngineTarget): GraphEngineWorkingState {
  const exists = state.favorites.some((item) => item.kind === target.kind && item.id === target.id);
  return {
    ...state,
    favorites: exists
      ? state.favorites.filter((item) => item.kind !== target.kind || item.id !== target.id)
      : [...state.favorites, target],
  };
}

export function isGraphEngineFavorite(state: GraphEngineWorkingState, target: GraphEngineTarget): boolean {
  return state.favorites.some((item) => item.kind === target.kind && item.id === target.id);
}

export function getGraphEngineTargetPosition(
  snapshot: GraphEngineSnapshot,
  state: GraphEngineWorkingState,
  target: GraphEngineTarget,
): GraphEnginePosition | null {
  if (target.kind === "node") return snapshot.nodes.find((node) => node.id === target.id)?.position ?? null;
  const edge = [...snapshot.edges, ...state.addedEdges].find((item) => item.id === target.id);
  if (!edge) return null;
  const source = snapshot.nodes.find((node) => node.id === edge.sourceId);
  const destination = snapshot.nodes.find((node) => node.id === edge.targetId);
  return source && destination
    ? { x: (source.position.x + destination.position.x) / 2, y: (source.position.y + destination.position.y) / 2 }
    : null;
}
