import path from "node:path";
import { expect, test } from "@playwright/test";

test.describe("FGA06 renderer comparison exhibit", () => {
  test("serves a landing page from the root URL", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "FGA 06 Renderer Lab" })).toBeVisible();
    await expect(page.getByRole("link", { name: /Compare four graph engines/i })).toHaveAttribute("href", "./comparison-exhibit.html");
    await expect(page.getByRole("link", { name: /Open the SVG semantic baseline/i })).toHaveAttribute("href", "./exhibit.html");
  });

  test.beforeEach(async ({ page }) => {
    await page.goto("/comparison-exhibit.html");
    await expect(page.locator(".engine-card")).toHaveCount(4);
  });

  test("mounts all open-source engines and exposes manual controls", async ({ page }) => {
    await expect(page.getByRole("tab")).toHaveCount(4);
    await expect(page.locator(".engine-card")).toHaveCount(4);
    await expect(page.locator(".engine-card:not([hidden]) .engine-surface")).toBeVisible();
    await expect(page.locator(".engine-card:not([hidden]) button[data-action='fit']")).toBeVisible();
    await expect(page.locator(".engine-card:not([hidden]) button[data-action='node']")).toBeVisible();
    await expect(page.locator(".engine-card:not([hidden]) button[data-action='edge']")).toBeVisible();
    await expect(page.locator("#inspector input[data-check]")).toHaveCount(5);
    await expect(page.locator(".engine-card:not([hidden]) .minimap")).toBeVisible();
    await page.screenshot({ path: path.resolve(process.cwd(), "../../reports/iteration-06/renderer-exhibit-manual-2026-11-03.png"), fullPage: true });
  });

  test("runs the same lifecycle and selection probes for every engine", async ({ page }) => {
    await page.getByTestId("run-all").click();
    await expect(page.locator("[data-role='auto-badge']")).toHaveCount(4);
    for (let index = 0; index < 4; index += 1) {
      await expect(page.locator(".engine-card").nth(index).locator("[data-role='auto-badge']")).toHaveText("AUTO PASS");
      await expect(page.locator(".engine-card").nth(index).locator("[data-role='auto-result']")).toContainText("selection probes passed");
    }
    await expect(page.getByTestId("report")).toContainText('"schema": "fga06-renderer-comparison-v3"');
    await expect(page.getByTestId("report")).toContainText('"fixture_sha256": "');
    await expect(page.getByTestId("report")).toContainText('"nodes": 18');
    await expect(page.getByTestId("report")).toContainText('"edges": 26');
    await expect(page.getByTestId("report")).toContainText('"selectedNodeId"');
    const downloadPromise = page.waitForEvent("download");
    await page.locator("#download-report").click();
    const download = await downloadPromise;
    await download.saveAs(path.resolve(process.cwd(), "../../reports/iteration-06/renderer-comparison-fga-2026-11-03.json"));
  });

  test("manual probe controls report stable FGA selections", async ({ page }) => {
    const tabs = page.getByRole("tab");
    for (let index = 0; index < 4; index += 1) {
      await tabs.nth(index).click();
      const card = page.locator(".engine-card:not([hidden])");
      await card.locator("button[data-action='node']").click();
      await card.locator("button[data-action='edge']").click();
      await expect(page.locator("#inspector")).toContainText("FIX-E-0000");
      await expect(page.locator("#inspector")).toContainText("DIRECTOR_OF");
      await card.locator("button[data-action='fit']").click();
      await card.locator("button[data-action='zoom-in']").click();
      await card.locator("button[data-action='reset']").click();
      await expect(page.locator("#inspector")).toContainText("3/5");
    }
  });

  test("opens contextual node and relationship menus in every engine tab", async ({ page }) => {
    const tabs = page.getByRole("tab");
    for (let index = 0; index < 4; index += 1) {
      await tabs.nth(index).click();
      const card = page.locator(".engine-card:not([hidden])");
      await card.locator("button[data-action='node']").click();
      await expect(page.locator("#inspector")).toContainText(/context menu · node/i);
      await expect(page.locator("#inspector")).toContainText("Stable ID");
      await card.locator("button[data-action='edge']").click();
      await expect(page.locator("#inspector")).toContainText(/context menu · relationship/i);
      await expect(page.locator("#inspector")).toContainText("DIRECT_SOURCE");
    }
  });
});
