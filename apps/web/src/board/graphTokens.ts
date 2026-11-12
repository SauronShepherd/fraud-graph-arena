export const GRAPH_NODE_TOKENS = {
  PERSON_RECORD: { fill: "#255a82", label: "Person record" },
  ORGANIZATION_RECORD: { fill: "#5d7f21", label: "Organization record" },
  DEVICE_RECORD: { fill: "#9b671f", label: "Device record" },
  ACCOUNT_RECORD: { fill: "#315e63", label: "Account record" },
  BANK_RECORD: { fill: "#255a82", label: "Bank record" },
  DEFAULT: { fill: "#595449", label: "Published record" },
} as const;

export const GRAPH_RELATIONSHIP_TOKENS = {
  DIRECT_SOURCE: { stroke: "#d9b46c", label: "Direct source relationship" },
  DEFAULT: { stroke: "#b6a384", label: "Published relationship" },
} as const;
