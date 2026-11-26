import { expect, test } from "@playwright/test";

test("the opening narrative keeps transcript, fallback and quiet controls usable", async ({ page }) => {
  await page.route("**/images/**", (route) => route.abort());
  await page.emulateMedia({ reducedMotion: "reduce" });
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
  await expect(page.locator("main.comic-shell")).toHaveAttribute("data-reduced-motion", /remove transition motion/i);
  const transitionDuration = await page.locator(".comic-page").evaluate((element) => Number.parseFloat(getComputedStyle(element).transitionDuration));
  expect(transitionDuration).toBeLessThanOrEqual(0.001);
  await page.getByText("Open transcript").first().click();
  await expect(page.locator(".comic-transcript").first()).toBeVisible();
  await page.getByRole("button", { name: /next page/i }).click();
  await expect(page.getByRole("heading", { name: "A Board with Nothing to Hide" })).toBeVisible();
});
