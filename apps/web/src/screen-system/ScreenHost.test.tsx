import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, useLocation, useNavigate } from "react-router-dom";
import { actions } from "./actions";
import { screenDefinitions } from "./definitions";
import { ScreenHost } from "./ScreenHost";
import { useScreenRuntime } from "./ScreenRuntimeContext";
import { TransitionCoordinator } from "./TransitionCoordinator";

function PendingActionProbe() {
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  const { pathname } = useLocation();
  return <>
    <output aria-label="host-route">{pathname}</output>
    <output aria-label="host-busy">{String(transitionLocked)}</output>
    <button type="button" onClick={() => void dispatchAction("BEGIN")}>Begin pending action</button>
  </>;
}

function NavigableHost() {
  const location = useLocation();
  const navigate = useNavigate();
  const screen = location.pathname === "/paths" ? "PATH_SELECTION" : "LAUNCH";
  const definition = screenDefinitions.get(screen)!;
  return <>
    <button type="button" onClick={() => navigate("/paths")}>Navigate to paths</button>
    <ScreenHost definition={definition} screen={screen} context={{}}>
      <h1 tabIndex={-1}>{screen}</h1>
      <PendingActionProbe />
    </ScreenHost>
  </>;
}

describe("screen host", () => {
  it("loads the screen model before focusing and announcing the view", async () => {
    const definition = screenDefinitions.get("LAUNCH")!;
    render(<MemoryRouter><TransitionCoordinator><ScreenHost definition={definition} screen="LAUNCH" context={{}}><h1 tabIndex={-1}>Launch</h1></ScreenHost></TransitionCoordinator></MemoryRouter>);
    expect(screen.getByRole("heading", { name: "Launch" })).toBeVisible();
    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("LAUNCH ready"));
    expect(screen.getByRole("heading", { name: "Launch" })).toHaveFocus();
  });

  it("resets pending UI on route change and ignores the obsolete action result", async () => {
    let resolveAction!: (result: Awaited<ReturnType<typeof actions.BEGIN>>) => void;
    vi.spyOn(actions, "BEGIN").mockImplementation(() => new Promise((resolve) => { resolveAction = resolve; }));
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("{}", { status: 200, headers: { "content-type": "application/json" } }));
    render(<MemoryRouter initialEntries={["/"]}><TransitionCoordinator><NavigableHost /></TransitionCoordinator></MemoryRouter>);

    fireEvent.click(screen.getByRole("button", { name: "Begin pending action" }));
    await waitFor(() => expect(screen.getByLabelText("host-busy")).toHaveTextContent("true"));
    fireEvent.click(screen.getByRole("button", { name: "Navigate to paths" }));
    await waitFor(() => expect(screen.getByLabelText("host-route")).toHaveTextContent("/paths"));
    expect(screen.getByLabelText("host-busy")).toHaveTextContent("false");

    resolveAction({ event: { type: "PATHS_REQUESTED" } });
    await waitFor(() => expect(screen.getByLabelText("host-route")).toHaveTextContent("/paths"));
    expect(screen.getByLabelText("host-busy")).toHaveTextContent("false");
  });
});
