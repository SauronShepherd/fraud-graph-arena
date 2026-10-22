import { defineConfig } from "@playwright/test";

const processEnvironment = (globalThis as typeof globalThis & { process?: { env?: Record<string, string | undefined> } }).process?.env;

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure"
  },
  webServer: [
    {
      command: "python -m uvicorn fraud_graph_arena.web.main:app --host 127.0.0.1 --port 8000",
      cwd: "../..",
      port: 8000,
      reuseExistingServer: false,
      env: {
        FGA_ENVIRONMENT: "test",
        FGA_ROUND_REPOSITORY: "sqlite",
        FGA_SQLITE_PATH: processEnvironment?.FGA_SQLITE_PATH ?? `${processEnvironment?.TEMP ?? processEnvironment?.TMP ?? processEnvironment?.TMPDIR ?? ".fga"}/fga-e2e-${globalThis.crypto.randomUUID()}.sqlite3`,
        FGA_FRONTEND_DIST: "apps/web/missing-dist"
      }
    },
    {
      command: "npm run dev",
      cwd: ".",
      port: 5173,
      reuseExistingServer: false
    }
  ]
});
