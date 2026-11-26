import type { AudioManager } from "./audio";

export function recordTranscriptOpen(details: Pick<HTMLDetailsElement, "open">, audioManager: AudioManager): void {
  if (details.open) audioManager.record("TRANSCRIPT_OPEN");
}
