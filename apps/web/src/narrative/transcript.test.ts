import { describe, expect, it } from "vitest";
import { AudioManager, type AudioStorage } from "./audio";
import { recordTranscriptOpen } from "./transcript";

function storage(): AudioStorage {
  const values = new Map<string, string>();
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  };
}

describe("narrative transcript disclosure", () => {
  it("records an opening but not a closing toggle", () => {
    const manager = new AudioManager(storage());
    const events: string[] = [];
    manager.subscribe((event) => events.push(event.type));

    recordTranscriptOpen({ open: false }, manager);
    recordTranscriptOpen({ open: true }, manager);

    expect(events).toEqual(["TRANSCRIPT_OPEN"]);
  });
});
