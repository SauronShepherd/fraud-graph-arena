import { defineConfig } from "vite";
import { resolve } from "node:path";

const modules = resolve(__dirname, "node_modules");

export default defineConfig({
  root: resolve(__dirname, "../../qualification"),
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
});
