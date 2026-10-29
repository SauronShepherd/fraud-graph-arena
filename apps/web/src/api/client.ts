import type {
  CatalogueSection,
  CatalogueSections,
  Opening,
  ProblemDetails,
  RoundSummary,
  Workspace
} from "./contracts";

const API_BASE = (import.meta.env.VITE_FGA_API_BASE_URL as string | undefined) ?? "/api/v1";

export class ApiProblem extends Error {
  readonly problem: ProblemDetails;

  constructor(problem: ProblemDetails) {
    super(problem.detail);
    this.name = "ApiProblem";
    this.problem = problem;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  const headers = new Headers(init?.headers);
  headers.set("Accept", "application/json, application/problem+json");
  if (init?.body !== undefined) headers.set("Content-Type", "application/json");
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...init,
      headers
    });
  } catch (cause) {
    throw new ApiProblem({
      type: "https://fraud-graph-arena.invalid/problems/backend-unavailable",
      title: "The office is not answering",
      status: 503,
      detail: "The game service could not be reached.",
      instance: path,
      code: "BACKEND_UNAVAILABLE",
      correlation_id: "client-side",
      recovery: "Check that the backend is running, then try again."
    });
  }

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/problem+json")) {
      throw new ApiProblem((await response.json()) as ProblemDetails);
    }
    throw new ApiProblem({
      type: "https://fraud-graph-arena.invalid/problems/unexpected-response",
      title: "Unexpected response",
      status: response.status,
      detail: "The service returned a response outside the agreed contract.",
      instance: path,
      code: "UNEXPECTED_RESPONSE",
      correlation_id: response.headers.get("x-correlation-id") ?? "unknown"
    });
  }

  return (await response.json()) as T;
}

export function listSections(signal?: AbortSignal): Promise<CatalogueSections> {
  return request<CatalogueSections>("/catalogue/sections", { signal });
}

export function getSection(pathId: string, signal?: AbortSignal): Promise<CatalogueSection> {
  return request<CatalogueSection>(`/catalogue/${encodeURIComponent(pathId)}`, { signal });
}

export async function createAndStartRound(pathId: string, caseId: string): Promise<RoundSummary> {
  const created = await request<RoundSummary>("/rounds", {
    method: "POST",
    body: JSON.stringify({
      player_id: "demo-hercule",
      path_id: pathId,
      case_id: caseId
    })
  });
  return request<RoundSummary>(`/rounds/${encodeURIComponent(created.id)}/start`, {
    method: "POST"
  });
}

export function getOpening(roundId: string, signal?: AbortSignal): Promise<Opening> {
  return request<Opening>(`/rounds/${encodeURIComponent(roundId)}/opening`, { signal });
}

export function completeOpening(roundId: string, completion: "FINISHED" | "SKIPPED" = "FINISHED"): Promise<RoundSummary> {
  return request<RoundSummary>(`/rounds/${encodeURIComponent(roundId)}/opening/complete`, {
    method: "POST",
    body: JSON.stringify({ completion })
  });
}

export function getWorkspace(roundId: string, signal?: AbortSignal): Promise<Workspace> {
  return request<Workspace>(`/rounds/${encodeURIComponent(roundId)}/workspace`, { signal });
}
