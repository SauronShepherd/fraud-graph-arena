import { describe, expect, it } from "vitest";
import { screenDefinitions, screenConfigurationError } from "./definitions";

describe("screen definition fail-closed boundary", () => {
  it("exports a validated definition map or a safe configuration error", () => {
    expect(screenConfigurationError === null || screenDefinitions.size === 0).toBe(true);
  });
});
