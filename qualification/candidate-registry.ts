import type { QualificationCandidate } from "./candidate-contract";

export type CandidateRole = "NORMATIVE_INCUMBENT" | "COMPARISON_CANDIDATE" | "REFERENCE_FALLBACK";
export type CandidateStatus = "NOT_INSTALLED" | "INSTALLED_NOT_MEASURED" | "AVAILABLE" | "MEASURED";

export type CandidateDescriptor = {
  name: string;
  role: CandidateRole;
  status: CandidateStatus;
  adapter?: QualificationCandidate;
  exactVersion?: string;
};

/**
 * The registry is deliberately explicit. A library is not considered
 * evaluated merely because it appears in the inventory; it must be registered
 * with an adapter and an exact version before a report can describe it as
 * available.
 */
export const candidateRegistry: readonly CandidateDescriptor[] = [
  { name: "FGA SVG semantic baseline", role: "REFERENCE_FALLBACK", status: "NOT_INSTALLED" },
  { name: "Cytoscape.js", role: "NORMATIVE_INCUMBENT", status: "NOT_INSTALLED" },
  { name: "Sigma.js", role: "COMPARISON_CANDIDATE", status: "NOT_INSTALLED" },
  { name: "D3", role: "COMPARISON_CANDIDATE", status: "NOT_INSTALLED" },
  { name: "React Flow", role: "COMPARISON_CANDIDATE", status: "NOT_INSTALLED" },
];

export function registerCandidate(
  descriptors: readonly CandidateDescriptor[],
  adapter: QualificationCandidate,
): CandidateDescriptor[] {
  return descriptors.map((descriptor) => descriptor.name === adapter.name
    ? { ...descriptor, adapter, exactVersion: adapter.version, status: "AVAILABLE" }
    : descriptor);
}

export function measuredCandidates(descriptors: readonly CandidateDescriptor[]): CandidateDescriptor[] {
  return descriptors.filter((descriptor) => descriptor.status === "MEASURED" && descriptor.adapter && descriptor.exactVersion);
}
