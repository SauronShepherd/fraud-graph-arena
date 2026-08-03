import { describe, expect, it } from "vitest";
import { forgetRound, recalledRound, rememberRound } from "../state/session";

describe("round session pointer", () => {
  it("stores only the round identifier needed to reconstruct authoritative state", () => {
    rememberRound("round-42");
    expect(recalledRound()).toBe("round-42");
    expect(window.localStorage.length).toBe(1);
  });

  it("can forget the pointer without pretending to delete server state", () => {
    rememberRound("round-42");
    forgetRound();
    expect(recalledRound()).toBeNull();
  });
});
