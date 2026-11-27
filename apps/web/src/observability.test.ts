import { beforeEach, describe, expect, it } from "vitest";
import { browserTraceId, frontendObservations, recordFrontendError } from "./observability";

describe("frontend observability", () => {
  beforeEach(() => {
    window.sessionStorage.clear();
  });

  it("keeps a session trace stable without accepting sensitive fields", () => {
    const first = browserTraceId();
    const second = browserTraceId();

    expect(first).toBe(second);
    recordFrontendError({ kind: "api", path: "/rounds", status: 503, code: "BACKEND_UNAVAILABLE" });
    expect(frontendObservations().at(-1)).toMatchObject({ trace_id: first, code: "BACKEND_UNAVAILABLE" });
    expect(JSON.stringify(frontendObservations())).not.toContain("player");
  });
});
