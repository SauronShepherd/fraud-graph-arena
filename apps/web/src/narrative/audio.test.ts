import { describe, expect, it } from "vitest";
import { AUDIO_PREFERENCES_KEY, AudioManager, type AudioStorage } from "./audio";

function storage(): AudioStorage {
  const values = new Map<string, string>();
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  };
}

describe("FGA-15 optional audio layer", () => {
  it("persists independent bus preferences and mute state", () => {
    const saved = storage();
    const manager = new AudioManager(saved);

    manager.update({ music: 0.25, voice: 0.5, muted: true, reducedSensory: true });
    const restored = new AudioManager(saved);

    expect(restored.snapshot()).toMatchObject({ music: 0.25, voice: 0.5, muted: true, reducedSensory: true });
    expect(saved.getItem(AUDIO_PREFERENCES_KEY)).toContain("reducedSensory");
  });

  it("falls back to text when an optional asset is missing or autoplay is not allowed", async () => {
    const events: string[] = [];
    const manager = new AudioManager(storage());
    manager.subscribe((event) => events.push(event.type));

    await expect(manager.play({ id: "missing-voice", src: null, bus: "voice" })).resolves.toBe("FALLBACK");
    await expect(manager.play({ id: "blocked-voice", src: "/optional.ogg", bus: "voice" })).resolves.toBe("FALLBACK");

    expect(events).toEqual(["MISSING_ASSET", "FALLBACK_ACTIVATED", "AUTOPLAY_BLOCKED", "FALLBACK_ACTIVATED"]);
  });

  it("suppresses playback in reduced-sensory mode without changing the transcript", async () => {
    const manager = new AudioManager(storage());
    manager.update({ reducedSensory: true });

    await expect(manager.play({ id: "panel-click", src: "/click.ogg", bus: "effects" })).resolves.toBe("SUPPRESSED");
  });
});
