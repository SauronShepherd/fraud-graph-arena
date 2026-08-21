import { useEffect, useState } from "react";
import { ApiProblem } from "../api/client";
import type { ProblemDetails } from "../api/contracts";
import type { DataSourceId, ScreenContext } from "./contracts";
import { type ScreenModel } from "./dataSources";
import { useScreenRuntime } from "./ScreenRuntimeContext";
export function apiProblem(error: unknown): ProblemDetails | null { return error instanceof ApiProblem ? error.problem : null; }
export function useScreenData<T extends ScreenModel>(source: DataSourceId, context: ScreenContext, key: string): { model: T | null; problem: ProblemDetails | null; retry: () => void } {
  const runtime = useScreenRuntime();
  const [model, setModel] = useState<T | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => { let active = true; setProblem(null); setModel(null); runtime.loadScreenModel(source, context).then((value) => { if (active) setModel(value as T); }).catch((error: unknown) => { if (active && error instanceof ApiProblem) setProblem(error.problem); }); return () => { active = false; }; }, [source, key, attempt]);
  return { model, problem, retry: () => setAttempt((value) => value + 1) };
}
