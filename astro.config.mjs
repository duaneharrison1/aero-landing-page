import { defineConfig } from "astro/config";
import { fileURLToPath } from "url";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://aeroapp.ai",
  output: "static",
  integrations: [sitemap(), tailwind()],
  vite: {
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
  },
  devToolbar: {
    enabled: false,
  },
});
