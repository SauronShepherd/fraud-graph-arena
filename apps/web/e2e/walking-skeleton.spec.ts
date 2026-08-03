import { expect, test } from "@playwright/test";

test("Academy walking skeleton preserves comic and board context across refresh", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();

  await expect(page.getByRole("button", { name: /puppy/i })).toBeDisabled();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("button", { name: /open training case/i }).click();

  await expect(page.getByRole("heading", { name: "The Academy Door" })).toBeVisible();
  await page.getByRole("button", { name: /next page/i }).click();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
  await expect(page).toHaveURL(/\/intro\?page=2$/);

  await page.reload();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
  await expect(page.getByText(/page 2 of 2/i)).toBeVisible();

  await page.getByRole("button", { name: /enter the academy/i }).click();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeVisible();
  await expect(page.getByText("ACADEMY_001")).toBeVisible();

  await page.reload();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeVisible();
  await expect(page.getByText("ACADEMY_001")).toBeVisible();
  await expect(page.getByText(/right dog reached the right room/i)).toBeVisible();
});
