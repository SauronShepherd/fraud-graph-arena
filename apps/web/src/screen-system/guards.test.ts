import { describe, expect, it } from "vitest";
import { guards } from "./guards";
describe("screen guards", () => {
  it("only evaluates safe presentation context", () => {
    expect(guards.REQUIRED_CONTEXT({ roundId: "r1" })).toBe(true);
    expect(guards.REQUIRED_CONTEXT({ roundId: "" })).toBe(false);
    expect(guards.ACTION_NOT_PENDING({})).toBe(true);
    expect(guards.ACTION_NOT_PENDING({ pendingAction: "OPEN_CASE" })).toBe(false);
  });
});
