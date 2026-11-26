import { expect, test } from "@playwright/test";

test("the opening narrative keeps transcript, fallback and quiet controls usable", async ({ page }) => {
  await page.route("**/images/**", (route) => route.abort());
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("article").filter({ hasText: "ACADEMY_001" }).getByRole("button", { name: /open training case/i }).click();

  await expect(page.getByRole("heading", { name: "The Academy Door" })).toBeVisible();
  await expect(page.getByText(/illustration unavailable/i)).toBeVisible();
  await page.getByRole("button", { name: /mute all audio/i }).click();
  await expect(page.getByRole("button", { name: /audio muted/i })).toBeVisible();
  await page.getByRole("checkbox", { name: /reduced sensory mode/i }).check();
  await expect(page.locator('main[data-reduced-sensory="true"]')).toBeVisible();
  await page.getByText("Open transcript").first().click();
  await expect(page.locator(".comic-transcript").first()).toBeVisible();
  await page.getByRole("button", { name: /next page/i }).click();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
});
