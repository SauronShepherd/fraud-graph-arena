export type PathStatus = "OPEN" | "COMING_SOON" | "LOCKED";

export interface PathSummary {
  id: string;
  name: string;
  description: string;
  ranked: boolean;
  status: PathStatus;
  access_message: string;
}

export interface CaseSummary {
  id: string;
  version: string;
  path_id: string;
  name: string;
  description: string;
  status: "OPEN" | "LOCKED" | "CLOSED";
}

export interface CatalogueSections {
  sections: PathSummary[];
}

export interface CatalogueSection {
  path: PathSummary;
  cases: CaseSummary[];
}

export interface RoundSummary {
  id: string;
  player_id: string;
  path_id: string;
  case_id: string;
  case_version: string;
  status: "CREATED" | "INTRO_PENDING" | "ACTIVE";
  created_at: string;
  started_at: string | null;
  intro_completed_at: string | null;
}

export interface ComicPage {
  id: string;
  position: number;
  title: string;
  narration: string;
  image_url: string;
  alt_text: string;
}

export interface ComicSequence {
  id: string;
  case_id: string;
  case_version: string;
  kind: "OPENING" | "CLOSING";
  skippable: boolean;
  pages: ComicPage[];
}

export interface Opening {
  round: RoundSummary;
  case: CaseSummary;
  sequence: ComicSequence;
}

export interface Workspace {
  round: RoundSummary;
  case: CaseSummary;
  board_message: string;
  evidence_count: number;
  suspect_count: number;
  path_name: string;
  empty_state_code: string;
  actions: ActionAvailability[];
  graph: Graph;
}
export interface GraphNode { record_id: string; record_type: string; record_subtype: string; label: string; source_system_id: string; provenance_ref: string; safe_summary: string; }
export interface GraphEdge { relationship_id: string; source_record_id: string; target_record_id: string; relationship_family: string; relationship_type: string; directed: boolean; provenance: string; event_time: string; player_safe_summary: string; }
export interface Graph { projection_version: string; nodes: GraphNode[]; edges: GraphEdge[]; node_count: number; edge_count: number; }

export type ActionState = "AVAILABLE" | "NOT_IMPLEMENTED" | "LOCKED" | "PENDING" | "FAILED";
export interface ActionAvailability { id: string; state: ActionState; reason_code: string; reason: string; }

export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
  code: string;
  correlation_id: string;
  recovery?: string;
}
