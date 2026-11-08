import path from "node:path";
import { pathToFileURL } from "node:url";

import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

const galleryPath = path.resolve(process.cwd(), "../../docs/iteration-06/examples/gallery.html");

test.describe("static graph gallery mini-game", () => {
  test("supports investigation progress, node movement and camera exploration", async ({ page }) => {
    await page.goto(pathToFileURL(galleryPath).href);

    await expect(page.locator("#scenario-title")).toHaveText("Dense cluster");
    await expect(page.locator("#game-progress-label")).toHaveText("0 / 4");
    await expect(page.locator("[data-node-id='EX-N-3003']")).toHaveCount(1);

    await page.getByRole("button", { name: "Hint" }).click();
    await expect(page.locator("#game-feedback")).toContainText("visible node");

    await page.locator("[data-node-id='EX-N-3003']").click();
    await expect(page.locator("#game-progress-label")).toHaveText("1 / 4");
    await expect(page.locator("#inspector")).toBeVisible();

    await page.locator("[data-target-edge]").first().click();
    await expect(page.locator("#game-progress-label")).toHaveText("2 / 4");
    await expect(page.locator("#inspector")).toContainText("Context menu · edge");

    const node = page.locator("[data-node-id='EX-N-3003']");
    const nodeBox = await node.boundingBox();
    if (!nodeBox) throw new Error("The selected graph node has no layout box.");
    await page.mouse.move(nodeBox.x + nodeBox.width / 2, nodeBox.y + nodeBox.height / 2);
    await page.mouse.down();
    await page.mouse.move(nodeBox.x + 100, nodeBox.y + 55, { steps: 5 });
    await page.mouse.up();
    await expect(page.locator("#game-progress-label")).toHaveText("3 / 4");
    await expect(page.locator("#inspector .log")).toContainText("Committed movement");
    await expect.poll(async () => page.locator(".node.moving").count()).toBeGreaterThan(0);

    await page.evaluate(() => window.scrollTo(0, 0));
    const canvasBackground = page.locator("#surface [data-canvas-background='true']");
    const surfaceBox = await canvasBackground.boundingBox();
    if (!surfaceBox) throw new Error("The graph surface has no layout box.");
    await page.mouse.move(surfaceBox.x + 18, surfaceBox.y + 100);
    await page.mouse.down();
    await page.mouse.move(surfaceBox.x + 70, surfaceBox.y + 126, { steps: 4 });
    await page.mouse.up();
    await expect(page.locator("#game-progress-label")).toHaveText("4 / 4");
    await expect(page.locator("#game-hud")).toHaveClass(/complete/);
    await expect(page.locator("#inspector .log")).toContainText("Panned camera");

    await page.locator("[data-command='reset']").click();
    const zoomSurface = await page.locator("#surface svg").boundingBox();
    if (!zoomSurface) throw new Error("The graph SVG has no layout box for wheel zoom.");
    const zoomBefore = await page.locator("#surface").getAttribute("data-zoom");
    await page.mouse.move(zoomSurface.x + zoomSurface.width / 2, zoomSurface.y + zoomSurface.height / 2);
    await page.mouse.wheel(0, -120);
    await expect(page.locator("#surface")).not.toHaveAttribute("data-zoom", zoomBefore || "1.00");

    await page.getByRole("button", { name: "Restart" }).click();
    await expect(page.locator("#game-progress-label")).toHaveText("0 / 4");
    const motionToggle = page.locator("[data-command='toggle-motion']");
    await expect(motionToggle).toHaveAttribute("aria-pressed", "true");
    await motionToggle.click();
    await expect(motionToggle).toHaveAttribute("aria-pressed", "false");
    await motionToggle.click();
    await expect(motionToggle).toHaveAttribute("aria-pressed", "true");

    const axe = await new AxeBuilder({ page }).analyze();
    expect(axe.violations).toEqual([]);
  });

  test("keeps all five scenarios and alternate views reachable", async ({ page }) => {
    await page.goto(pathToFileURL(galleryPath).href);
    await expect(page.locator("[role='tab']")).toHaveCount(5);

    const topology = page.locator("#topology-select");
    for (const value of ["radial", "ring", "chain", "star", "grid", "native"]) {
      await topology.selectOption(value);
      await expect(page.locator("#surface")).toHaveAttribute("data-topology", value);
    }

    for (const tab of await page.locator("[role='tab']").all()) {
      await tab.click();
      await expect(page.locator("#scenario-title")).not.toHaveText("Loading example…");
      for (const view of ["node-link", "matrix", "path", "semantic-list"]) {
        await page.locator(`[data-view='${view}']`).click();
        await expect(page.locator("#surface")).toBeVisible();
      }
    }
  });

  test("opens contextual hover panels, marks targets and manages working relationships", async ({ page }) => {
    await page.goto(pathToFileURL(galleryPath).href);

    const node = page.locator("[data-node-id='EX-N-3003']");
    await node.hover();
    await expect(page.locator("#hover-preview")).toBeVisible();
    await expect(page.locator("#hover-preview")).toContainText("Hover preview · node");
    const hoverBox = await page.locator("#hover-preview").boundingBox();
    if (!hoverBox) throw new Error("The contextual hover panel has no layout box.");
    await page.mouse.move(hoverBox.x + hoverBox.width / 2, hoverBox.y + hoverBox.height / 2, { steps: 5 });
    await expect(page.locator("#hover-preview")).toBeVisible();
    await expect(page.locator("#hover-preview [data-hover-action='favorite']")).toHaveAttribute("aria-label", "Add to highlights");
    await expect(page.locator("#hover-preview [data-hover-action='center']")).toHaveAttribute("aria-label", "Center on graph");
    await page.locator("#hover-preview [data-hover-action='favorite']").click();
    await expect(page.locator("#hover-preview [data-hover-action='favorite']")).toHaveAttribute("aria-label", "Remove from highlights");
    await page.locator("#hover-preview [data-hover-action='favorite']").click();
    await page.locator("#hover-preview [data-hover-action='center']").click();

    await expect(page.locator("#inspector")).toContainText("Context menu · selected node");
    await expect(page.locator("[data-context-action='favorite']")).toHaveAttribute("aria-label", "Add to highlights");
    await expect(page.locator("[data-context-action='center']")).toHaveAttribute("aria-label", "Center on graph");
    await page.locator("[data-context-action='favorite']").click();
    await expect(page.locator("[data-context-action='favorite']")).toHaveAttribute("aria-label", "Remove from highlights");
    await page.locator("[data-context-action='center']").click();
    await expect(page.locator("#favorites-panel")).toBeVisible();
    await expect(page.locator("#favorites-panel")).toContainText("R-1042 · J. GARCIA");

    await page.locator("#favorites-panel [data-favorite-target]").click();
    await expect(page.locator("#inspector")).toContainText("Context menu · selected node");
    await page.locator("#favorites-panel [data-favorite-remove]").click();
    await expect(page.locator("#favorites-panel")).toBeHidden();

    await page.locator("[data-target-edge]").first().click();
    await page.locator("[data-context-action='favorite']").click();
    await expect(page.locator(".edge.favorite")).toHaveCount(1);
    await expect(page.locator("#favorites-panel")).toContainText("LINKED_TO");
    await page.locator("#favorites-panel [data-favorite-remove]").click();
    await expect(page.locator("#favorites-panel")).toBeHidden();

    await page.locator("[data-command='toggle-composer']").click();
    await expect(page.locator("#inspector")).toContainText("Add working relationship");
    await page.locator("form.relationship-composer button[type='submit']").click();
    await expect(page.locator(".edge.working")).toHaveCount(1);
    await expect(page.locator("#inspector")).toContainText("removable local investigation state");
    await page.locator("[data-context-action='delete-relation']").click();
    await expect(page.locator(".edge.working")).toHaveCount(0);

    const axe = await new AxeBuilder({ page }).analyze();
    expect(axe.violations).toEqual([]);
  });
});
