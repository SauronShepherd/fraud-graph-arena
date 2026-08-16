import { describe, expect, it } from "vitest";
import { message } from "../messages";

describe("message catalogue", () => {
  it("returns stable English copy", () => expect(message("board.tools")).toBe("Investigation tools"));
  it("supports deterministic pseudo-localization", () => expect(message("board.tools", "pseudo")).toBe("[Ïnvëstïgàtïôn tôôls]"));
});
