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
  it("normalizes invalid intro pages and malformed percent escapes", () => {
    expect(parseLocation("/rounds/r1/intro", "?page=-4", screenDefinitions)).toMatchObject({ screen: "CASE_INTRODUCTION", context: { roundId: "r1", page: 1 }, replace: true });
    expect(parseLocation("/rounds/%E0%A4%A/intro", "", screenDefinitions)).toMatchObject({ screen: "LAUNCH", replace: true });
  });
  it("normalizes non-canonical numeric aliases for intro pages", () => {
    expect(parseLocation("/rounds/r1/intro", "?page=1.0", screenDefinitions)).toMatchObject({ screen: "CASE_INTRODUCTION", context: { roundId: "r1", page: 1 }, replace: true });
    expect(parseLocation("/rounds/r1/intro", "?page=02", screenDefinitions)).toMatchObject({ screen: "CASE_INTRODUCTION", context: { roundId: "r1", page: 2 }, replace: true });
  });
  it("treats route literals as literals instead of regular expression syntax", () => {
    const definition = screenDefinitions.get("PATH_SELECTION")!;
    const literal = { ...definition, route: { mode: "PUBLIC" as const, pattern: "/paths.v1" } };
    expect(parseLocation("/paths.v1", "", new Map([["PATH_SELECTION", literal]]))).toMatchObject({ screen: "PATH_SELECTION" });
    expect(parseLocation("/pathsXv1", "", new Map([["PATH_SELECTION", literal]]))).toMatchObject({ screen: "LAUNCH", replace: true });
  });
});
