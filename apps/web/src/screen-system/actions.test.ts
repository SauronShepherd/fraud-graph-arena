import { describe, expect, it, vi } from "vitest";
import { actions } from "./actions";
import * as api from "../api/client";
vi.mock("../api/client", async () => ({ ...(await vi.importActual<typeof import("../api/client")>("../api/client")), createAndStartRound: vi.fn() }));
describe("semantic actions", () => {
  it("emits semantic events and preserves context", async () => {
    await expect(actions.BEGIN({ context: {} })).resolves.toMatchObject({ event: { type: "PATHS_REQUESTED" } });
    await expect(actions.SELECT_PATH({ context: {}, payload: { pathId: "DETECTIVE_ACADEMY" } })).resolves.toMatchObject({ event: { type: "PATH_SELECTED" } });
  });
  it("deduplicates an accepted open-case request while pending", async () => {
    let resolveRound!: (value: Awaited<ReturnType<typeof api.createAndStartRound>>) => void;
    vi.mocked(api.createAndStartRound).mockImplementation(() => new Promise((resolve) => { resolveRound = resolve; }));
    const first = actions.OPEN_CASE({ context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_001" } });
    await expect(actions.OPEN_CASE({ context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_001" } })).rejects.toThrow("ACTION_PENDING");
    resolveRound({ id: "round-1" } as Awaited<ReturnType<typeof api.createAndStartRound>>);
    await first;
  });

  it("does not block a different screen instance", async () => {
    const resolves: Array<(value: Awaited<ReturnType<typeof api.createAndStartRound>>) => void> = [];
    vi.mocked(api.createAndStartRound).mockImplementation(() => new Promise((resolve) => { resolves.push(resolve); }));
    const first = actions.OPEN_CASE({ instanceId: "screen-a", context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_001" } });
    const second = actions.OPEN_CASE({ instanceId: "screen-b", context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_001" } });
    resolves[0]({ id: "round-a" } as Awaited<ReturnType<typeof api.createAndStartRound>>);
    await expect(first).resolves.toMatchObject({ context: { roundId: "round-a" } });
    resolves[1]({ id: "round-b" } as Awaited<ReturnType<typeof api.createAndStartRound>>);
    await expect(second).resolves.toMatchObject({ context: { roundId: "round-b" } });
  });

  it("forwards the retry-stable command key to the API", async () => {
    vi.mocked(api.createAndStartRound).mockResolvedValue({ id: "round-keyed" } as Awaited<ReturnType<typeof api.createAndStartRound>>);
    await actions.OPEN_CASE({ instanceId: "screen-keyed", context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_001", commandKey: "intent-123" } });
    expect(api.createAndStartRound).toHaveBeenCalledWith("DETECTIVE_ACADEMY", "ACADEMY_001", "intent-123");
  });

  it("reuses an uncertain OPEN_CASE command key after failure", async () => {
    vi.mocked(api.createAndStartRound)
      .mockRejectedValueOnce(new Error("network outcome uncertain"))
      .mockResolvedValueOnce({ id: "round-replayed" } as Awaited<ReturnType<typeof api.createAndStartRound>>);
    const input = { instanceId: "screen-retry", context: { pathId: "DETECTIVE_ACADEMY" }, payload: { caseId: "ACADEMY_002" } };
    await expect(actions.OPEN_CASE(input)).rejects.toThrow("network outcome uncertain");
    await actions.OPEN_CASE({ ...input, instanceId: "screen-after-navigation" });
    const firstKey = vi.mocked(api.createAndStartRound).mock.calls.at(-2)?.[2];
    const secondKey = vi.mocked(api.createAndStartRound).mock.calls.at(-1)?.[2];
    expect(firstKey).toBeTruthy();
    expect(secondKey).toBe(firstKey);
  });
});
