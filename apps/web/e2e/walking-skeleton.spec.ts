import { expect, test } from "@playwright/test";

test("Academy walking skeleton preserves comic and board context across refresh", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /fraud graph arena/i })).toBeFocused();
  await page.getByRole("button", { name: /choose your trench coat/i }).click();
  await expect(page.getByRole("heading", { name: /choose your trench coat/i })).toBeFocused();

  await expect(page.getByRole("button", { name: /puppy/i })).toBeDisabled();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("button", { name: /open training case/i }).click();

  const introductionHeading = page.getByRole("heading", { name: "The Case of the Empty Evidence Board" });
  await expect(introductionHeading).toBeVisible();
  await expect(introductionHeading).toBeFocused();
  await page.getByRole("button", { name: /next page/i }).click();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
  await expect(page).toHaveURL(/\/intro\?page=2$/);

  await page.reload();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeFocused();
  await expect(page.getByText(/page 2 of 2/i)).toBeVisible();

  await page.getByRole("button", { name: /enter the academy/i }).click();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeFocused();
  await expect(page.getByText("ACADEMY_001")).toBeVisible();

  await page.reload();
  await expect(page.getByRole("heading", { name: "The Case of the Empty Evidence Board" })).toBeVisible();
  await expect(page.getByText("ACADEMY_001")).toBeVisible();
  await expect(page.getByRole("heading", { name: /evidence graph/i })).toBeVisible();
});
