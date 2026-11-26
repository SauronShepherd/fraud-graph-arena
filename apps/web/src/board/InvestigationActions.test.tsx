import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { InvestigationActions } from "./InvestigationActions";
import type { Graph, Workspace } from "../api/contracts";

const api = vi.hoisted(() => ({
  getInvestigationHistory: vi.fn(),
  submitManualHypothesis: vi.fn(),
  getEntityResolutionHistory: vi.fn(),
  runEntityResolution: vi.fn(),
  reviewEntityResolutionCandidate: vi.fn(),
  getGraphAnalysisHistory: vi.fn(),
  runGraphAnalysis: vi.fn(),
}));
vi.mock("../api/client", () => api);

const workspace = {
  round: { id: "round-1" },
  case: { id: "ACADEMY_T02" },
  actions: [{ id: "CREATE_HYPOTHESIS", state: "AVAILABLE", reason_code: "READY", reason: "Ready" }],
} as unknown as Workspace;
const graph = {
  nodes: [
    { record_id: "P1", label: "Puppy One" },
    { record_id: "O1", label: "Office One" },
  ],
  edges: [],
} as unknown as Graph;

describe("InvestigationActions", () => {
  beforeEach(() => {
    Object.values(api).forEach((mock) => mock.mockReset());
    api.getInvestigationHistory.mockResolvedValue({ commands: [] });
    try {
      globalThis.sessionStorage?.clear();
    } catch {
      // The retry test still covers the in-memory path when storage is unavailable.
    }
  });

  it("records a free hypothesis and says that it is not revealed evidence", async () => {
    api.submitManualHypothesis.mockResolvedValue({
      command_id: "cmd-1",
      round_id: "round-1",
      idempotency_key: "key-1",
      action: "MANUAL_HYPOTHESIS",
      source_record_id: "P1",
      target_record_id: "O1",
      relationship_type: "POSSIBLE_CONTROL",
      status: "RECORDED",
      charged_credits: 0,
      revealed_record_ids: [],
      created_at: "2026-11-14T00:00:00Z",
    });
    render(<InvestigationActions workspace={workspace} graph={graph} />);

    fireEvent.change(screen.getByLabelText("From"), { target: { value: "P1" } });
    fireEvent.change(screen.getByLabelText("To"), { target: { value: "O1" } });
    fireEvent.click(await screen.findByRole("button", { name: "Record hypothesis" }));

    await waitFor(() => expect(api.submitManualHypothesis).toHaveBeenCalledOnce());
    expect(await screen.findByText(/no credits were charged and no evidence was revealed/i)).toBeVisible();
    expect(screen.getByText(/P1 → O1/)).toBeVisible();
  });

  it("offers the selected graph node as a subject shortcut", async () => {
    const view = render(<InvestigationActions workspace={workspace} graph={graph} selectedNodeId="P1" />);
    fireEvent.click(screen.getByRole("button", { name: "Use selected as From" }));
    expect(screen.getByLabelText("From")).toHaveValue("P1");

    view.rerender(<InvestigationActions workspace={workspace} graph={graph} selectedNodeId="O1" />);
    fireEvent.click(screen.getByRole("button", { name: "Use selected as To" }));
    expect(screen.getByLabelText("To")).toHaveValue("O1");
  });

  it("reuses the same idempotency key after an ambiguous transport failure", async () => {
    api.submitManualHypothesis.mockRejectedValueOnce(new Error("connection lost"));
    api.submitManualHypothesis.mockResolvedValueOnce({
      command_id: "cmd-retried",
      round_id: "round-1",
      idempotency_key: "key-2",
      action: "MANUAL_HYPOTHESIS",
      source_record_id: "P1",
      target_record_id: "O1",
      relationship_type: "POSSIBLE_CONTROL",
      status: "RECORDED",
      charged_credits: 0,
      revealed_record_ids: [],
      created_at: "2026-11-14T00:00:00Z",
    });
    render(<InvestigationActions workspace={workspace} graph={graph} />);

    fireEvent.change(screen.getByLabelText("From"), { target: { value: "P1" } });
    fireEvent.change(screen.getByLabelText("To"), { target: { value: "O1" } });
    const button = await screen.findByRole("button", { name: "Record hypothesis" });
    fireEvent.click(button);
    await screen.findByText(/could not be confirmed/i);
    fireEvent.click(button);

    await waitFor(() => expect(api.submitManualHypothesis).toHaveBeenCalledTimes(2));
    expect(api.submitManualHypothesis.mock.calls[0][1].idempotency_key).toBe(
      api.submitManualHypothesis.mock.calls[1][1].idempotency_key,
    );
  });

  it("runs a player-safe identity analysis and records a candidate review", async () => {
    const identityWorkspace = {
      ...workspace,
      actions: [
        { id: "COMPARE_IDENTITIES", state: "AVAILABLE", reason_code: "READY", reason: "Ready" },
      ],
    } as unknown as Workspace;
    api.getEntityResolutionHistory.mockResolvedValue({ analyses: [], reviews: [] });
    api.runEntityResolution.mockResolvedValue({
      analysis_id: "analysis-1",
      round_id: "round-1",
      idempotency_key: "analysis-key",
      focus_record_id: "P1",
      status: "COMPLETED",
      charged_credits: 3,
      normalization_version: "fga09-norm-v1",
      model_version: "fga09-deterministic-fallback-v1",
      threshold_version: "fga09-review-thresholds-v1",
      snapshot_version: "snap-1",
      generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
      framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
      actual_engine_run: false,
      exact_matches: [],
      candidates: [{
        candidate_id: "candidate-1",
        left_record_id: "P1",
        right_record_id: "O1",
        entity_type: "PERSON",
        confidence_band: "MEDIUM",
        estimated_score: 0.5,
        agreement_fields: ["surname"],
        disagreement_fields: ["email"],
        missing_fields: ["phone"],
        evidence_reasons: ["Contact fields disagree; review is required."],
        model_version: "fga09-deterministic-fallback-v1",
        threshold_version: "fga09-review-thresholds-v1",
        normalization_version: "fga09-norm-v1",
        framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
        generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
        actual_engine_run: false,
        review_required: true,
        snapshot_version: "snap-1",
      }],
    });
    api.reviewEntityResolutionCandidate.mockResolvedValue({
      review_id: "review-1",
      round_id: "round-1",
      candidate_id: "candidate-1",
      outcome: "REJECTED",
      status: "RECORDED",
      created_at: "2026-11-16T00:00:00Z",
    });
    render(<InvestigationActions workspace={identityWorkspace} graph={graph} selectedNodeId="P1" />);

    fireEvent.click(await screen.findByRole("button", { name: "Run identity analysis" }));
    await waitFor(() => expect(api.runEntityResolution).toHaveBeenCalledOnce());
    expect(await screen.findByText(/deterministic fallback/i)).toBeVisible();
    expect(await screen.findByText(/missing: phone/i)).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Reject candidate" }));

    await waitFor(() => expect(api.reviewEntityResolutionCandidate).toHaveBeenCalledOnce());
    expect(await screen.findByText(/review: rejected/i)).toBeVisible();
    expect(screen.getByText(/not a canonical merge or fraud verdict/i)).toBeVisible();
  });

  it("keeps an identity retry key across a panel remount", async () => {
    const identityWorkspace = {
      ...workspace,
      actions: [
        { id: "COMPARE_IDENTITIES", state: "AVAILABLE", reason_code: "READY", reason: "Ready" },
      ],
    } as unknown as Workspace;
    api.getEntityResolutionHistory.mockResolvedValue({ analyses: [], reviews: [] });
    api.runEntityResolution
      .mockRejectedValueOnce(new Error("connection lost"))
      .mockResolvedValueOnce({
        analysis_id: "analysis-remount",
        round_id: "round-1",
        idempotency_key: "replayed-analysis-key",
        focus_record_id: "P1",
        status: "COMPLETED",
        charged_credits: 3,
        normalization_version: "fga09-norm-v1",
        model_version: "fga09-deterministic-fallback-v1",
        threshold_version: "fga09-review-thresholds-v1",
        snapshot_version: "snap-1",
        generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
        framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
        actual_engine_run: false,
        exact_matches: [],
        candidates: [],
      });

    const first = render(<InvestigationActions workspace={identityWorkspace} graph={graph} selectedNodeId="P1" />);
    fireEvent.click(await screen.findByRole("button", { name: "Run identity analysis" }));
    await screen.findByText(/could not be completed/i);
    const firstKey = api.runEntityResolution.mock.calls[0][1].idempotency_key;

    first.unmount();
    render(<InvestigationActions workspace={identityWorkspace} graph={graph} selectedNodeId="P1" />);
    fireEvent.click(await screen.findByRole("button", { name: "Run identity analysis" }));

    await waitFor(() => expect(api.runEntityResolution).toHaveBeenCalledTimes(2));
    expect(api.runEntityResolution.mock.calls[1][1].idempotency_key).toBe(firstKey);
  });

  it("shows the latest review outcome after a candidate is revised", async () => {
    const identityWorkspace = {
      ...workspace,
      actions: [
        { id: "COMPARE_IDENTITIES", state: "AVAILABLE", reason_code: "READY", reason: "Ready" },
      ],
    } as unknown as Workspace;
    api.getEntityResolutionHistory.mockResolvedValue({
      analyses: [{
        analysis_id: "analysis-history",
        round_id: "round-1",
        idempotency_key: "analysis-history-key",
        focus_record_id: null,
        status: "COMPLETED",
        charged_credits: 3,
        normalization_version: "fga09-norm-v1",
        model_version: "fga09-deterministic-fallback-v1",
        threshold_version: "fga09-review-thresholds-v1",
        snapshot_version: "snap-1",
        generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
        framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
        actual_engine_run: false,
        exact_matches: [],
        candidates: [{
          candidate_id: "candidate-history",
          left_record_id: "P1",
          right_record_id: "O1",
          entity_type: "PERSON",
          confidence_band: "MEDIUM",
          estimated_score: 0.5,
          agreement_fields: ["surname"],
          disagreement_fields: ["email"],
          missing_fields: [],
          evidence_reasons: ["Contact fields disagree; review is required."],
          model_version: "fga09-deterministic-fallback-v1",
          threshold_version: "fga09-review-thresholds-v1",
          normalization_version: "fga09-norm-v1",
          framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
          generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
          actual_engine_run: false,
          review_required: true,
          snapshot_version: "snap-1",
        }],
      }],
      reviews: [
        { review_id: "review-old", round_id: "round-1", candidate_id: "candidate-history", outcome: "ACCEPTED", status: "RECORDED", created_at: "2026-11-16T00:00:00Z" },
        { review_id: "review-new", round_id: "round-1", candidate_id: "candidate-history", outcome: "REJECTED", status: "RECORDED", created_at: "2026-11-17T00:00:00Z" },
      ],
    });
    render(<InvestigationActions workspace={identityWorkspace} graph={graph} />);

    expect(await screen.findByText(/review: rejected/i)).toBeVisible();
    expect(screen.queryByText(/review: accepted/i)).not.toBeInTheDocument();
  });

  it("runs a bounded graph question and explains that structure is not a verdict", async () => {
    const graphWorkspace = {
      ...workspace,
      actions: [
        { id: "RUN_GRAPH_ANALYSIS", state: "AVAILABLE", reason_code: "READY", reason: "Ready" },
      ],
    } as unknown as Workspace;
    api.getGraphAnalysisHistory.mockResolvedValue({ analyses: [] });
    api.runGraphAnalysis.mockResolvedValue({
      analysis_id: "graph-analysis-1",
      round_id: "round-1",
      algorithm: "NEIGHBOURHOOD",
      status: "COMPLETED",
      result_type: "NEIGHBOURHOOD_FOUND",
      parameters: { algorithm: "NEIGHBOURHOOD" },
      snapshot_version: "snap-1",
      projection_version: "1",
      graph_engine: "FGA_GRAPH_ANALYTICS_ADAPTER",
      framework_semantics: "GRAPHFRAMES_STYLE_ALGORITHM_CONTRACT",
      generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
      actual_engine_run: false,
      input_node_count: 2,
      input_edge_count: 1,
      nodes: [],
      edges: [],
      paths: [],
      components: [],
      ranked_leads: [],
      motifs: [],
      supporting_relationship_ids: ["E1"],
      partial: false,
      omitted_result_count: 0,
      interpretation: "Structural importance is a lead, not a conviction.",
      limitations: ["Not culpability."],
      cache_key: "fga10:test",
      cached: false,
      execution_millis: 1,
    });
    render(<InvestigationActions workspace={graphWorkspace} graph={graph} selectedNodeId="P1" />);

    fireEvent.click(await screen.findByRole("button", { name: "Run graph analysis" }));
    await waitFor(() => expect(api.runGraphAnalysis).toHaveBeenCalledOnce());
    expect(api.runGraphAnalysis.mock.calls[0][1].visible_record_ids).toEqual(["P1", "O1"]);
    expect(await screen.findByText(/structural importance is a lead/i)).toBeVisible();
  });

  it("reuses an identity analysis key after an ambiguous transport failure", async () => {
    const identityWorkspace = {
      ...workspace,
      actions: [
        { id: "COMPARE_IDENTITIES", state: "AVAILABLE", reason_code: "READY", reason: "Ready" },
      ],
    } as unknown as Workspace;
    api.getEntityResolutionHistory.mockResolvedValue({ analyses: [], reviews: [] });
    api.runEntityResolution
      .mockRejectedValueOnce(new Error("connection lost"))
      .mockResolvedValueOnce({
        analysis_id: "analysis-retry",
        round_id: "round-1",
        idempotency_key: "analysis-retry-key",
        focus_record_id: null,
        status: "COMPLETED",
        charged_credits: 3,
        normalization_version: "fga09-norm-v1",
        model_version: "fga09-deterministic-fallback-v1",
        threshold_version: "fga09-review-thresholds-v1",
        snapshot_version: "snap-1",
        generation_mode: "RUNTIME_DETERMINISTIC_FALLBACK",
        framework_semantics: "ZINGG_LIKE_ENTITY_RESOLUTION_CANDIDATE",
        actual_engine_run: false,
        exact_matches: [],
        candidates: [],
      });
    render(<InvestigationActions workspace={identityWorkspace} graph={graph} />);

    const button = await screen.findByRole("button", { name: "Run identity analysis" });
    fireEvent.click(button);
    await screen.findByText(/could not be completed/i);
    fireEvent.click(button);

    await waitFor(() => expect(api.runEntityResolution).toHaveBeenCalledTimes(2));
    expect(api.runEntityResolution.mock.calls[0][1].idempotency_key).toBe(
      api.runEntityResolution.mock.calls[1][1].idempotency_key,
    );
  });
});
