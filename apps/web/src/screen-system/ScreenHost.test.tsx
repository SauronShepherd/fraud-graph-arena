import { describe, expect, it } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { screenDefinitions } from "./definitions";
import { ScreenHost } from "./ScreenHost";
import { TransitionCoordinator } from "./TransitionCoordinator";
describe("screen host", () => {
  it("loads the screen model before focusing and announcing the view", async () => {
    const definition = screenDefinitions.get("LAUNCH")!;
    render(<MemoryRouter><TransitionCoordinator><ScreenHost definition={definition} screen="LAUNCH" context={{}}><h1 tabIndex={-1}>Launch</h1></ScreenHost></TransitionCoordinator></MemoryRouter>);
    expect(screen.getByRole("heading", { name: "Launch" })).toBeVisible();
    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("LAUNCH ready"));
    expect(screen.getByRole("heading", { name: "Launch" })).toHaveFocus();
  });
});
