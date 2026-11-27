import { defineConfig } from "@playwright/test";

// Keep the local test runner quiet when the host exports a forced colour flag.
process.env.FORCE_COLOR = "0";

const sqlitePath = process.env.FGA_SQLITE_PATH ?? ".fga/e2e.sqlite3";
const pythonCommand = process.env.FGA_PYTHON ?? "python";

export default defineConfig({
  testDir: "./e2e",
  testIgnore: ["**/qualification-exhibit.spec.ts", "**/performance-qualification.spec.ts", "**/renderer-manual-capture.spec.ts"],
  fullyParallel: false,
  workers: 1,
  retries: 0,
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure"
  },
  webServer: [
    {
      command: `${pythonCommand} -m uvicorn fraud_graph_arena.web.main:app --host 127.0.0.1 --port 8000`,
      cwd: "../..",
      port: 8000,
      reuseExistingServer: true,
      env: {
        PYTHONPATH: "src",
        FGA_ENVIRONMENT: "test",
        FGA_ROUND_REPOSITORY: "sqlite",
        FGA_SQLITE_PATH: sqlitePath,
        FGA_FRONTEND_DIST: "apps/web/missing-dist"
      }
    },
    {
      command: "npm run dev",
      cwd: ".",
      port: 5173,
      reuseExistingServer: true
    }
  ]
});
