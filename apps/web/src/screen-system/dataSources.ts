import * as api from "../api/client";
import { recalledRound } from "../state/session";
import type { DataSourceId, ScreenContext } from "./contracts";

export type ScreenModel = unknown;
export type DataSourceLoader = (context: ScreenContext, signal: AbortSignal) => Promise<ScreenModel>;
function required(context: ScreenContext, key: string): string { const value = context[key]; if (typeof value !== "string" || !value) throw new Error(`MISSING_CONTEXT:${key}`); return value; }
export const dataSources: Record<DataSourceId, DataSourceLoader> = {
  LAST_ROUND_POINTER: async () => ({ roundId: recalledRound() }),
  CATALOGUE_SECTIONS: async (_, signal) => api.listSections(signal),
  CATALOGUE_SECTION: async (context, signal) => api.getSection(required(context, "pathId"), signal),
  ROUND_OPENING: async (context, signal) => api.getOpening(required(context, "roundId"), signal),
  ROUND_WORKSPACE: async (context, signal) => api.getWorkspace(required(context, "roundId"), signal),
  RESOLUTION_CONTEXT: async () => ({ available: false })
};
