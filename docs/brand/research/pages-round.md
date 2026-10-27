---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/research/.
version: 2026-10-26.1
---

# Pages round: site page, test page, Visits, Figma convert, upsells

Board: `app-ui/pages-round.html` (built by `app-ui/build_pages_round.py` from the v3 kit). Bundled copy for sending: `Aero-pages-round.html` (made with `bundle_pages_round.py`). Proposal only; nothing is built.

## Summary
- **One pattern for both pages.** Work on the left, a Settings rail on the right, hairline rows, same order (Name, link, access, look or recording, source), same saving (switches at once, fields on blur with "Saved"). Delete moves into the ⋯ menu.
- **Tests get a preview.** The site page's preview component at its small size at the top of Setup, plus a 52px thumbnail by the title on every tab. Tests already carry previewUrl and previewColors.
- **One home per action.** Test this site: Tests section and ⋯. Update with a prompt, Site source and Drop a new version become one Update block (files, prompt, Figma link). Upload to this test is the same block on the test.
- **Figma convert is half finished.** Label it as advanced; do not hide or promote it.
- **Plans in place.** Locked rows name the plan, limits show where they bite, one card per page at most. The Free site page has six banners today.
- **Visits** is rebuilt from the data the Plausible endpoint returns, in the v3 style.

## Decisions Duane needs to make
1. One skeleton and Settings rail on both pages, delete moved into ⋯? (Recommended yes.)
2. Test preview: B (site-style preview at the top of Setup plus a header thumbnail) or A (small thumbnail in the rail, as in the website demo)?
3. Tests get no custom domain or favicon rows, and the hero demo drops them?
4. Merge Drop a new version, Publish automatically, Update with a prompt and Site source into one Update block?
5. Add Download files (site) and Duplicate test to the ⋯ menus, or take Download files out of the demo?
6. Convert with AI: label it (recommended), hide it, or finish it?
7. Upsells: locked rows plus at most one card per page (recommended), or the plan summary card?
8. At the session limit: stop new sessions, or record and hide them until an upgrade? (Open since the first UI round.)
9. Visits stays at Solo and above, with Free and Basic seeing a plain locked skeleton and no sample numbers?
10. Remove "Target responses" from Setup and replace the Save button with autosave?
11. Before the Free card claims a plan keeps a site live, confirm paid sites never go offline. PRICING-FACTS only says Free sites stay live 7 days.

## Figma "Convert with AI", in plain words
- Aero writes a prompt (`buildAgentPrompt` in `CreateFlow.js`). It says: read my Figma design at (link) "using the Figma connector", turn it into one self-contained responsive `index.html` with inline CSS and colour blocks for images, zip it, and POST it to `aeroapp.ai/api/deploy-site` with a publish key.
- The screen tells the person to add the Figma connector themselves (Claude: claude.ai/customize/connectors; ChatGPT: Settings, Apps). Nothing in the repo mentions Dev Mode or an MCP address. Figma's own guide describes a remote MCP server at `mcp.figma.com/mcp` that needs no desktop app; the connector is almost certainly that, but I could not open Claude's connector listing to confirm.
- "Needs a paid Figma seat" is only Aero's copy (two places). Figma's rate limits: View and Collab seats get 20 tool calls a month on every plan; Full and Dev seats get 200 a day on Professional; on Starter, Full and Dev are not available. So a paid Dev or Full seat is the realistic minimum.
- Aero's side reads correctly (draft saved at copy, key minted, page watches for the deploy). No test covers it, it is not counted in creation stats, and I did not run it (needs a paid seat and a chat with a shell). Treat it as unverified.
- The output is a plain layout page, not the prototype: no flows or hotspots, so testers cannot click through the Figma prototype.
- Recommendation: keep under Other ways, rename to "Build real code from your design" with an Advanced tag, say what it gives and the seat, name Claude or ChatGPT once. To finish it: run five real files on a paid seat, ask the agent to run `whoami` first, handle images, check the upload landed, count it.

## Plans and upsells
- Figmafolio's `FeatureGate`: the real control greyed, a CTA row with a benefit headline ("Need to keep things confidential?"), one Upgrade now that opens the plans dialog in place. Used on password, favicon, custom domain, address rename, analytics, and a "Session limit reached" row. Good because there are one or two per page, each on the feature.
- Aero copied it into `AeroFeatureGate`, but the one-page site has six gated blocks (address, domain, password, favicon, analytics, badge), so a Free site page carries six banners with six Upgrade now buttons.
- Recommended: locked row with the plan and a lock, limits in place (sidebar meter, "Offline in 5 days on Free", "3 of 3 sessions kept"), at most one card per page for a real clock or limit, never on review screens, no prices on these pages (regional logic stays in the dialog).

## Visits: the data the app has
- Plausible, one shared account, filtered to the site's own hostnames (`api/plausible.js`; the script is added by `api/site.js`). Nothing in Firestore. Periods: today, 7 days, 30 days, this month, 12 months.
- Visitors, visits, pageviews, views per visit, bounce rate and visit duration, each with its change on the previous period; a time series of the same (hourly for Today, daily, monthly for 12 months); lists of sources, countries, cities, devices, browsers and operating systems (visitor counts only). A pages list exists in the API and is unused. Solo and Pro only.
- Not available: anything per tester or session, events, goals.

## Motion
Opacity and transform only; 120ms, 220ms, 420ms from the tokens; only skeletons and the processing and recording dots loop; reduced motion removes movement and keeps the state change. No cursor, no typing. Full table on the board.

## Sources
- Figma, Guide to the Figma MCP server: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server
- Figma, Rate limits and access: https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/
- saasui.design, upgrade and paywall UX patterns: https://www.saasui.design/blog/saas-upgrade-paywall-ux-patterns
- Vercel Hobby plan: https://vercel.com/docs/plans/hobby ; Maze free trials: https://help.maze.co/hc/en-us/articles/28513024118547-Maze-free-trials ; Loom pricing: https://www.loom.com/pricing ; Lyssna pricing: https://www.lyssna.com/pricing/ ; Framer pricing: https://www.framer.com/pricing/ ; Netlify credit-based plans: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/
- I read documentation and pricing pages, not logged-in screens, so in-app lock or banner visuals for those products are not claimed. Webflow's help page could not be opened and is not used.
- Code read: `src/pages/AeroSites/*`, `src/pages/UserTesting/*`, `src/components/CreateFlow/*`, `src/components/Aero/AeroFeatureGate.js`, `src/components/FeatureGate`, `src/components/Analytics/Analytics.js`, `api/plausible.js`, `functions/preview/plan.js`.
