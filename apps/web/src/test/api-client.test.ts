import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiProblem, completeOpening, createAndStartRound, getOpening, getWorkspace } from "../api/client";

const response = (body: unknown, status = 200, contentType = "application/json") =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": contentType, "x-correlation-id": "server-1" }
  });

describe("API client contracts", () => {
  beforeEach(() => vi.restoreAllMocks());

  it("creates and starts the spoiler-free Academy round", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(response({ id: "r1", status: "CREATED" }, 201))
      .mockResolvedValueOnce(response({ id: "r1", status: "INTRO_PENDING" }));

    const round = await createAndStartRound("DETECTIVE_ACADEMY", "ACADEMY_001");

    expect(round).toMatchObject({ id: "r1", status: "INTRO_PENDING" });
    expect(fetchMock.mock.calls[0]?.[1]?.body).toBe(JSON.stringify({
      player_id: "demo-hercule",
      path_id: "DETECTIVE_ACADEMY",
      case_id: "ACADEMY_001"
    }));
  });

  it("uses explicit opening contracts before requesting the board", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(response({ sequence: { kind: "OPENING", pages: [] } }))
      .mockResolvedValueOnce(response({ id: "r1", status: "ACTIVE" }));

    await getOpening("r1");
    await completeOpening("r1");

    expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/v1/rounds/r1/opening");
    expect(fetchMock.mock.calls[1]?.[0]).toBe("/api/v1/rounds/r1/opening/complete");
    expect(fetchMock.mock.calls[1]?.[1]?.method).toBe("POST");
  });

  it("preserves problem details instead of inventing a frontend error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(response({
      type: "about:blank",
      title: "Introduction required",
      status: 409,
      detail: "Finish the briefing",
      instance: "/rounds/x/workspace",
      code: "INTRO_REQUIRED",
      correlation_id: "server-1"
    }, 409, "application/problem+json"));

    await expect(getWorkspace("x")).rejects.toMatchObject({
      problem: { code: "INTRO_REQUIRED" }
    });
  });
});
