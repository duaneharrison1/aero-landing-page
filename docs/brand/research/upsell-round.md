---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/research/.
version: 2026-11-05.1
---

# Upsell round: locked rows, what a click does, the custom domain row

Board: `app-ui/upsell-round.html` (built by `app-ui/build_upsell_round.py` from the v3 kit and the pages-round helpers). Bundled copy for sending: `Aero-upsell-round.html` (`bundle_upsell_round.py`). Proposal only; nothing is built. Plans and prices come only from `PRICING-FACTS.md` (USD; the app keeps its regional price logic at checkout).

## Summary
- **Locked rows: A.** Replace the plan pill with a lock and the plan word in grey, no border. The row keeps its one-line description. Other options drawn: B (benefit line plus a plan link), C (grouped "With Basic" / "With Solo" at the foot), D (control works, then a "saved as a draft" note).
- **Click: a popover next to the row** (bottom sheet on a phone). Names the plan, lists what it includes, one button "Try Basic free for 7 days" (true today: every paid plan has a 7-day trial), and a "Compare plans" link that opens the existing plans dialog with that plan selected. Also drawn: small modal with the plan preselected, side sheet with a comparison table, inline expansion. A full plans page is described, not drawn.
- **Custom domain is Solo, not Basic** (PRICING-FACTS). Today it is the last grey row, "Custom domain, use a domain you already own". Proposed: an "Address" group with "Aero address" and "Your own domain: use your own address, like app.yourname.com".
- **Tests row fixed.** Rebuilt as one value per column (name and address, "3 sessions", "2 new" in ink with an accent dot, status). The blue was `--ae-link` (#1F63DD), not the accent. `--ae-blue` equals `--aero-accent` (#3478F6).
- **Research caveat.** I could not see logged-in screens for any of the ten products. Official help pages mostly say which plan has a feature, not how the lock looks.

## What others do (detail on the board, section 1)
- **Webflow:** help says "Add a Site plan to your Webflow site" before connecting a domain; upgrade is Site settings, Plans, pick tab and billing period, "Continue to payment". Lock on the domain field: not seen.
- **Framer:** a paid site plan is needed for a custom domain; a free Framer subdomain needs none. Where the upgrade button sits: not described.
- **Vercel:** Password Protection page (updated 15 Sep 2026): Hobby "Not available, upgrade to Pro to enable". **Netlify:** password protection on Pro and Enterprise; on Free it offers "make it private" instead.
- **Canva:** developer guidelines: crown or Pro badge, hover tooltip, upgrade dialog immediately on click, button "Upgrade to Canva Pro". A 2024 teardown (revised Sep 2026) says the dialog shows Pro with a preview of that feature.
- **Figma:** forum post (22 Dec 2025): Dev Mode on a Starter file opens "Upgrade to work in Dev Mode" with "Learn More" and "Back to Design Mode"; neither buys anything. Working path is Account settings, "Upgrade Figma Plan".
- **Notion, Linear:** upgrade lives in Settings or billing settings; locked-control UI not documented. **Loom:** limits are counts (25 videos), work is kept. **Maze:** 30-day trial of paid features.
- **Figmafolio today:** `FeatureGate` / `AeroFeatureGate` keep the real control visible and greyed, then show a tinted banner (two-tone icon, benefit headline such as "Need to keep things confidential?", one line, "Upgrade now") that opens the plans dialog in place. The tier is not named and the dialog does not preselect a plan.

## Recommendation
Treatment A for rows, popover for the click, "Compare plans" into the existing dialog with the plan preselected, the Address group for the custom domain, and the rebuilt Tests row. It drops the per-block banners; one card per page stays for a real clock or limit (the 7-day Free card, sessions at the limit).

## Decisions for Duane
1. Replace the plan pill with a lock and grey plan word on every locked row (A)? Or B, or C.
2. Click on a locked row: popover (bottom sheet on a phone) with one trial button? Or small modal with plan preselected, or side sheet.
3. Is "Try Basic free for 7 days" the right button? It needs checkout to start a trial from the row (new work).
4. "Compare plans" opens the existing dialog with the clicked feature's plan selected? (AeroPricingModal needs a `plan` prop.)
5. Give the custom domain its own Address group and the words "Use your own address, like app.yourname.com"?
6. Say plainly that the custom domain is on Solo, not Basic, in the app and the popover?
7. Show "$3/mo after the trial" in the popover, or leave prices to the dialog? Regional prices would then need to show here too.
8. Drop the per-block upgrade banners (Figmafolio pattern) from the Aero site page?
9. Keep the Free-site 7-day card as the only card on the page?
10. Change the style guide's "2 new" to ink text with an accent dot (`.ae-test-row__new` in components.css)? The mockup overrides it locally.
11. Treatment D: not recommended now, it needs a draft state for locked settings that does not exist.

## Sources
- Webflow: [Quick connect a custom domain](https://help.webflow.com/hc/en-us/articles/33961266716307); [I paid for a plan but still can't connect my custom domain](https://help.webflow.com/hc/en-us/articles/39916315383699-I-paid-for-a-plan-but-still-can-t-connect-my-custom-domain)
- Framer: [Connect a custom domain](https://www.framer.com/help/articles/how-to-connect-a-custom-domain/); [Site plans overview](https://www.framer.com/help/articles/site-plans-explained/)
- Vercel: [Password Protection](https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/password-protection). Netlify: [Site protection](https://docs.netlify.com/manage/security/secure-access-to-sites/site-protection/)
- Notion: [Change your plan](https://www.notion.com/help/upgrade-or-downgrade-your-plan); [locked feature paywall flow, Lazyweb](https://experiments.lazyweb.com/flow/notion/locked-feature-paywall) (July 2026, screens behind sign-up). Linear: [Pricing plan changes](https://linear.app/docs/changes-to-linears-pricing-plans)
- Figma forum: [Dev Mode upgrade thread, 22 Dec 2025](https://forum.figma.com/share-your-feedback-26/why-does-figma-deliberately-add-friction-to-the-account-upgrade-process-48900); [Upgrade to Professional on a Starter team](https://forum.figma.com/report-a-problem-6/i-have-a-full-seat-account-with-my-company-however-am-seeing-a-upgrade-to-professional-when-trying-to-access-figma-sites-or-dev-mode-40617)
- Canva: [Premium apps guidelines](https://www.canva.dev/docs/apps/design-guidelines/premium-apps/); [Canva paywall masterclass, Plandalf](https://plandalf-site.pages.dev/blog/posts/canva-paywall-masterclass)
- Loom: [Starter plan FAQ](https://support.atlassian.com/loom/docs/starter-plan-faq/). Maze: [Free trials](https://help.maze.co/hc/en-us/articles/28513024118547-Maze-free-trials)
- In this repo: `src/components/FeatureGate/FeatureGate.js`, `src/components/Aero/AeroFeatureGate.js`, `src/pages/AeroSites/tabs/SiteDomainTab.js`, `docs/brand/PRICING-FACTS.md`.
