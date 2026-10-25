import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { InvestigationActions } from "./InvestigationActions";
import type { Graph, Workspace } from "../api/contracts";

const api = vi.hoisted(() => ({ getInvestigationHistory: vi.fn(), submitManualHypothesis: vi.fn() }));
vi.mock("../api/client", () => api);

const workspace = { round: { id: "round-1" }, case: { id: "ACADEMY_T02" }, actions: [] } as unknown as Workspace;
const graph = { nodes: [
  { record_id: "P1", label: "Puppy One" }, { record_id: "O1", label: "Office One" },
], edges: [] } as unknown as Graph;

describe("InvestigationActions", () => {
  beforeEach(() => { api.getInvestigationHistory.mockResolvedValue({ commands: [] }); api.submitManualHypothesis.mockReset(); });

  it("records a free hypothesis and presents that it is not revealed evidence", async () => {
    api.submitManualHypothesis.mockResolvedValue({ command_id: "cmd-1", action: "MANUAL_HYPOTHESIS", source_record_id: "P1", target_record_id: "O1", relationship_type: "POSSIBLE_CONTROL", status: "RECORDED", charged_credits: 0, revealed_record_ids: [] });
    render(<InvestigationActions workspace={workspace} graph={graph} />);
    fireEvent.change(screen.getByLabelText("From"), { target: { value: "P1" } });
    fireEvent.change(screen.getByLabelText("To"), { target: { value: "O1" } });
    fireEvent.click(screen.getByRole("button", { name: "Record hypothesis" }));
    await waitFor(() => expect(api.submitManualHypothesis).toHaveBeenCalledOnce());
    expect(await screen.findByText(/no credits were charged and no evidence was revealed/i)).toBeVisible();
    expect(screen.getByText(/P1 → O1/)).toBeVisible();
  });

  it("reuses the same idempotency key after an ambiguous transport failure", async () => {
    api.submitManualHypothesis.mockRejectedValueOnce(new Error("connection lost"));
    api.submitManualHypothesis.mockResolvedValueOnce({ command_id: "cmd-retried", source_record_id: "P1", target_record_id: "O1", relationship_type: "POSSIBLE_CONTROL", status: "RECORDED" });
    render(<InvestigationActions workspace={workspace} graph={graph} />);
    fireEvent.change(screen.getByLabelText("From"), { target: { value: "P1" } });
    fireEvent.change(screen.getByLabelText("To"), { target: { value: "O1" } });
    const button = screen.getByRole("button", { name: "Record hypothesis" });
    fireEvent.click(button);
    await screen.findByText(/could not be recorded/i);
    fireEvent.click(button);
    await waitFor(() => expect(api.submitManualHypothesis).toHaveBeenCalledTimes(2));
    expect(api.submitManualHypothesis.mock.calls[0][1].idempotency_key).toBe(api.submitManualHypothesis.mock.calls[1][1].idempotency_key);
  });
});
