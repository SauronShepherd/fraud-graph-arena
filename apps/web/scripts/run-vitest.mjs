import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";

const localStorageFile = join(tmpdir(), "fraud-graph-arena-vitest-localstorage.json");
const nodeOptions = process.env.NODE_OPTIONS ?? "";
if (!nodeOptions.includes("--localstorage-file")) {
  process.env.NODE_OPTIONS = `${nodeOptions} --localstorage-file=${localStorageFile}`.trim();
}

const vitest = join(process.cwd(), "node_modules", "vitest", "vitest.mjs");
const result = spawnSync(process.execPath, [vitest, ...process.argv.slice(2)], {
  stdio: "inherit",
  env: process.env,
});

if (result.error) {
  console.error(result.error);
  process.exit(1);
}
process.exit(result.status ?? 1);
