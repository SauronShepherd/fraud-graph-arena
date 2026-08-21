import { useEffect, useState } from "react";
import { ApiProblem } from "../api/client";
import type { ProblemDetails } from "../api/contracts";
import type { DataSourceId, ScreenContext } from "./contracts";
import { dataSources, type ScreenModel } from "./dataSources";
export function apiProblem(error: unknown): ProblemDetails | null { return error instanceof ApiProblem ? error.problem : null; }
export function useScreenData<T extends ScreenModel>(source: DataSourceId, context: ScreenContext, key: string): { model: T | null; problem: ProblemDetails | null; retry: () => void } {
  const [model, setModel] = useState<T | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => { const controller = new AbortController(); setProblem(null); setModel(null); dataSources[source](context, controller.signal).then((value) => { if (!controller.signal.aborted) setModel(value as T); }).catch((error: unknown) => { if (!controller.signal.aborted && error instanceof ApiProblem) setProblem(error.problem); }); return () => controller.abort(); }, [source, key, attempt]);
  return { model, problem, retry: () => setAttempt((value) => value + 1) };
}
