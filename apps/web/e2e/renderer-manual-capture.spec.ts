import path from "node:path";
import { expect, test } from "@playwright/test";

test("captures each renderer tab for human review", async ({ page }) => {
  await page.goto("/comparison-exhibit.html");
  const tabs = page.getByRole("tab");
  await expect(tabs).toHaveCount(4);
  for (let index = 0; index < 4; index += 1) {
    await tabs.nth(index).click();
    const card = page.locator(".engine-card:not([hidden])");
    await card.locator("button[data-action='node']").click();
    await expect(page.locator("#inspector")).toContainText("Stable ID");
    await page.screenshot({ path: path.resolve(process.cwd(), `../../reports/iteration-06/renderer-${index + 1}-manual-2026-11-08.png`), fullPage: true });
  }
});
