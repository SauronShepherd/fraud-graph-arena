import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  testMatch: ["**/gallery-mini-game.spec.ts", "**/qualification-exhibit.spec.ts", "**/performance-qualification.spec.ts", "**/renderer-manual-capture.spec.ts"],
  fullyParallel: false,
  // The performance page intentionally runs 48 mount/fit/resize/cleanup cycles.
  // Running it beside the other browser suites makes the measurement and its
  // completion signal scheduler-dependent, so qualification is single-worker.
  workers: 1,
  retries: 0,
  use: {
    baseURL: "http://127.0.0.1:4174",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "node node_modules/vite/bin/vite.js --config vite.qualification.config.ts --host 127.0.0.1 --port 4174",
    cwd: ".",
    port: 4174,
    reuseExistingServer: true,
  },
});
