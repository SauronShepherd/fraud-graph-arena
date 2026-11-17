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
  credits_remaining: number;
  version: number;
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
export interface Graph {
  projection_version: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  node_count: number;
  edge_count: number;
  partial?: boolean;
  omitted_node_count?: number;
  omitted_edge_count?: number;
  relationship_filters?: string[];
}
export interface InvestigationCommand {
  command_id: string;
  round_id: string;
  idempotency_key: string;
  action: string;
  source_record_id: string;
  target_record_id: string;
  relationship_type: string;
  status: string;
  charged_credits: number;
  revealed_record_ids: string[];
  created_at: string;
  replayed?: boolean;
}

export interface IdentityCandidate {
  candidate_id: string;
  left_record_id: string;
  right_record_id: string;
  entity_type: string;
  confidence_band: string;
  estimated_score: number;
  agreement_fields: string[];
  disagreement_fields: string[];
  missing_fields: string[];
  evidence_reasons: string[];
  model_version: string;
  threshold_version: string;
  normalization_version: string;
  framework_semantics: string;
  generation_mode: string;
  actual_engine_run: boolean;
  review_required: boolean;
  snapshot_version: string;
}

export interface ExactIdentityMatch {
  match_id: string;
  left_record_id: string;
  right_record_id: string;
  entity_type: string;
  rule_id: string;
  evidence_fields: string[];
  evidence_reasons: string[];
  normalization_version: string;
  snapshot_version: string;
  provenance_refs: string[];
}

export interface EntityResolutionAnalysis {
  analysis_id: string;
  round_id: string;
  idempotency_key: string;
  focus_record_id: string | null;
  status: string;
  charged_credits: number;
  normalization_version: string;
  model_version: string;
  threshold_version: string;
  snapshot_version: string;
  generation_mode: string;
  framework_semantics: string;
  actual_engine_run: boolean;
  exact_matches: ExactIdentityMatch[];
  candidates: IdentityCandidate[];
  replayed?: boolean;
}

export interface EntityResolutionReview {
  review_id: string;
  round_id: string;
  candidate_id: string;
  outcome: "ACCEPTED" | "REJECTED" | "UNRESOLVED";
  status: string;
  created_at: string;
  replayed?: boolean;
}

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
