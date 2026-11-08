import { defineConfig } from "vite";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const configDir = fileURLToPath(new URL(".", import.meta.url));
const modules = resolve(configDir, "node_modules");
const fixturePath = resolve(configDir, "../../qualification/fixture-v1.json");
const fixtureSha256 = createHash("sha256").update(readFileSync(fixturePath)).digest("hex");

export default defineConfig({
  define: { __FGA_FIXTURE_SHA256__: JSON.stringify(fixtureSha256) },
  root: resolve(configDir, "../../qualification"),
  resolve: {
    alias: {
      "@xyflow/react": resolve(modules, "@xyflow/react"),
      cytoscape: resolve(modules, "cytoscape"),
      d3: resolve(modules, "d3"),
      graphology: resolve(modules, "graphology"),
      react: resolve(modules, "react"),
      "react-dom": resolve(modules, "react-dom"),
      sigma: resolve(modules, "sigma"),
    },
  },
  build: {
    rollupOptions: {
      input: {
        index: resolve(configDir, "../../qualification/index.html"),
        comparison: resolve(configDir, "../../qualification/comparison-exhibit.html"),
        benchmark: resolve(configDir, "../../qualification/benchmark-runner.html"),
        performance: resolve(configDir, "../../qualification/performance-runner.html"),
        semantic: resolve(configDir, "../../qualification/exhibit.html"),
      },
    },
  },
});
