import { describe, expect, it } from "vitest";
import { screenDefinitions } from "./definitions";
import { locationFor, parseLocation } from "./routeCodec";

describe("screen route codec", () => {
  it("round-trips encoded round identifiers and intro page", () => {
    const definition = screenDefinitions.get("CASE_INTRODUCTION")!;
    const location = locationFor(definition, { roundId: "round/a", page: 2 });
    expect(parseLocation(location.split("?")[0], `?${location.split("?")[1]}`, screenDefinitions)).toMatchObject({ screen: "CASE_INTRODUCTION", context: { roundId: "round/a", page: 2 } });
  });
  it("fails unknown routes closed to launch", () => {
    expect(parseLocation("/not-a-screen", "", screenDefinitions)).toMatchObject({ screen: "LAUNCH", replace: true });
  });
});
