import { describe, expect, it } from "vitest";
import { screenDefinitions } from "./definitions";
import { resolveTransition } from "./machine";

describe("screen machine", () => {
  it("walks the Academy journey through declared transitions", () => {
    const launch = screenDefinitions.get("LAUNCH")!;
    const paths = resolveTransition(launch, {}, { type: "PATHS_REQUESTED" }, screenDefinitions)!;
    expect(paths.target).toBe("PATH_SELECTION");
    const cases = resolveTransition(screenDefinitions.get(paths.target)!, {}, { type: "PATH_SELECTED", context: { pathId: "DETECTIVE_ACADEMY" } }, screenDefinitions)!;
    expect(cases.target).toBe("CASE_SELECTION");
    const intro = resolveTransition(screenDefinitions.get(cases.target)!, cases.context, { type: "CASE_OPENED", context: { roundId: "r1" } }, screenDefinitions)!;
    expect(intro.target).toBe("CASE_INTRODUCTION");
    const board = resolveTransition(screenDefinitions.get(intro.target)!, intro.context, { type: "INTRODUCTION_COMPLETED" }, screenDefinitions)!;
    expect(board.target).toBe("INVESTIGATION_BOARD");
    expect(board.effect).toBe("FADE_TO_BLACK");
    expect(board.history).toBe("REPLACE");
  });
  it("rejects events from the wrong screen and missing context", () => {
    expect(resolveTransition(screenDefinitions.get("LAUNCH")!, {}, { type: "INTRODUCTION_COMPLETED" }, screenDefinitions)).toBeNull();
    expect(resolveTransition(screenDefinitions.get("CASE_INTRODUCTION")!, {}, { type: "INTRODUCTION_COMPLETED" }, screenDefinitions)).toBeNull();
  });
});
