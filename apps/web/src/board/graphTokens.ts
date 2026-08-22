export const GRAPH_NODE_TOKENS = {
  PERSON_RECORD: { fill: "#8c5a45", label: "Person record" },
  ORGANIZATION_RECORD: { fill: "#496b68", label: "Organization record" },
  DEFAULT: { fill: "#6f6876", label: "Published record" },
} as const;

export const GRAPH_RELATIONSHIP_TOKENS = {
  DIRECT_SOURCE: { stroke: "#d9b46c", label: "Direct source relationship" },
  DEFAULT: { stroke: "#b6a384", label: "Published relationship" },
} as const;
