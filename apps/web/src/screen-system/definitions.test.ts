import { describe, expect, it } from "vitest";
import { screenSet, validateScreenSet } from "./definitions";
import { ScreenConfigurationError } from "./contracts";
import validationCases from "./test-fixtures/validation-cases.json";

function setPath(root: unknown, path: (string | number)[], value: unknown): void {
  let target = root as Record<string | number, unknown>;
  for (const segment of path.slice(0, -1)) target = target[segment] as Record<string | number, unknown>;
  target[path[path.length - 1]] = value;
}

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

  it("rejects ambiguous public routes and route parameters without required context", () => {
    const collision = structuredClone(screenSet);
    collision.screens[1].route.pattern = "/";
    try { validateScreenSet(collision); throw new Error("EXPECTED_CONFIGURATION_ERROR"); }
    catch (error) { expect((error as ScreenConfigurationError).diagnostics).toContain("AMBIGUOUS_PUBLIC_ROUTE:LAUNCH:PATH_SELECTION"); }

    const missingContext = structuredClone(screenSet);
    missingContext.screens.find((screen) => screen.id === "CASE_SELECTION")!.validation.required_context = [];
    try { validateScreenSet(missingContext); throw new Error("EXPECTED_CONFIGURATION_ERROR"); }
    catch (error) { expect((error as ScreenConfigurationError).diagnostics).toContain("ROUTE_CONTEXT_MISSING:CASE_SELECTION:pathId"); }
  });

  it("rejects every shared semantic-invalid fixture like the build validator", () => {
    for (const fixture of validationCases) {
      const candidate = structuredClone(screenSet);
      setPath(candidate, fixture.path, fixture.value);
      expect(() => validateScreenSet(candidate), fixture.name).toThrow(ScreenConfigurationError);
    }
  });
});
