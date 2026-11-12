import type {
  GraphEngineAction,
  GraphEnginePosition,
  GraphEngineSnapshot,
  GraphEngineStatus,
  GraphEngineTarget,
  GraphEngineView,
} from "./examples";
import {
  addGraphEngineRelationship,
  createGraphEngineWorkingState,
  getGraphEngineTargetPosition,
  removeGraphEngineRelationship,
  toggleGraphEngineFavorite,
  type GraphEngineWorkingState,
} from "./workingState";

export type GraphEngineActionSource = "pointer" | "keyboard" | "touch" | "semantic" | "system" | "replay";

export type GraphEngineCameraState = {
  readonly center: GraphEnginePosition;
  readonly zoom: number;
};

export type GraphEngineControllerState = {
  readonly sequence: number;
  readonly selection: GraphEngineTarget | null;
  readonly contextTarget: GraphEngineTarget | null;
  readonly focusedClusterId: string | null;
  readonly view: GraphEngineView;
  readonly hiddenStatuses: readonly GraphEngineStatus[];
  readonly camera: GraphEngineCameraState;
  readonly positions: Readonly<Record<string, GraphEnginePosition>>;
  readonly draftPositions: Readonly<Record<string, GraphEnginePosition>>;
  readonly working: GraphEngineWorkingState;
};

export type GraphEngineControllerEvent = {
  readonly sequence: number;
  readonly source: GraphEngineActionSource;
  readonly action: GraphEngineAction;
};

export type GraphEngineControllerDispatch = {
  readonly state: GraphEngineControllerState;
  readonly event: GraphEngineControllerEvent;
};

const DEFAULT_ZOOM = 1;
const FOCUSED_ZOOM = 1.15;

const clonePosition = (position: GraphEnginePosition): GraphEnginePosition => ({ x: position.x, y: position.y });

const snapshotPositions = (snapshot: GraphEngineSnapshot): Record<string, GraphEnginePosition> =>
  Object.fromEntries(snapshot.nodes.map((node) => [node.id, clonePosition(node.position)]));

const graphCenter = (positions: Readonly<Record<string, GraphEnginePosition>>): GraphEnginePosition => {
  const values = Object.values(positions);
  if (values.length === 0) return { x: 0, y: 0 };
  return {
    x: values.reduce((total, position) => total + position.x, 0) / values.length,
    y: values.reduce((total, position) => total + position.y, 0) / values.length,
  };
};

const fitZoom = (positions: Readonly<Record<string, GraphEnginePosition>>): number => {
  const values = Object.values(positions);
  if (values.length < 2) return DEFAULT_ZOOM;
  const width = Math.max(...values.map((position) => position.x)) - Math.min(...values.map((position) => position.x));
  const height = Math.max(...values.map((position) => position.y)) - Math.min(...values.map((position) => position.y));
  return Math.max(.35, Math.min(1.2, Math.min(640 / Math.max(width, 640), 440 / Math.max(height, 440))));
};

const getVisiblePosition = (
  state: GraphEngineControllerState,
  nodeId: string,
): GraphEnginePosition | null => state.draftPositions[nodeId] ?? state.positions[nodeId] ?? null;

const getCurrentTargetPosition = (
  snapshot: GraphEngineSnapshot,
  state: GraphEngineControllerState,
  target: GraphEngineTarget,
): GraphEnginePosition | null => {
  if (target.kind === "node") return getVisiblePosition(state, target.id);
  const edge = [...snapshot.edges, ...state.working.addedEdges].find((item) => item.id === target.id);
  if (!edge) return null;
  const source = getVisiblePosition(state, edge.sourceId);
  const destination = getVisiblePosition(state, edge.targetId);
  return source && destination ? { x: (source.x + destination.x) / 2, y: (source.y + destination.y) / 2 } : null;
};

const initialState = (snapshot: GraphEngineSnapshot): GraphEngineControllerState => {
  const positions = snapshotPositions(snapshot);
  return {
    sequence: 0,
    selection: null,
    contextTarget: null,
    focusedClusterId: null,
    view: "node-link",
    hiddenStatuses: [],
    camera: { center: graphCenter(positions), zoom: fitZoom(positions) },
    positions,
    draftPositions: {},
    working: createGraphEngineWorkingState(),
  };
};

const isKnownNode = (snapshot: GraphEngineSnapshot, nodeId: string): boolean => snapshot.nodes.some((node) => node.id === nodeId);

const isKnownTarget = (snapshot: GraphEngineSnapshot, state: GraphEngineControllerState, target: GraphEngineTarget): boolean =>
  target.kind === "node"
    ? isKnownNode(snapshot, target.id)
    : [...snapshot.edges, ...state.working.addedEdges].some((edge) => edge.id === target.id);

const replacePosition = (
  positions: Readonly<Record<string, GraphEnginePosition>>,
  nodeId: string,
  position: GraphEnginePosition,
): Readonly<Record<string, GraphEnginePosition>> => ({
  ...positions,
  [nodeId]: clonePosition(position),
});

const removePosition = (
  positions: Readonly<Record<string, GraphEnginePosition>>,
  nodeId: string,
): Readonly<Record<string, GraphEnginePosition>> => {
  const next = { ...positions };
  delete next[nodeId];
  return next;
};

const resetState = (snapshot: GraphEngineSnapshot, sequence: number): GraphEngineControllerState => ({
  ...initialState(snapshot),
  sequence,
});

/**
 * Apply one renderer-neutral command. The reducer owns no DOM, timers or
 * renderer objects, so it can be used by React, the static gallery, a replay
 * harness or a future renderer adapter without creating a second graph truth.
 */
export function reduceGraphEngineController(
  snapshot: GraphEngineSnapshot,
  state: GraphEngineControllerState,
  action: GraphEngineAction,
  sequence = state.sequence + 1,
): GraphEngineControllerState {
  switch (action.kind) {
    case "fit":
      return {
        ...state,
        sequence,
        camera: { center: graphCenter(state.positions), zoom: fitZoom(state.positions) },
      };
    case "reset":
      return resetState(snapshot, sequence);
    case "select":
      if (!isKnownTarget(snapshot, state, action.target)) return { ...state, sequence };
      return { ...state, sequence, selection: action.target };
    case "open-context-menu":
      if (!isKnownTarget(snapshot, state, action.target)) return { ...state, sequence };
      return { ...state, sequence, selection: action.target, contextTarget: action.target };
    case "focus-cluster":
      if (!isKnownTarget(snapshot, state, action.target)) return { ...state, sequence };
      return { ...state, sequence, focusedClusterId: action.clusterId, selection: action.target };
    case "move-preview":
      if (!isKnownNode(snapshot, action.nodeId)) return { ...state, sequence };
      return { ...state, sequence, draftPositions: replacePosition(state.draftPositions, action.nodeId, action.position) };
    case "move-commit":
      if (!isKnownNode(snapshot, action.nodeId)) return { ...state, sequence };
      return {
        ...state,
        sequence,
        positions: replacePosition(state.positions, action.nodeId, action.position),
        draftPositions: removePosition(state.draftPositions, action.nodeId),
      };
    case "move-cancel":
      return { ...state, sequence, draftPositions: removePosition(state.draftPositions, action.nodeId) };
    case "set-view":
      return { ...state, sequence, view: action.view };
    case "filter-status": {
      const hidden = new Set(state.hiddenStatuses);
      if (action.visible) hidden.delete(action.status);
      else hidden.add(action.status);
      return { ...state, sequence, hiddenStatuses: [...hidden].sort((left, right) => left.localeCompare(right)) };
    }
    case "add-relationship":
      return {
        ...state,
        sequence,
        working: addGraphEngineRelationship(snapshot, state.working, action.relationship),
      };
    case "delete-relationship": {
      const working = removeGraphEngineRelationship(state.working, action.edgeId);
      return {
        ...state,
        sequence,
        working: {
          ...working,
          favorites: working.favorites.filter((target) => target.kind !== "edge" || target.id !== action.edgeId),
        },
      };
    }
    case "toggle-favorite":
      if (!isKnownTarget(snapshot, state, action.target)) return { ...state, sequence };
      return { ...state, sequence, working: toggleGraphEngineFavorite(state.working, action.target) };
    case "center-target": {
      const center = getCurrentTargetPosition(snapshot, state, action.target);
      return center
        ? { ...state, sequence, selection: action.target, camera: { center, zoom: Math.max(state.camera.zoom, FOCUSED_ZOOM) } }
        : { ...state, sequence };
    }
  }
};

export function createGraphEngineController(snapshot: GraphEngineSnapshot) {
  let state = initialState(snapshot);
  const eventLog: GraphEngineControllerEvent[] = [];

  return {
    getState: (): GraphEngineControllerState => state,
    getEvents: (): readonly GraphEngineControllerEvent[] => eventLog,
    dispatch: (action: GraphEngineAction, source: GraphEngineActionSource = "system"): GraphEngineControllerDispatch => {
      const sequence = state.sequence + 1;
      state = reduceGraphEngineController(snapshot, state, action, sequence);
      const event = { sequence, source, action } satisfies GraphEngineControllerEvent;
      eventLog.push(event);
      return { state, event };
    },
  };
}

export function replayGraphEngineActions(
  snapshot: GraphEngineSnapshot,
  actions: readonly GraphEngineAction[],
): GraphEngineControllerState {
  return actions.reduce(
    (state, action, index) => reduceGraphEngineController(snapshot, state, action, index + 1),
    initialState(snapshot),
  );
}

/** Exposed for adapter conformance tests that need to compare target geometry. */
export function getGraphEngineControllerTargetPosition(
  snapshot: GraphEngineSnapshot,
  state: GraphEngineControllerState,
  target: GraphEngineTarget,
): GraphEnginePosition | null {
  return getCurrentTargetPosition(snapshot, state, target) ?? getGraphEngineTargetPosition(snapshot, state.working, target);
}
