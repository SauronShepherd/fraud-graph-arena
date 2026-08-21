import { afterEach, describe, expect, it, vi } from "vitest";
import { ScreenLoadCoordinator } from "./loadCoordinator";

describe("screen load coordinator", () => {
  afterEach(() => vi.restoreAllMocks());
  it("aborts the previous screen read when a new read starts", async () => {
    vi.spyOn(globalThis, "fetch").mockImplementation((_input, init) => new Promise((_resolve, reject) => {
      init?.signal?.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
    }) as Promise<Response>);
    const coordinator = new ScreenLoadCoordinator();
    const first = coordinator.load("CATALOGUE_SECTIONS", {});
    const second = coordinator.load("CATALOGUE_SECTIONS", {});
    coordinator.abort();
    await expect(Promise.allSettled([first, second])).resolves.toHaveLength(2);
  });
});
