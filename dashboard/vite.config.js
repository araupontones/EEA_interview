import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The repository's data/ folder, written by the Python pipeline (scripts/run_pipeline.py).
const DATA_DIR = fileURLToPath(new URL("../data", import.meta.url));

export default defineConfig({
  plugins: [react()],
  // GitHub Pages serves the site under the repository name: https://<user>.github.io/EEA_interview/
  base: "/EEA_interview/",
  resolve: {
    // import data with "@data/processed/<file>.json" or "@data/lookups/<file>.json"
    alias: { "@data": DATA_DIR },
  },
  server: {
    // let the dev server read data/, which is outside the dashboard folder
    fs: { allow: [".", DATA_DIR] },
  },
});
