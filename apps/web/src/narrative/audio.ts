export type AudioBus = "master" | "music" | "voice" | "effects";

export interface AudioPreferences {
  master: number;
  music: number;
  voice: number;
  effects: number;
  muted: boolean;
  reducedSensory: boolean;
  autoplayAllowed: boolean;
}

export type NarrativeEventType =
  | "PLAYBACK_START"
  | "PLAYBACK_STOP"
  | "MUTE_CHANGED"
  | "MISSING_ASSET"
  | "TRANSCRIPT_OPEN"
  | "FALLBACK_ACTIVATED"
  | "AUTOPLAY_BLOCKED"
  | "STACK_SUPPRESSED"
  | "PREFERENCES_CHANGED";

export interface NarrativeEvent {
  type: NarrativeEventType;
  assetId?: string;
}

export interface AudioStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}

export interface OptionalAudioAsset {
  id: string;
  src: string | null;
  bus: Exclude<AudioBus, "master">;
  maxConcurrency?: number;
}

export const AUDIO_PREFERENCES_KEY = "fga.narrativeAudio.v1";

export const DEFAULT_AUDIO_PREFERENCES: AudioPreferences = {
  master: 1,
  music: 0.7,
  voice: 1,
  effects: 0.8,
  muted: false,
  reducedSensory: false,
  autoplayAllowed: false,
};

function fallbackStorage(): AudioStorage {
  if (typeof window !== "undefined" && window.localStorage) return window.localStorage;
  const values = new Map<string, string>();
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  };
}

function clamp(value: number): number {
  return Math.min(1, Math.max(0, Number.isFinite(value) ? value : 0));
}

function readPreferences(storage: AudioStorage): AudioPreferences {
  try {
    const raw = storage.getItem(AUDIO_PREFERENCES_KEY);
    if (!raw) return { ...DEFAULT_AUDIO_PREFERENCES };
    const parsed = JSON.parse(raw) as Partial<AudioPreferences>;
    return {
      master: clamp(parsed.master ?? DEFAULT_AUDIO_PREFERENCES.master),
      music: clamp(parsed.music ?? DEFAULT_AUDIO_PREFERENCES.music),
      voice: clamp(parsed.voice ?? DEFAULT_AUDIO_PREFERENCES.voice),
      effects: clamp(parsed.effects ?? DEFAULT_AUDIO_PREFERENCES.effects),
      muted: Boolean(parsed.muted ?? DEFAULT_AUDIO_PREFERENCES.muted),
      reducedSensory: Boolean(parsed.reducedSensory ?? DEFAULT_AUDIO_PREFERENCES.reducedSensory),
      autoplayAllowed: Boolean(parsed.autoplayAllowed ?? DEFAULT_AUDIO_PREFERENCES.autoplayAllowed),
    };
  } catch {
    return { ...DEFAULT_AUDIO_PREFERENCES };
  }
}

export class AudioManager {
  private preferences: AudioPreferences;
  private readonly listeners = new Set<(event: NarrativeEvent) => void>();
  private readonly activeByBus = new Map<Exclude<AudioBus, "master">, number>();

  constructor(private readonly storage: AudioStorage = fallbackStorage()) {
    this.preferences = readPreferences(storage);
  }

  snapshot(): AudioPreferences {
    return { ...this.preferences };
  }

  subscribe(listener: (event: NarrativeEvent) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  record(type: NarrativeEventType, assetId?: string): void {
    const event = assetId ? { type, assetId } : { type };
    this.listeners.forEach((listener) => listener(event));
  }

  update(patch: Partial<AudioPreferences>): AudioPreferences {
    const next: AudioPreferences = {
      ...this.preferences,
      ...patch,
      master: clamp(patch.master ?? this.preferences.master),
      music: clamp(patch.music ?? this.preferences.music),
      voice: clamp(patch.voice ?? this.preferences.voice),
      effects: clamp(patch.effects ?? this.preferences.effects),
    };
    this.preferences = next;
    this.storage.setItem(AUDIO_PREFERENCES_KEY, JSON.stringify(next));
    if (patch.muted !== undefined) this.record("MUTE_CHANGED");
    this.record("PREFERENCES_CHANGED");
    return this.snapshot();
  }

  async play(asset: OptionalAudioAsset): Promise<"PLAYING" | "FALLBACK" | "SUPPRESSED"> {
    if (!asset.src) {
      this.record("MISSING_ASSET", asset.id);
      this.record("FALLBACK_ACTIVATED", asset.id);
      return "FALLBACK";
    }
    if (this.preferences.muted || this.preferences.reducedSensory) return "SUPPRESSED";
    if (!this.preferences.autoplayAllowed) {
      this.record("AUTOPLAY_BLOCKED", asset.id);
      this.record("FALLBACK_ACTIVATED", asset.id);
      return "FALLBACK";
    }
    if (typeof Audio === "undefined") {
      this.record("MISSING_ASSET", asset.id);
      this.record("FALLBACK_ACTIVATED", asset.id);
      return "FALLBACK";
    }
    const active = this.activeByBus.get(asset.bus) ?? 0;
    if (active >= (asset.maxConcurrency ?? 1)) {
      this.record("STACK_SUPPRESSED", asset.id);
      return "SUPPRESSED";
    }
    const element = new Audio(asset.src);
    const volume = this.preferences.master * this.preferences[asset.bus];
    element.volume = clamp(volume);
    this.activeByBus.set(asset.bus, active + 1);
    this.record("PLAYBACK_START", asset.id);
    try {
      await element.play();
      element.addEventListener("ended", () => {
        this.activeByBus.set(asset.bus, Math.max(0, (this.activeByBus.get(asset.bus) ?? 1) - 1));
        this.record("PLAYBACK_STOP", asset.id);
      }, { once: true });
      return "PLAYING";
    } catch {
      this.activeByBus.set(asset.bus, Math.max(0, (this.activeByBus.get(asset.bus) ?? 1) - 1));
      this.record("AUTOPLAY_BLOCKED", asset.id);
      this.record("FALLBACK_ACTIVATED", asset.id);
      return "FALLBACK";
    }
  }
}
