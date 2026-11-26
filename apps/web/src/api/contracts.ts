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
  status: "CREATED" | "INTRO_PENDING" | "ACTIVE" | "SUBMITTED";
  created_at: string;
  started_at: string | null;
  intro_completed_at: string | null;
  credits_remaining: number;
  version: number;
  submitted_at: string | null;
  submission_id: string | null;
}

export interface ComicPage {
  id: string;
  position: number;
  title: string;
  narration: string;
  image_url: string;
  alt_text: string;
  caption: string;
  transcript: string;
  audio_asset_id: string | null;
}

export interface ComicSequence {
  id: string;
  case_id: string;
  case_version: string;
  kind: "OPENING" | "CLOSING";
  skippable: boolean;
  pages: ComicPage[];
  variants: Record<string, ComicPage[]>;
  fictionalization_statement: string;
  reduced_motion_behavior: string;
  preload_next: boolean;
  audio_asset_ids: string[];
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

export interface GraphAnalysisPath {
  record_ids: string[];
  relationship_ids: string[];
  length: number;
}

export interface GraphAnalysisComponent {
  component_id: string;
  record_ids: string[];
  node_count: number;
  edge_count: number;
}

export interface GraphAnalysisLead {
  rank: number;
  record_id: string;
  metric: string;
  score: number;
  supporting_relationship_ids: string[];
}

export interface GraphAnalysisMotif {
  motif_type: string;
  record_ids: string[];
  relationship_ids: string[];
  length: number;
  event_times: string[];
  time_span: string | null;
  chronology_observed: boolean;
}

export interface GraphAnalysis {
  analysis_id: string;
  round_id: string;
  algorithm: string;
  status: string;
  result_type: string;
  parameters: Record<string, unknown>;
  snapshot_version: string;
  projection_version: string;
  graph_engine: string;
  framework_semantics: string;
  generation_mode: string;
  actual_engine_run: boolean;
  input_node_count: number;
  input_edge_count: number;
  nodes: GraphNode[];
  edges: GraphEdge[];
  paths: GraphAnalysisPath[];
  components: GraphAnalysisComponent[];
  ranked_leads: GraphAnalysisLead[];
  motifs: GraphAnalysisMotif[];
  supporting_relationship_ids: string[];
  partial: boolean;
  omitted_result_count: number;
  interpretation: string;
  limitations: string[];
  cache_key: string;
  cached: boolean;
  execution_millis: number;
}

export interface GraphAnalysisRequest {
  idempotency_key?: string;
  algorithm: string;
  seed_record_id?: string | null;
  source_record_id?: string | null;
  target_record_id?: string | null;
  max_hops?: number;
  max_path_length?: number;
  result_limit?: number;
  directed?: boolean;
  centrality_metric?: string;
  relationship_families?: string[];
  relationship_types?: string[];
  time_from?: string | null;
  time_to?: string | null;
  visible_record_ids: string[];
}

export interface ScoreDimensions {
  conclusion_accuracy: number;
  evidence_quality: number;
  relationship_interpretation: number;
  protected_actor_discipline: number;
  efficiency: number;
}

export interface Submission {
  submission_id: string;
  round_id: string;
  idempotency_key: string;
  status: string;
  score: number;
  ending_code: string;
  ending_title: string;
  ending_narrative: string;
  dimensions: ScoreDimensions;
  false_accusations: number;
  required_claims_complete: boolean;
  submitted_suspect_count: number;
  credits_remaining: number;
  scoring_version: string;
  economy_version: string;
  created_at: string;
  replayed?: boolean;
}

export interface LedgerEntry {
  entry_id: string;
  round_id: string;
  idempotency_key: string;
  action: string;
  entry_type: string;
  amount: number;
  balance_after: number;
  status: string;
  rules_version: string;
  created_at: string;
}

export interface ResolutionContext {
  available: boolean;
  submission: Submission;
  ledger: { entries: LedgerEntry[] };
  closing?: Opening;
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
