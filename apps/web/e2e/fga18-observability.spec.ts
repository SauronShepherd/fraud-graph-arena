import { expect, test } from "@playwright/test";

test("a graph action carries the browser trace into the API request", async ({ page }) => {
  let graphTraceId: string | undefined;
  page.on("request", (request) => {
    if (request.url().includes("/investigations/graph-analytics")) {
      graphTraceId = request.headers()["x-trace-id"];
    }
  });

  await page.goto("/");
  await page.getByRole("link", { name: /choose your trench coat/i }).click();
  await page.getByRole("button", { name: /detective academy/i }).click();
  await page.getByRole("article").filter({ hasText: "ACADEMY_T02" }).getByRole("button", { name: /open training case/i }).click();
  await page.getByRole("button", { name: /enter the academy/i }).click();
  await expect(page.getByRole("heading", { name: "The Circular Collar" })).toBeVisible();
  await page.locator("details.graph-semantic summary").click();
  await page.getByRole("button", { name: "Cipher Corgi (T2-P-CIPHER-A)" }).click();
  await page.getByRole("button", { name: "Run graph analysis", exact: true }).click();
  await expect(page.locator(".graph-analytics-results")).toBeVisible();

  expect(graphTraceId).toMatch(/^[A-Za-z0-9._:-]{1,128}$/);
  expect(graphTraceId).not.toContain("player");
});
