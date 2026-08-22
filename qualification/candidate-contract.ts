export type FgaNode = { id: string; recordType: string; label: string; x: number; y: number };
export type FgaEdge = { id: string; sourceId: string; targetId: string; relationshipFamily: string; relationshipType: string; directed: boolean };
export type FgaViewport = { zoom: number; panX: number; panY: number };

/** Candidate adapters may wrap a library, but native library objects stop here. */
export interface QualificationCandidate {
  readonly name: string;
  readonly version: string;
  mount(container: HTMLElement, nodes: readonly FgaNode[], edges: readonly FgaEdge[], callbacks: {
    onNodeSelect(id: string | null): void;
    onEdgeSelect(id: string | null): void;
  }): CandidateInstance;
}

export interface CandidateInstance {
  fit(): void;
  setViewport(viewport: FgaViewport): void;
  resize(): void;
  destroy(): void;
}

export const HARD_REQUIREMENTS = [
  "H01 semantic node styling",
  "H02 semantic relationship styling",
  "H03 stable FGA node IDs",
  "H04 stable FGA edge IDs",
  "H05 zoom and pan",
  "H06 programmatic fit/reset",
  "H07 preset positions",
  "H08 predictable resize",
  "H09 lifecycle cleanup",
  "H10 persistent details",
  "H11 project-owned semantic fallback",
  "H12 measured performance",
  "H13 production maturity",
  "H14 compatible license",
  "H15 no native objects in app contracts",
] as const;
