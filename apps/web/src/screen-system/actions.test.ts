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
});
