import { describe, expect, it } from "vitest";
import { dataSources } from "./dataSources";
import { vi } from "vitest";
import * as api from "../api/client";
vi.mock("../api/client");
describe("screen data sources", () => {
  it("requires safe route context before loading round data", async () => {
    await expect(dataSources.ROUND_WORKSPACE({}, new AbortController().signal)).rejects.toThrow("MISSING_CONTEXT:roundId");
  });
  it("loads the public resolution receipt with its round context", async () => {
    vi.mocked(api.getResolutionContext).mockResolvedValue({ available: true, submission: {} as never, ledger: { entries: [] } });
    await expect(dataSources.RESOLUTION_CONTEXT({ roundId: "r1" }, new AbortController().signal)).resolves.toMatchObject({ available: true });
    expect(api.getResolutionContext).toHaveBeenCalledWith("r1", expect.any(AbortSignal));
  });
});
