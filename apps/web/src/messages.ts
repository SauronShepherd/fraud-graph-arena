export type MessageId = "board.tools" | "board.toolsUnavailable" | "board.trainingRound" | "board.backToAcademy";
type MessageCatalogue = Record<MessageId, string>;

const ENGLISH: MessageCatalogue = {
  "board.tools": "Investigation tools",
  "board.toolsUnavailable": "Academy tools · unavailable",
  "board.trainingRound": "Training round:",
  "board.backToAcademy": "Back to Academy catalogue",
};

function pseudo(text: string): string {
  const substitutions: Record<string, string> = { a: "à", e: "ë", i: "ï", o: "ô", u: "ü", A: "À", E: "Ë", I: "Ï", O: "Ô", U: "Ü" };
  return `[${[...text].map((character) => substitutions[character] ?? character).join("")}]`;
}

export function message(id: MessageId, locale = "en"): string {
  const value = ENGLISH[id];
  return locale.toLowerCase() === "pseudo" ? pseudo(value) : value;
}
