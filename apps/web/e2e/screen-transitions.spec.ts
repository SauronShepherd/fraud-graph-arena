import { expect, test } from "@playwright/test";

test("intro completion uses the centralized fade effect and still reaches the board", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("button", { name: /open training case/i }).click();
  await page.getByRole("button", { name: /next page/i }).click();
  await page.getByRole("button", { name: /enter the academy/i }).click();
  await expect(page.locator("[data-transition-effect=FADE_TO_BLACK]")).toBeVisible();
  await expect(page.getByRole("heading", { name: /empty evidence board/i })).toBeVisible();
});
