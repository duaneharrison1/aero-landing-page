# SEO on the Aero website: what is set up and how to keep it right

Written 21 Nov 2026. The plan and the numbers behind it are in the project docs ("Aero SEO playbook", "Aero SEO baseline").

## What is in place

| Thing | Where | Notes |
|---|---|---|
| `robots.txt` | `public/robots.txt` | Allows everything and points at the sitemap. |
| Sitemap | made by `@astrojs/sitemap` | `https://aeroapp.ai/sitemap-index.xml`. Redirect addresses are left out. |
| `llms.txt` | `src/pages/llms.txt.ts` | Written as the questions people ask. Built from `src/data/guides.json`, so a new guide appears in it without an edit. The plan and price lines are typed in and must match `docs/brand/PRICING-FACTS.md`. |
| IndexNow key | `public/<key>.txt` | The file name and its contents are the key. The same name is in figmaApp `middleware.js` (`INDEXNOW_KEY_FILE`), so change both together. |
| Home schema | `src/data/pages.json`, `home.jsonld` | Organization, WebSite and SoftwareApplication. Pricing, guides and posts already had their own. |
| SEO build check | `scripts/check-seo.mjs` | Runs after `astro build`. Fails the build if a page breaks a rule (below). |

## The rules the build check enforces

- Title 1 to 60 characters; description 70 to 155 characters.
- Titles and descriptions are not repeated across pages.
- Canonical link present, on `aeroapp.ai`, and the same as the page address.
- Exactly one visible `<h1>`.
- Every JSON-LD block parses.

Run it on its own after a build with `node scripts/check-seo.mjs`.

## Why `llms.txt` and the key file needed a change in figmaApp

`aeroapp.ai` is served by the app's edge middleware, which only forwards a short list of paths to this site. `robots.txt` and the sitemaps were on that list; `llms.txt` and the IndexNow key file were added to it in figmaApp (`isMarketingRootFile` in `middleware.js`). Any new root-level file here needs the same.

## Home page layout shift

The home hero used to jump after load (desktop CLS 0.257 in PageSpeed, 21 Nov). Three causes, now fixed:
1. `lay-c` (the centred hero) was added to `<html>` by `home.js` after first paint. It is now in the HTML (`SiteLayout.astro`).
2. The rotating word box was 0 wide until the script sized it, so the lead line re-wrapped on phones. It now starts at the first word's width (`.hm-rot` in `home.css`).
3. The Geist web font swapping in changed line wraps. `aero.css` defines "Geist Fallback" (Arial resized to Geist) to reduce this.

Check after any hero change: PageSpeed on the home page, mobile and desktop, CLS under 0.1.

## Not done yet

- Some phone widths (412 and 414 px) can still shift when the web font arrives after first paint. Re-check on the live site.
- Colour contrast and heading order inside the example app screens on the home and Features pages (they are copies of real app screens). The page text itself passes.
- The two older Markdown blog posts (`src/content/blog`) are unchanged apart from a description and a shorter title; their future is Duane's call.
