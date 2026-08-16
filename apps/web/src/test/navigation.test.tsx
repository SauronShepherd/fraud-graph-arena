import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { App } from "../App";

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" }
  });
}

const paths = {
  sections: [
    {
      id: "DETECTIVE_ACADEMY",
      name: "Detective Academy",
      description: "The public training laboratory.",
      ranked: false,
      status: "OPEN",
      access_message: "Academy doors are open."
    },
    {
      id: "PUPPY",
      name: "Puppy",
      description: "The first ranked trail.",
      ranked: true,
      status: "COMING_SOON",
      access_message: "Ranked cases remain sealed."
    }
  ]
};

const section = {
  path: paths.sections[0],
  cases: [
    {
      id: "ACADEMY_001",
      version: "1.0.0-i01",
      path_id: "DETECTIVE_ACADEMY",
      name: "The Case of the Empty Evidence Board",
      description: "Spoiler-free training file.",
      status: "OPEN"
    }
  ]
};

const pendingRound = {
  id: "round-1",
  player_id: "demo-hercule",
  path_id: "DETECTIVE_ACADEMY",
  case_id: "ACADEMY_001",
  case_version: "1.0.0-i01",
  status: "INTRO_PENDING",
  created_at: "2026-08-03T00:00:00Z",
  started_at: "2026-08-03T00:00:01Z",
  intro_completed_at: null
};

const activeRound = {
  ...pendingRound,
  status: "ACTIVE",
  intro_completed_at: "2026-08-03T00:00:02Z"
};

const opening = {
  round: pendingRound,
  case: section.cases[0],
  sequence: {
    id: "ACADEMY_001_OPENING",
    case_id: "ACADEMY_001",
    case_version: "1.0.0-i01",
    kind: "OPENING",
    skippable: true,
    pages: [
      {
        id: "INTRO_1",
        position: 1,
        title: "The Academy Door",
        narration: "Hercule reports for training.",
        image_url: "/assets/academy-intro-01.svg",
        alt_text: "Hercule at the Academy door."
      },
      {
        id: "INTRO_2",
        position: 2,
        title: "A Board with Nothing to Hide",
        narration: "The empty board waits.",
        image_url: "/assets/academy-intro-02.svg",
        alt_text: "Hercule facing an empty training board."
      }
    ]
  }
};

const workspace = {
  round: activeRound,
  case: section.cases[0],
  board_message: "The Academy workspace is intentionally empty.",
  evidence_count: 0,
  suspect_count: 0
  ,path_name: "Detective Academy",
  empty_state_code: "NO_EVIDENCE_REVEALED",
  actions: [
    { id: "COMPARE_IDENTITIES", state: "NOT_IMPLEMENTED", reason_code: "CAPABILITY_NOT_IMPLEMENTED", reason: "Identity comparison is not available in Academy yet." },
    { id: "FIND_SHARED_FIELDS", state: "NOT_IMPLEMENTED", reason_code: "CAPABILITY_NOT_IMPLEMENTED", reason: "Exact shared-field analysis is not available in Academy yet." },
    { id: "SEARCH_EVIDENCE", state: "NOT_IMPLEMENTED", reason_code: "CAPABILITY_NOT_IMPLEMENTED", reason: "Evidence search will unlock when the case publishes evidence." },
    { id: "OPEN_CASE_FILE", state: "NOT_IMPLEMENTED", reason_code: "CAPABILITY_NOT_IMPLEMENTED", reason: "Case-file construction is not available in the empty Academy round." }
  ]
};

describe("walking skeleton navigation", () => {
  it("carries Academy 001 through its opening comic to the board", async () => {
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse(paths))
      .mockResolvedValueOnce(jsonResponse(section))
      .mockResolvedValueOnce(jsonResponse({ ...pendingRound, status: "CREATED" }, 201))
      .mockResolvedValueOnce(jsonResponse(pendingRound))
      .mockResolvedValueOnce(jsonResponse(opening))
      .mockResolvedValueOnce(jsonResponse(activeRound))
      .mockResolvedValueOnce(jsonResponse(workspace));

    render(<MemoryRouter initialEntries={["/"]}><App /></MemoryRouter>);

    fireEvent.click(screen.getByRole("link", { name: /choose your trench coat/i }));
    expect(await screen.findByRole("button", { name: /puppy/i })).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: /detective academy/i }));
    fireEvent.click(await screen.findByRole("button", { name: /open training case/i }));

    expect(await screen.findByRole("heading", { name: "The Academy Door" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: /next page/i }));
    expect(await screen.findByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: /enter the academy/i }));
    await waitFor(() => expect(globalThis.fetch).toHaveBeenCalledTimes(7));
    expect(await screen.findByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeVisible();
    expect(screen.getByText("ACADEMY_001")).toBeVisible();
    expect(screen.getAllByText(/no evidence has been revealed/i)).toHaveLength(2);
    expect(screen.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /compare identities/i })).toBeDisabled();
  });

  it("reconstructs an active Academy board directly from its round route", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(jsonResponse(workspace));

    render(
      <MemoryRouter initialEntries={["/rounds/round-1/board"]}>
        <App />
      </MemoryRouter>
    );

    await waitFor(() => expect(screen.getByText("ACADEMY_001")).toBeVisible());
    expect(window.localStorage.getItem("fga.lastRoundId")).toBe("round-1");
  });

  it("reconstructs a comic page from the URL instead of component-local memory", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(jsonResponse(opening));

    render(
      <MemoryRouter initialEntries={["/rounds/round-1/intro?page=2"]}>
        <App />
      </MemoryRouter>
    );

    expect(await screen.findByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
    expect(screen.getByText(/page 2 of 2/i)).toBeVisible();
  });
});
