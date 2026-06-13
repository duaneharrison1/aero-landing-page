# Aero landing page

Marketing landing page for Aero, where an AI agent can publish a prototype and get real
humans testing it.

## Stack
- Astro 5 (static output)
- Tailwind CSS 3.4 via @astrojs/tailwind
- astro-seo for SEO, canonical and OpenGraph tags
- @astrojs/sitemap
- DM Sans (self-hosted via @fontsource-variable/dm-sans)

## Develop
```
npm install
npm run dev
```

## Build
```
npm run build
```
Output is static, in `dist/`.

## Deploy (Vercel)
Import the repo into Vercel. The Astro framework preset is auto-detected. No environment
variables are required. Security headers are set in `vercel.json`.

Note: the apex domain cutover is a separate, human-run step and is intentionally not
configured here.
