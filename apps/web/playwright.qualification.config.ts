import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  testMatch: "**/*.spec.ts",
  fullyParallel: false,
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
