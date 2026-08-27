import { expect, test } from "@playwright/test";

test("public screen URLs reconstruct semantic screens and malformed URLs recover safely", async ({ page }) => {
  await page.goto("/paths");
  await expect(page.getByRole("heading", { name: /choose your trench coat/i })).toBeVisible();
  await page.goto("/not-a-screen");
  await expect(page.getByRole("heading", { name: /fraud graph arena/i })).toBeVisible();
  await expect(page).toHaveURL(/\/$/);
});

test("intro page is addressable and browser history returns to the prior screen", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("article").filter({ hasText: "ACADEMY_001" }).getByRole("button", { name: /open training case/i }).click();
  await expect(page).toHaveURL(/\/intro\?page=1$/);
  await page.getByRole("button", { name: /next page/i }).click();
  await expect(page).toHaveURL(/\/intro\?page=2$/);
  await page.goBack();
  await expect(page).toHaveURL(/\/intro\?page=1$/);
  await expect(page.getByRole("heading", { name: "The Academy Door" })).toBeVisible();
});
