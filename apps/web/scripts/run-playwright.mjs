import { spawn } from "node:child_process";
import { join } from "node:path";

const environment = { ...process.env, FORCE_COLOR: "0" };
delete environment.NO_COLOR;
const cli = join(process.cwd(), "node_modules", "@playwright", "test", "cli.js");
const child = spawn(process.execPath, [cli, "test", ...process.argv.slice(2)], {
  env: environment,
  stdio: "inherit"
});

child.on("error", (error) => {
  console.error(error);
  process.exitCode = 1;
});

child.on("exit", (code, signal) => {
  process.exitCode = code ?? (signal ? 1 : 0);
});
