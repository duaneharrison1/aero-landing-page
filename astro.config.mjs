import { defineConfig } from "astro/config";
import { fileURLToPath } from "url";
import path from "path";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  site: "https://aeroapp.ai",
  // Old addresses from the earlier site, kept working (Oct 2026 redesign). See docs/website/README.md.
  redirects: {
    "/how-it-works": "/",
    "/pricing-test": "/pricing",
    "/features/analytics": "/features#publish",
    "/features/code-conversion": "/features#publish",
    "/features/custom-domain": "/features#publish",
    "/features/custom-favicon": "/features#publish",
    "/features/password-protection": "/features#publish",
    "/features/project-showcase": "/features",
    "/features/responsive-design": "/features#publish",
    "/features/user-testing": "/features#test",
  },
  integrations: [mdx(), sitemap({ filter: (page) => !page.includes("/404") }), icon(), tailwind({ applyBaseStyles: false })],
  vite: {
    // Keep every script a real file in /_astro/ (glass-settings.js stays one readable file in production too).
    build: { assetsInlineLimit: 0 },
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
