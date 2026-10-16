import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Faza 2 UI dev server. The workbench API runs separately (`npm run serve --
// <projectRoot>` from the repo root, default port 4173); this proxy is what
// lets the SPA call `/api/...` without hardcoding a host.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:4173",
    },
  },
});
