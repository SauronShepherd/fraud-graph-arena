import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { CaseSubmissionPanel } from "./CaseSubmissionPanel";
import type { Graph, Workspace } from "../api/contracts";

const api = vi.hoisted(() => ({ submitCase: vi.fn() }));
vi.mock("../api/client", () => api);

const workspace = {
  round: { id: "round-11", status: "ACTIVE", credits_remaining: 3 },
} as unknown as Workspace;
const graph = { nodes: [{ record_id: "P1", label: "Cipher" }, { record_id: "P2", label: "Alias" }] } as unknown as Graph;

describe("CaseSubmissionPanel", () => {
  beforeEach(() => api.submitCase.mockReset());

  it("shows the economy and submits selected actors and claims with one retry key", async () => {
    api.submitCase.mockResolvedValue({ submission_id: "s1" });
    render(<CaseSubmissionPanel workspace={workspace} graph={graph} />);
    expect(screen.getByText(/3 credits left/i)).toBeVisible();
    fireEvent.click(screen.getByLabelText(/Cipher P1/i));
    fireEvent.click(screen.getByLabelText(/The matching contact pair/i));
    fireEvent.click(screen.getByRole("button", { name: "Submit investigation" }));
    await waitFor(() => expect(api.submitCase).toHaveBeenCalledOnce());
    expect(api.submitCase.mock.calls[0][1].suspect_record_ids).toEqual(["P1"]);
    expect(api.submitCase.mock.calls[0][1].evidence_claim_ids).toEqual(["IDENTITY_MERGE"]);
    expect(api.submitCase.mock.calls[0][1].idempotency_key).toBeTruthy();
  });
});
