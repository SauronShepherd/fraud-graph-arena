import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";

async function openBoard(page: Page) {
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("button", { name: /open training case/i }).click();
  await page.getByRole("button", { name: /next page/i }).click();
  await page.getByRole("button", { name: /enter the academy/i }).click();
  await expect(page.getByRole("heading", { name: /empty evidence board/i })).toBeVisible();
}

test.describe("I02 investigation board", () => {
  for (const viewport of [{ name: "wide", width: 1440, height: 900 }, { name: "laptop", width: 1024, height: 768 }, { name: "portrait", width: 420, height: 900 }]) {
    test(`${viewport.name} preserves the empty investigation contract`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await openBoard(page);
      await expect(page.getByText("ACADEMY_001")).toBeVisible();
      await expect(page.getByText("ACTIVE", { exact: true })).toBeVisible();
      await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
      await expect(page.locator("[data-action-id]")).toHaveCount(4);
      await expect(page.locator("[data-action-id][data-state=NOT_IMPLEMENTED]")).toHaveCount(4);
      await expect(page.locator("[data-graph-node], [data-graph-edge]")).toHaveCount(0);
      await page.reload();
      await expect(page.getByText("ACADEMY_001")).toBeVisible();
    });
  }
});
