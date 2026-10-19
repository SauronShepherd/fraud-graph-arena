import { describe, expect, it } from "vitest";
import { screenSet, validateScreenSet } from "./definitions";
import { ScreenConfigurationError } from "./contracts";

describe("screen definition validation", () => {
  it("accepts the production screen set and its per-screen versions", () => {
    expect(validateScreenSet(screenSet).size).toBe(6);
    expect(screenSet.screens.every((screen) => screen.document_version && screen.minimum_runtime_version)).toBe(true);
  });

  it("rejects definitions that require a newer runtime", () => {
    const candidate = structuredClone(screenSet);
    candidate.screens[0].minimum_runtime_version = "1.1.0";
    expect(() => validateScreenSet(candidate)).toThrow(ScreenConfigurationError);
  });

  it("rejects unsupported fields at runtime startup", () => {
    const candidate = structuredClone(screenSet) as unknown as Record<string, unknown>;
    (candidate.screens as Array<Record<string, unknown>>)[0].executable = "return true";
    try { validateScreenSet(candidate); throw new Error("EXPECTED_CONFIGURATION_ERROR"); }
    catch (error) { expect(error).toBeInstanceOf(ScreenConfigurationError); expect((error as ScreenConfigurationError).diagnostics).toContain("UNKNOWN_FIELD:screens[0].executable"); }
  });

  it("reports malformed screen records without crashing the validator", () => {
    const candidate = structuredClone(screenSet) as unknown as Record<string, unknown>;
    (candidate.screens as unknown[])[0] = { id: "LAUNCH" };
    expect(() => validateScreenSet(candidate)).toThrow(ScreenConfigurationError);
  });
});
