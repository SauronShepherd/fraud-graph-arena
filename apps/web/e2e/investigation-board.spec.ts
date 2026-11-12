import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

async function openBoard(page: Page, failArt = false) {
  if (failArt) await page.route("**/assets/board/**", async (route) => route.fulfill({ status: 404, body: "missing" }));
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("article").filter({ hasText: "ACADEMY_001" }).getByRole("button", { name: /open training case/i }).click();
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
      await expect(page.getByLabel("Round status ACTIVE")).toBeVisible();
      await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
      await expect(page.locator("[data-action-id]")).toHaveCount(4);
      await expect(page.locator("[data-action-id][data-state=NOT_IMPLEMENTED]")).toHaveCount(4);
      await expect(page.locator("[data-graph-node], [data-graph-edge]")).toHaveCount(0);
      const accessibility = await new AxeBuilder({ page }).analyze();
      expect(accessibility.violations).toEqual([]);
      await page.reload();
      await expect(page.getByText("ACADEMY_001")).toBeVisible();
    });
  }
  test("remains usable when decorative board art fails", async ({ page }) => {
    await openBoard(page, true);
    await expect(page.getByText("ACADEMY_001")).toBeVisible();
    await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
    await expect(page.locator("[data-action-id]")).toHaveCount(4);
  });
  test("preserves state under reduced motion and effective high zoom", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.setViewportSize({ width: 640, height: 900 });
    await openBoard(page);
    await page.evaluate(() => { document.documentElement.style.zoom = "2"; });
    await expect(page.getByText("ACADEMY_001")).toBeVisible();
    await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
    await expect(page.locator("[data-action-id]")).toHaveCount(4);
  });

  test("supports the populated graph investigation contract", async ({ page }) => {
    const start = Date.now();
    await page.goto("/");
    await page.getByRole("link", { name: /choose your trench coat/i }).click();
    await page.getByRole("button", { name: /detective academy/i }).click();
    await page.getByRole("article").filter({ hasText: "ACADEMY_T02" }).getByRole("button", { name: /open training case/i }).click();
    await expect(page.getByRole("heading", { name: "The Circular Collar" })).toBeVisible();
    await page.getByRole("button", { name: /enter the academy/i }).click();
    await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
    expect(Date.now() - start).toBeLessThan(5000);
    await expect(page.getByRole("button", { name: /Expand Blue Bowl Bakery/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Collapse Blue Bowl Bakery/i })).toBeVisible();
    await page.getByRole("button", { name: /Collapse Blue Bowl Bakery/i }).click();
    await expect(page.getByRole("button", { name: /Restore Blue Bowl Bakery/i })).toBeVisible();
    await page.getByRole("button", { name: /Restore Blue Bowl Bakery/i }).click();
    await page.getByRole("button", { name: /Blue Bowl Bakery, T2-O-BAKERY/ }).click();
    await page.getByRole("button", { name: "Focus selection" }).click();
    await expect(page.getByRole("button", { name: "Show all nodes" })).toBeVisible();
    await expect(page.getByRole("img", { name: /nodes in current graph view/i })).toBeVisible();
    await page.getByText("Semantic evidence list").click();
    await expect(page.getByText(/Blue Bowl Bakery \(T2-O-BAKERY\)/)).toBeVisible();
  });
});
