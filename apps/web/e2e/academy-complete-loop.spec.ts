import { expect, test } from "@playwright/test";

test("Academy completes the real investigation loop from UI to persisted receipt", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("article").filter({ hasText: "ACADEMY_T02" }).getByRole("button", { name: /open training case/i }).click();
  await page.getByRole("button", { name: /enter the academy/i }).click();

  await expect(page.getByRole("heading", { name: "The Circular Collar" })).toBeVisible();
  await page.locator("details.graph-semantic summary").click();
  await page.getByRole("button", { name: "Cipher Corgi (T2-P-CIPHER-A)" }).click();
  await page.getByRole("button", { name: "Run identity analysis" }).click();
  await expect(page.getByRole("heading", { name: "Strict identity observations" })).toBeVisible();
  await page.getByRole("button", { name: "Run graph analysis", exact: true }).click();
  await expect(page.locator(".graph-analytics-results")).toBeVisible();

  await page.getByRole("checkbox", { name: "Cipher Corgi T2-P-CIPHER-A", exact: true }).check();
  await page.getByRole("checkbox", { name: "C. Corgi T2-P-CIPHER-B", exact: true }).check();
  for (const claim of [
    /The matching contact pair supports one identity/i,
    /The similar candidate stays separate/i,
    /The payment relationships keep their direction/i,
    /Exact device and IP relationships support coordination/i,
    /Shared address and kiosk are not guilt by association/i,
  ]) {
    await page.getByLabel(claim).check();
  }
  await page.getByRole("button", { name: "Submit investigation" }).click();
  await expect(page).toHaveURL(/\/resolution$/);
  await expect(page.getByRole("heading", { name: "Clean Collar" })).toBeVisible();
  await expect(page.getByText("Credits left").locator("..").getByText("3", { exact: true })).toBeVisible();

  await page.reload();
  await expect(page.getByRole("heading", { name: "Clean Collar" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Investigation ledger" })).toBeVisible();
  await expect(page.getByText(/COMPARE IDENTITIES/i)).toBeVisible();
  await expect(page.getByText(/RUN GRAPH ANALYSIS/i)).toBeVisible();
});
