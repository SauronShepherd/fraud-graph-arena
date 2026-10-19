import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { actions } from "./actions";
import { screenDefinitions } from "./definitions";
import { ScreenRuntimeProvider, useScreenRuntime } from "./ScreenRuntimeContext";
import { TransitionCoordinator } from "./TransitionCoordinator";

function RuntimeProbe() {
  const { dispatchAction, problem, transitionLocked } = useScreenRuntime();
  const location = useLocation();
  return <>
    <output aria-label="problem-code">{problem?.code ?? ""}</output>
    <output aria-label="busy">{String(transitionLocked)}</output>
    <output aria-label="route">{location.pathname}</output>
    <button type="button" onClick={() => void dispatchAction("COMPLETE_INTRO")}>Complete intro</button>
    <button type="button" onClick={() => void dispatchAction("BEGIN")}>Begin</button>
  </>;
}

afterEach(() => vi.restoreAllMocks());

describe("screen runtime dispatch", () => {
  it("checks the screen action allowlist before invoking a handler", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<MemoryRouter initialEntries={["/"]}><TransitionCoordinator><ScreenRuntimeProvider definition={screenDefinitions.get("LAUNCH")!} context={{}}><RuntimeProbe /></ScreenRuntimeProvider></TransitionCoordinator></MemoryRouter>);
    fireEvent.click(screen.getByRole("button", { name: "Complete intro" }));
    await waitFor(() => expect(screen.getByLabelText("problem-code")).toHaveTextContent("SCREEN_RUNTIME_FAILURE"));
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("locks commands while a handler is pending and commits only one result", async () => {
    let resolveAction!: (result: Awaited<ReturnType<typeof actions.COMPLETE_INTRO>>) => void;
    const actionSpy = vi.spyOn(actions, "COMPLETE_INTRO").mockImplementation(() => new Promise((resolve) => { resolveAction = resolve; }));
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ round: { id: "round-1", status: "INTRO_PENDING" }, case: {}, sequence: { pages: [] } }), { status: 200, headers: { "content-type": "application/json" } }));
    render(<MemoryRouter initialEntries={["/rounds/round-1/intro?page=2"]}><TransitionCoordinator><ScreenRuntimeProvider definition={screenDefinitions.get("CASE_INTRODUCTION")!} context={{ roundId: "round-1", page: 2 }}><RuntimeProbe /></ScreenRuntimeProvider></TransitionCoordinator></MemoryRouter>);
    fireEvent.click(screen.getByRole("button", { name: "Complete intro" }));
    fireEvent.click(screen.getByRole("button", { name: "Complete intro" }));
    expect(actionSpy).toHaveBeenCalledOnce();
    expect(screen.getByLabelText("busy")).toHaveTextContent("true");
    resolveAction({ event: { type: "INTRODUCTION_COMPLETED", context: { roundId: "round-1", roundStatus: "ACTIVE" } } });
    await waitFor(() => expect(screen.getByLabelText("route")).toHaveTextContent("/rounds/round-1/board"));
  });
});
