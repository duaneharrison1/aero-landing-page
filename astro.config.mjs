import { defineConfig } from "astro/config";
import { fileURLToPath } from "url";
import path from "path";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  site: "https://app.figmafolio.com",
  integrations: [mdx(), sitemap(), icon(), tailwind()],
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
