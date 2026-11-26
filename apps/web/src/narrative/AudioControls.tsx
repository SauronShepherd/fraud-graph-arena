import { useEffect, useState } from "react";
import { AudioManager, type AudioPreferences } from "./audio";

interface Props {
  manager: AudioManager;
}

export function AudioControls({ manager }: Props) {
  const [preferences, setPreferences] = useState<AudioPreferences>(manager.snapshot());

  useEffect(() => manager.subscribe((event) => {
    if (event.type === "PREFERENCES_CHANGED" || event.type === "MUTE_CHANGED") setPreferences(manager.snapshot());
  }), [manager]);

  function setBus(bus: "master" | "music" | "voice" | "effects", value: string) {
    setPreferences(manager.update({ [bus]: Number(value) }));
  }

  return (
    <section className="audio-controls" aria-labelledby="audio-controls-title">
      <div className="audio-controls__heading">
        <div>
          <p className="eyebrow">Optional sensory layer</p>
          <h2 id="audio-controls-title">The office can stay quiet</h2>
        </div>
        <button className="button secondary" type="button" onClick={() => setPreferences(manager.update({ muted: !preferences.muted }))}>
          {preferences.muted ? "Audio muted" : "Mute all audio"}
        </button>
      </div>
      <p className="audio-controls__note">No sound is required for evidence, scoring or submission. Nothing starts until you ask it to.</p>
      <div className="audio-buses">
        {(["master", "music", "voice", "effects"] as const).map((bus) => (
          <label key={bus}>
            <span>{bus === "master" ? "Master" : bus[0].toUpperCase() + bus.slice(1)}</span>
            <input type="range" min="0" max="1" step="0.05" value={preferences[bus]} onChange={(event) => setBus(bus, event.target.value)} aria-label={`${bus} volume`} />
          </label>
        ))}
      </div>
      <label className="audio-toggle">
        <input type="checkbox" checked={preferences.reducedSensory} onChange={(event) => setPreferences(manager.update({ reducedSensory: event.target.checked }))} />
        Reduced sensory mode
      </label>
    </section>
  );
}

export function useAudioManager(): AudioManager {
  // The manager owns the local preference boundary and is intentionally shared by
  // the current screen. A later app shell can lift this hook without changing it.
  const [manager] = useState(() => new AudioManager());
  return manager;
}
