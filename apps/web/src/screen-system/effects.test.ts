import { describe, expect, it } from "vitest";
import { effectPlan } from "./effects";
describe("transition effects", () => {
  it("centralizes fade timing and reduced-motion behavior", () => {
    expect(effectPlan("FADE_TO_BLACK").durationMs).toBe(500);
    expect(effectPlan("FADE_TO_BLACK", true).durationMs).toBe(0);
    expect(effectPlan("NONE").durationMs).toBe(0);
  });
});
