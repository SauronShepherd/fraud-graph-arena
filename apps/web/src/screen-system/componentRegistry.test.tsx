import { describe, expect, it } from "vitest";
import { componentRegistry, resolveComponent } from "./componentRegistry";
describe("screen component registry", () => {
  it("registers every playable screen family", () => {
    expect(Object.keys(componentRegistry)).toEqual(expect.arrayContaining(["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD", "CASE_RESOLUTION"]));
  });
  it("resolves the internal resolution family without making it reachable", () => { expect(resolveComponent("CASE_RESOLUTION")).toBeDefined(); });
});
