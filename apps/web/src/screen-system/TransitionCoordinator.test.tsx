import { useRef, useState } from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, useLocation, useNavigate } from "react-router-dom";
import { describe, expect, it } from "vitest";
import type { TransitionPlan } from "./contracts";
import { TransitionCoordinator, useTransitionCoordinator } from "./TransitionCoordinator";

function Harness({ plan }: { plan: TransitionPlan }) {
  const coordinator = useTransitionCoordinator();
  const location = useLocation();
  const navigate = useNavigate();
  const [accepted, setAccepted] = useState(0);
  const initialToken = useRef(coordinator.captureToken());
  return <>
    <output aria-label="location">{location.pathname}{location.search}</output>
    <output aria-label="transition-lock">{String(coordinator.transitionLocked)}</output>
    <output aria-label="accepted-count">{accepted}</output>
    <button type="button" onClick={() => { if (coordinator.request(plan, initialToken.current)) setAccepted((count) => count + 1); }}>Commit transition</button>
    <button type="button" onClick={() => navigate(-1)}>Back</button>
    <button type="button" onClick={() => navigate("/rounds/round-2/intro")}>Open another round</button>
  </>;
}

function renderHarness(plan: TransitionPlan, initialEntries: string[], initialIndex = initialEntries.length - 1) {
  return render(<MemoryRouter initialEntries={initialEntries} initialIndex={initialIndex}><TransitionCoordinator><Harness plan={plan} /></TransitionCoordinator></MemoryRouter>);
}

describe("transition coordinator", () => {
  it("locks duplicate commits and honors PUSH history", async () => {
    renderHarness({ source: "PATH_SELECTION", target: "CASE_SELECTION", context: { pathId: "DETECTIVE_ACADEMY" }, effect: "NONE", history: "PUSH", event: "PATH_SELECTED" }, ["/", "/paths"]);
    fireEvent.click(screen.getByRole("button", { name: "Commit transition" }));
    fireEvent.click(screen.getByRole("button", { name: "Commit transition" }));
    expect(screen.getByLabelText("accepted-count")).toHaveTextContent("1");
    await waitFor(() => expect(screen.getByLabelText("location")).toHaveTextContent("/paths/DETECTIVE_ACADEMY/cases"));
    fireEvent.click(screen.getByRole("button", { name: "Back" }));
    await waitFor(() => expect(screen.getByLabelText("location")).toHaveTextContent("/paths"));
  });

  it("honors REPLACE history for completed introductions", async () => {
    renderHarness({ source: "CASE_INTRODUCTION", target: "INVESTIGATION_BOARD", context: { roundId: "round-1", roundStatus: "ACTIVE" }, effect: "NONE", history: "REPLACE", event: "INTRODUCTION_COMPLETED" }, ["/paths", "/rounds/round-1/intro?page=2"]);
    fireEvent.click(screen.getByRole("button", { name: "Commit transition" }));
    await waitFor(() => expect(screen.getByLabelText("location")).toHaveTextContent("/rounds/round-1/board"));
    fireEvent.click(screen.getByRole("button", { name: "Back" }));
    await waitFor(() => expect(screen.getByLabelText("location")).toHaveTextContent("/paths"));
  });

  it("rejects a stale plan whose source screen is no longer current", () => {
    renderHarness({ source: "LAUNCH", target: "PATH_SELECTION", context: {}, effect: "NONE", history: "PUSH", event: "PATHS_REQUESTED" }, ["/paths"]);
    fireEvent.click(screen.getByRole("button", { name: "Commit transition" }));
    expect(screen.getByLabelText("accepted-count")).toHaveTextContent("0");
    expect(screen.getByLabelText("location")).toHaveTextContent("/paths");
  });

  it("rejects a delayed result after the route context changes within the same screen family", async () => {
    renderHarness({ source: "CASE_INTRODUCTION", target: "INVESTIGATION_BOARD", context: { roundId: "round-1", roundStatus: "ACTIVE" }, effect: "NONE", history: "REPLACE", event: "INTRODUCTION_COMPLETED" }, ["/rounds/round-1/intro"]);
    fireEvent.click(screen.getByRole("button", { name: "Open another round" }));
    await waitFor(() => expect(screen.getByLabelText("location")).toHaveTextContent("/rounds/round-2/intro"));
    fireEvent.click(screen.getByRole("button", { name: "Commit transition" }));
    expect(screen.getByLabelText("accepted-count")).toHaveTextContent("0");
    expect(screen.getByLabelText("location")).toHaveTextContent("/rounds/round-2/intro");
  });
});
