import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("production entry and catalogue screens remain keyboard and axe accessible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /fraud graph arena/i })).toBeVisible();
  await expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  await page.getByRole("link", { name: /choose your trench coat/i }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: /choose your trench coat/i })).toBeVisible();
  await expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  await expect(page.getByRole("button", { name: /puppy/i })).toBeDisabled();
});
