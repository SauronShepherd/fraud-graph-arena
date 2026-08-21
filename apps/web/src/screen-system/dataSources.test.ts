import { describe, expect, it } from "vitest";
import { dataSources } from "./dataSources";
describe("screen data sources", () => {
  it("requires safe route context before loading round data", async () => {
    await expect(dataSources.ROUND_WORKSPACE({}, new AbortController().signal)).rejects.toThrow("MISSING_CONTEXT:roundId");
  });
  it("does not expose production resolution data", async () => {
    await expect(dataSources.RESOLUTION_CONTEXT({}, new AbortController().signal)).resolves.toEqual({ available: false });
  });
});
