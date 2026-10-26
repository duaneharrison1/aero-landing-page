# The Aero website: where everything lives and how to change it

The site was rebuilt in October 2026 from the approved mockups (website round 9, "go live" on 25 Oct 2026; the
decisions are in `docs/brand/DECISIONS.md` in figmaApp, copied here). Every page is static Astro. This page says where
each thing is, so a change is one edit in one place.

## Pages

| Address | Built by | Body | Words |
|---|---|---|---|
| `/` | `src/pages/index.astro` | `src/markup/home.html` | `src/data/copy/home.json` |
| `/features` | `src/pages/features.astro` | `src/markup/features.html` | `src/data/copy/features.json` |
| `/pricing` | `src/pages/pricing.astro` | `src/markup/pricing.html` | `src/data/copy/pricing.json` |
| `/use-cases` | `src/pages/use-cases.astro` | `src/markup/use-cases.html` | `src/data/copy/use-cases.json` |
| `/guides` | `src/pages/guides/index.astro` | `src/markup/guides.html` | `src/data/copy/guides.json` |
| `/guides/publish-a-claude-artifact` | `src/pages/guides/publish-a-claude-artifact.astro` | `src/markup/publish-a-claude-artifact.html` | `src/data/copy/publish-a-claude-artifact.json` |
| `/blog` | `src/pages/blog/index.astro` | `src/markup/blog.html` (the list comes from `src/data/blog.json`) | `src/data/copy/blog.json` |
| `/blog/<slug>` | `src/pages/blog/[slug].astro` | `src/markup/blog/<slug>.html` | `src/data/copy/blog/<slug>.json` |
| `/about`, `/contact`, 404 | their `.astro` files (Tailwind, `src/layouts/Layout.astro`) | in the file | in the file |

The page title, meta description, JSON-LD (FAQ, HowTo, breadcrumbs) and body class of each new page are in
`src/data/pages.json`. The sitemap is made by `@astrojs/sitemap` at build time.

## Change words

- **Most words:** edit the page's file in `src/data/copy/`. Any element in the markup marked `data-c="key"` takes its
  text from that key when the site is built (`src/lib/website.ts`, `applyCopy`). Headlines keep their round blue dot
  on their own; leave the full stop at the end of the string or not, either works.
- **Words inside the product pictures** (app screens, Claude, WhatsApp, the example web app Pocket) and table cells are
  in the markup file itself. Search for the text in `src/markup/<page>.html` and change it there. Some lists
  (for example the homepage comparison table, `pr.rows`) are in both places; change both.
- **Header and footer:** `src/data/site.json` (menu, footer columns, the fine print).
- **Title and description for search and sharing:** `src/data/pages.json`.
- Follow `docs/brand/TONE_OF_VOICE.md`: no em dashes, British spelling, sentence case. Example names are made up and
  labelled "Example". Plans and limits only from `docs/brand/PRICING-FACTS.md`.

## Links

`src/data/site.json` → `links` holds the shared addresses. In any markup or data file, write `@login`, `@signup`,
`@privacy` or `@terms` as an `href` and the build puts the real address in.

- Log in: `https://aeroapp.ai/login`, Start free: `https://aeroapp.ai/signup` (the app answers these paths on the apex,
  as on the earlier site).
- Privacy and Terms are the app's pages (`/privacy-policy`, `/terms-and-conditions`).

## Glass (buttons and the header)

- **`src/glass/glass-settings.js` is the one file that tunes the glass** on every page. To change it, open the glass
  panel in the research folder, nudge it, press "Export for site" and paste the result over the whole file.
- `src/glass/glass-v3.js` is the engine. Don't edit it for a look change; that's what the settings are for.
- Both load in this order at the end of every page (`src/layouts/SiteLayout.astro`). A button is glass when it has
  `class="btn g3 sm|md|lg"` and `data-glass-v3="primary"` (ink, with `data-fill="rgba(29,29,31,.8)"`) or
  `"secondary"` (white). The header (`.site-nav`) is glass on its own. How the engine works: `docs/website/GLASS.md`.

## Colours, type and spacing (tokens)

- `src/styles/website/aero.css` holds every token (`:root` custom properties: colours, the step colours Publish blue,
  Test green, Review orange, type, radius) and the shared website block (header, footer, buttons, washes, pills,
  the headline dot). Change a token there and every page follows.
- `extra.css` and `review.css`: the app screens drawn in the pictures. `home.css`: the homepage. `site.css`: the
  other pages. Each page loads one bundle in order: `home-page.css` or `site-page.css`.

## The hero animation

- It's `src/markup/home.html` (the scenes, inside `.hm-stage`) driven by `src/scripts/website/home.js`.
- **Timing:** one clock in `home.js`, in seconds of script time. `T` is the loop length; `SCENES` lists when each
  screen is on; `CUR` is the cursor's path; `warp()` slows the paste and send for the visitor; `JUMP` / `JT` are where
  the Publish, Test and Review steps jump to. `?t=12.5` on the homepage freezes the loop at that moment (script time),
  which helps when adjusting.
- The Publish, Test and Review steps under it jump to each part. With reduced motion there is no loop: a still of the
  test and the steps filled in.
- It pauses off screen and in a hidden tab.

## Prices

- Plan facts (sessions, features, trial) come only from `docs/brand/PRICING-FACTS.md`; the US prices are written in
  `src/markup/pricing.html` and the homepage table.
- **Regional prices are intentional; never change the currency or the pricing logic.** On `/pricing`, every element
  with `data-price="basic|solo|pro"` gets the visitor's regional monthly price from
  `src/scripts/website/regional-pricing.js`, which is the same logic as the earlier pricing table
  (`src/components/PricingTableNew.astro`: Firestore `config/pricing`, ipinfo country, the same fallbacks). If anything
  fails, the US price in the markup stays.

## Blog posts

To add a post:

1. Add an entry to `src/data/blog.json` (`slug`, `date` as `YYYY-MM-DD`, `title`, `summary`, `pill`:
   `pill pill-publish`, `pill pill-test`, `pill pill-review` or `pill`, and `label`: Publish, Test, Review or
   "Plans and account"). The blog list, its month headings and the Older / Newer links all come from this file.
2. Copy an existing post's markup to `src/markup/blog/<slug>.html` and its words to `src/data/copy/blog/<slug>.json`.
   Keep `<!--prev-next-->` where the Older / Newer links go.
3. Add the page to `src/data/pages.json` as `blog/<slug>` (title, description, `"bodyClass": "site s-page"`,
   `"route": "/blog/<slug>"`).

The two earlier Markdown posts in `src/content/blog/` still render at their old addresses with the new header and
footer; they're not in the list.

## Features the app doesn't have yet

The pictures come from the v3 app designs, which include a few things the app doesn't do yet. They're tagged
`data-soon="..."` in the markup and hidden by `src/styles/website/not-yet-live.css` (tester first name, Private sites,
"Taking new sessions", free Preview as tester runs, a test's own domain and favicon, word highlight and click to jump
in replays). When one ships, delete its rule in that file and it comes back on every page. The Features page keeps its
own "Coming soon" tags as Duane decided them.

## Old addresses

`astro.config.mjs` → `redirects` keeps the earlier site's addresses working: `/how-it-works` → `/`,
`/pricing-test` → `/pricing`, and the eight `/features/<name>` pages → the matching section of `/features`.

## Serving on aeroapp.ai

aeroapp.ai is served by the app (figmaApp); its `middleware.js` proxies a fixed list of marketing paths to this
site (`MARKETING_EXACT`, `MARKETING_PREFIXES`, `/_astro/`, `/opengraph.jpg`, sitemaps). Every asset this site uses is
built into `/_astro/` for that reason (nothing new in `public/` except `opengraph.jpg`). A new top-level page (such as
`/use-cases` and `/guides`) also needs adding to that list in figmaApp, or aeroapp.ai shows the app instead.

## Checking a change

`npm run build` must pass. `npx astro preview` serves the built site on port 4321.
