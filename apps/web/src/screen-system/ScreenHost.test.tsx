import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { screenDefinitions } from "./definitions";
import { ScreenHost } from "./ScreenHost";
describe("screen host", () => {
  it("mounts a semantic screen and live announcement", () => {
    const definition = screenDefinitions.get("LAUNCH")!;
    render(<ScreenHost definition={definition} screen="LAUNCH"><h1 tabIndex={-1}>Launch</h1></ScreenHost>);
    expect(screen.getByRole("heading", { name: "Launch" })).toBeVisible();
    expect(screen.getByRole("status")).toHaveTextContent("Screen ready");
  });
});
