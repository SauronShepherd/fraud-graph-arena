import fs from "node:fs/promises";
import path from "node:path";
import { expect, test } from "@playwright/test";

test("records repeated FGA06 renderer performance evidence", async ({ page }) => {
  test.setTimeout(90_000);
  await page.goto("/performance-runner.html");
  await page.getByRole("button", { name: "Run 12 repetitions" }).click();
  await expect(page.locator("#status")).toContainText("PASS", { timeout: 75_000 });
  const report = await page.evaluate(() => (window as Window & { __FGA06_PERFORMANCE_REPORT__?: unknown }).__FGA06_PERFORMANCE_REPORT__);
  expect(report).toBeTruthy();
  const reportPath = path.resolve(process.cwd(), "../../reports/iteration-06/renderer-performance-fga-2026-11-08.json");
  await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  expect((report as { status: string }).status).toBe("PASS");
});
