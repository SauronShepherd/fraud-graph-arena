import { describe, expect, it, vi } from "vitest";
import { lifecycle } from "./lifecycle";
describe("screen lifecycle registry", () => {
  it("executes registered focus, announcement and abort hooks", () => {
    const focus = vi.fn(); const announce = vi.fn(); const abort = vi.fn();
    const services = { focusPrimaryHeading: focus, announce, abortReads: abort };
    lifecycle.FOCUS_PRIMARY_HEADING(services); lifecycle.ANNOUNCE_SCREEN(services); lifecycle.ABORT_OBSOLETE_READS(services);
    expect(focus).toHaveBeenCalledOnce(); expect(announce).toHaveBeenCalledWith("Screen ready"); expect(abort).toHaveBeenCalledOnce();
  });
});
