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
}

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
