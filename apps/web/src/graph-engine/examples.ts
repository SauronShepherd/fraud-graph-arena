/**
 * Renderer-neutral examples for the FGA graph engine.
 *
 * These examples are executable contract fixtures, not a renderer and not a
 * source of investigative truth. They describe safe presentation snapshots,
 * user intents and expected interaction outcomes so every renderer can be
 * exercised with the same scenarios.
 */

export const GRAPH_ENGINE_STATUSES = [
  "UNINVESTIGATED",
  "CANDIDATE",
  "INVESTIGATED",
  "FRAUD_CONFIRMED",
  "DISCARDED",
] as const;

export type GraphEngineStatus = (typeof GRAPH_ENGINE_STATUSES)[number];
export type GraphEngineView = "node-link" | "matrix" | "path" | "semantic-list";
export type GraphEngineTarget = { kind: "node" | "edge"; id: string };
export type GraphEnginePosition = { x: number; y: number };

export type GraphEngineNode = {
  readonly id: string;
  readonly recordType: string;
  readonly label: string;
  readonly status: GraphEngineStatus;
  readonly position: GraphEnginePosition;
  readonly clusterId: string;
  readonly icon: string;
};

export type GraphEngineEdge = {
  readonly id: string;
  readonly sourceId: string;
  readonly targetId: string;
  readonly relationshipFamily: string;
  readonly relationshipType: string;
  readonly directed: boolean;
  readonly confidence: "low" | "medium" | "high" | "documented";
  /** Presentation origin. Detected relationships are immutable; working relationships are removable. */
  readonly origin?: "detected" | "investigator-added";
};

export type GraphEngineSnapshot = {
  readonly version: string;
  readonly nodes: readonly GraphEngineNode[];
  readonly edges: readonly GraphEngineEdge[];
};

export type GraphEngineAction =
  | { readonly kind: "fit" }
  | { readonly kind: "reset" }
  | { readonly kind: "select"; readonly target: GraphEngineTarget; readonly via: "pointer" | "keyboard" | "semantic-list" }
  | { readonly kind: "open-context-menu"; readonly target: GraphEngineTarget; readonly via: "pointer" | "keyboard" }
  | { readonly kind: "focus-cluster"; readonly clusterId: string; readonly target: GraphEngineTarget }
  | { readonly kind: "move-preview"; readonly nodeId: string; readonly position: GraphEnginePosition }
  | { readonly kind: "move-commit"; readonly nodeId: string; readonly position: GraphEnginePosition }
  | { readonly kind: "move-cancel"; readonly nodeId: string }
  | { readonly kind: "set-view"; readonly view: GraphEngineView }
  | { readonly kind: "filter-status"; readonly status: GraphEngineStatus; readonly visible: boolean }
  | { readonly kind: "add-relationship"; readonly relationship: Omit<GraphEngineEdge, "origin"> }
  | { readonly kind: "delete-relationship"; readonly edgeId: string }
  | { readonly kind: "toggle-favorite"; readonly target: GraphEngineTarget }
  | { readonly kind: "center-target"; readonly target: GraphEngineTarget };

export type GraphEngineExample = {
  readonly id: string;
  readonly title: string;
  readonly purpose: string;
  readonly description: string;
  readonly recommendedViews: readonly GraphEngineView[];
  readonly snapshot: GraphEngineSnapshot;
  readonly actions: readonly GraphEngineAction[];
  readonly expectedOutcomes: readonly string[];
};

const node = (
  id: string,
  recordType: string,
  label: string,
  status: GraphEngineStatus,
  x: number,
  y: number,
  clusterId: string,
  icon: string,
): GraphEngineNode => ({ id, recordType, label, status, position: { x, y }, clusterId, icon });

const edge = (
  id: string,
  sourceId: string,
  targetId: string,
  relationshipFamily: string,
  relationshipType: string,
  confidence: GraphEngineEdge["confidence"],
): GraphEngineEdge => ({ id, sourceId, targetId, relationshipFamily, relationshipType, directed: true, confidence });

const select = (id: string, kind: GraphEngineTarget["kind"], via: Extract<GraphEngineAction, { kind: "select" }>["via"]): GraphEngineAction => ({ kind: "select", target: { kind, id }, via });
const context = (id: string, kind: GraphEngineTarget["kind"], via: Extract<GraphEngineAction, { kind: "open-context-menu" }>["via"]): GraphEngineAction => ({ kind: "open-context-menu", target: { kind, id }, via });

const emptyAcademy: GraphEngineExample = {
  id: "empty-academy-board",
  title: "The empty Academy board",
  purpose: "Prove that an empty projection is a valid, accessible graph state.",
  description: "The engine renders an honest empty state without inventing nodes, edges or investigative meaning.",
  recommendedViews: ["node-link", "semantic-list"],
  snapshot: { version: "ACADEMY_001:v1", nodes: [], edges: [] },
  actions: [{ kind: "fit" }, { kind: "set-view", view: "semantic-list" }, { kind: "reset" }],
  expectedOutcomes: ["The empty state is announced.", "Fit and reset remain safe no-ops.", "No renderer receives fabricated graph objects."],
};

const sharedDevice: GraphEngineExample = {
  id: "shared-device-investigation",
  title: "Shared device cluster",
  purpose: "Exercise node context, edge context, cluster focus and committed movement.",
  description: "A compact, safe graph where a shared device links people, an account and an organisation.",
  recommendedViews: ["node-link", "matrix", "semantic-list"],
  snapshot: {
    version: "EXAMPLE_SHARED_DEVICE:v1",
    nodes: [
      node("EX-N-0001", "PERSON_RECORD", "Marta Silva", "INVESTIGATED", 180, 250, "harbor", "◉"),
      node("EX-N-0002", "PERSON_RECORD", "L. Costa", "UNINVESTIGATED", 180, 440, "harbor", "◉"),
      node("EX-N-0003", "DEVICE_RECORD", "Shared device 42", "CANDIDATE", 430, 330, "northstar", "⌁"),
      node("EX-N-0004", "ACCOUNT_RECORD", "Harbor account", "INVESTIGATED", 690, 230, "harbor", "◈"),
      node("EX-N-0005", "ORGANIZATION_RECORD", "Northstar Cashbox", "UNINVESTIGATED", 700, 450, "northstar", "▦"),
      node("EX-N-0006", "ADDRESS_RECORD", "Parcel locker 7", "DISCARDED", 940, 330, "northstar", "⌂"),
    ],
    edges: [
      edge("EX-E-0001", "EX-N-0001", "EX-N-0003", "DEVICE_OBSERVATION", "USES_DEVICE", "medium"),
      edge("EX-E-0002", "EX-N-0002", "EX-N-0003", "DEVICE_OBSERVATION", "USES_DEVICE", "low"),
      edge("EX-E-0003", "EX-N-0003", "EX-N-0004", "SHARED_ATTRIBUTE", "LINKED_TO", "high"),
      edge("EX-E-0004", "EX-N-0004", "EX-N-0005", "TRANSACTIONAL", "TRANSFERS_TO", "documented"),
      edge("EX-E-0005", "EX-N-0005", "EX-N-0006", "DIRECT_SOURCE", "USES_ADDRESS", "documented"),
    ],
  },
  actions: [
    select("EX-N-0003", "node", "pointer"),
    context("EX-N-0003", "node", "keyboard"),
    { kind: "focus-cluster", clusterId: "northstar", target: { kind: "node", id: "EX-N-0003" } },
    context("EX-E-0003", "edge", "pointer"),
    { kind: "set-view", view: "matrix" },
    { kind: "move-preview", nodeId: "EX-N-0003", position: { x: 470, y: 350 } },
    { kind: "move-commit", nodeId: "EX-N-0003", position: { x: 470, y: 350 } },
    { kind: "reset" },
  ],
  expectedOutcomes: ["Node and edge menus retain stable IDs.", "Cluster focus changes visibility, not source data.", "Only the movement commit enters replay history.", "Matrix and node-link views share selection but keep independent cameras."],
};

const temporalPath: GraphEngineExample = {
  id: "temporal-path-tracing",
  title: "Temporal path tracing",
  purpose: "Exercise directional relationships, path context and coordinated views.",
  description: "A short directed chain for testing source/target inspection without claiming that a path proves culpability.",
  recommendedViews: ["node-link", "path", "matrix", "semantic-list"],
  snapshot: {
    version: "EXAMPLE_TEMPORAL_PATH:v1",
    nodes: [
      node("EX-N-0101", "PERSON_RECORD", "A. Vega", "CANDIDATE", 120, 290, "orbit", "◉"),
      node("EX-N-0102", "ACCOUNT_RECORD", "Orbit account", "INVESTIGATED", 340, 290, "orbit", "◈"),
      node("EX-N-0103", "ORGANIZATION_RECORD", "Vega Payments", "UNINVESTIGATED", 560, 290, "orbit", "▦"),
      node("EX-N-0104", "ACCOUNT_RECORD", "Eastline settlement", "UNINVESTIGATED", 780, 290, "orbit", "◈"),
      node("EX-N-0105", "ADDRESS_RECORD", "Dock address", "DISCARDED", 1000, 290, "orbit", "⌂"),
    ],
    edges: [
      edge("EX-E-0101", "EX-N-0101", "EX-N-0102", "DIRECT_SOURCE", "AUTHORISED_BY", "documented"),
      edge("EX-E-0102", "EX-N-0102", "EX-N-0103", "TRANSACTIONAL", "PAYS", "medium"),
      edge("EX-E-0103", "EX-N-0103", "EX-N-0104", "TRANSACTIONAL", "SETTLES_WITH", "high"),
      edge("EX-E-0104", "EX-N-0104", "EX-N-0105", "DIRECT_SOURCE", "USES_ADDRESS", "documented"),
    ],
  },
  actions: [
    select("EX-E-0102", "edge", "pointer"),
    context("EX-E-0102", "edge", "keyboard"),
    { kind: "set-view", view: "path" },
    select("EX-N-0103", "node", "semantic-list"),
    { kind: "set-view", view: "matrix" },
    { kind: "filter-status", status: "DISCARDED", visible: false },
    { kind: "fit" },
  ],
  expectedOutcomes: ["The edge remains the focus target after its menu closes.", "Path view explains sequence without changing graph truth.", "Filtering changes the projection while preserving stable IDs."],
};

const keyboardJourney: GraphEngineExample = {
  id: "keyboard-and-semantic-journey",
  title: "Keyboard and semantic journey",
  purpose: "Exercise parity between pointer, keyboard and semantic-list entry points.",
  description: "A small graph whose interaction sequence is intentionally driven through non-pointer paths.",
  recommendedViews: ["node-link", "semantic-list"],
  snapshot: {
    version: "EXAMPLE_KEYBOARD:v1",
    nodes: [
      node("EX-N-0201", "PERSON_RECORD", "R. Garcia", "UNINVESTIGATED", 200, 250, "harbor", "◉"),
      node("EX-N-0202", "DEVICE_RECORD", "Pine VPN", "CANDIDATE", 500, 250, "harbor", "⌁"),
      node("EX-N-0203", "ORGANIZATION_RECORD", "Eastline Bank", "INVESTIGATED", 800, 250, "harbor", "▦"),
    ],
    edges: [
      edge("EX-E-0201", "EX-N-0201", "EX-N-0202", "DEVICE_OBSERVATION", "USES_DEVICE", "medium"),
      edge("EX-E-0202", "EX-N-0202", "EX-N-0203", "DIRECT_SOURCE", "OBSERVED_WITH", "documented"),
    ],
  },
  actions: [
    select("EX-N-0201", "node", "keyboard"),
    context("EX-N-0201", "node", "keyboard"),
    select("EX-E-0201", "edge", "semantic-list"),
    context("EX-E-0201", "edge", "keyboard"),
    { kind: "move-preview", nodeId: "EX-N-0202", position: { x: 530, y: 280 } },
    { kind: "move-cancel", nodeId: "EX-N-0202" },
    { kind: "set-view", view: "semantic-list" },
  ],
  expectedOutcomes: ["Keyboard and semantic-list selection produce the same stable target.", "Shift+F10-style menu invocation uses the same command path as pointer invocation.", "Cancelled movement does not enter replay history."],
};

const denseRingSpecs = [
  { start: 3010, count: 10, centerX: 305, centerY: 355, radius: 155, status: "INVESTIGATED" as const, clusterId: "green-cluster", icon: "◉", hub: "EX-N-3000", label: "Kennel witness" },
  { start: 3020, count: 10, centerX: 560, centerY: 145, radius: 145, status: "FRAUD_CONFIRMED" as const, clusterId: "red-cluster", icon: "◉", hub: "EX-N-3001", label: "Claim contact" },
  { start: 3030, count: 10, centerX: 855, centerY: 345, radius: 155, status: "UNINVESTIGATED" as const, clusterId: "blue-cluster", icon: "◉", hub: "EX-N-3002", label: "Bank customer" },
] as const;

const denseClusterNodes: readonly GraphEngineNode[] = [
  node("EX-N-3000", "ORGANIZATION_RECORD", "ORG-221 · Golden Kennel Ltd", "INVESTIGATED", 305, 355, "green-cluster", "▣"),
  node("EX-N-3001", "CLAIM_CLUSTER", "RING-07 · Claim cluster", "FRAUD_CONFIRMED", 560, 145, "red-cluster", "✦"),
  node("EX-N-3002", "BANK_RECORD", "BANK-91 · Atlantic Mutual", "UNINVESTIGATED", 855, 345, "blue-cluster", "▥"),
  node("EX-N-3003", "PERSON_RECORD", "R-1042 · J. GARCIA", "UNINVESTIGATED", 560, 355, "case-center", "◉"),
  ...denseRingSpecs.flatMap((spec) => Array.from({ length: spec.count }, (_, index) => {
    const angle = (-Math.PI / 2) + ((Math.PI * 2) / spec.count) * index;
    return node(`EX-N-${String(spec.start + index).padStart(4, "0")}`, "PERSON_RECORD", `${spec.label} ${index + 1}`, spec.status, spec.centerX + Math.cos(angle) * spec.radius, spec.centerY + Math.sin(angle) * spec.radius, spec.clusterId, spec.icon);
  })),
];

const denseClusterEdges: readonly GraphEngineEdge[] = [
  edge("EX-E-3000", "EX-N-3003", "EX-N-3001", "SHARED_ATTRIBUTE", "LINKED_TO", "high"),
  edge("EX-E-3001", "EX-N-3003", "EX-N-3000", "DEVICE_OBSERVATION", "OBSERVED_ON", "medium"),
  edge("EX-E-3002", "EX-N-3003", "EX-N-3002", "TRANSACTIONAL", "TRANSFERS_TO", "high"),
  edge("EX-E-3003", "EX-N-3000", "EX-N-3003", "SHARED_ATTRIBUTE", "LINKED_TO", "high"),
  edge("EX-E-3004", "EX-N-3001", "EX-N-3003", "TRANSACTIONAL", "TRANSFERS_TO", "medium"),
  edge("EX-E-3005", "EX-N-3002", "EX-N-3003", "DIRECT_SOURCE", "REFERENCES", "documented"),
  ...denseRingSpecs.flatMap((spec, clusterIndex) => Array.from({ length: spec.count }, (_, index) => {
    const id = `EX-N-${String(spec.start + index).padStart(4, "0")}`;
    const nextId = `EX-N-${String(spec.start + ((index + 1) % spec.count)).padStart(4, "0")}`;
    const edgeId = `EX-E-${String(3010 + clusterIndex * 20 + index * 2).padStart(4, "0")}`;
    return [
      edge(edgeId, spec.hub, id, clusterIndex === 1 ? "TRANSACTIONAL" : "SHARED_ATTRIBUTE", clusterIndex === 1 ? "TRANSFERS_TO" : "LINKED_TO", index % 3 === 0 ? "high" : "medium"),
      edge(`${edgeId}-R`, id, nextId, clusterIndex === 0 ? "DEVICE_OBSERVATION" : "SHARED_ATTRIBUTE", "RELATED_TO", "low"),
    ];
  }).flat()),
];

const denseCluster: GraphEngineExample = {
  id: "dense-cluster-progressive-disclosure",
  title: "Dense cluster and progressive disclosure",
  purpose: "Exercise minimap, filtering, bounded rendering and gradual detail reveal.",
  description: "A deterministic three-cluster scene designed to expose hairball prevention, progressive disclosure and tactile layout behaviour.",
  recommendedViews: ["node-link", "matrix", "semantic-list"],
  snapshot: {
    version: "EXAMPLE_DENSE_CLUSTER:v1",
    nodes: denseClusterNodes,
    edges: denseClusterEdges,
  },
  actions: [
    { kind: "set-view", view: "matrix" },
    { kind: "filter-status", status: "UNINVESTIGATED", visible: false },
    { kind: "fit" },
    select("EX-N-3003", "node", "pointer"),
    context("EX-N-3003", "node", "keyboard"),
    { kind: "set-view", view: "semantic-list" },
    { kind: "reset" },
  ],
  expectedOutcomes: ["The visible subset can be bounded without mutating the source snapshot.", "The minimap is an optional overview, not a second source of truth.", "The semantic list exposes every visible target even when the node-link view is dense."],
};

const examples: readonly GraphEngineExample[] = [emptyAcademy, sharedDevice, temporalPath, keyboardJourney, denseCluster];

function nodeIds(example: GraphEngineExample): ReadonlySet<string> {
  return new Set(example.snapshot.nodes.map((item) => item.id));
}

function edgeIds(example: GraphEngineExample): ReadonlySet<string> {
  return new Set(example.snapshot.edges.map((item) => item.id));
}

export function validateGraphEngineExample(example: GraphEngineExample): void {
  const ids = nodeIds(example);
  const relationships = edgeIds(example);
  if (!example.id || !example.snapshot.version) throw new Error("Graph example requires an id and snapshot version");
  if (new Set(example.snapshot.nodes.map((item) => item.id)).size !== example.snapshot.nodes.length) throw new Error(`Duplicate node ID in ${example.id}`);
  if (new Set(example.snapshot.edges.map((item) => item.id)).size !== example.snapshot.edges.length) throw new Error(`Duplicate edge ID in ${example.id}`);
  for (const relationship of example.snapshot.edges) {
    if (!ids.has(relationship.sourceId) || !ids.has(relationship.targetId)) throw new Error(`Dangling edge ${relationship.id} in ${example.id}`);
  }
  for (const action of example.actions) {
    if (action.kind === "select" || action.kind === "open-context-menu" || action.kind === "focus-cluster") {
      const targetIds = action.target.kind === "node" ? ids : relationships;
      if (!targetIds.has(action.target.id)) throw new Error(`Unknown ${action.target.kind} target ${action.target.id} in ${example.id}`);
    }
    if ((action.kind === "move-preview" || action.kind === "move-commit" || action.kind === "move-cancel") && !ids.has(action.nodeId)) {
      throw new Error(`Unknown movement target ${action.nodeId} in ${example.id}`);
    }
    if (action.kind === "focus-cluster" && !example.snapshot.nodes.some((item) => item.clusterId === action.clusterId)) {
      throw new Error(`Unknown cluster ${action.clusterId} in ${example.id}`);
    }
  }
}

export function createGraphEngineExampleLibrary(): readonly GraphEngineExample[] {
  examples.forEach(validateGraphEngineExample);
  return examples;
}

export function getGraphEngineExample(id: string): GraphEngineExample {
  const example = examples.find((item) => item.id === id);
  if (!example) throw new Error(`Unknown graph engine example: ${id}`);
  validateGraphEngineExample(example);
  return example;
}

export function graphEngineExampleIds(): readonly string[] {
  return examples.map((item) => item.id);
}

export function serializeGraphEngineExample(example: GraphEngineExample): string {
  validateGraphEngineExample(example);
  return JSON.stringify(example, null, 2);
}

