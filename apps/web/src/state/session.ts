const LAST_ROUND_KEY = "fga.lastRoundId";

export function rememberRound(roundId: string): void {
  window.localStorage.setItem(LAST_ROUND_KEY, roundId);
}

export function recalledRound(): string | null {
  return window.localStorage.getItem(LAST_ROUND_KEY);
}

export function forgetRound(): void {
  window.localStorage.removeItem(LAST_ROUND_KEY);
}
